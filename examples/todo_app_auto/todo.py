"""
todo.py — Defines the Todo data model.
"""

from datetime import datetime


class Todo:
    """Represents a single todo item."""

    def __init__(self, title: str):
        if not title or not title.strip():
            raise ValueError("Todo title must not be empty.")
        self.title: str = title.strip()
        self.done: bool = False
        self.created_at: datetime = datetime.now()

    def toggle(self) -> None:
        """Toggle the completion state of this todo."""
        self.done = not self.done

    def __repr__(self) -> str:
        status = "✓" if self.done else "○"
        created = self.created_at.strftime("%Y-%m-%d %H:%M")
        return f"[{status}] {self.title!r} (created: {created})"

    def to_dict(self) -> dict:
        """Serialize the todo to a plain dictionary."""
        return {
            "title": self.title,
            "done": self.done,
            "created_at": self.created_at.isoformat(),
        }
