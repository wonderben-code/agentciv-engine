"""Benchmark analysis layer — network, temporal, and comparative analytics.

Computes Tier 2 and Tier 3 metrics from raw run data:
  - Network metrics from communication pairs (density, centrality, clustering)
  - Temporal analysis from tick snapshots (phase transitions, convergence)
  - Comparative analysis across presets (rankings, statistical significance)
  - Export to publication formats (CSV, JSON, LaTeX-ready tables)

Uses stdlib only — no numpy/scipy required. Statistical tests are
simple enough to implement directly and this keeps dependencies at zero.
"""

from __future__ import annotations

import csv
import io
import json
import math
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from ..chronicle.observer import ChronicleReport, ConflictRecord, TickSnapshot
from .metrics import AggregatedMetrics, RunMetrics, StatSummary


# ---------------------------------------------------------------------------
# Network metrics (Tier 2) — computed from communication_pairs
# ---------------------------------------------------------------------------

@dataclass
class NetworkMetrics:
    """Communication network analysis for a single run."""
    graph_density: float = 0.0  # actual_edges / possible_edges
    in_degree: dict[str, float] = field(default_factory=dict)  # normalised
    out_degree: dict[str, float] = field(default_factory=dict)  # normalised
    betweenness: dict[str, float] = field(default_factory=dict)
    reciprocity: float = 0.0  # bidirectional / total pairs
    hub_spoke_ratio: float = 0.0  # max(centrality) / mean(centrality)
    communication_efficiency: float = 0.0  # success / comm_volume
    clustering_coefficient: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "graph_density": round(self.graph_density, 4),
            "in_degree": {k: round(v, 4) for k, v in self.in_degree.items()},
            "out_degree": {k: round(v, 4) for k, v in self.out_degree.items()},
            "betweenness": {k: round(v, 4) for k, v in self.betweenness.items()},
            "reciprocity": round(self.reciprocity, 4),
            "hub_spoke_ratio": round(self.hub_spoke_ratio, 4),
            "communication_efficiency": round(self.communication_efficiency, 4),
            "clustering_coefficient": round(self.clustering_coefficient, 4),
        }


