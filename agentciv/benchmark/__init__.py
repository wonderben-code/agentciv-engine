"""Test tasks suite — built-in tasks across all presets with statistics.

Usage:
  agentciv test-tasks --tasks all --presets all --runs 3
  agentciv test-tasks --tasks fizzbuzz --presets collaborative,competitive --mock
  agentciv test-tasks --dry-run
"""

from .runner import run_benchmark, BenchmarkConfig
from .tasks import TASK_BANK, get_task, get_all_tasks, get_tasks_by_difficulty
from .report import BenchmarkResult
from .analysis import (
    analyse_run,
    compute_network_metrics,
    compute_temporal_metrics,
    compute_preset_comparison,
    export_comparison_csv,
    export_comparison_json,
    export_latex_table,
    kruskal_wallis,
    mann_whitney_u,
    NetworkMetrics,
    TemporalMetrics,
    PresetComparison,
    RunAnalysis,
)
from .city_grid import (
    BuildingType,
    CityGrid,
    ContributionGrid,
    GridSnapshot,
    GRID_SIZE,
)
from .city_scorer import CityScore, score_city
from .city_renderer import (
    render_ascii,
    render_png,
    render_heatmap,
    render_radar,
    render_comparison,
)

__all__ = [
    "run_benchmark",
    "BenchmarkConfig",
    "BenchmarkResult",
    "TASK_BANK",
    "get_task",
    "get_all_tasks",
    "get_tasks_by_difficulty",
    # Analysis layer
    "analyse_run",
    "compute_network_metrics",
    "compute_temporal_metrics",
    "compute_preset_comparison",
    "export_comparison_csv",
    "export_comparison_json",
    "export_latex_table",
    "kruskal_wallis",
    "mann_whitney_u",
    "NetworkMetrics",
    "TemporalMetrics",
    "PresetComparison",
    "RunAnalysis",
    # City Grid (Paper 6)
    "BuildingType",
    "CityGrid",
    "ContributionGrid",
    "GridSnapshot",
    "GRID_SIZE",
    "CityScore",
    "score_city",
    "render_ascii",
    "render_png",
    "render_heatmap",
    "render_radar",
    "render_comparison",
]
