"""The Engine — orchestrates agents, ticks, and the workspace.

This is the main loop. Each tick:
1. Gather events and messages from last tick
2. Run each agent's cognitive loop (observe → reason → decide → act → reflect)
3. Collect actions, broadcast results as events
4. Update workspace state
5. Run chronicle observation
6. Check for convergence
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any

from .agent import Agent
from .event_bus import EventBus
from .types import (
    Action,
    AgentIdentity,
    AgentState,
    Event,
    EventType,
    Message,
)
from ..org.config import EngineConfig, OrgDimensions

log = logging.getLogger(__name__)


@dataclass
class Engine:
    """The core engine that runs agent communities."""

    config: EngineConfig
    agents: list[Agent] = field(default_factory=list)
    event_bus: EventBus = field(default_factory=EventBus)
    tick: int = 0
    running: bool = False

    # Per-tick state
    _messages: list[Message] = field(default_factory=list)
    _events: list[Event] = field(default_factory=list)

    async def run(self) -> None:
        """Run the engine for max_ticks or until convergence."""
        self.running = True
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
                workspace=None,  # TODO: wire up workspace
                org=self.config.org_dimensions,
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

        self.event_bus.emit(Event(
            type=EventType.TICK_END,
            tick=self.tick,
            data={"actions": len(all_actions)},
        ))

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
