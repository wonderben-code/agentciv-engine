"""Workspace — the shared project environment.

The workspace IS the world. Instead of a 2D grid with tiles, resources, and
structures, the workspace is a project directory with files, build state,
and task signals.

Every agent can see the workspace. What they see is mediated by the
perception system (smart file relevance) and the organisational config
(information flow dimension).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..core.types import AgentState, TaskSignal


@dataclass
class FileInfo:
    """Metadata about a file in the workspace."""
    path: str  # relative to project root
    size: int = 0
    language: str = "unknown"
    last_modified_tick: int = 0
    last_modified_by: str | None = None
    summary: str = ""  # brief description of contents


@dataclass
class Workspace:
    """The shared project environment that all agents perceive and modify."""

    project_dir: Path
    task_description: str = ""

    # State
    files: dict[str, FileInfo] = field(default_factory=dict)
    task_board: list[TaskSignal] = field(default_factory=list)
    build_status: str = "unknown"  # "unknown", "passing", "failing"
    test_status: str = "unknown"

    # Agent presence
    _agent_states: dict[str, AgentState] = field(default_factory=dict)

    def scan(self) -> None:
        """Scan the project directory and index all files."""
        self.files.clear()
        for root, dirs, filenames in os.walk(self.project_dir):
            # Skip hidden dirs and common non-code dirs
            dirs[:] = [
                d for d in dirs
                if not d.startswith(".") and d not in {
                    "node_modules", "__pycache__", "venv", ".venv",
                    "dist", "build", ".git",
                }
            ]
            for fname in filenames:
                if fname.startswith("."):
                    continue
                full_path = Path(root) / fname
                rel_path = str(full_path.relative_to(self.project_dir))
                self.files[rel_path] = FileInfo(
                    path=rel_path,
                    size=full_path.stat().st_size,
                    language=self._detect_language(fname),
                )

    def get_visible_files(self, agent: AgentState) -> list[dict[str, Any]]:
        """Get files visible to an agent, sorted by relevance.

        TODO: Smart perception — dependency graphs, import trees, co-change
        frequency, relevance to agent's current focus. For now, returns all
        files sorted by relevance to working_files.
        """
        all_files = list(self.files.values())

        # Boost files the agent is working on
        working = set(agent.working_files)
        scored = []
        for f in all_files:
            score = 0.5
            if f.path in working:
                score = 1.0
            elif f.last_modified_by == agent.identity.id:
                score = 0.8
            elif f.last_modified_by is not None:
                score = 0.6  # recently touched by someone
            scored.append((score, f))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {"path": f.path, "language": f.language, "summary": f.summary, "size": f.size}
            for _, f in scored
        ]

    def get_task_board(self) -> list[TaskSignal]:
        """Get current task signals."""
        return list(self.task_board)

    def register_agent(self, state: AgentState) -> None:
        """Register an agent's state for cross-agent awareness."""
        self._agent_states[state.identity.id] = state

    def get_agent_summaries(self, exclude: str | None = None) -> list[dict[str, Any]]:
        """Get summaries of what other agents are doing."""
        summaries = []
        for agent_id, state in self._agent_states.items():
            if agent_id == exclude:
                continue
            summaries.append({
                "id": agent_id,
                "name": state.identity.name,
                "focus": state.current_focus or "idle",
                "working_files": state.working_files[:3],
                "skills": [
                    {"name": s.name, "tier": s.tier, "count": s.action_count}
                    for s in sorted(
                        state.skills.values(),
                        key=lambda s: s.action_count,
                        reverse=True,
                    )[:3]
                ],
            })
        return summaries

    def read_file(self, path: str) -> str | None:
        """Read a file from the workspace."""
        full_path = self.project_dir / path
        if not full_path.exists():
            return None
        return full_path.read_text(errors="replace")

    def write_file(self, path: str, content: str, agent_id: str, tick: int) -> bool:
        """Write content to a file. Returns True on success."""
        full_path = self.project_dir / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)

        # Update file index
        rel_path = str(Path(path))
        if rel_path not in self.files:
            self.files[rel_path] = FileInfo(path=rel_path)
        self.files[rel_path].last_modified_tick = tick
        self.files[rel_path].last_modified_by = agent_id
        self.files[rel_path].size = len(content)
        return True

    @staticmethod
    def _detect_language(filename: str) -> str:
        """Simple language detection from file extension."""
        ext_map = {
            ".py": "python", ".js": "javascript", ".ts": "typescript",
            ".tsx": "typescript", ".jsx": "javascript", ".rs": "rust",
            ".go": "go", ".java": "java", ".rb": "ruby", ".cpp": "cpp",
            ".c": "c", ".h": "c", ".cs": "csharp", ".swift": "swift",
            ".kt": "kotlin", ".md": "markdown", ".json": "json",
            ".yaml": "yaml", ".yml": "yaml", ".toml": "toml",
            ".html": "html", ".css": "css", ".sql": "sql",
            ".sh": "shell", ".bash": "shell",
        }
        ext = Path(filename).suffix.lower()
        return ext_map.get(ext, "unknown")
