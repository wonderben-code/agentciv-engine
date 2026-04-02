"""The Engine — orchestrates agents, ticks, and the workspace.

This is the main loop. Each tick:
1. Gather events and messages from last tick
2. Update attention map with last tick's actions
3. Run each agent's cognitive loop (observe → reason → decide → act → reflect)
4. Collect actions, broadcast results as events
5. Update workspace state and relationships
6. Run chronicle observation
7. Check for convergence
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any

from .agent import Agent
from .attention import AttentionMap
from .event_bus import EventBus
from .types import (
    Action,
    ActionType,
    AgentIdentity,
    AgentState,
    Event,
    EventType,
    Message,
    Relationship,
)
from ..org.config import EngineConfig, OrgDimensions
from ..org.enforcer import OrgEnforcer
from ..workspace.workspace import Workspace

log = logging.getLogger(__name__)


@dataclass
class Engine:
    """The core engine that runs agent communities."""

    config: EngineConfig
    workspace: Workspace
    agents: list[Agent] = field(default_factory=list)
    event_bus: EventBus = field(default_factory=EventBus)
    enforcer: OrgEnforcer | None = None
    attention: AttentionMap = field(default_factory=AttentionMap)
    tick: int = 0
    running: bool = False

    # Per-tick state
    _messages: list[Message] = field(default_factory=list)
    _events: list[Event] = field(default_factory=list)

    async def run(self) -> None:
        """Run the engine for max_ticks or until convergence."""
        self.running = True

        # Initialise org enforcer
        if self.enforcer is None:
            self.enforcer = OrgEnforcer(
                dimensions=self.config.org_dimensions,
                parameters=self.config.parameters,
            )
            self.enforcer.assign_initial_roles(
                [a.state.identity.id for a in self.agents]
            )

        # Register all agents in the attention map
        for agent in self.agents:
            self.attention.register_agent(
                agent.state.identity.id,
                agent.state.identity.name,
            )

        self.event_bus.emit(Event(
            type=EventType.ENGINE_STARTED,
            tick=0,
            data={"config": self.config.org_preset, "agents": self.config.agent_count},
        ))

        log.info(
            "Engine started: %d agents, org=%s, max_ticks=%d",
            len(self.agents), self.config.org_preset, self.config.max_ticks,
        )

        try:
            for self.tick in range(1, self.config.max_ticks + 1):
                if not self.running:
                    break
                await self._execute_tick()
        finally:
            self.running = False
            self.event_bus.emit(Event(
                type=EventType.ENGINE_STOPPED,
                tick=self.tick,
            ))
            log.info("Engine stopped at tick %d", self.tick)

    def stop(self) -> None:
        """Signal the engine to stop after the current tick."""
        self.running = False

    async def _execute_tick(self) -> None:
        """Execute a single tick — all agents act."""
        self.event_bus.emit(Event(type=EventType.TICK_START, tick=self.tick))

        # Snapshot messages and events for this tick
        tick_events = list(self._events)
        tick_messages = list(self._messages)
        self._events.clear()
        self._messages.clear()

        # Run all agents (concurrency bounded by agent count)
        all_actions: list[Action] = []
        tasks = [
            agent.tick(
                workspace=self.workspace,
                org=self.config.org_dimensions,
                enforcer=self.enforcer,
                attention=self.attention,
                events=tick_events,
                messages=tick_messages,
                tick=self.tick,
            )
            for agent in self.agents
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for agent, result in zip(self.agents, results):
            if isinstance(result, Exception):
                log.error(
                    "Agent %s failed: %s",
                    agent.state.identity.name, result,
                )
                continue
            all_actions.extend(result)

        # --- Post-tick updates ---

        # Update attention map from actions
        self._update_attention(all_actions)

        # Update relationships from collaboration signals
        if self.config.parameters.enable_relationships:
            self._update_relationships(all_actions)

        # Convert actions to events for next tick
        for action in all_actions:
            event = self._action_to_event(action)
            if event:
                self._events.append(event)
                self.event_bus.emit(event)

        # Collect messages from communication actions
        for action in all_actions:
            if action.type.name in ("COMMUNICATE", "BROADCAST") and action.content:
                self._messages.append(Message(
                    sender_id=action.agent_id,
                    receiver_ids=action.target_agents,
                    content=action.content,
                    tick=self.tick,
                    is_broadcast=action.type.name == "BROADCAST",
                ))

        # Tick idle counters
        self.attention.tick_idle(self.tick)

        self.event_bus.emit(Event(
            type=EventType.TICK_END,
            tick=self.tick,
            data={"actions": len(all_actions)},
        ))

    def _update_attention(self, actions: list[Action]) -> None:
        """Update the attention map based on this tick's actions."""
        for action in actions:
            aid = action.agent_id
            # Update focus from task claims
            if action.type == ActionType.CLAIM_TASK:
                self.attention.update_focus(aid, action.content)
            elif action.type == ActionType.RELEASE_TASK:
                self.attention.update_focus(aid, None)

            # Track files being touched
            if action.file_path and action.type in (
                ActionType.WRITE_FILE, ActionType.CREATE_FILE, ActionType.READ_FILE,
            ):
                self.attention.update_files(aid, action.file_path)

            # Record last action
            if action.type != ActionType.IDLE:
                desc = action.type.name
                if action.file_path:
                    desc += f" {action.file_path}"
                self.attention.update_action(aid, desc, action.tick)

    def _update_relationships(self, actions: list[Action]) -> None:
        """Update agent relationships based on collaboration signals.

        Positive signals: direct messages, helpful responses, working on related files
        Negative signals: file conflicts (when we add git), communication failures
        """
        # Track who communicated with whom this tick
        communicators: dict[str, set[str]] = {}
        for action in actions:
            if action.type == ActionType.COMMUNICATE and action.target_agents:
                sender = action.agent_id
                for target in action.target_agents:
                    communicators.setdefault(sender, set()).add(target)
                    communicators.setdefault(target, set()).add(sender)

        # Track who worked on the same files (potential collaboration)
        file_workers: dict[str, list[str]] = {}
        for action in actions:
            if action.file_path and action.type in (
                ActionType.WRITE_FILE, ActionType.CREATE_FILE,
            ):
                file_workers.setdefault(action.file_path, []).append(action.agent_id)

        # Update relationships
        for agent in self.agents:
            aid = agent.state.identity.id

            # Communication = positive interaction
            for partner in communicators.get(aid, set()):
                rel = agent.state.relationships.setdefault(
                    partner, Relationship(agent_id=partner)
                )
                rel.interaction_count += 1
                rel.positive_count += 1
                rel.last_tick = self.tick

            # Shared file work = weaker positive signal
            for _file, workers in file_workers.items():
                if aid in workers:
                    for partner in workers:
                        if partner != aid:
                            rel = agent.state.relationships.setdefault(
                                partner, Relationship(agent_id=partner)
                            )
                            rel.interaction_count += 1
                            # Only count as positive if they weren't also touching it
                            # (could be a conflict). For now, assume positive.
                            rel.positive_count += 1
                            rel.last_tick = self.tick

        # Apply relationship decay
        decay = self.config.parameters.relationship_decay
        if decay < 1.0:
            for agent in self.agents:
                for rel in agent.state.relationships.values():
                    if rel.last_tick < self.tick:
                        # Decay by reducing positive count slightly
                        rel.positive_count = max(0, int(rel.positive_count * decay))

    @staticmethod
    def _action_to_event(action: Action) -> Event | None:
        """Convert an action into an event for the bus."""
        mapping = {
            "WRITE_FILE": EventType.FILE_MODIFIED,
            "CREATE_FILE": EventType.FILE_CREATED,
            "DELETE_FILE": EventType.FILE_DELETED,
            "COMMUNICATE": EventType.MESSAGE_SENT,
            "BROADCAST": EventType.BROADCAST_SENT,
            "CLAIM_TASK": EventType.TASK_CLAIMED,
            "RELEASE_TASK": EventType.TASK_RELEASED,
            "REQUEST_REVIEW": EventType.REVIEW_REQUESTED,
            "PROPOSE_RESTRUCTURE": EventType.RESTRUCTURE_PROPOSED,
            "VOTE": EventType.RESTRUCTURE_VOTED,
        }
        event_type = mapping.get(action.type.name)
        if not event_type:
            return None
        return Event(
            type=event_type,
            tick=action.tick,
            agent_id=action.agent_id,
            data={
                "file": action.file_path,
                "content_preview": (action.content or "")[:100],
                "targets": action.target_agents,
                "reasoning": action.reasoning,
            },
        )
