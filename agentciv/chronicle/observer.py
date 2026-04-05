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
class TickSnapshot:
    """Per-tick metric snapshot for temporal analysis (Tier 3).

    Captured at the end of every tick. Enables phase transition detection,
    convergence speed analysis, and predictive models (can tick-10 predict outcome?).
    """
    tick: int
    files_created_cumulative: int = 0
    files_modified_cumulative: int = 0
    messages_cumulative: int = 0
    broadcasts_cumulative: int = 0
    merge_conflicts_cumulative: int = 0
    merges_succeeded_cumulative: int = 0
    active_agents: int = 0  # agents that took non-idle actions this tick
    # Per-agent file ops this tick (for computing running Gini)
    agent_file_ops: dict[str, int] = field(default_factory=dict)
    # Per-tick relationship trust snapshot (for research export)
    # Format: {"AgentA → AgentB": trust_score, ...}
    relationships: dict[str, float] = field(default_factory=dict)


@dataclass
class ConflictRecord:
    """Tracks a single merge conflict from detection to resolution (Step 0c).

    Resolution is detected when the same file is successfully merged in a later tick.
    Delta (resolved_tick - detected_tick) = conflict resolution time.
    """
    file: str
    agent_id: str
    detected_tick: int
    resolved_tick: int | None = None

    @property
    def resolution_time(self) -> int | None:
        if self.resolved_tick is not None:
            return self.resolved_tick - self.detected_tick
        return None


