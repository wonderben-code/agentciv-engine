"""Benchmark runner — orchestrates task x preset x run matrix.

Reuses the existing experiment.run_single() for engine execution.
Adds seed file setup, verification, metrics extraction, and statistics.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..chronicle.observer import ChronicleReport
from ..experiment import run_single
from .metrics import (
    AggregatedMetrics,
    RunMetrics,
    VerificationResult,
    aggregate,
    extract_metrics,
)
from .tasks import TASK_BANK, BenchmarkTask, get_all_tasks

log = logging.getLogger(__name__)

# All 13 presets
ALL_PRESETS = [
    "collaborative", "competitive", "meritocratic", "auto",
    "hierarchical", "startup", "pair-programming", "open-source",
    "military", "research-lab", "swarm", "hackathon", "code-review",
]


@dataclass
class BenchmarkConfig:
    """Configuration for a benchmark run."""
    tasks: list[str]  # task IDs
    presets: list[str]  # preset names
    runs_per_combo: int = 3
    agent_count: int = 4
    model: str = "claude-sonnet-4-6"
    max_ticks_override: int | None = None  # override per-task defaults
    dry_run: bool = False
    mock: bool = False
    output_path: str | None = None
    verbose: bool = False


@dataclass
class SingleRunResult:
    """Result of one (task, preset, run_index) execution."""
    task_id: str
    preset: str
    run_index: int
    report: ChronicleReport
    verification: VerificationResult
    metrics: RunMetrics
    success: bool = True
    error: str | None = None
    wall_time_seconds: float = 0.0


async def run_benchmark(config: BenchmarkConfig) -> dict[str, Any]:
    """Run the full benchmark matrix and return results.

    Returns a dict suitable for BenchmarkResult construction.
    """
    from .report import BenchmarkResult

    # Resolve task list
    tasks: list[BenchmarkTask] = []
    for task_id in config.tasks:
        if task_id == "all":
            tasks = get_all_tasks()
            break
        elif task_id in ("simple", "medium", "hard"):
            from .tasks import get_tasks_by_difficulty
            tasks.extend(get_tasks_by_difficulty(task_id))
        elif task_id in TASK_BANK:
            tasks.append(TASK_BANK[task_id])
        else:
            log.warning("Unknown task: %s", task_id)

    # Resolve preset list
    presets = config.presets
    if "all" in presets:
        presets = ALL_PRESETS

    # Determine model (mock mode overrides)
    model = "mock" if config.mock else config.model

    total_runs = len(tasks) * len(presets) * config.runs_per_combo

    # Dry run — just print the plan
    if config.dry_run:
        return _dry_run_plan(tasks, presets, config, total_runs)

    print(f"\n  AgentCiv Benchmark")
    print(f"  {'─' * 60}")
    print(f"  Tasks: {len(tasks)} | Presets: {len(presets)} | Runs per combo: {config.runs_per_combo}")
    print(f"  Total runs: {total_runs} | Model: {model} | Agents: {config.agent_count}")
    print(f"  {'─' * 60}\n")

    runs: list[SingleRunResult] = []
    run_number = 0
    start_time = time.time()

    for task in tasks:
        print(f"  Task: {task.name} ({task.difficulty})")
        print(f"  {'─' * 50}")

        for preset in presets:
            for run_idx in range(config.runs_per_combo):
                run_number += 1
                max_ticks = config.max_ticks_override or task.max_ticks
                suffix = f" run {run_idx + 1}" if config.runs_per_combo > 1 else ""
                print(
                    f"  [{run_number}/{total_runs}] {preset}{suffix}...",
                    end="", flush=True,
                )

                result = await _execute_single_run(
                    task=task,
                    preset=preset,
                    run_index=run_idx,
                    agent_count=config.agent_count,
                    model=model,
                    max_ticks=max_ticks,
                    verbose=config.verbose,
                )
                runs.append(result)

                if result.success:
                    v = result.verification
                    print(
                        f" done ({result.report.total_ticks} ticks, "
                        f"{v.tests_passed}/{v.tests_total} tests, "
                        f"{result.wall_time_seconds:.1f}s)"
                    )
                else:
                    print(f" FAILED: {result.error}")

        print()

    total_time = time.time() - start_time

    # Aggregate statistics
    aggregated: dict[tuple[str, str], AggregatedMetrics] = {}
    for task in tasks:
        for preset in presets:
            combo_runs = [
                r.metrics for r in runs
                if r.task_id == task.id and r.preset == preset and r.success
            ]
            if combo_runs:
                aggregated[(task.id, preset)] = aggregate(task.id, preset, combo_runs)

    # Build result
    result = BenchmarkResult(
        config=config,
        tasks=[t.id for t in tasks],
        presets=presets,
        runs=runs,
        aggregated=aggregated,
        total_wall_time=total_time,
    )

    return result


async def _execute_single_run(
    task: BenchmarkTask,
    preset: str,
    run_index: int,
    agent_count: int,
    model: str,
    max_ticks: int,
    verbose: bool = False,
) -> SingleRunResult:
    """Execute a single (task, preset, run) and return results."""
    start = time.time()

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir) / "project"
            project.mkdir()

            # Write seed files
            for path, content in task.seed_files.items():
                fpath = project / path
                fpath.parent.mkdir(parents=True, exist_ok=True)
                fpath.write_text(content)

            # Run the engine
            report = await run_single(
                task=task.description,
                org_preset=preset,
                agent_count=agent_count,
                model=model,
                max_ticks=max_ticks,
                project_dir=project,
                verbose=verbose,
            )

            wall_time = time.time() - start

            # Run verification
            verification = _verify(task, project)

            # Extract metrics
            metrics = extract_metrics(report, verification, wall_time)

            return SingleRunResult(
                task_id=task.id,
                preset=preset,
                run_index=run_index,
                report=report,
                verification=verification,
                metrics=metrics,
                wall_time_seconds=wall_time,
            )

    except Exception as e:
        wall_time = time.time() - start
        log.exception("Benchmark run failed: %s / %s / %d", task.id, preset, run_index)

        # Create empty report and metrics for failed runs
        empty_report = ChronicleReport(
            task=task.description, org_preset=preset,
            agent_count=agent_count, total_ticks=0,
        )
        empty_verification = VerificationResult(passed=False, error=str(e))
        empty_metrics = RunMetrics(
            completion_rate=0.0, ticks_used=0, files_produced=0,
            test_pass_rate=0.0, communication_volume=0,
            merge_conflicts=0, emergent_specialisation=0.0,
            wall_time_seconds=wall_time,
        )

        return SingleRunResult(
            task_id=task.id,
            preset=preset,
            run_index=run_index,
            report=empty_report,
            verification=empty_verification,
            metrics=empty_metrics,
            success=False,
            error=str(e),
            wall_time_seconds=wall_time,
        )


def _verify(task: BenchmarkTask, project_dir: Path) -> VerificationResult:
    """Run a task's verification script in a subprocess."""
    try:
        result = subprocess.run(
            ["python3", "-c", task.verification_script],
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = result.stdout.strip()

        # Parse JSON output from verification script
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            return VerificationResult(
                passed=result.returncode == 0,
                output=output,
                error=result.stderr.strip() if result.stderr else None,
            )

        tests_total = data.get("tests_total", 0)
        tests_passed = data.get("tests_passed", 0)
        files_present = data.get("files_present", [])

        return VerificationResult(
            passed=tests_total > 0 and tests_passed == tests_total,
            tests_total=tests_total,
            tests_passed=tests_passed,
            tests_failed=tests_total - tests_passed,
            expected_files_present=len(files_present),
            expected_files_total=len(task.expected_files),
            output=output,
            error=data.get("error"),
        )

    except subprocess.TimeoutExpired:
        return VerificationResult(
            passed=False,
            error="Verification timed out (30s)",
        )
    except Exception as e:
        return VerificationResult(
            passed=False,
            error=str(e),
        )


def _dry_run_plan(
    tasks: list[BenchmarkTask],
    presets: list[str],
    config: BenchmarkConfig,
    total_runs: int,
) -> dict[str, Any]:
    """Print execution plan without running anything."""
    print(f"\n  AgentCiv Benchmark — DRY RUN")
    print(f"  {'─' * 60}")
    print(f"  Model: {'mock' if config.mock else config.model}")
    print(f"  Agents: {config.agent_count}")
    print(f"  Runs per combo: {config.runs_per_combo}")
    print(f"  Total runs: {total_runs}")
    print()
    print(f"  Tasks ({len(tasks)}):")
    for t in tasks:
        ticks = config.max_ticks_override or t.max_ticks
        print(f"    {t.id:20s} {t.difficulty:8s} {ticks:3d} ticks  {', '.join(t.expected_files)}")
    print()
    print(f"  Presets ({len(presets)}):")
    for p in presets:
        print(f"    {p}")
    print()
    print(f"  Matrix: {len(tasks)} tasks x {len(presets)} presets x {config.runs_per_combo} runs = {total_runs} total")
    print(f"  {'─' * 60}\n")

    return {
        "dry_run": True,
        "total_runs": total_runs,
        "tasks": [t.id for t in tasks],
        "presets": presets,
    }
