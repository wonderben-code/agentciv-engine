"""Gardener mode — human-in-the-loop mid-run intervention.

You don't command the garden. You shape conditions and prune.

The gardener can:
  - Inject requirements as messages visible to agents
  - Redirect agents by modifying the task context
  - Force a meta-tick (restructuring discussion)
  - Adjust org parameters live
  - Stop the run when satisfied

Interventions are queued between ticks and applied before the next tick.
The agents see the intervention as events and messages — they don't know
(or need to know) that a human is gardening.

CLI usage:
  agentciv solve --task "..." --gardener
  After each tick, type an instruction or press Enter to continue.

MCP usage:
  agentciv_intervene(message="Focus on tests")
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

log = logging.getLogger(__name__)


@dataclass
class Intervention:
    """A human instruction delivered mid-run."""
    type: str  # "message", "redirect", "meta_tick", "adjust", "stop"
    content: str = ""
    target_agents: list[str] = field(default_factory=list)  # empty = all
    parameters: dict[str, Any] = field(default_factory=dict)
    tick: int = 0


class Gardener:
    """Human-in-the-loop mid-run intervention system.

    The gardener submits interventions to a queue. The engine drains
    the queue between ticks and applies each intervention.

    This is designed to work with any frontend (CLI, MCP, web UI) —
    all they need to do is call gardener.submit(intervention).
    """

    def __init__(self) -> None:
        self._queue: list[Intervention] = []
        self._enabled: bool = False
        self._history: list[Intervention] = []

    def enable(self) -> None:
        self._enabled = True

    @property
    def is_enabled(self) -> bool:
        return self._enabled

    def submit(self, intervention: Intervention) -> None:
        """Queue an intervention for the next tick."""
        self._queue.append(intervention)
        self._history.append(intervention)
        log.info("Gardener intervention queued: %s", intervention.type)

    def drain(self) -> list[Intervention]:
        """Get and clear all pending interventions."""
        interventions = list(self._queue)
        self._queue.clear()
        return interventions

    @property
    def intervention_count(self) -> int:
        return len(self._history)

    @staticmethod
    def parse_input(raw: str, tick: int = 0) -> Intervention | None:
        """Parse a CLI input line into an Intervention.

        Formats:
          <text>              → message to all agents
          /redirect <text>    → change task focus
          /meta               → force a meta-tick
          /set <param> <val>  → adjust a parameter
          /stop               → stop the engine
        """
        raw = raw.strip()
        if not raw:
            return None

        if raw.startswith("/stop"):
            return Intervention(type="stop", tick=tick)

        if raw.startswith("/meta"):
            return Intervention(type="meta_tick", tick=tick)

        if raw.startswith("/redirect "):
            content = raw[len("/redirect "):].strip()
            return Intervention(type="redirect", content=content, tick=tick)

        if raw.startswith("/set "):
            parts = raw[len("/set "):].strip().split(None, 1)
            if len(parts) == 2:
                return Intervention(
                    type="adjust",
                    parameters={parts[0]: parts[1]},
                    tick=tick,
                )
            return None

        # Default: message to all agents
        return Intervention(type="message", content=raw, tick=tick)