def compute_network_metrics(
    report: ChronicleReport,
    success_rate: float = 0.0,
) -> NetworkMetrics:
    """Compute network metrics from a chronicle report's communication pairs.

    Args:
        report: Chronicle report with communication_pairs ("A → B" → count).
        success_rate: Task success rate (for communication efficiency).
    """
    pairs = report.communication_pairs
    if not pairs:
        return NetworkMetrics()

    # Parse directed edges: "sender → receiver" → (sender, receiver, count)
    edges: list[tuple[str, str, int]] = []
    nodes: set[str] = set()
    for pair_str, count in pairs.items():
        parts = pair_str.split(" → ")
        if len(parts) == 2:
            sender, receiver = parts
            edges.append((sender, receiver, count))
            nodes.add(sender)
            nodes.add(receiver)

    if not nodes:
        return NetworkMetrics()

    n = len(nodes)
    node_list = sorted(nodes)

    # Graph density: actual edges / possible directed edges
    possible_edges = n * (n - 1) if n > 1 else 1
    unique_edges = len({(s, r) for s, r, _ in edges})
    density = unique_edges / possible_edges

    # In/out degree (normalised by total messages)
    total_msgs = sum(c for _, _, c in edges)
    in_counts: dict[str, int] = defaultdict(int)
    out_counts: dict[str, int] = defaultdict(int)
    for s, r, c in edges:
        out_counts[s] += c
        in_counts[r] += c

    in_degree = {node: in_counts.get(node, 0) / max(total_msgs, 1) for node in node_list}
    out_degree = {node: out_counts.get(node, 0) / max(total_msgs, 1) for node in node_list}

    # Reciprocity: fraction of pairs that are bidirectional
    directed_pairs = {(s, r) for s, r, _ in edges}
    bidirectional = sum(1 for s, r in directed_pairs if (r, s) in directed_pairs)
    reciprocity = bidirectional / max(len(directed_pairs), 1)

    # Hub-spoke ratio: max(total_degree) / mean(total_degree)
    total_degree = {
        node: in_counts.get(node, 0) + out_counts.get(node, 0)
        for node in node_list
    }
    degrees = list(total_degree.values())
    mean_deg = statistics.mean(degrees) if degrees else 1.0
    max_deg = max(degrees) if degrees else 0
    hub_spoke = max_deg / max(mean_deg, 0.001)

    # Communication efficiency: success / volume
    comm_volume = report.total_messages + report.total_broadcasts
    comm_efficiency = success_rate / max(comm_volume, 1)

    # Betweenness centrality (simplified: based on degree, not full shortest-path)
    # For small agent networks (2-20 agents), degree centrality correlates well
    betweenness = {}
    for node in node_list:
        # Approximate: how much of total traffic flows through this node
        through = in_counts.get(node, 0) + out_counts.get(node, 0)
        betweenness[node] = through / max(total_msgs * 2, 1)

    # Clustering coefficient (fraction of node's neighbours that communicate)
    clustering_coeffs = []
    for node in node_list:
        neighbours = set()
        for s, r, _ in edges:
            if s == node:
                neighbours.add(r)
            if r == node:
                neighbours.add(s)
        if len(neighbours) < 2:
            clustering_coeffs.append(0.0)
            continue
        # Count edges between neighbours
        neighbour_edges = 0
        for n1 in neighbours:
            for n2 in neighbours:
                if n1 != n2 and (n1, n2) in directed_pairs:
                    neighbour_edges += 1
        possible = len(neighbours) * (len(neighbours) - 1)
        clustering_coeffs.append(neighbour_edges / max(possible, 1))

    avg_clustering = statistics.mean(clustering_coeffs) if clustering_coeffs else 0.0

    return NetworkMetrics(
        graph_density=density,
        in_degree=in_degree,
        out_degree=out_degree,
        betweenness=betweenness,
        reciprocity=reciprocity,
        hub_spoke_ratio=hub_spoke,
        communication_efficiency=comm_efficiency,
        clustering_coefficient=avg_clustering,
    )


# ---------------------------------------------------------------------------
# Temporal analysis (Tier 3) — computed from tick snapshots
# ---------------------------------------------------------------------------

@dataclass
class TemporalMetrics:
    """Temporal analysis of a single run from tick snapshots."""
    convergence_tick: int | None = None  # tick where output stabilised
    phase_transitions: list[int] = field(default_factory=list)  # ticks with regime changes
    activity_curve: list[float] = field(default_factory=list)  # active_agents per tick
    cumulative_progress: list[float] = field(default_factory=list)  # files created over time
    avg_conflict_resolution_time: float | None = None
    conflict_resolution_times: list[int] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "convergence_tick": self.convergence_tick,
            "phase_transitions": self.phase_transitions,
            "activity_curve": [round(v, 2) for v in self.activity_curve],
            "cumulative_progress": [round(v, 2) for v in self.cumulative_progress],
            "avg_conflict_resolution_time": (
                round(self.avg_conflict_resolution_time, 2)
                if self.avg_conflict_resolution_time is not None else None
            ),
            "conflict_resolution_times": self.conflict_resolution_times,
        }


