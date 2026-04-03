"""Run history — persistent storage of run outcomes.

Stores RunRecords as JSON Lines in ~/.agentciv/run_history.jsonl.
Global across projects so learnings transfer between tasks.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

HISTORY_DIR = Path.home() / ".agentciv"
HISTORY_FILE = HISTORY_DIR / "run_history.jsonl"

# Common stopwords to filter from task descriptions
_STOPWORDS = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "must", "shall", "can",
    "that", "this", "these", "those", "it", "its", "not", "no", "so",
    "if", "then", "else", "when", "where", "how", "what", "which", "who",
    "all", "each", "every", "both", "few", "more", "most", "other",
    "some", "such", "only", "own", "same", "than", "too", "very",
    "just", "about", "above", "after", "again", "also", "any", "because",
    "before", "between", "into", "through", "during", "out", "up",
    "build", "create", "make", "write", "implement", "develop", "add",
    "using", "use", "simple", "basic", "small", "new", "good",
})


@dataclass
class RunRecord:
    """A single run's outcome for the learning system."""

    timestamp: str
    task_description: str
    task_keywords: list[str]
    org_preset: str
    final_org_state: dict[str, str]
    agent_count: int
    model: str
    ticks_used: int
    max_ticks: int

    # Outcomes
    files_produced: int = 0
    total_messages: int = 0
    total_broadcasts: int = 0
    merge_conflicts: int = 0
    merges_succeeded: int = 0
    restructures_adopted: int = 0
    restructure_log: list[dict[str, Any]] = field(default_factory=list)

    # Success signals
    success: bool = True
    completion_rate: float | None = None
    test_pass_rate: float | None = None

    # Computed quality score (0-1, higher = better)
    quality_score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RunRecord:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


def extract_keywords(text: str) -> list[str]:
    """Extract meaningful keywords from a task description."""
    # Normalise: lowercase, split on non-alphanumeric
    words = re.findall(r"[a-z0-9]+", text.lower())
    # Filter stopwords and short words
    keywords = [w for w in words if w not in _STOPWORDS and len(w) >= 3]
    # Deduplicate preserving order
    seen: set[str] = set()
    result: list[str] = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            result.append(kw)
    return result


def keyword_similarity(a: list[str], b: list[str]) -> float:
    """Jaccard similarity between two keyword lists."""
    set_a = set(a)
    set_b = set(b)
    if not set_a or not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


class RunHistory:
    """Persistent run history with similarity search."""

    def __init__(self, history_file: Path | None = None):
        self._file = history_file or HISTORY_FILE
        self._records: list[RunRecord] | None = None

    def _ensure_dir(self) -> None:
        self._file.parent.mkdir(parents=True, exist_ok=True)

    def save_run(self, record: RunRecord) -> None:
        """Append a run record to the history file."""
        self._ensure_dir()
        try:
            with open(self._file, "a") as f:
                f.write(json.dumps(record.to_dict()) + "\n")
            # Invalidate cache
            self._records = None
            log.info(
                "Saved run record: %s / %s (quality=%.2f)",
                record.org_preset, record.task_keywords[:3], record.quality_score,
            )
        except Exception as e:
            log.warning("Failed to save run record: %s", e)

    def load_all(self) -> list[RunRecord]:
        """Load all records from history."""
        if self._records is not None:
            return self._records

        records: list[RunRecord] = []
        if not self._file.exists():
            self._records = records
            return records

        try:
            with open(self._file) as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        records.append(RunRecord.from_dict(data))
                    except (json.JSONDecodeError, TypeError) as e:
                        log.warning("Skipping corrupt record at line %d: %s", line_num, e)
        except Exception as e:
            log.warning("Failed to load run history: %s", e)

        self._records = records
        return records

    def find_similar(
        self,
        task_description: str,
        min_similarity: float = 0.15,
        max_results: int = 20,
    ) -> list[tuple[RunRecord, float]]:
        """Find runs with similar task descriptions.

        Returns list of (record, similarity_score) sorted by similarity desc.
        """
        keywords = extract_keywords(task_description)
        if not keywords:
            return []

        records = self.load_all()
        scored: list[tuple[RunRecord, float]] = []

        for record in records:
            sim = keyword_similarity(keywords, record.task_keywords)
            if sim >= min_similarity:
                scored.append((record, sim))

        scored.sort(key=lambda x: (-x[1], -x[0].quality_score))
        return scored[:max_results]

    def get_stats(self) -> dict[str, Any]:
        """Return summary statistics about the history."""
        records = self.load_all()
        if not records:
            return {"total_runs": 0}

        presets = {}
        for r in records:
            presets.setdefault(r.org_preset, []).append(r.quality_score)

        return {
            "total_runs": len(records),
            "unique_presets": len(presets),
            "preset_avg_quality": {
                preset: round(sum(scores) / len(scores), 3)
                for preset, scores in sorted(presets.items())
            },
            "successful_runs": sum(1 for r in records if r.success),
        }

    def clear(self) -> None:
        """Clear all history."""
        if self._file.exists():
            self._file.unlink()
        self._records = None
        log.info("Run history cleared")
