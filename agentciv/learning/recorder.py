"""Run recorder — bridges ChronicleReport → RunRecord.

Extracts the right signals from a completed run and computes a
quality score, then persists to the global history.
"""

from __future__ import annotations

import logging
from datetime import datetime

from ..chronicle.observer import ChronicleReport
from ..org.config import OrgDimensions
from .history import RunHistory, RunRecord, extract_keywords

log = logging.getLogger(__name__)


def compute_quality_score(
    report: ChronicleReport,
    completion_rate: float | None = None,
    test_pass_rate: float | None = None,
) -> float:
    """Compute a 0-1 quality score from run outcomes.

    Weights:
    - completion_rate (40%) — did the task get done?
    - test_pass_rate (30%) — did the code work?
    - efficiency (15%) — fewer ticks relative to max is better
    - collaboration (15%) — files produced, low conflicts
    """
    score = 0.0

    # Completion (40%)
    if completion_rate is not None:
        score += 0.4 * completion_rate
    elif report.final_test_status == "passed":
        score += 0.4
    elif report.files_created:
        score += 0.2  # partial credit for producing files

    # Test pass rate (30%)
    if test_pass_rate is not None:
        score += 0.3 * test_pass_rate
    elif report.final_test_status == "passed":
        score += 0.3

    # Efficiency (15%) — lower ticks / max_ticks ratio is better
    # We don't have max_ticks on the report, so use a heuristic:
    # finishing in fewer ticks is good, cap at 1.0
    if report.total_ticks > 0:
        efficiency = min(1.0, 10.0 / report.total_ticks)
        score += 0.15 * efficiency

    # Collaboration health (15%)
    if report.files_created:
        # Files produced = sign of productivity
        file_signal = min(1.0, len(report.files_created) / 5.0)
        # Low conflicts = healthy collaboration
        conflict_penalty = min(1.0, report.merge_conflicts / 5.0)
        collab_score = file_signal * (1.0 - conflict_penalty * 0.5)
        score += 0.15 * collab_score

    return min(1.0, max(0.0, score))


def record_from_report(
    report: ChronicleReport,
    org_dimensions: OrgDimensions,
    model: str,
    max_ticks: int,
    completion_rate: float | None = None,
    test_pass_rate: float | None = None,
    success: bool = True,
) -> RunRecord:
    """Create a RunRecord from a ChronicleReport and org config."""
    quality = compute_quality_score(report, completion_rate, test_pass_rate)

    # Extract final org state
    final_org: dict[str, str] = {}
    for dim_name in [
        "authority", "communication", "roles", "decisions",
        "incentives", "information", "conflict_resolution",
        "groups", "adaptation",
    ]:
        val = getattr(org_dimensions, dim_name, None)
        if val:
            final_org[dim_name] = val
    for k, v in org_dimensions.extra.items():
        final_org[k] = str(v)

    # Restructure log
    restructure_log: list[dict] = []
    if hasattr(report, "restructure_log") and report.restructure_log:
        for entry in report.restructure_log:
            if isinstance(entry, dict):
                restructure_log.append(entry)
            else:
                # RestructureEvent dataclass
                restructure_log.append({
                    "dimension": getattr(entry, "dimension", ""),
                    "old_value": getattr(entry, "old_value", ""),
                    "new_value": getattr(entry, "new_value", ""),
                })

    return RunRecord(
        timestamp=datetime.now().isoformat(),
        task_description=report.task,
        task_keywords=extract_keywords(report.task),
        org_preset=report.org_preset,
        final_org_state=final_org,
        agent_count=report.agent_count,
        model=model,
        ticks_used=report.total_ticks,
        max_ticks=max_ticks,
        files_produced=len(report.files_created),
        total_messages=report.total_messages,
        total_broadcasts=report.total_broadcasts,
        merge_conflicts=report.merge_conflicts,
        merges_succeeded=report.merges_succeeded,
        restructures_adopted=report.restructures_adopted,
        restructure_log=restructure_log,
        success=success,
        completion_rate=completion_rate,
        test_pass_rate=test_pass_rate,
        quality_score=quality,
    )


def save_run(
    report: ChronicleReport,
    org_dimensions: OrgDimensions,
    model: str,
    max_ticks: int,
    completion_rate: float | None = None,
    test_pass_rate: float | None = None,
    success: bool = True,
    history: RunHistory | None = None,
) -> RunRecord:
    """Create and persist a RunRecord from a completed run.

    This is the main entry point — call after any run completes.
    """
    if history is None:
        history = RunHistory()

    record = record_from_report(
        report=report,
        org_dimensions=org_dimensions,
        model=model,
        max_ticks=max_ticks,
        completion_rate=completion_rate,
        test_pass_rate=test_pass_rate,
        success=success,
    )

    history.save_run(record)
    return record