def compute_temporal_metrics(report: ChronicleReport) -> TemporalMetrics:
    """Compute temporal metrics from tick snapshots and conflict records."""
    snapshots = report.tick_snapshots
    conflicts = report.conflict_records

    if not snapshots:
        return TemporalMetrics()

    # Activity curve: active agents per tick
    activity = [float(s.active_agents) for s in snapshots]

    # Cumulative progress: files created over time (normalised to 0-1)
    max_files = max(s.files_created_cumulative for s in snapshots) if snapshots else 1
    progress = [
        s.files_created_cumulative / max(max_files, 1)
        for s in snapshots
    ]

    # Convergence detection: find the tick where cumulative files stop changing
    convergence_tick = None
    if len(snapshots) >= 3:
        for i in range(len(snapshots) - 2, -1, -1):
            if snapshots[i].files_created_cumulative < snapshots[-1].files_created_cumulative:
                convergence_tick = snapshots[min(i + 1, len(snapshots) - 1)].tick
                break

    # Phase transition detection: significant changes in activity level
    transitions = []
    if len(activity) >= 3:
        for i in range(1, len(activity) - 1):
            prev_avg = statistics.mean(activity[max(0, i - 2):i])
            next_avg = statistics.mean(activity[i + 1:min(len(activity), i + 3)])
            if prev_avg > 0 and abs(next_avg - prev_avg) / max(prev_avg, 0.001) > 0.5:
                transitions.append(snapshots[i].tick)

    # Conflict resolution times (Step 0c)
    resolution_times = []
    for c in conflicts:
        if c.resolution_time is not None:
            resolution_times.append(c.resolution_time)

    avg_resolution = (
        statistics.mean(resolution_times) if resolution_times else None
    )

    return TemporalMetrics(
        convergence_tick=convergence_tick,
        phase_transitions=transitions,
        activity_curve=activity,
        cumulative_progress=progress,
        avg_conflict_resolution_time=avg_resolution,
        conflict_resolution_times=resolution_times,
    )


# ---------------------------------------------------------------------------
# Comparative analysis — across presets
# ---------------------------------------------------------------------------

@dataclass
class PresetComparison:
    """Comparative analysis between presets for a single task."""
    task_id: str
    rankings: list[tuple[str, float]]  # preset → composite score, sorted
    best_preset: str = ""
    worst_preset: str = ""
    superadditivity: dict[str, float] = field(default_factory=dict)  # preset → ratio vs baseline
    effect_sizes: dict[str, float] = field(default_factory=dict)  # preset pair → Cohen's d

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "rankings": [{"preset": p, "score": round(s, 4)} for p, s in self.rankings],
            "best_preset": self.best_preset,
            "worst_preset": self.worst_preset,
            "superadditivity": {k: round(v, 4) for k, v in self.superadditivity.items()},
            "effect_sizes": {k: round(v, 4) for k, v in self.effect_sizes.items()},
        }


def compute_preset_comparison(
    task_id: str,
    aggregated: dict[tuple[str, str], AggregatedMetrics],
    baseline_preset: str = "single_agent",
) -> PresetComparison:
    """Compare presets for a single task.

    Computes composite score (completion weighted most), rankings,
    superadditivity vs baseline, and effect sizes between top presets.
    """
    # Get all presets for this task
    task_aggs = {
        preset: agg for (tid, preset), agg in aggregated.items()
        if tid == task_id
    }

    if not task_aggs:
        return PresetComparison(task_id=task_id, rankings=[])

    # Composite score: 60% completion, 20% test_pass, 10% efficiency, 10% -conflicts
    scores: list[tuple[str, float]] = []
    for preset, agg in task_aggs.items():
        # Normalise ticks: lower is better, invert
        max_ticks = max(a.ticks_used.mean for a in task_aggs.values()) or 1
        tick_score = 1.0 - (agg.ticks_used.mean / max_ticks)

        # Normalise conflicts: lower is better, invert
        max_conflicts = max(a.merge_conflicts.mean for a in task_aggs.values()) or 1
        conflict_score = 1.0 - (agg.merge_conflicts.mean / max_conflicts)

        composite = (
            0.60 * agg.completion_rate.mean
            + 0.20 * agg.test_pass_rate.mean
            + 0.10 * tick_score
            + 0.10 * conflict_score
        )
        scores.append((preset, composite))

    scores.sort(key=lambda x: -x[1])

    best = scores[0][0] if scores else ""
    worst = scores[-1][0] if scores else ""

    # Superadditivity: preset completion / baseline completion
    baseline = task_aggs.get(baseline_preset)
    superadditivity = {}
    if baseline and baseline.completion_rate.mean > 0:
        for preset, agg in task_aggs.items():
            if preset != baseline_preset:
                superadditivity[preset] = (
                    agg.completion_rate.mean / baseline.completion_rate.mean
                )

    # Effect sizes (Cohen's d) between adjacent ranked presets
    effect_sizes = {}
    for i in range(len(scores) - 1):
        p1, _ = scores[i]
        p2, _ = scores[i + 1]
        agg1 = task_aggs[p1]
        agg2 = task_aggs[p2]
        d = _cohens_d(
            agg1.completion_rate.mean, agg1.completion_rate.std,
            agg2.completion_rate.mean, agg2.completion_rate.std,
            agg1.n_runs, agg2.n_runs,
        )
        if d is not None:
            effect_sizes[f"{p1}_vs_{p2}"] = d

    return PresetComparison(
        task_id=task_id,
        rankings=scores,
        best_preset=best,
        worst_preset=worst,
        superadditivity=superadditivity,
        effect_sizes=effect_sizes,
    )


