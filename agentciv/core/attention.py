"""Attention map — shared persistent view of who's working on what.

Like a shared kanban board that agents check before starting work.
Prevents duplicated effort — the key coordination problem beyond 3 agents.

The attention map is a first-class context source. Every agent sees it
alongside files, messages, and events. It answers: "What is everyone
doing right now, and what files are they touching?"

Updated in real-time as agents claim/release tasks and modify files.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

log = logging.getLogger(__name__)


@dataclass
class AttentionEntry:
    """What one agent is currently focused on."""
    agent_id: str
    agent_name: str
    focus: str | None = None  # current task description
    active_files: list[str] = field(default_factory=list)  # files being touched
    last_action: str = ""  # most recent action description
    last_tick: int = 0
    idle_ticks: int = 0  # how long since last action

    @property
    def is_active(self) -> bool:
        return self.idle_ticks < 3


@dataclass
class AttentionMap:
    """Shared view of all agent activity. Updated by the engine each tick."""

    _entries: dict[str, AttentionEntry] = field(default_factory=dict)

    def register_agent(self, agent_id: str, agent_name: str) -> None:
        """Register an agent in the attention map."""
        self._entries[agent_id] = AttentionEntry(
            agent_id=agent_id,
            agent_name=agent_name,
        )

    def update_focus(self, agent_id: str, focus: str | None) -> None:
        """Update what an agent is working on."""
        if agent_id in self._entries:
            self._entries[agent_id].focus = focus

    def update_files(self, agent_id: str, file_path: str) -> None:
        """Record that an agent is touching a file."""
        if agent_id in self._entries:
            entry = self._entries[agent_id]
            if file_path not in entry.active_files:
                entry.active_files.append(file_path)
                # Keep only recent files (last 5)
                if len(entry.active_files) > 5:
                    entry.active_files = entry.active_files[-5:]

    def update_action(self, agent_id: str, action_desc: str, tick: int) -> None:
        """Record an agent's most recent action."""
        if agent_id in self._entries:
            entry = self._entries[agent_id]
            entry.last_action = action_desc
            entry.last_tick = tick
            entry.idle_ticks = 0

    def tick_idle(self, tick: int) -> None:
        """Increment idle counters for agents that didn't act this tick."""
        for entry in self._entries.values():
            if entry.last_tick < tick:
                entry.idle_ticks += 1

    def get_entry(self, agent_id: str) -> AttentionEntry | None:
        return self._entries.get(agent_id)

    def is_file_being_worked_on(self, file_path: str, exclude_agent: str = "") -> str | None:
        """Check if any agent is currently working on a file.

        Returns the agent name if someone is working on it, None otherwise.
        Used for soft contention signalling before git-level locking.
        """
        for entry in self._entries.values():
            if entry.agent_id == exclude_agent:
                continue
            if file_path in entry.active_files and entry.is_active:
                return entry.agent_name
        return None

    def get_claimed_tasks(self) -> list[dict[str, str]]:
        """Return all currently claimed tasks with agent names."""
        return [
            {"agent": e.agent_name, "task": e.focus}
            for e in self._entries.values()
            if e.focus and e.is_active
        ]

    def to_prompt_context(self, exclude_agent: str = "") -> str:
        """Render the attention map as context for an agent's prompt.

        This is what agents actually see — a clear picture of who's doing what.
        """
        lines: list[str] = []
        for entry in self._entries.values():
            if entry.agent_id == exclude_agent:
                continue
            if not entry.is_active:
                lines.append(f"  {entry.agent_name}: idle")
                continue

            parts = [entry.agent_name + ":"]
            if entry.focus:
                parts.append(f"working on \"{entry.focus}\"")
            if entry.active_files:
                parts.append(f"files: {', '.join(entry.active_files[-3:])}")
            if entry.last_action:
                parts.append(f"last: {entry.last_action}")

            lines.append("  " + " | ".join(parts))

        if not lines:
            return ""
        return "Team activity (attention map):\n" + "\n".join(lines)

    def to_dict(self) -> list[dict[str, Any]]:
        """Serialise for chronicle/logging."""
        return [
            {
                "agent_id": e.agent_id,
                "agent_name": e.agent_name,
                "focus": e.focus,
                "active_files": e.active_files,
                "last_action": e.last_action,
                "idle_ticks": e.idle_ticks,
            }
            for e in self._entries.values()
        ]
