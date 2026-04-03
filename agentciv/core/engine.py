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
from .context import AgentContext, TickSummary
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
from ..chronicle.observer import Chronicle
from ..gardener import Gardener, Intervention
from ..learning.insights import generate_insights
from ..org.auto import AutoOrgManager
from ..org.config import EngineConfig, OrgDimensions
from ..org.enforcer import OrgEnforcer
from ..workspace.git import GitManager
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
    auto_org: AutoOrgManager | None = None
    git: GitManager | None = None
    chronicle: Chronicle | None = None
    gardener: Gardener | None = None
    tick: int = 0
    running: bool = False

    # Per-tick state
    _messages: list[Message] = field(default_factory=list)
    _events: list[Event] = field(default_factory=list)

    # Max Plan Mode scratch (set by prepare_tick, read by complete_tick)
    _tick_events: list[Event] = field(default_factory=list)
    _tick_messages: list[Message] = field(default_factory=list)
    _tick_is_meta: bool = False

    async def run(self) -> None:
        """Run the engine for max_ticks or until convergence."""
        if not self.agents:
            raise ValueError("Cannot run engine with 0 agents")
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

        # Initialise auto-org manager if meta-ticks are enabled
        if self.config.parameters.meta_tick_interval > 0 and self.auto_org is None:
            # Generate learning insights from run history
            learning_prompt = ""
            try:
                insights = generate_insights(self.config.task)
                if insights.has_data():
                    learning_prompt = insights.prompt
                    log.info(
                        "Learning: %d matching runs found for task",
                        insights.matching_runs,
                    )
            except Exception as e:
                log.debug("Learning insights unavailable: %s", e)

            self.auto_org = AutoOrgManager(
                dimensions=self.config.org_dimensions,
                parameters=self.config.parameters,
                agent_count=len(self.agents),
                learning_prompt=learning_prompt,
            )
            log.info("Auto-organisation enabled (meta-tick interval: %d)", self.config.parameters.meta_tick_interval)

        # Initialise git integration if enabled
        if self.config.parameters.enable_git_branches and self.git is None:
            if await GitManager.is_available():
                self.git = GitManager(self.workspace.project_dir)
                await self.git.init()
                log.info(
                    "Git branch-per-agent enabled (strategy: %s)",
                    self.config.parameters.contention_strategy,
                )
            else:
                log.warning(
                    "Git not available — falling back to optimistic contention handling"
                )

        # Initialise chronicle observer
        if self.config.enable_chronicle and self.chronicle is None:
            agent_names = {
                a.state.identity.id: a.state.identity.name
                for a in self.agents
            }
            self.chronicle = Chronicle(
                task=self.config.task,
                org_preset=self.config.org_preset,
                agent_count=len(self.agents),
                agent_names=agent_names,
            )
            self.event_bus.subscribe(None, self.chronicle.observe)
            log.info("Chronicle observer enabled")

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
            # Clean up git worktrees
            if self.git:
                await self.git.cleanup_all()
            self.event_bus.emit(Event(
                type=EventType.ENGINE_STOPPED,
                tick=self.tick,
            ))
            log.info("Engine stopped at tick %d", self.tick)

    def stop(self) -> None:
        """Signal the engine to stop after the current tick."""
        self.running = False

    # -------------------------------------------------------------------
    # Max Plan Mode — step-by-step orchestration API
    # -------------------------------------------------------------------

    async def initialize(self) -> dict:
        """Initialise the engine without starting the run loop.

        Sets up org enforcer, auto-org, git, chronicle, attention map —
        everything that run() does before the tick loop. Returns a summary
        of the initialised state.

        For Max Plan Mode: call this once, then use prepare_tick() /
        complete_tick() in a loop driven by the MCP client.
        """
        self.running = True

        # Org enforcer
        if self.enforcer is None:
            self.enforcer = OrgEnforcer(
                dimensions=self.config.org_dimensions,
                parameters=self.config.parameters,
            )
            self.enforcer.assign_initial_roles(
                [a.state.identity.id for a in self.agents]
            )

        # Auto-org
        if self.config.parameters.meta_tick_interval > 0 and self.auto_org is None:
            learning_prompt = ""
            try:
                insights = generate_insights(self.config.task)
                if insights.has_data():
                    learning_prompt = insights.prompt
            except Exception:
                pass

            self.auto_org = AutoOrgManager(
                dimensions=self.config.org_dimensions,
                parameters=self.config.parameters,
                agent_count=len(self.agents),
                learning_prompt=learning_prompt,
            )

        # Git
        if self.config.parameters.enable_git_branches and self.git is None:
            if await GitManager.is_available():
                self.git = GitManager(self.workspace.project_dir)
                await self.git.init()

        # Chronicle
        if self.config.enable_chronicle and self.chronicle is None:
            agent_names = {
                a.state.identity.id: a.state.identity.name
                for a in self.agents
            }
            self.chronicle = Chronicle(
                task=self.config.task,
                org_preset=self.config.org_preset,
                agent_count=len(self.agents),
                agent_names=agent_names,
            )
            self.event_bus.subscribe(None, self.chronicle.observe)

        # Attention map
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
            "Engine initialised (Max Plan): %d agents, org=%s, max_ticks=%d",
            len(self.agents), self.config.org_preset, self.config.max_ticks,
        )

        return {
            "agents": [
                {
                    "id": a.state.identity.id,
                    "name": a.state.identity.name,
                    "model": a.state.identity.model,
                }
                for a in self.agents
            ],
            "org_preset": self.config.org_preset,
            "max_ticks": self.config.max_ticks,
            "git_enabled": self.git is not None,
            "auto_org": self.auto_org is not None,
        }

    async def prepare_tick(self) -> tuple[list[AgentContext], bool]:
        """Prepare the next tick and return agent contexts.

        Returns:
            - List of AgentContext, one per agent (ready for external LLM)
            - Whether this is a meta-tick

        The MCP client iterates the contexts, sends each to its LLM,
        and submits tool calls via agent.apply_tool_calls().
        """
        self.tick += 1

        if self.tick > self.config.max_ticks or not self.running:
            return [], False

        # Gardener interventions
        force_meta = False
        if self.gardener and self.gardener.is_enabled:
            for intervention in self.gardener.drain():
                result = self._apply_intervention(intervention)
                if result == "force_meta":
                    force_meta = True
                elif result == "stop":
                    self.running = False
                    return [], False

        # Detect meta-tick
        is_meta_tick = force_meta
        if not is_meta_tick and self.auto_org and self.auto_org.is_meta_tick(self.tick):
            is_meta_tick = True
        if is_meta_tick and self.auto_org:
            self.auto_org.start_meta_tick(self.tick)

        self.event_bus.emit(Event(
            type=EventType.TICK_START,
            tick=self.tick,
            data={"is_meta_tick": is_meta_tick},
        ))

        # Update task-based groups
        if self.enforcer and self.enforcer.dimensions.groups == "task-based":
            focus_map = {
                a.state.identity.id: a.state.current_focus
                for a in self.agents
            }
            self.enforcer.update_task_groups(focus_map)

        # Snapshot and clear per-tick state
        tick_events = list(self._events)
        tick_messages = list(self._messages)
        self._events.clear()
        self._messages.clear()

        # Store for complete_tick()
        self._tick_events = tick_events
        self._tick_messages = tick_messages
        self._tick_is_meta = is_meta_tick

        # Set up git worktrees
        if self.git:
            for agent in self.agents:
                worktree = await self.git.create_agent_worktree(
                    agent.state.identity.id,
                    agent.state.identity.name,
                    self.tick,
                )
                agent.executor.working_dir = worktree

        # Build agent contexts
        contexts: list[AgentContext] = []
        for agent in self.agents:
            ctx = agent.prepare_context(
                workspace=self.workspace,
                org=self.config.org_dimensions,
                enforcer=self.enforcer,
                attention=self.attention,
                events=tick_events,
                messages=tick_messages,
                tick=self.tick,
                step=0,
                is_meta_tick=is_meta_tick,
                auto_org=self.auto_org,
            )
            contexts.append(ctx)

        return contexts, is_meta_tick

    async def complete_tick(self, all_actions: list[Action]) -> TickSummary:
        """Complete the current tick after all agents have acted.

        Handles: git merge, auto-org proposals, attention map, relationships,
        events, messages, chronicle. Returns a summary.

        The MCP client collects actions from apply_tool_calls() for each
        agent and passes the combined list here.
        """
        is_meta_tick = getattr(self, "_tick_is_meta", False)
        tick_events_out: list[dict] = []
        org_changes: list[dict] = []
        merge_summaries: list[dict] = []

        # Merge agent branches
        if self.git:
            for agent in self.agents:
                aid = agent.state.identity.id
                name = agent.state.identity.name

                merge = await self.git.commit_and_merge(aid, name, self.tick)
                agent.executor.working_dir = None

                if merge.files_changed:
                    merge_summaries.append({
                        "agent": name,
                        "success": merge.success,
                        "files_changed": merge.files_changed,
                        "conflicts": merge.conflicts,
                    })
                    if merge.success:
                        self.event_bus.emit(Event(
                            type=EventType.BRANCH_MERGED,
                            tick=self.tick,
                            agent_id=aid,
                            data={
                                "files": merge.files_changed,
                                "count": len(merge.files_changed),
                            },
                        ))
                    else:
                        conflict_event = Event(
                            type=EventType.MERGE_CONFLICT,
                            tick=self.tick,
                            agent_id=aid,
                            data={
                                "conflicts": merge.conflicts,
                                "files_attempted": merge.files_changed,
                                "summary": (
                                    f"{name}'s changes to "
                                    f"{', '.join(merge.conflicts)} conflicted."
                                ),
                            },
                        )
                        self.event_bus.emit(conflict_event)
                        self._events.append(conflict_event)

            self.workspace.scan()

        # Auto-org proposals and votes
        if self.auto_org:
            self._process_auto_org_actions(all_actions)

        # Attention map
        self._update_attention(all_actions)

        # Relationships
        if self.config.parameters.enable_relationships:
            self._update_relationships(all_actions)

        # Convert actions to events
        for action in all_actions:
            event = self._action_to_event(action)
            if event:
                self._events.append(event)
                self.event_bus.emit(event)
                tick_events_out.append({
                    "type": event.type.name,
                    "agent": event.agent_id,
                    "tick": event.tick,
                })

        # Collect messages
        for action in all_actions:
            if action.type.name in ("COMMUNICATE", "BROADCAST") and action.content:
                self._messages.append(Message(
                    sender_id=action.agent_id,
                    receiver_ids=action.target_agents,
                    content=action.content,
                    tick=self.tick,
                    is_broadcast=action.type.name == "BROADCAST",
                ))
                if self.enforcer and action.target_agents:
                    self.enforcer.record_communication(
                        action.agent_id, action.target_agents,
                    )

        # Resolve proposals at end of meta-tick
        if is_meta_tick and self.auto_org:
            adopted = self.auto_org.resolve_proposals(self.tick)
            for evt in adopted:
                change = {
                    "dimension": evt.dimension,
                    "old_value": evt.old_value,
                    "new_value": evt.new_value,
                    "proposer": evt.proposer,
                }
                org_changes.append(change)
                self.event_bus.emit(Event(
                    type=EventType.RESTRUCTURE_ADOPTED,
                    tick=self.tick,
                    data=change,
                ))

        # Tick idle counters
        self.attention.tick_idle(self.tick)

        self.event_bus.emit(Event(
            type=EventType.TICK_END,
            tick=self.tick,
            data={"actions": len(all_actions), "is_meta_tick": is_meta_tick},
        ))

        should_continue = self.running and self.tick < self.config.max_ticks

        return TickSummary(
            tick=self.tick,
            actions_count=len(all_actions),
            merge_results=merge_summaries,
            events=tick_events_out,
            org_changes=org_changes,
            should_continue=should_continue,
        )

    async def cleanup(self) -> None:
        """Clean up engine resources. Call when the run is finished."""
        self.running = False
        if self.git:
            await self.git.cleanup_all()
        self.event_bus.emit(Event(
            type=EventType.ENGINE_STOPPED,
            tick=self.tick,
        ))
        log.info("Engine cleaned up at tick %d", self.tick)

    async def _execute_tick(self) -> None:
        """Execute a single tick — all agents act."""
        # Process gardener interventions before the tick
        force_meta = False
        if self.gardener and self.gardener.is_enabled:
            for intervention in self.gardener.drain():
                result = self._apply_intervention(intervention)
                if result == "force_meta":
                    force_meta = True
                elif result == "stop":
                    self.running = False
                    return

        # Detect meta-tick (restructuring discussion for --org auto)
        is_meta_tick = force_meta  # gardener can force a meta-tick
        if not is_meta_tick and self.auto_org and self.auto_org.is_meta_tick(self.tick):
            is_meta_tick = True
        if is_meta_tick and self.auto_org:
            self.auto_org.start_meta_tick(self.tick)

        self.event_bus.emit(Event(
            type=EventType.TICK_START,
            tick=self.tick,
            data={"is_meta_tick": is_meta_tick},
        ))

        # Update task-based groups from agent focus
        if self.enforcer and self.enforcer.dimensions.groups == "task-based":
            focus_map = {
                a.state.identity.id: a.state.current_focus
                for a in self.agents
            }
            self.enforcer.update_task_groups(focus_map)

        # Snapshot messages and events for this tick
        tick_events = list(self._events)
        tick_messages = list(self._messages)
        self._events.clear()
        self._messages.clear()

        # Set up git worktrees — each agent gets an isolated working directory
        if self.git:
            for agent in self.agents:
                worktree = await self.git.create_agent_worktree(
                    agent.state.identity.id,
                    agent.state.identity.name,
                    self.tick,
                )
                agent.executor.working_dir = worktree

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
                is_meta_tick=is_meta_tick,
                auto_org=self.auto_org,
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

        # Merge agent branches back to main
        if self.git:
            await self._merge_agent_branches()

        # Handle auto-org proposals and votes
        if self.auto_org:
            self._process_auto_org_actions(all_actions)

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
                # Track communication history for whisper visibility
                if self.enforcer and action.target_agents:
                    self.enforcer.record_communication(
                        action.agent_id, action.target_agents,
                    )

        # Resolve proposals at end of meta-tick
        if is_meta_tick and self.auto_org:
            adopted = self.auto_org.resolve_proposals(self.tick)
            for event in adopted:
                self.event_bus.emit(Event(
                    type=EventType.RESTRUCTURE_ADOPTED,
                    tick=self.tick,
                    data={
                        "dimension": event.dimension,
                        "old_value": event.old_value,
                        "new_value": event.new_value,
                        "proposer": event.proposer,
                        "yes_votes": event.yes_votes,
                        "no_votes": event.no_votes,
                    },
                ))
                self._events.append(Event(
                    type=EventType.RESTRUCTURE_ADOPTED,
                    tick=self.tick,
                    data={
                        "dimension": event.dimension,
                        "old_value": event.old_value,
                        "new_value": event.new_value,
                    },
                ))

        # Tick idle counters
        self.attention.tick_idle(self.tick)

        self.event_bus.emit(Event(
            type=EventType.TICK_END,
            tick=self.tick,
            data={"actions": len(all_actions), "is_meta_tick": is_meta_tick},
        ))

    def _apply_intervention(self, intervention: Intervention) -> str | None:
        """Apply a gardener intervention. Returns a signal string or None."""
        match intervention.type:
            case "message":
                # Inject as a message from "gardener" visible to all agents
                self._messages.append(Message(
                    sender_id="gardener",
                    receiver_ids=[],
                    content=f"[GARDENER] {intervention.content}",
                    tick=self.tick,
                    is_broadcast=True,
                ))
                self._events.append(Event(
                    type=EventType.BROADCAST_SENT,
                    tick=self.tick,
                    agent_id="gardener",
                    data={"content_preview": intervention.content[:100]},
                ))
                log.info("Gardener message: %s", intervention.content[:100])

            case "redirect":
                # Update the task description — agents see the new task next tick
                old_task = self.workspace.task_description
                self.workspace.task_description = intervention.content
                self.config.task = intervention.content
                log.info(
                    "Gardener redirected: '%s' → '%s'",
                    old_task[:50], intervention.content[:50],
                )

            case "meta_tick":
                log.info("Gardener forced meta-tick")
                return "force_meta"

            case "adjust":
                # Adjust org dimensions or parameters live
                for key, value in intervention.parameters.items():
                    if hasattr(self.config.org_dimensions, key):
                        setattr(self.config.org_dimensions, key, value)
                        log.info("Gardener adjusted dimension: %s → %s", key, value)
                    elif hasattr(self.config.parameters, key):
                        setattr(self.config.parameters, key, value)
                        log.info("Gardener adjusted parameter: %s → %s", key, value)
                    else:
                        self.config.org_dimensions.extra[key] = value
                        log.info("Gardener set custom dimension: %s → %s", key, value)

            case "stop":
                log.info("Gardener stopped the engine")
                return "stop"

        return None

    async def _merge_agent_branches(self) -> None:
        """Merge each agent's worktree branch back to main.

        Agents are merged in order. If Agent B's changes conflict with
        Agent A's already-merged changes, Agent B gets a conflict report.
        """
        for agent in self.agents:
            aid = agent.state.identity.id
            name = agent.state.identity.name

            merge = await self.git.commit_and_merge(aid, name, self.tick)

            # Reset the executor to the main working directory
            agent.executor.working_dir = None

            if merge.files_changed:
                if merge.success:
                    self.event_bus.emit(Event(
                        type=EventType.BRANCH_MERGED,
                        tick=self.tick,
                        agent_id=aid,
                        data={
                            "files": merge.files_changed,
                            "count": len(merge.files_changed),
                        },
                    ))
                else:
                    # Conflict — emit event so the agent sees it next tick
                    conflict_event = Event(
                        type=EventType.MERGE_CONFLICT,
                        tick=self.tick,
                        agent_id=aid,
                        data={
                            "conflicts": merge.conflicts,
                            "files_attempted": merge.files_changed,
                            "summary": (
                                f"{name}'s changes to "
                                f"{', '.join(merge.conflicts)} conflicted "
                                f"with another agent's merged changes."
                            ),
                        },
                    )
                    self.event_bus.emit(conflict_event)
                    self._events.append(conflict_event)
                    log.warning(
                        "Merge conflict for %s: %s",
                        name, merge.conflicts,
                    )

        # Rescan workspace to pick up merged file changes
        self.workspace.scan()

    def _process_auto_org_actions(self, actions: list[Action]) -> None:
        """Process propose_restructure and vote actions through AutoOrgManager."""
        # Map agent IDs to names
        agent_names = {a.state.identity.id: a.state.identity.name for a in self.agents}

        for action in actions:
            if action.type == ActionType.PROPOSE_RESTRUCTURE and self.auto_org:
                dimension = action.content or ""
                value = action.target_agents[0] if action.target_agents else ""
                reasoning = action.reasoning or ""
                name = agent_names.get(action.agent_id, action.agent_id)
                self.auto_org.submit_proposal(
                    agent_id=action.agent_id,
                    agent_name=name,
                    dimension=dimension,
                    value=value,
                    reasoning=reasoning,
                    tick=action.tick,
                )
            elif action.type == ActionType.VOTE and self.auto_org:
                proposal_id = action.content or ""
                vote = action.target_agents[0] if action.target_agents else "no"
                reasoning = action.reasoning or ""
                result = self.auto_org.submit_vote(
                    agent_id=action.agent_id,
                    proposal_id=proposal_id,
                    vote=vote,
                    reasoning=reasoning,
                )
                log.debug("Vote result for %s: %s", action.agent_id, result)

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