def _cohens_d(
    mean1: float, std1: float,
    mean2: float, std2: float,
    n1: int, n2: int,
) -> float | None:
    """Compute Cohen's d effect size between two groups."""
    if n1 < 2 or n2 < 2:
        return None
    # Pooled standard deviation
    pooled_var = ((n1 - 1) * std1**2 + (n2 - 1) * std2**2) / (n1 + n2 - 2)
    if pooled_var <= 0:
        return None
    pooled_std = math.sqrt(pooled_var)
    if pooled_std == 0:
        return None
    return (mean1 - mean2) / pooled_std


# ---------------------------------------------------------------------------
# Kruskal-Wallis H-test (non-parametric, pre-registered)
# ---------------------------------------------------------------------------

def kruskal_wallis(groups: list[list[float]]) -> tuple[float, int]:
    """Compute Kruskal-Wallis H statistic.

    Non-parametric test for whether samples come from the same distribution.
    Pre-registered as our primary statistical test.

    Returns (H_statistic, degrees_of_freedom).
    p-value can be looked up in chi-squared table with df = k-1.
    """
    # Pool and rank all values
    all_values: list[tuple[float, int]] = []
    for gi, group in enumerate(groups):
        for val in group:
            all_values.append((val, gi))

    if not all_values:
        return 0.0, 0

    # Assign ranks (average for ties)
    all_values.sort(key=lambda x: x[0])
    n_total = len(all_values)
    ranks: list[tuple[float, int]] = []

    i = 0
    while i < n_total:
        j = i
        while j < n_total and all_values[j][0] == all_values[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0  # average rank for ties
        for k_idx in range(i, j):
            ranks.append((avg_rank, all_values[k_idx][1]))
        i = j

    # Sum of ranks per group
    rank_sums: dict[int, float] = defaultdict(float)
    group_sizes: dict[int, int] = defaultdict(int)
    for rank, gi in ranks:
        rank_sums[gi] += rank
        group_sizes[gi] += 1

    # H statistic
    k = len(groups)
    h = 0.0
    for gi in range(k):
        ni = group_sizes.get(gi, 0)
        if ni == 0:
            continue
        ri = rank_sums.get(gi, 0)
        h += (ri ** 2) / ni

    h = (12.0 / (n_total * (n_total + 1))) * h - 3 * (n_total + 1)

    return h, k - 1


# ---------------------------------------------------------------------------
# Mann-Whitney U (pairwise, pre-registered)
# ---------------------------------------------------------------------------

def mann_whitney_u(group1: list[float], group2: list[float]) -> float:
    """Compute Mann-Whitney U statistic for two groups.

    Returns the U statistic. For significance, compare against
    critical values or use normal approximation for larger samples.
    """
    n1 = len(group1)
    n2 = len(group2)
    if n1 == 0 or n2 == 0:
        return 0.0

    # Count how many times a value from group1 exceeds a value from group2
    u = 0.0
    for v1 in group1:
        for v2 in group2:
            if v1 > v2:
                u += 1.0
            elif v1 == v2:
                u += 0.5

    return u


# ---------------------------------------------------------------------------
# Full run analysis — combines everything
# ---------------------------------------------------------------------------

@dataclass
class RunAnalysis:
    """Complete analysis of a single benchmark run."""
    network: NetworkMetrics
    temporal: TemporalMetrics

    def to_dict(self) -> dict[str, Any]:
        return {
            "network": self.network.to_dict(),
            "temporal": self.temporal.to_dict(),
        }


def analyse_run(report: ChronicleReport, metrics: RunMetrics) -> RunAnalysis:
    """Compute full analysis for a single run."""
    return RunAnalysis(
        network=compute_network_metrics(report, metrics.completion_rate),
        temporal=compute_temporal_metrics(report),
    )


# ---------------------------------------------------------------------------
# Export utilities
# ---------------------------------------------------------------------------

def export_comparison_csv(
    aggregated: dict[tuple[str, str], AggregatedMetrics],
) -> str:
    """Export aggregated results as CSV for publication."""
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "task_id", "preset", "n_runs",
        "completion_mean", "completion_std",
        "ticks_mean", "ticks_std",
        "test_pass_mean", "test_pass_std",
        "comm_volume_mean", "comm_volume_std",
        "conflicts_mean", "conflicts_std",
        "specialisation_mean", "specialisation_std",
        "tokens_mean", "tokens_std",
        "file_completeness_mean", "file_completeness_std",
    ])

    for (task_id, preset), agg in sorted(aggregated.items()):
        writer.writerow([
            task_id, preset, agg.n_runs,
            f"{agg.completion_rate.mean:.4f}", f"{agg.completion_rate.std:.4f}",
            f"{agg.ticks_used.mean:.1f}", f"{agg.ticks_used.std:.1f}",
            f"{agg.test_pass_rate.mean:.4f}", f"{agg.test_pass_rate.std:.4f}",
            f"{agg.communication_volume.mean:.1f}", f"{agg.communication_volume.std:.1f}",
            f"{agg.merge_conflicts.mean:.1f}", f"{agg.merge_conflicts.std:.1f}",
            f"{agg.emergent_specialisation.mean:.4f}", f"{agg.emergent_specialisation.std:.4f}",
            f"{agg.total_tokens.mean:.0f}", f"{agg.total_tokens.std:.0f}",
            f"{agg.file_completeness.mean:.4f}", f"{agg.file_completeness.std:.4f}",
        ])

    return output.getvalue()


