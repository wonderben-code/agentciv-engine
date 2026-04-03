"""Chronicle observer — watches the engine run and produces structured reports.

Every run produces data. The chronicle captures what happened, who did what,
how agents collaborated, and how the organisation evolved. This is the
foundation for the research flywheel: tool → data → research → better presets.

The chronicle subscribes to the event bus and accumulates statistics.
Call generate_report() at the end for the full picture.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from ..core.types import Event, EventType


@dataclass
class AgentContribution:
    """Summary of what one agent did during the run."""
    agent_id: str
    agent_name: str = ""
    files_created: list[str] = field(default_factory=list)
    files_modified: list[str] = field(default_factory=list)
    messages_sent: int = 0
    broadcasts_sent: int = 0
    tasks_claimed: list[str] = field(default_factory=list)
    reviews_requested: int = 0
    proposals_made: int = 0
    votes_cast: int = 0
    merge_conflicts: int = 0
    merges_succeeded: int = 0


@dataclass
class TimelineEntry:
    """A notable moment in the run."""
    tick: int
    event_type: str
    agent: str | None
    summary: str


@dataclass
class ChronicleReport:
    """Full structured report of an engine run.

    Every field is data, not narrative. Downstream consumers (CLI, website,
    experiment mode, whitepaper) can format this however they want.
    """
    # Run metadata
    task: str
    org_preset: str
    agent_count: int
    total_ticks: int

    # Per-agent contributions
    contributions: list[AgentContribution] = field(default_factory=list)

    # Communication
    total_messages: int = 0
    total_broadcasts: int = 0
    communication_pairs: dict[str, int] = field(default_factory=dict)  # "A→B" → count

    # Files
    files_created: list[str] = field(default_factory=list)
    total_file_modifications: int = 0

    # Git
    merges_succeeded: int = 0
    merge_conflicts: int = 0

    # Organisation dynamics
    restructures_proposed: int = 0
    restructures_adopted: int = 0
    restructure_log: list[dict[str, Any]] = field(default_factory=list)

    # Build & test
    final_build_status: str = "unknown"
    final_test_status: str = "unknown"

    # Timeline — key moments
    timeline: list[TimelineEntry] = field(default_factory=list)

    def to_terminal(self) -> str:
        """Render a clean terminal summary."""
        lines: list[str] = []
        lines.append("")
        lines.append("  Chronicle Report")
        lines.append(f"  {'─' * 50}")
        lines.append(f"  Task: {self.task}")
        lines.append(f"  Org: {self.org_preset} | Agents: {self.agent_count} | Ticks: {self.total_ticks}")
        lines.append("")

        # Agent contributions
        lines.append("  Agent Contributions:")
        for c in self.contributions:
            created = len(c.files_created)
            modified = len(c.files_modified)
            lines.append(
                f"    {c.agent_name:12s} "
                f"files: {created} created, {modified} modified | "
                f"msgs: {c.messages_sent} sent, {c.broadcasts_sent} broadcast"
            )
            if c.tasks_claimed:
                lines.append(f"{'':16s} tasks: {', '.join(c.tasks_claimed[:3])}")
            if c.merge_conflicts:
                lines.append(f"{'':16s} conflicts: {c.merge_conflicts}")
        lines.append("")

        # Communication
        if self.communication_pairs:
            lines.append("  Communication Patterns:")
            sorted_pairs = sorted(
                self.communication_pairs.items(),
                key=lambda x: x[1],
                reverse=True,
            )
            for pair, count in sorted_pairs[:8]:
                lines.append(f"    {pair}: {count} messages")
            lines.append("")

        # Git
        if self.merges_succeeded or self.merge_conflicts:
            lines.append(
                f"  Git: {self.merges_succeeded} merges, "
                f"{self.merge_conflicts} conflicts"
            )

        # Org dynamics
        if self.restructures_proposed:
            lines.append(
                f"  Organisation: {self.restructures_proposed} proposals, "
                f"{self.restructures_adopted} adopted"
            )
            for r in self.restructure_log:
                lines.append(
                    f"    tick {r.get('tick', '?')}: "
                    f"{r.get('dimension', '?')} → {r.get('new_value', '?')}"
                )

        # Build/test
        if self.final_test_status != "unknown" or self.final_build_status != "unknown":
            lines.append(
                f"  Build: {self.final_build_status} | "
                f"Tests: {self.final_test_status}"
            )

        # Timeline highlights
        if self.timeline:
            lines.append("")
            lines.append("  Timeline:")
            for entry in self.timeline[:15]:
                agent_str = f" {entry.agent}" if entry.agent else ""
                lines.append(f"    [{entry.tick:3d}]{agent_str} {entry.summary}")

        lines.append(f"  {'─' * 50}")
        lines.append("")
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        """Serialisable dict for JSON output and experiment mode."""
        return {
            "task": self.task,
            "org_preset": self.org_preset,
            "agent_count": self.agent_count,
            "total_ticks": self.total_ticks,
            "contributions": [
                {
                    "agent_id": c.agent_id,
                    "agent_name": c.agent_name,
                    "files_created": c.files_created,
                    "files_modified": c.files_modified,
                    "messages_sent": c.messages_sent,
                    "broadcasts_sent": c.broadcasts_sent,
                    "tasks_claimed": c.tasks_claimed,
                    "merge_conflicts": c.merge_conflicts,
                }
                for c in self.contributions
            ],
            "communication": {
                "total_messages": self.total_messages,
                "total_broadcasts": self.total_broadcasts,
                "pairs": self.communication_pairs,
            },
            "files": {
                "created": self.files_created,
                "total_modifications": self.total_file_modifications,
            },
            "git": {
                "merges_succeeded": self.merges_succeeded,
                "merge_conflicts": self.merge_conflicts,
            },
            "organisation": {
                "restructures_proposed": self.restructures_proposed,
                "restructures_adopted": self.restructures_adopted,
                "restructure_log": self.restructure_log,
            },
            "build_status": self.final_build_status,
            "test_status": self.final_test_status,
            "timeline": [
                {
                    "tick": e.tick,
                    "type": e.event_type,
                    "agent": e.agent,
                    "summary": e.summary,
                }
                for e in self.timeline
            ],
        }


class Chronicle:
    """Observer that watches the engine run and produces a structured report.

    Usage:
        chronicle = Chronicle(task="Build API", org_preset="collaborative", agent_count=4)
        event_bus.subscribe(None, chronicle.observe)
        # ... engine runs ...
        report = chronicle.generate_report()
        print(report.to_terminal())
    """

    def __init__(
        self, task: str, org_preset: str, agent_count: int,
        agent_names: dict[str, str] | None = None,
    ):
        self.task = task
        self.org_preset = org_preset
        self.agent_count = agent_count
        self._agent_names = agent_names or {}  # agent_id → display name

        # Accumulation state
        self._agents: dict[str, AgentContribution] = {}
        self._timeline: list[TimelineEntry] = []
        self._comm_pairs: dict[str, int] = defaultdict(int)
        self._files_created: list[str] = []
        self._total_modifications: int = 0
        self._merges_succeeded: int = 0
        self._merge_conflicts: int = 0
        self._restructures_proposed: int = 0
        self._restructures_adopted: int = 0
        self._restructure_log: list[dict[str, Any]] = []
        self._build_status: str = "unknown"
        self._test_status: str = "unknown"
        self._total_messages: int = 0
        self._total_broadcasts: int = 0
        self._last_tick: int = 0

    def observe(self, event: Event) -> None:
        """Event handler — called for every event via event_bus.subscribe."""
        self._last_tick = max(self._last_tick, event.tick)

        match event.type:
            case EventType.FILE_CREATED:
                f = event.data.get("file", "?")
                self._files_created.append(f)
                self._total_modifications += 1
                agent = self._get_agent(event.agent_id)
                if agent:
                    agent.files_created.append(f)
                self._add_timeline(event, f"created {f}")

            case EventType.FILE_MODIFIED:
                f = event.data.get("file", "?")
                self._total_modifications += 1
                agent = self._get_agent(event.agent_id)
                if agent:
                    if f not in agent.files_modified:
                        agent.files_modified.append(f)

            case EventType.MESSAGE_SENT:
                self._total_messages += 1
                agent = self._get_agent(event.agent_id)
                if agent:
                    agent.messages_sent += 1
                targets = event.data.get("targets", [])
                for t in targets:
                    if t and event.agent_id:
                        key = f"{event.agent_id} → {t}"
                        self._comm_pairs[key] += 1

            case EventType.BROADCAST_SENT:
                self._total_broadcasts += 1
                agent = self._get_agent(event.agent_id)
                if agent:
                    agent.broadcasts_sent += 1

            case EventType.TASK_CLAIMED:
                preview = event.data.get("content_preview", "")
                agent = self._get_agent(event.agent_id)
                if agent and preview:
                    agent.tasks_claimed.append(preview[:80])
                self._add_timeline(event, f"claimed: {preview[:60]}")

            case EventType.REVIEW_REQUESTED:
                agent = self._get_agent(event.agent_id)
                if agent:
                    agent.reviews_requested += 1

            case EventType.BRANCH_MERGED:
                self._merges_succeeded += 1
                count = event.data.get("count", 0)
                agent = self._get_agent(event.agent_id)
                if agent:
                    agent.merges_succeeded += 1
                if count > 2:
                    self._add_timeline(event, f"merged {count} files")

            case EventType.MERGE_CONFLICT:
                self._merge_conflicts += 1
                conflicts = event.data.get("conflicts", [])
                agent = self._get_agent(event.agent_id)
                if agent:
                    agent.merge_conflicts += 1
                self._add_timeline(
                    event, f"CONFLICT: {', '.join(conflicts)}"
                )

            case EventType.RESTRUCTURE_PROPOSED:
                self._restructures_proposed += 1
                agent = self._get_agent(event.agent_id)
                if agent:
                    agent.proposals_made += 1
                preview = event.data.get("content_preview", "")
                self._add_timeline(event, f"proposed restructure: {preview[:60]}")

            case EventType.RESTRUCTURE_VOTED:
                agent = self._get_agent(event.agent_id)
                if agent:
                    agent.votes_cast += 1

            case EventType.RESTRUCTURE_ADOPTED:
                self._restructures_adopted += 1
                self._restructure_log.append(event.data)
                dim = event.data.get("dimension", "?")
                new_val = event.data.get("new_value", "?")
                self._add_timeline(
                    event, f"RESTRUCTURED: {dim} → {new_val}"
                )

            case EventType.TESTS_PASSED:
                self._test_status = "passing"
                self._add_timeline(event, "tests passing")

            case EventType.TESTS_FAILED:
                self._test_status = "failing"
                self._add_timeline(event, "tests failing")

            case EventType.BUILD_SUCCEEDED:
                self._build_status = "passing"

            case EventType.BUILD_FAILED:
                self._build_status = "failing"
                self._add_timeline(event, "build failed")

            case EventType.ENGINE_STARTED:
                agents = event.data.get("agents", "?")
                org = event.data.get("config", "?")
                self._add_timeline(
                    event, f"engine started: {agents} agents, org={org}"
                )

            case EventType.ENGINE_STOPPED:
                self._add_timeline(event, "engine stopped")

    def generate_report(self) -> ChronicleReport:
        """Produce the final structured report."""
        return ChronicleReport(
            task=self.task,
            org_preset=self.org_preset,
            agent_count=self.agent_count,
            total_ticks=self._last_tick,
            contributions=list(self._agents.values()),
            total_messages=self._total_messages,
            total_broadcasts=self._total_broadcasts,
            communication_pairs=dict(self._comm_pairs),
            files_created=self._files_created,
            total_file_modifications=self._total_modifications,
            merges_succeeded=self._merges_succeeded,
            merge_conflicts=self._merge_conflicts,
            restructures_proposed=self._restructures_proposed,
            restructures_adopted=self._restructures_adopted,
            restructure_log=self._restructure_log,
            final_build_status=self._build_status,
            final_test_status=self._test_status,
            timeline=self._timeline,
        )

    # --- Private helpers ---

    def _get_agent(self, agent_id: str | None) -> AgentContribution | None:
        """Get or create agent contribution tracker."""
        if not agent_id:
            return None
        if agent_id not in self._agents:
            name = self._agent_names.get(agent_id, agent_id)
            self._agents[agent_id] = AgentContribution(agent_id=agent_id, agent_name=name)
        return self._agents[agent_id]

    def _add_timeline(self, event: Event, summary: str) -> None:
        """Add a notable moment to the timeline."""
        self._timeline.append(TimelineEntry(
            tick=event.tick,
            event_type=event.type.name,
            agent=event.agent_id,
            summary=summary,
        ))
