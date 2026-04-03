"""Benchmark report — terminal display and JSON export.

Formats benchmark results into:
  - Clean terminal comparison tables
  - Publishable JSON (for website, paper, further analysis)
  - Rankings (overall, by task, by difficulty)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .metrics import AggregatedMetrics, StatSummary


@dataclass
class BenchmarkResult:
    """Full benchmark result with aggregated statistics."""
    config: Any  # BenchmarkConfig (avoid circular import)
    tasks: list[str]
    presets: list[str]
    runs: list[Any]  # list[SingleRunResult]
    aggregated: dict[tuple[str, str], AggregatedMetrics]
    total_wall_time: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_terminal(self) -> str:
        """Render comparison tables for the terminal."""
        lines: list[str] = []

        total_runs = len(self.runs)
        successful = sum(1 for r in self.runs if r.success)
        failed = total_runs - successful

        lines.append("")
        lines.append("  AgentCiv Test Tasks Report")
        lines.append(f"  {'─' * 70}")
        lines.append(f"  Tasks: {len(self.tasks)} | Presets: {len(self.presets)} | Runs per combo: {self.config.runs_per_combo}")
        lines.append(f"  Total runs: {total_runs} ({successful} succeeded, {failed} failed)")
        lines.append(f"  Model: {'mock' if self.config.mock else self.config.model} | Agents: {self.config.agent_count}")
        lines.append(f"  Wall time: {self._fmt_time(self.total_wall_time)}")
        lines.append("")

        # Per-task comparison tables
        for task_id in self.tasks:
            lines.append(f"  Task: {task_id}")
            lines.append(f"  {'─' * 70}")
            header = (
                f"  {'Preset':20s} {'Complete':>9s} {'Ticks':>8s} "
                f"{'Files':>7s} {'Tests':>8s} {'Comms':>7s} "
                f"{'Conflicts':>10s} {'Special.':>9s}"
            )
            lines.append(header)
            lines.append(f"  {'─' * 70}")

            for preset in self.presets:
                key = (task_id, preset)
                agg = self.aggregated.get(key)
                if not agg:
                    lines.append(f"  {preset:20s} {'FAILED':>9s}")
                    continue

                lines.append(
                    f"  {preset:20s} "
                    f"{self._fmt_stat(agg.completion_rate):>9s} "
                    f"{self._fmt_stat(agg.ticks_used):>8s} "
                    f"{self._fmt_stat(agg.files_produced):>7s} "
                    f"{self._fmt_stat(agg.test_pass_rate):>8s} "
                    f"{self._fmt_stat(agg.communication_volume):>7s} "
                    f"{self._fmt_stat(agg.merge_conflicts):>10s} "
                    f"{self._fmt_stat(agg.emergent_specialisation):>9s}"
                )

            lines.append("")

        # Overall results
        rankings = self._compute_rankings()
        if rankings:
            lines.append("  Overall Results (by completion rate, then avg ticks)")
            lines.append(f"  {'─' * 50}")
            for i, (preset, score) in enumerate(rankings[:10], 1):
                lines.append(
                    f"  {i:2d}. {preset:20s} "
                    f"completion: {score['avg_completion']:.2f}  "
                    f"avg ticks: {score['avg_ticks']:.1f}"
                )
            lines.append("")

        lines.append(f"  {'─' * 70}")
        lines.append("")
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        """Serialise for JSON export."""
        return {
            "metadata": {
                "engine": "agentciv",
                "timestamp": self.timestamp,
                "model": "mock" if self.config.mock else self.config.model,
                "agent_count": self.config.agent_count,
                "runs_per_combo": self.config.runs_per_combo,
                "total_runs": len(self.runs),
                "successful_runs": sum(1 for r in self.runs if r.success),
                "wall_time_seconds": round(self.total_wall_time, 1),
            },
            "tasks": self.tasks,
            "presets": self.presets,
            "results": {
                task_id: {
                    preset: self.aggregated[(task_id, preset)].to_dict()
                    for preset in self.presets
                    if (task_id, preset) in self.aggregated
                }
                for task_id in self.tasks
            },
            "rankings": {
                "overall": [
                    {"preset": p, **s}
                    for p, s in self._compute_rankings()
                ],
            },
            "raw_runs": [
                {
                    "task_id": r.task_id,
                    "preset": r.preset,
                    "run_index": r.run_index,
                    "success": r.success,
                    "error": r.error,
                    "wall_time": round(r.wall_time_seconds, 1),
                    "metrics": {
                        "completion_rate": r.metrics.completion_rate,
                        "ticks_used": r.metrics.ticks_used,
                        "files_produced": r.metrics.files_produced,
                        "test_pass_rate": r.metrics.test_pass_rate,
                        "communication_volume": r.metrics.communication_volume,
                        "merge_conflicts": r.metrics.merge_conflicts,
                        "emergent_specialisation": round(r.metrics.emergent_specialisation, 3),
                        "file_completeness": r.metrics.file_completeness,
                    } if r.success else None,
                    "report": r.report.to_dict() if r.success else None,
                }
                for r in self.runs
            ],
        }

    def to_json(self, path: str) -> None:
        """Write JSON results to a file."""
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    def _compute_rankings(self) -> list[tuple[str, dict[str, float]]]:
        """Rank presets by average completion rate, then by ticks."""
        preset_scores: dict[str, dict[str, list[float]]] = {}

        for (task_id, preset), agg in self.aggregated.items():
            if preset not in preset_scores:
                preset_scores[preset] = {"completions": [], "ticks": []}
            preset_scores[preset]["completions"].append(agg.completion_rate.mean)
            preset_scores[preset]["ticks"].append(agg.ticks_used.mean)

        rankings = []
        for preset, scores in preset_scores.items():
            comps = scores["completions"]
            ticks = scores["ticks"]
            avg_comp = sum(comps) / len(comps) if comps else 0.0
            avg_ticks = sum(ticks) / len(ticks) if ticks else 999.0
            rankings.append((preset, {
                "avg_completion": round(avg_comp, 3),
                "avg_ticks": round(avg_ticks, 1),
            }))

        # Sort: higher completion first, then lower ticks
        rankings.sort(key=lambda x: (-x[1]["avg_completion"], x[1]["avg_ticks"]))
        return rankings

    @staticmethod
    def _fmt_stat(stat: StatSummary) -> str:
        """Format a stat as mean +/- std for terminal display."""
        if stat.std > 0.005:
            return f"{stat.mean:.2f}\u00b1{stat.std:.2f}"
        return f"{stat.mean:.2f}"

    @staticmethod
    def _fmt_time(seconds: float) -> str:
        """Format seconds as human-readable time."""
        if seconds < 60:
            return f"{seconds:.0f}s"
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        if minutes < 60:
            return f"{minutes}m {secs}s"
        hours = minutes // 60
        minutes = minutes % 60
        return f"{hours}h {minutes}m"