def export_comparison_json(
    aggregated: dict[tuple[str, str], AggregatedMetrics],
    comparisons: list[PresetComparison] | None = None,
) -> dict[str, Any]:
    """Export full analysis as JSON for publication and charts."""
    result: dict[str, Any] = {
        "aggregated": {
            f"{task_id}/{preset}": agg.to_dict()
            for (task_id, preset), agg in sorted(aggregated.items())
        },
    }

    if comparisons:
        result["comparisons"] = [c.to_dict() for c in comparisons]

    return result


def export_latex_table(
    task_id: str,
    aggregated: dict[tuple[str, str], AggregatedMetrics],
) -> str:
    """Export a single task's results as a LaTeX table."""
    lines = [
        r"\begin{table}[h]",
        r"\centering",
        f"\\caption{{Results for {task_id}}}",
        r"\begin{tabular}{lcccccc}",
        r"\toprule",
        r"Preset & Completion & Ticks & Tests & Comms & Conflicts & Gini \\",
        r"\midrule",
    ]

    for (tid, preset), agg in sorted(aggregated.items()):
        if tid != task_id:
            continue
        lines.append(
            f"{preset} & "
            f"${agg.completion_rate.mean:.2f} \\pm {agg.completion_rate.std:.2f}$ & "
            f"${agg.ticks_used.mean:.1f} \\pm {agg.ticks_used.std:.1f}$ & "
            f"${agg.test_pass_rate.mean:.2f} \\pm {agg.test_pass_rate.std:.2f}$ & "
            f"${agg.communication_volume.mean:.0f} \\pm {agg.communication_volume.std:.0f}$ & "
            f"${agg.merge_conflicts.mean:.1f} \\pm {agg.merge_conflicts.std:.1f}$ & "
            f"${agg.emergent_specialisation.mean:.3f} \\pm {agg.emergent_specialisation.std:.3f}$ \\\\"
        )

    lines.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
    ])

    return "\n".join(lines)
