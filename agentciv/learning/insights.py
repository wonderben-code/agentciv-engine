"""Learning insights — generate recommendations from historical run data.

Analyses similar past runs to produce data-informed suggestions for
auto mode agents. The agents see empirical evidence, not mandates —
they're free to vote differently.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from .history import RunHistory, RunRecord, extract_keywords, keyword_similarity

log = logging.getLogger(__name__)

# The org dimensions we track and can recommend on
TRACKED_DIMENSIONS = [
    "authority", "communication", "roles", "decisions",
    "incentives", "information", "conflict_resolution",
    "groups", "adaptation",
]


@dataclass
class DimensionInsight:
    """Performance data for one dimension value."""
    dimension: str
    value: str
    run_count: int
    avg_quality: float
    avg_completion: float | None = None


@dataclass
class PresetInsight:
    """Performance data for one preset."""
    preset: str
    run_count: int
    avg_quality: float
    avg_completion: float | None = None


@dataclass
class LearningInsights:
    """Compiled insights from historical runs for a given task."""
    task_keywords: list[str]
    matching_runs: int
    total_history: int

    # Top performing presets for similar tasks
    preset_rankings: list[PresetInsight] = field(default_factory=list)

    # Per-dimension best values
    dimension_insights: list[DimensionInsight] = field(default_factory=list)

    # Raw recommendation text for agent prompt injection
    prompt: str = ""

    def has_data(self) -> bool:
        """Whether we have enough data to make recommendations."""
        return self.matching_runs >= 2

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_keywords": self.task_keywords,
            "matching_runs": self.matching_runs,
            "total_history": self.total_history,
            "preset_rankings": [
                {
                    "preset": p.preset,
                    "run_count": p.run_count,
                    "avg_quality": round(p.avg_quality, 3),
                }
                for p in self.preset_rankings
            ],
            "dimension_insights": [
                {
                    "dimension": d.dimension,
                    "value": d.value,
                    "run_count": d.run_count,
                    "avg_quality": round(d.avg_quality, 3),
                }
                for d in self.dimension_insights
            ],
        }


def generate_insights(
    task_description: str,
    history: RunHistory | None = None,
) -> LearningInsights:
    """Generate learning insights for a task from historical data.

    Returns insights with a prompt string ready for injection into
    the auto mode agent context.
    """
    if history is None:
        history = RunHistory()

    keywords = extract_keywords(task_description)
    all_records = history.load_all()
    similar = history.find_similar(task_description, min_similarity=0.15)

    insights = LearningInsights(
        task_keywords=keywords,
        matching_runs=len(similar),
        total_history=len(all_records),
    )

    if not insights.has_data():
        insights.prompt = _no_data_prompt(len(all_records))
        return insights

    # Extract just the records (drop similarity scores)
    records = [r for r, _ in similar]

    # Analyse preset performance
    insights.preset_rankings = _analyse_presets(records)

    # Analyse dimension values
    insights.dimension_insights = _analyse_dimensions(records)

    # Build the prompt
    insights.prompt = _build_prompt(insights)

    log.info(
        "Generated insights for '%s': %d matching runs, %d presets ranked",
        task_description[:50], insights.matching_runs, len(insights.preset_rankings),
    )

    return insights


def _analyse_presets(records: list[RunRecord]) -> list[PresetInsight]:
    """Rank presets by quality score across matching runs."""
    preset_data: dict[str, list[RunRecord]] = {}
    for r in records:
        preset_data.setdefault(r.org_preset, []).append(r)

    rankings: list[PresetInsight] = []
    for preset, runs in preset_data.items():
        quality_scores = [r.quality_score for r in runs]
        completion_scores = [
            r.completion_rate for r in runs if r.completion_rate is not None
        ]
        rankings.append(PresetInsight(
            preset=preset,
            run_count=len(runs),
            avg_quality=sum(quality_scores) / len(quality_scores),
            avg_completion=(
                sum(completion_scores) / len(completion_scores)
                if completion_scores else None
            ),
        ))

    rankings.sort(key=lambda x: -x.avg_quality)
    return rankings


def _analyse_dimensions(records: list[RunRecord]) -> list[DimensionInsight]:
    """Find best-performing dimension values across matching runs."""
    # Collect (dimension, value) → quality scores
    dim_data: dict[tuple[str, str], list[float]] = {}

    for r in records:
        org = r.final_org_state
        for dim in TRACKED_DIMENSIONS:
            value = org.get(dim)
            if value:
                dim_data.setdefault((dim, value), []).append(r.quality_score)

    # For each dimension, find the best value
    best_per_dim: dict[str, DimensionInsight] = {}
    for (dim, value), scores in dim_data.items():
        avg = sum(scores) / len(scores)
        if dim not in best_per_dim or avg > best_per_dim[dim].avg_quality:
            best_per_dim[dim] = DimensionInsight(
                dimension=dim,
                value=value,
                run_count=len(scores),
                avg_quality=avg,
            )

    # Only include dimensions with at least 2 data points
    return [
        insight for insight in best_per_dim.values()
        if insight.run_count >= 2
    ]


def _build_prompt(insights: LearningInsights) -> str:
    """Build the learning insights prompt for agent context injection."""
    lines: list[str] = []
    lines.append(
        f"\n--- LEARNING INSIGHTS (from {insights.matching_runs} similar past runs) ---"
    )

    # Preset rankings
    if insights.preset_rankings:
        lines.append("\nPreset performance on similar tasks:")
        for p in insights.preset_rankings[:5]:
            quality_str = f"quality: {p.avg_quality:.2f}"
            if p.avg_completion is not None:
                quality_str += f", completion: {p.avg_completion:.0%}"
            lines.append(f"  {p.preset:20s} ({p.run_count} runs, {quality_str})")

    # Dimension insights
    if insights.dimension_insights:
        lines.append("\nBest-performing dimension values for this type of task:")
        for d in insights.dimension_insights:
            lines.append(
                f"  {d.dimension}: {d.value} "
                f"(quality: {d.avg_quality:.2f}, {d.run_count} runs)"
            )

    lines.append(
        "\nThis is empirical data from past runs — use it to inform your "
        "restructuring proposals, but you are free to deviate if the current "
        "situation warrants it."
    )
    lines.append("--- END LEARNING INSIGHTS ---\n")

    return "\n".join(lines)


def _no_data_prompt(total_history: int) -> str:
    """Prompt when insufficient data exists."""
    if total_history == 0:
        return ""  # Don't inject anything if no history at all
    return (
        f"\n(Learning system: {total_history} runs in history but fewer than 2 "
        f"match this task type. More data needed for recommendations.)\n"
    )
