"""The Agent — a reasoning entity in a community.

Built from first principles for a developer tool. No grid-world legacy.
The cognitive loop: observe → reason → decide → act → reflect.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Protocol

from .types import (
    Action,
    ActionResult,
    ActionType,
    AgentIdentity,
    AgentMemoryEntry,
    AgentSkill,
    AgentState,
    Event,
    Message,
    Relationship,
    TaskSignal,
)

if TYPE_CHECKING:
    from ..llm.client import LLMClient
    from ..org.config import OrgDimensions
    from ..workspace.workspace import Workspace

log = logging.getLogger(__name__)


class ActionExecutor(Protocol):
    """Interface for executing actions on the workspace."""

    async def execute(self, action: Action) -> ActionResult: ...


@dataclass
class Agent:
    """A single agent in the community.

    Owns its state, runs the cognitive loop, and interacts with the workspace
    through the ActionExecutor interface.
    """

    state: AgentState
    llm: LLMClient
    executor: ActionExecutor

    # Per-tick context (rebuilt each tick)
    _visible_files: list[dict[str, Any]] = field(default_factory=list)
    _recent_events: list[Event] = field(default_factory=list)
    _recent_messages: list[Message] = field(default_factory=list)
    _task_board: list[TaskSignal] = field(default_factory=list)
    _other_agents: list[dict[str, Any]] = field(default_factory=list)
    _org_description: str = ""

    # -----------------------------------------------------------------------
    # Cognitive loop
    # -----------------------------------------------------------------------

    async def tick(
        self,
        workspace: Workspace,
        org: OrgDimensions,
        events: list[Event],
        messages: list[Message],
        tick: int,
    ) -> list[Action]:
        """Run one full cognitive loop. Returns all actions taken this tick."""
        self.state.ticks_active += 1
        actions_taken: list[Action] = []

        # --- OBSERVE ---
        self._observe(workspace, org, events, messages)

        # --- Multi-step ReAct loop (max steps per tick) ---
        max_steps = 4
        for step in range(max_steps):

            # --- REASON + DECIDE ---
            action = await self._reason_and_decide(tick, step)
            if action is None or action.type == ActionType.IDLE:
                break

            # --- ACT ---
            result = await self.executor.execute(action)
            actions_taken.append(action)

            # --- REFLECT ---
            self._reflect(action, result, tick)

            # If the action failed, the agent might want to reconsider
            if not result.success:
                log.debug(
                    "Agent %s action %s failed: %s",
                    self.state.identity.name, action.type.name, result.error,
                )

        return actions_taken

    # -----------------------------------------------------------------------
    # Observe — perceive the workspace and context
    # -----------------------------------------------------------------------

    def _observe(
        self,
        workspace: Workspace,
        org: OrgDimensions,
        events: list[Event],
        messages: list[Message],
    ) -> None:
        """Build the agent's perception of the current state."""
        self._visible_files = workspace.get_visible_files(self.state)
        self._task_board = workspace.get_task_board()
        self._other_agents = workspace.get_agent_summaries(exclude=self.state.identity.id)
        self._recent_events = events
        self._recent_messages = [
            m for m in messages
            if m.sender_id != self.state.identity.id  # don't re-read own messages
        ]
        self._org_description = org.to_prompt_description()

    # -----------------------------------------------------------------------
    # Reason + Decide — LLM call to determine next action
    # -----------------------------------------------------------------------

    async def _reason_and_decide(self, tick: int, step: int) -> Action | None:
        """Ask the LLM what to do next. Returns an Action or None to stop."""
        prompt = self._build_prompt(tick, step)
        response = await self.llm.complete(prompt)
        return self._parse_action(response, tick)

    def _build_prompt(self, tick: int, step: int) -> str:
        """Construct the full prompt for the LLM.

        Describes state and context. Does NOT prescribe behaviour — the agent
        decides what to do based on what it perceives and what it thinks is
        needed. Emergent behaviour from context, not instructions.
        """
        sections: list[str] = []

        # Identity
        sections.append(
            f"You are {self.state.identity.name}, an agent in a community "
            f"working together on a software project.\n"
            f"Tick: {tick} | Step: {step + 1}/4"
        )

        # Organisation — how this community is structured
        sections.append(self._org_description)

        # Current focus and plan
        if self.state.current_focus:
            sections.append(f"Your current focus: {self.state.current_focus}")
        if self.state.current_plan:
            sections.append(
                "Your plan:\n" + "\n".join(f"  {i+1}. {s}" for i, s in enumerate(self.state.current_plan))
            )

        # Skills
        if self.state.skills:
            skill_lines = [
                f"  {s.name}: {s.tier} ({s.action_count} actions)"
                for s in self.state.skills.values()
            ]
            sections.append("Your skills:\n" + "\n".join(skill_lines))

        # Memory — top entries by importance
        if self.state.memories:
            sorted_memories = sorted(
                self.state.memories,
                key=lambda m: m.importance * 0.7 + (1.0 / (tick - m.tick + 1)) * 0.3,
                reverse=True,
            )[:15]
            mem_lines = [f"  [{m.tick}] {m.summary}" for m in sorted_memories]
            sections.append("Recent memory:\n" + "\n".join(mem_lines))

        # Visible files
        if self._visible_files:
            file_lines = [
                f"  {f['path']} ({f.get('summary', 'unknown')})"
                for f in self._visible_files[:20]
            ]
            sections.append("Project files:\n" + "\n".join(file_lines))

        # Task board
        if self._task_board:
            task_lines = []
            for t in self._task_board:
                status = f"[{t.status}]"
                claimed = f" (claimed by {t.claimed_by})" if t.claimed_by else ""
                task_lines.append(f"  {status} {t.description}{claimed}")
            sections.append("Task board:\n" + "\n".join(task_lines))

        # Other agents
        if self._other_agents:
            agent_lines = [
                f"  {a['name']}: working on {a.get('focus', 'unknown')}"
                for a in self._other_agents
            ]
            sections.append("Other agents:\n" + "\n".join(agent_lines))

        # Recent events
        if self._recent_events:
            event_lines = [
                f"  [{e.type.name}] {e.data.get('summary', '')}"
                for e in self._recent_events[:10]
            ]
            sections.append("Recent events:\n" + "\n".join(event_lines))

        # Messages received
        if self._recent_messages:
            msg_lines = [
                f"  {m.sender_id}: {m.content}"
                for m in self._recent_messages[:10]
            ]
            sections.append("Messages:\n" + "\n".join(msg_lines))

        # Available actions
        sections.append(
            "Available actions:\n"
            "  READ_FILE <path> — read a file\n"
            "  WRITE_FILE <path> — write/edit a file\n"
            "  CREATE_FILE <path> — create a new file\n"
            "  RUN_COMMAND <cmd> — run a shell command (build, test, lint)\n"
            "  COMMUNICATE <agent> <message> — message an agent\n"
            "  BROADCAST <message> — message all agents\n"
            "  CLAIM_TASK <description> — signal you're working on something\n"
            "  RELEASE_TASK — stop working on current task\n"
            "  REQUEST_REVIEW — ask others to review your work\n"
            "  IDLE — wait and observe\n"
        )

        # Final instruction — minimal, non-prescriptive
        sections.append(
            "What do you do next? State your reasoning, then your action."
        )

        return "\n\n".join(sections)

    def _parse_action(self, response: str, tick: int) -> Action | None:
        """Parse the LLM response into a concrete Action.

        TODO: Implement robust parsing with fallback strategies.
        This is a placeholder that will be fully built in Phase 1.
        """
        # Placeholder — returns IDLE. Full implementation in next session.
        return Action(
            type=ActionType.IDLE,
            agent_id=self.state.identity.id,
            tick=tick,
            reasoning=response,
        )

    # -----------------------------------------------------------------------
    # Reflect — update memory and skills after acting
    # -----------------------------------------------------------------------

    def _reflect(self, action: Action, result: ActionResult, tick: int) -> None:
        """Update agent state based on the outcome of an action."""
        # Record to memory
        summary = f"{action.type.name}"
        if action.file_path:
            summary += f" {action.file_path}"
        if result.success:
            summary += " — succeeded"
        else:
            summary += f" — failed: {result.error}"

        self.state.memories.append(AgentMemoryEntry(
            tick=tick,
            summary=summary,
            importance=0.5 if result.success else 0.7,  # failures are more memorable
            source="action",
            related_files=[action.file_path] if action.file_path else [],
            related_agents=action.target_agents,
        ))

        # Update skills (emergent specialisation)
        skill_name = self._action_to_skill(action)
        if skill_name:
            if skill_name not in self.state.skills:
                self.state.skills[skill_name] = AgentSkill(name=skill_name)
            self.state.skills[skill_name].action_count += 1

        # Prune memory if over capacity (keep most important)
        max_memories = 200
        if len(self.state.memories) > max_memories:
            self.state.memories.sort(
                key=lambda m: m.importance * 0.7 + (1.0 / (tick - m.tick + 1)) * 0.3,
                reverse=True,
            )
            self.state.memories = self.state.memories[:max_memories]

    @staticmethod
    def _action_to_skill(action: Action) -> str | None:
        """Map an action to a skill category for emergent specialisation."""
        mapping = {
            ActionType.WRITE_FILE: "coding",
            ActionType.CREATE_FILE: "coding",
            ActionType.RUN_COMMAND: "devops",
            ActionType.COMMUNICATE: "collaboration",
            ActionType.BROADCAST: "collaboration",
            ActionType.REQUEST_REVIEW: "quality",
        }
        return mapping.get(action.type)
