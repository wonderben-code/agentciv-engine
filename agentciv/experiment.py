"""Experiment mode — the research flywheel in one command.

Run the same task under multiple organisational configurations and
produce a comparison report. Every experiment is data for Computational
Organisational Theory.

Usage:
  agentciv experiment \
    --task "Build a REST API with auth" \
    --orgs collaborative,competitive,meritocratic,auto \
    --runs 2 \
    --agents 4 \
    --max-ticks 30

Produces:
  - Per-org chronicle reports
  - Comparison table: ticks to completion, files, communication, conflicts
  - JSON output for further analysis
"""

from __future__ import annotations

import logging
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .chronicle.observer import ChronicleReport
from .core.agent import Agent
from .core.attention import AttentionMap
from .core.engine import Engine
from .core.event_bus import EventBus
from .core.types import AgentIdentity, AgentState
from .learning.recorder import save_run
from .llm.client import create_client
from .org.config import EngineConfig
from .org.enforcer import OrgEnforcer
from .workspace.executor import WorkspaceExecutor
from .workspace.workspace import Workspace

log = logging.getLogger(__name__)

AGENT_NAMES = [
    "Atlas", "Nova", "Sage", "Flux", "Echo",
    "Drift", "Pulse", "Cinder", "Wren", "Quill",
]


@dataclass
class ExperimentRun:
    """Result of a single run within an experiment."""
    org_preset: str
    run_index: int
    report: ChronicleReport
    success: bool = True
    error: str | None = None


@dataclass
class ExperimentResult:
    """Full result of an experiment across multiple org configs."""
    task: str
    orgs: list[str]
    runs_per_org: int
    agent_count: int
    max_ticks: int
    model: str
    runs: list[ExperimentRun] = field(default_factory=list)

    def to_terminal(self) -> str:
        """Render comparison table for the terminal."""
        lines: list[str] = []
        lines.append("")
        lines.append("  Experiment Report")
        lines.append(f"  {'─' * 60}")
        lines.append(f"  Task: {self.task}")
        lines.append(f"  Agents: {self.agent_count} | Max ticks: {self.max_ticks} | Model: {self.model}")
        lines.append(f"  Configurations: {', '.join(self.orgs)} | Runs per config: {self.runs_per_org}")
        lines.append("")

        # Comparison table
        header = f"  {'Org':20s} {'Ticks':>6s} {'Files':>6s} {'Msgs':>6s} {'Bcasts':>7s} {'Merges':>7s} {'Conflicts':>10s}"
        lines.append(header)
        lines.append(f"  {'─' * 68}")

        for org in self.orgs:
            org_runs = [r for r in self.runs if r.org_preset == org and r.success]
            if not org_runs:
                lines.append(f"  {org:20s} {'FAILED':>6s}")
                continue

            for run in org_runs:
                r = run.report
                suffix = f" (run {run.run_index + 1})" if self.runs_per_org > 1 else ""
                lines.append(
                    f"  {org + suffix:20s} "
                    f"{r.total_ticks:6d} "
                    f"{len(r.files_created):6d} "
                    f"{r.total_messages:6d} "
                    f"{r.total_broadcasts:7d} "
                    f"{r.merges_succeeded:7d} "
                    f"{r.merge_conflicts:10d}"
                )

            # Average if multiple runs
            if len(org_runs) > 1:
                avg_ticks = sum(r.report.total_ticks for r in org_runs) / len(org_runs)
                avg_files = sum(len(r.report.files_created) for r in org_runs) / len(org_runs)
                avg_msgs = sum(r.report.total_messages for r in org_runs) / len(org_runs)
                lines.append(
                    f"  {'  ↳ average':20s} "
                    f"{avg_ticks:6.1f} "
                    f"{avg_files:6.1f} "
                    f"{avg_msgs:6.1f}"
                )

        lines.append(f"  {'─' * 60}")

        # Org dynamics summary for auto runs
        auto_runs = [r for r in self.runs if r.org_preset == "auto" and r.success]
        if auto_runs:
            lines.append("")
            lines.append("  Auto-org dynamics:")
            for run in auto_runs:
                r = run.report
                if r.restructures_adopted:
                    for change in r.restructure_log:
                        dim = change.get("dimension", "?")
                        val = change.get("new_value", "?")
                        lines.append(f"    run {run.run_index + 1}: {dim} → {val}")
                else:
                    lines.append(f"    run {run.run_index + 1}: no restructures adopted")

        lines.append("")
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        """Serialisable dict for JSON output."""
        return {
            "task": self.task,
            "orgs": self.orgs,
            "runs_per_org": self.runs_per_org,
            "agent_count": self.agent_count,
            "max_ticks": self.max_ticks,
            "model": self.model,
            "runs": [
                {
                    "org_preset": r.org_preset,
                    "run_index": r.run_index,
                    "success": r.success,
                    "error": r.error,
                    "report": r.report.to_dict() if r.success else None,
                }
                for r in self.runs
            ],
        }


