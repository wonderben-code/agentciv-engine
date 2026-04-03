"""Feature discovery — contextual tips that help users find capabilities.

After a run completes, suggests the most relevant next feature based on
what happened. Tracks which features the user has already discovered so
tips don't repeat.

Design principles:
  - Context-aware: tips triggered by specific run characteristics
  - Non-repetitive: tracks what's been shown
  - Subtle: one line, not a wall of text
  - Suppressible: --no-tips or MCP clients can ignore hints
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

TRACKER_FILE = Path.home() / ".agentciv" / "features_seen.json"


@dataclass
class Tip:
    """A contextual tip to show the user."""
    feature: str  # feature ID for tracking
    text: str     # the actual tip text


class FeatureTracker:
    """Tracks which features the user has discovered."""

    def __init__(self, tracker_file: Path | None = None):
        self._file = tracker_file or TRACKER_FILE
        self._seen: set[str] | None = None

    def _load(self) -> set[str]:
        if self._seen is not None:
            return self._seen
        try:
            if self._file.exists():
                data = json.loads(self._file.read_text())
                self._seen = set(data.get("seen", []))
            else:
                self._seen = set()
        except Exception:
            self._seen = set()
        return self._seen

    def has_seen(self, feature: str) -> bool:
        return feature in self._load()

    def mark_seen(self, feature: str) -> None:
        seen = self._load()
        if feature not in seen:
            seen.add(feature)
            self._save()

    def mark_used(self, command: str) -> None:
        """Track that the user ran a command (solve, experiment, etc.)."""
        self.mark_seen(f"cmd:{command}")

    def has_used(self, command: str) -> bool:
        return self.has_seen(f"cmd:{command}")

    def _save(self) -> None:
        try:
            self._file.parent.mkdir(parents=True, exist_ok=True)
            self._file.write_text(json.dumps({
                "seen": sorted(self._load()),
            }))
        except Exception as e:
            log.debug("Failed to save feature tracker: %s", e)


def generate_post_run_tip(
    org_preset: str,
    merge_conflicts: int = 0,
    total_messages: int = 0,
    restructures_adopted: int = 0,
    agent_count: int = 0,
    tracker: FeatureTracker | None = None,
) -> Tip | None:
    """Generate a contextual tip based on what happened during a run.

    Returns None if no relevant unseen tip exists.
    """
    if tracker is None:
        tracker = FeatureTracker()

    # Priority-ordered tips — first match wins
    tips: list[Tip] = []

    # High conflicts → suggest code-review
    if merge_conflicts >= 2 and org_preset != "code-review":
        tips.append(Tip(
            feature="tip:code-review",
            text=f"Tip: {merge_conflicts} merge conflicts. Try --org code-review for peer review before merge.",
        ))

    # No communication → suggest collaborative
    if total_messages == 0 and org_preset not in ("collaborative", "startup", "pair-programming"):
        tips.append(Tip(
            feature="tip:more-communication",
            text="Tip: Agents didn't communicate. Try --org collaborative or --org pair-programming for tighter coordination.",
        ))

    # First run ever → suggest experiment
    if not tracker.has_used("experiment"):
        tips.append(Tip(
            feature="tip:experiment",
            text="Tip: Compare org structures with `agentciv experiment --task \"...\" --orgs collaborative,meritocratic,auto`",
        ))

    # Used solve but not auto → suggest auto
    if org_preset != "auto" and not tracker.has_used("auto"):
        tips.append(Tip(
            feature="tip:auto",
            text="Tip: Try --org auto — agents design their own organisational structure through proposals and votes.",
        ))

    # Auto run → mention learning
    if org_preset == "auto" and not tracker.has_seen("tip:learning"):
        tips.append(Tip(
            feature="tip:learning",
            text="Tip: This run's data feeds into auto mode learning. Future --org auto runs get smarter from accumulated history.",
        ))

    # Auto run with restructures → mention gardener
    if restructures_adopted > 0 and not tracker.has_used("gardener"):
        tips.append(Tip(
            feature="tip:gardener",
            text="Tip: Use --gardener to intervene mid-run — guide agents, force meta-ticks, or adjust parameters live.",
        ))

    # Multiple agents → mention benchmark
    if agent_count >= 3 and not tracker.has_used("benchmark"):
        tips.append(Tip(
            feature="tip:benchmark",
            text="Tip: Run standardised benchmarks with `agentciv benchmark --tasks all --presets all` to compare all 13 configs.",
        ))

    # History exists → mention it
    if not tracker.has_seen("tip:history"):
        tips.append(Tip(
            feature="tip:history",
            text="Tip: View learning data with `agentciv history` or find similar past runs with `agentciv history --similar \"your task\"`",
        ))

    # Filter to unseen tips
    for tip in tips:
        if not tracker.has_seen(tip.feature):
            tracker.mark_seen(tip.feature)
            return tip

    return None


def generate_post_experiment_tip(
    orgs_tested: list[str],
    tracker: FeatureTracker | None = None,
) -> Tip | None:
    """Generate a tip after an experiment run."""
    if tracker is None:
        tracker = FeatureTracker()

    tips: list[Tip] = []

    if "auto" not in orgs_tested and not tracker.has_seen("tip:experiment-auto"):
        tips.append(Tip(
            feature="tip:experiment-auto",
            text="Tip: Include 'auto' in your experiment — agents design their own org and often match or beat manual presets.",
        ))

    if not tracker.has_seen("tip:experiment-json"):
        tips.append(Tip(
            feature="tip:experiment-json",
            text="Tip: Add --output results.json to export experiment data for further analysis.",
        ))

    for tip in tips:
        if not tracker.has_seen(tip.feature):
            tracker.mark_seen(tip.feature)
            return tip

    return None


def generate_mcp_hints(
    context: str,
    session_data: dict[str, Any] | None = None,
) -> list[str]:
    """Generate hints for MCP response enrichment.

    Returns a list of short suggestion strings to include in MCP responses.
    Unlike CLI tips, these don't track state — MCP clients may ignore them.
    """
    hints: list[str] = []

    if context == "solve_started":
        hints.append("Monitor progress with agentciv_status(session_id='...')")
        hints.append("Guide agents with agentciv_intervene(session_id='...', message='...')")

    elif context == "solve_completed":
        if session_data:
            conflicts = session_data.get("merge_conflicts", 0)
            org = session_data.get("org_preset", "")
            if conflicts >= 2:
                hints.append("High merge conflicts — consider 'code-review' preset next time")
            if org != "auto":
                hints.append("Try org='auto' to let agents design their own structure")
        hints.append("Compare structures with agentciv_experiment()")
        hints.append("View accumulated learning data with agentciv_status()")

    elif context == "experiment_completed":
        hints.append("Export results: add output parameter for JSON")
        hints.append("Include 'auto' in orgs to see self-organising performance")

    elif context == "info":
        hints.append("Start with agentciv_solve(task='...', org='collaborative')")
        hints.append("The crown jewel: org='auto' — agents vote on their own structure")

    return hints
