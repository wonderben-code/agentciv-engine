"""Learning module — run data feeds back into auto mode.

Every completed run produces a RunRecord stored in ~/.agentciv/run_history.jsonl.
When --org auto starts, the learning system consults history for similar tasks
and provides data-informed recommendations to agents during meta-ticks.

The research flywheel made concrete: tool → data → better decisions → tool.
"""

from .history import RunHistory, RunRecord
from .insights import LearningInsights, generate_insights

__all__ = [
    "RunHistory",
    "RunRecord",
    "LearningInsights",
    "generate_insights",
]