async def run_single(
    task: str,
    org_preset: str,
    agent_count: int,
    model: str,
    max_ticks: int,
    project_dir: Path,
    verbose: bool = False,
) -> ChronicleReport:
    """Run a single engine instance and return its chronicle report."""
    config = EngineConfig.from_preset(org_preset)
    config.task = task
    config.agent_count = agent_count
    config.model = model
    config.max_ticks = max_ticks
    config.project_dir = str(project_dir)
    config.enable_chronicle = True

    workspace = Workspace(project_dir=project_dir, task_description=task)
    workspace.scan()

    event_bus = EventBus()
    attention = AttentionMap()

    agents: list[Agent] = []
    for i in range(agent_count):
        name = AGENT_NAMES[i % len(AGENT_NAMES)]
        agent_id = f"agent_{i}"
        # Per-agent model: check by agent_id, then by name, then default
        agent_model = config.models.get(agent_id) or config.models.get(name) or model
        identity = AgentIdentity(id=agent_id, name=name, model=agent_model)
        state = AgentState(
            identity=identity,
            token_budget_remaining=config.parameters.token_budget_per_agent,
        )
        llm = create_client(agent_model, max_tokens=4096)
        executor = WorkspaceExecutor(workspace, attention=attention)
        agent = Agent(state=state, llm=llm, executor=executor)
        workspace.register_agent(state)
        agents.append(agent)

    enforcer = OrgEnforcer(
        dimensions=config.org_dimensions,
        parameters=config.parameters,
    )
    enforcer.assign_initial_roles([a.state.identity.id for a in agents])

    engine = Engine(
        config=config,
        workspace=workspace,
        agents=agents,
        event_bus=event_bus,
        enforcer=enforcer,
        attention=attention,
    )

    await engine.run()
    report = engine.chronicle.generate_report()

    # Save to learning history
    try:
        save_run(
            report=report,
            org_dimensions=config.org_dimensions,
            model=model,
            max_ticks=max_ticks,
        )
    except Exception as e:
        log.warning("Failed to save learning record: %s", e)

    return report


async def run_experiment(
    task: str,
    orgs: list[str],
    runs_per_org: int = 1,
    agent_count: int = 4,
    model: str = "claude-sonnet-4-6",
    max_ticks: int = 30,
    source_dir: str = ".",
    verbose: bool = False,
) -> ExperimentResult:
    """Run a full experiment: same task across multiple org configs.

    Each run gets a fresh copy of the project directory so runs are
    completely independent.
    """
    result = ExperimentResult(
        task=task,
        orgs=orgs,
        runs_per_org=runs_per_org,
        agent_count=agent_count,
        max_ticks=max_ticks,
        model=model,
    )

    source = Path(source_dir).resolve()
    total_runs = len(orgs) * runs_per_org

    from . import display
    display.console.print(
        f"\n  [bold]Experiment:[/bold] {total_runs} runs "
        f"[dim]({len(orgs)} orgs × {runs_per_org} each)[/dim]"
    )
    display.console.print(f"  [dim]{'─' * 50}[/dim]\n")

    run_number = 0
    for org in orgs:
        for run_idx in range(runs_per_org):
            run_number += 1
            display.show_experiment_progress(run_number, total_runs, org, run_idx)

            try:
                # Fresh project copy for each run
                with tempfile.TemporaryDirectory() as tmpdir:
                    project = Path(tmpdir) / "project"
                    if source.exists() and any(source.iterdir()):
                        try:
                            shutil.copytree(
                                source, project,
                                ignore=shutil.ignore_patterns(
                                    ".git", ".agentciv", "__pycache__",
                                    "node_modules", ".venv", "venv",
                                ),
                                copy_function=shutil.copy2,
                            )
                        except shutil.Error:
                            # Fallback: create empty project if copy fails
                            # (e.g. socket files, permission issues)
                            if not project.exists():
                                project.mkdir(parents=True)
                    else:
                        project.mkdir()

                    report = await run_single(
                        task=task,
                        org_preset=org,
                        agent_count=agent_count,
                        model=model,
                        max_ticks=max_ticks,
                        project_dir=project,
                        verbose=verbose,
                    )

                    result.runs.append(ExperimentRun(
                        org_preset=org,
                        run_index=run_idx,
                        report=report,
                    ))
                    display.show_experiment_run_done(report.total_ticks)

            except Exception as e:
                log.exception("Run failed: %s run %d", org, run_idx)
                result.runs.append(ExperimentRun(
                    org_preset=org,
                    run_index=run_idx,
                    report=ChronicleReport(task=task, org_preset=org, agent_count=agent_count, total_ticks=0),
                    success=False,
                    error=str(e),
                ))
                display.show_experiment_run_failed(str(e))

    return result
