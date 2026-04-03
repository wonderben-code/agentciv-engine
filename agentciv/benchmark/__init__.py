"""Test tasks suite — built-in tasks across all presets with statistics.

Usage:
  agentciv test-tasks --tasks all --presets all --runs 3
  agentciv test-tasks --tasks fizzbuzz --presets collaborative,competitive --mock
  agentciv test-tasks --dry-run
"""

from .runner import run_benchmark, BenchmarkConfig
from .tasks import TASK_BANK, get_task, get_all_tasks, get_tasks_by_difficulty
from .report import BenchmarkResult

__all__ = [
    "run_benchmark",
    "BenchmarkConfig",
    "BenchmarkResult",
    "TASK_BANK",
    "get_task",
    "get_all_tasks",
    "get_tasks_by_difficulty",
]
