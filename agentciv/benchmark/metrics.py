"""Metrics extraction and statistical aggregation.

Extracts structured metrics from ChronicleReport + verification results,
and computes statistical summaries across multiple runs.

Uses stdlib only — no numpy or scipy needed.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from typing import Any

from ..chronicle.observer import ChronicleReport


@dataclass
class VerificationResult:
    """Outcome of running a task's verification script."""
    passed: bool
    tests_total: int = 0
    tests_passed: int = 0
    tests_failed: int = 0
    expected_files_present: int = 0
    expected_files_total: int = 0
    output: str = ""
    error: str | None = None


@dataclass
class RunMetrics:
    """Extracted metrics from a single benchmark run."""
    # Core metrics
    completion_rate: float  # 1.0 if verification passed, else fraction of tests
    ticks_used: int
    files_produced: int
    test_pass_rate: float  # tests_passed / tests_total (0.0 if no tests)
    communication_volume: int  # messages + broadcasts
    merge_conflicts: int
    emergent_specialisation: float  # Gini coefficient of file operations

    # Token metrics (Step 0a)
    total_tokens: int = 0
    tokens_per_agent: dict[str, int] = field(default_factory=dict)

    # Bonus metrics
    merges_succeeded: int = 0
    restructures_adopted: int = 0
    wall_time_seconds: float = 0.0
    file_completeness: float = 0.0  # expected_files_present / expected_files_total


@dataclass
class StatSummary:
    """Statistical summary of a metric across multiple runs."""
    mean: float
    std: float
    min: float
    max: float
    values: list[float] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "mean": round(self.mean, 3),
            "std": round(self.std, 3),
            "min": round(self.min, 3),
            "max": round(self.max, 3),
        }


@dataclass
class AggregatedMetrics:
    """Statistics for one (task, preset) combo across N runs."""
    task_id: str
    preset: str
    n_runs: int
    completion_rate: StatSummary
    ticks_used: StatSummary
    files_produced: StatSummary
    test_pass_rate: StatSummary
    communication_volume: StatSummary
    merge_conflicts: StatSummary
    emergent_specialisation: StatSummary
    file_completeness: StatSummary
    total_tokens: StatSummary = field(default_factory=lambda: StatSummary(0.0, 0.0, 0.0, 0.0))

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "preset": self.preset,
            "n_runs": self.n_runs,
            "completion_rate": self.completion_rate.to_dict(),
            "ticks_used": self.ticks_used.to_dict(),
            "files_produced": self.files_produced.to_dict(),
            "test_pass_rate": self.test_pass_rate.to_dict(),
            "communication_volume": self.communication_volume.to_dict(),
            "merge_conflicts": self.merge_conflicts.to_dict(),
            "emergent_specialisation": self.emergent_specialisation.to_dict(),
            "file_completeness": self.file_completeness.to_dict(),
            "total_tokens": self.total_tokens.to_dict(),
        }


def extract_metrics(
    report: ChronicleReport,
    verification: VerificationResult,
    wall_time: float = 0.0,
    agent_tokens: dict[str, int] | None = None,
) -> RunMetrics:
    """Extract structured metrics from a chronicle report + verification.

    Args:
        report: Chronicle report from the engine run.
        verification: Results from running the task's verification script.
        wall_time: Wall-clock time for the run in seconds.
        agent_tokens: Per-agent token consumption {agent_id: tokens_consumed}.
            Calculated as initial_budget - remaining for each agent.
    """
    # File completeness (computed first — used in completion fallback)
    if verification.expected_files_total > 0:
        file_comp = verification.expected_files_present / verification.expected_files_total
    else:
        file_comp = 1.0

    # Completion: based on verification test results
    if verification.tests_total > 0:
        completion = verification.tests_passed / verification.tests_total
        test_pass_rate = verification.tests_passed / verification.tests_total
    else:
        # No tests ran — verification couldn't import/run the code
        # Use file completeness as a partial signal, but cap at 0.5
        # (having files isn't the same as having working code)
        completion = 0.0 if not verification.passed else min(0.5, file_comp)
        test_pass_rate = 0.0

    # Communication volume
    comm_volume = report.total_messages + report.total_broadcasts

    # Emergent specialisation (Gini coefficient of file operations per agent)
    specialisation = _compute_specialisation(report)

    # Token metrics
    tokens = agent_tokens or {}
    total_tokens = sum(tokens.values())

    return RunMetrics(
        completion_rate=completion,
        ticks_used=report.total_ticks,
        files_produced=len(report.files_created),
        test_pass_rate=test_pass_rate,
        communication_volume=comm_volume,
        merge_conflicts=report.merge_conflicts,
        emergent_specialisation=specialisation,
        total_tokens=total_tokens,
        tokens_per_agent=tokens,
        merges_succeeded=report.merges_succeeded,
        restructures_adopted=report.restructures_adopted,
        wall_time_seconds=wall_time,
        file_completeness=file_comp,
    )


def _compute_specialisation(report: ChronicleReport) -> float:
    """Compute emergent specialisation using Gini coefficient.

    Measures inequality in file operation distribution across agents.
    0.0 = perfectly equal (every agent did the same amount)
    1.0 = maximum inequality (one agent did everything)

    Hierarchical/military orgs should show higher specialisation than
    flat/collaborative ones — this is a real, measurable signal.
    """
    if not report.contributions:
        return 0.0

    # Count total file operations per agent
    ops = []
    for c in report.contributions:
        total = len(c.files_created) + len(c.files_modified)
        ops.append(total)

    if not ops or sum(ops) == 0:
        return 0.0

    return _gini(ops)


def _gini(values: list[int | float]) -> float:
    """Compute the Gini coefficient of a list of values."""
    n = len(values)
    if n == 0:
        return 0.0

    sorted_vals = sorted(values)
    total = sum(sorted_vals)
    if total == 0:
        return 0.0

    # Standard Gini formula
    cumulative = 0.0
    weighted_sum = 0.0
    for i, val in enumerate(sorted_vals):
        cumulative += val
        weighted_sum += (2 * (i + 1) - n - 1) * val

    return weighted_sum / (n * total)


def _summarise(values: list[float]) -> StatSummary:
    """Compute summary statistics for a list of values."""
    if not values:
        return StatSummary(mean=0.0, std=0.0, min=0.0, max=0.0, values=[])

    mean = statistics.mean(values)
    std = statistics.stdev(values) if len(values) > 1 else 0.0

    return StatSummary(
        mean=mean,
        std=std,
        min=min(values),
        max=max(values),
        values=list(values),
    )


def aggregate(
    task_id: str, preset: str, runs: list[RunMetrics],
) -> AggregatedMetrics:
    """Aggregate metrics across multiple runs into statistical summaries."""
    return AggregatedMetrics(
        task_id=task_id,
        preset=preset,
        n_runs=len(runs),
        completion_rate=_summarise([r.completion_rate for r in runs]),
        ticks_used=_summarise([float(r.ticks_used) for r in runs]),
        files_produced=_summarise([float(r.files_produced) for r in runs]),
        test_pass_rate=_summarise([r.test_pass_rate for r in runs]),
        communication_volume=_summarise([float(r.communication_volume) for r in runs]),
        merge_conflicts=_summarise([float(r.merge_conflicts) for r in runs]),
        emergent_specialisation=_summarise([r.emergent_specialisation for r in runs]),
        file_completeness=_summarise([r.file_completeness for r in runs]),
        total_tokens=_summarise([float(r.total_tokens) for r in runs]),
    )