@dataclass
class TimelineEntry:
    """A notable moment in the run."""
    tick: int
    event_type: str
    agent: str | None
    summary: str
    content: str | None = None  # full message/reasoning text for research export
    reasoning: str | None = None  # agent's reasoning behind this action


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

    # Benchmark additions
    tick_snapshots: list[TickSnapshot] = field(default_factory=list)
    conflict_records: list[ConflictRecord] = field(default_factory=list)
    tokens_per_agent: dict[str, int] = field(default_factory=dict)  # injected post-run

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
                    **({"content": e.content} if e.content else {}),
                    **({"reasoning": e.reasoning} if e.reasoning else {}),
                }
                for e in self.timeline
            ],
            "tick_snapshots": [
                {
                    "tick": s.tick,
                    "files_created": s.files_created_cumulative,
                    "files_modified": s.files_modified_cumulative,
                    "messages": s.messages_cumulative,
                    "broadcasts": s.broadcasts_cumulative,
                    "merge_conflicts": s.merge_conflicts_cumulative,
                    "merges_succeeded": s.merges_succeeded_cumulative,
                    "active_agents": s.active_agents,
                    "agent_file_ops": s.agent_file_ops,
                    **({"relationships": s.relationships} if s.relationships else {}),
                }
                for s in self.tick_snapshots
            ],
            "conflict_records": [
                {
                    "file": c.file,
                    "agent_id": c.agent_id,
                    "detected_tick": c.detected_tick,
                    "resolved_tick": c.resolved_tick,
                    "resolution_time": c.resolution_time,
                }
                for c in self.conflict_records
            ],
            "tokens_per_agent": self.tokens_per_agent,
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

        # Benchmark: per-tick snapshots (Step 0b)
        self._tick_snapshots: list[TickSnapshot] = []
        self._tick_active_agents: set[str] = set()  # reset each tick
        self._tick_agent_file_ops: dict[str, int] = defaultdict(int)  # reset each tick

        # Benchmark: conflict resolution timing (Step 0c)
        self._conflict_records: list[ConflictRecord] = []
        self._unresolved_conflicts: dict[str, ConflictRecord] = {}  # file → record

    def observe(self, event: Event) -> None:
        """Event handler — called for every event via event_bus.subscribe."""
        self._last_tick = max(self._last_tick, event.tick)

        match event.type:
            case EventType.TICK_START:
                # Reset per-tick trackers
                self._tick_active_agents.clear()
                self._tick_agent_file_ops.clear()

            case EventType.FILE_CREATED:
                f = event.data.get("file", "?")
                self._files_created.append(f)
                self._total_modifications += 1
                agent = self._get_agent(event.agent_id)
                if agent:
                    agent.files_created.append(f)
                if event.agent_id:
                    self._tick_active_agents.add(event.agent_id)
                    self._tick_agent_file_ops[event.agent_id] += 1
                self._add_timeline(
                    event, f"created {f}",
                    reasoning=event.data.get("reasoning"),
                )

            case EventType.FILE_MODIFIED:
                f = event.data.get("file", "?")
                self._total_modifications += 1
                agent = self._get_agent(event.agent_id)
                if agent:
                    if f not in agent.files_modified:
                        agent.files_modified.append(f)
                if event.agent_id:
                    self._tick_active_agents.add(event.agent_id)
                    self._tick_agent_file_ops[event.agent_id] += 1

            case EventType.MESSAGE_SENT:
                self._total_messages += 1
                agent = self._get_agent(event.agent_id)
                if agent:
                    agent.messages_sent += 1
                if event.agent_id:
                    self._tick_active_agents.add(event.agent_id)
                targets = event.data.get("targets", [])
                for t in targets:
                    if t and event.agent_id:
                        sender = self._agent_names.get(event.agent_id, event.agent_id)
                        target = self._agent_names.get(t, t)
                        key = f"{sender} → {target}"
                        self._comm_pairs[key] += 1
                # Capture full message content for research export
                msg_content = event.data.get("content") or event.data.get("content_preview", "")
                msg_reasoning = event.data.get("reasoning")
                preview = (msg_content or "")[:60]
                target_names = [self._agent_names.get(t, t) for t in targets]
                self._add_timeline(
                    event, f"→ {', '.join(target_names)}: {preview}",
                    content=msg_content, reasoning=msg_reasoning,
                )

            case EventType.BROADCAST_SENT:
                self._total_broadcasts += 1
                agent = self._get_agent(event.agent_id)
                if agent:
                    agent.broadcasts_sent += 1
                if event.agent_id:
                    self._tick_active_agents.add(event.agent_id)
                # Capture full broadcast content for research export
                bcast_content = event.data.get("content") or event.data.get("content_preview", "")
                bcast_reasoning = event.data.get("reasoning")
                preview = (bcast_content or "")[:60]
                self._add_timeline(
                    event, f"broadcast: {preview}",
                    content=bcast_content, reasoning=bcast_reasoning,
                )

            case EventType.TASK_CLAIMED:
                task_content = event.data.get("content") or event.data.get("content_preview", "")
                preview = task_content[:80] if task_content else ""
                agent = self._get_agent(event.agent_id)
                if agent and preview:
                    agent.tasks_claimed.append(preview)
                if event.agent_id:
                    self._tick_active_agents.add(event.agent_id)
                self._add_timeline(
                    event, f"claimed: {preview[:60]}",
                    content=task_content, reasoning=event.data.get("reasoning"),
                )

            case EventType.REVIEW_REQUESTED:
                agent = self._get_agent(event.agent_id)
                if agent:
                    agent.reviews_requested += 1
                if event.agent_id:
                    self._tick_active_agents.add(event.agent_id)

            case EventType.BRANCH_MERGED:
                self._merges_succeeded += 1
                count = event.data.get("count", 0)
                agent = self._get_agent(event.agent_id)
                if agent:
                    agent.merges_succeeded += 1
                if event.agent_id:
                    self._tick_active_agents.add(event.agent_id)
                if count > 2:
                    self._add_timeline(event, f"merged {count} files")
                # Check if this resolves any previously conflicted files
                merged_files = event.data.get("files", [])
                for f in merged_files:
                    if f in self._unresolved_conflicts:
                        self._unresolved_conflicts[f].resolved_tick = event.tick
                        del self._unresolved_conflicts[f]

            case EventType.MERGE_CONFLICT:
                self._merge_conflicts += 1
                conflicts = event.data.get("conflicts", [])
                agent = self._get_agent(event.agent_id)
                if agent:
                    agent.merge_conflicts += 1
                # Track conflict timing (Step 0c)
                for f in conflicts:
                    record = ConflictRecord(
                        file=f,
                        agent_id=event.agent_id or "",
                        detected_tick=event.tick,
                    )
                    self._conflict_records.append(record)
                    self._unresolved_conflicts[f] = record
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

            case EventType.TICK_END:
                # Capture per-tick metric snapshot (Step 0b)
                snapshot = TickSnapshot(
                    tick=event.tick,
                    files_created_cumulative=len(self._files_created),
                    files_modified_cumulative=self._total_modifications,
                    messages_cumulative=self._total_messages,
                    broadcasts_cumulative=self._total_broadcasts,
                    merge_conflicts_cumulative=self._merge_conflicts,
                    merges_succeeded_cumulative=self._merges_succeeded,
                    active_agents=len(self._tick_active_agents),
                    agent_file_ops=dict(self._tick_agent_file_ops),
                    relationships=event.data.get("relationships", {}),
                )
                self._tick_snapshots.append(snapshot)

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
            tick_snapshots=self._tick_snapshots,
            conflict_records=self._conflict_records,
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

    def _add_timeline(
        self, event: Event, summary: str,
        content: str | None = None, reasoning: str | None = None,
    ) -> None:
        """Add a notable moment to the timeline."""
        agent_display = self._agent_names.get(event.agent_id, event.agent_id) if event.agent_id else None
        self._timeline.append(TimelineEntry(
            tick=event.tick,
            event_type=event.type.name,
            agent=agent_display,
            summary=summary,
            content=content,
            reasoning=reasoning,
        ))
