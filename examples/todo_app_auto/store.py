"""
store.py — Defines the TodoStore, managing a collection of Todo items.
"""

from typing import List, Optional
from todo import Todo


class TodoNotFoundError(Exception):
    """Raised when a requested todo item does not exist."""
    pass


class TodoStore:
    """
    In-memory store for Todo items.

    Methods
    -------
    add(title)      → Todo        Add a new todo and return it.
    remove(index)   → Todo        Remove todo at 1-based index; return it.
    toggle(index)   → Todo        Toggle done state; return updated todo.
    list()          → List[Todo]  Return all todos (copy).
    get(index)      → Todo        Return todo at 1-based index.
    """

    def __init__(self):
        self._todos: List[Todo] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add(self, title: str) -> Todo:
        """Create a new Todo with the given title and store it.

        Parameters
        ----------
        title : str
            Non-empty title for the todo item.

        Returns
        -------
        Todo
            The newly created todo.
        """
        todo = Todo(title)
        self._todos.append(todo)
        return todo

    def remove(self, index: int) -> Todo:
        """Remove the todo at the given 1-based index.

        Parameters
        ----------
        index : int
            1-based position of the todo to remove.

        Returns
        -------
        Todo
            The removed todo.

        Raises
        ------
        TodoNotFoundError
            If the index is out of range.
        """
        self._validate_index(index)
        return self._todos.pop(index - 1)

    def toggle(self, index: int) -> Todo:
        """Toggle the done state of the todo at the given 1-based index.

        Parameters
        ----------
        index : int
            1-based position of the todo to toggle.

        Returns
        -------
        Todo
            The updated todo.

        Raises
        ------
        TodoNotFoundError
            If the index is out of range.
        """
        todo = self.get(index)
        todo.toggle()
        return todo

    def list(self) -> List[Todo]:
        """Return a shallow copy of all stored todos.

        Returns
        -------
        List[Todo]
            All current todos in insertion order.
        """
        return list(self._todos)

    def get(self, index: int) -> Todo:
        """Return the todo at the given 1-based index without removing it.

        Parameters
        ----------
        index : int
            1-based position of the todo to retrieve.

        Returns
        -------
        Todo
            The todo at that position.

        Raises
        ------
        TodoNotFoundError
            If the index is out of range.
        """
        self._validate_index(index)
        return self._todos[index - 1]

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _validate_index(self, index: int) -> None:
        if not isinstance(index, int) or index < 1 or index > len(self._todos):
            raise TodoNotFoundError(
                f"No todo at index {index}. "
                f"Valid range: 1–{len(self._todos)} "
                f"({len(self._todos)} item(s) stored)."
            )

    def __len__(self) -> int:
        return len(self._todos)

    def __repr__(self) -> str:
        return f"TodoStore({len(self._todos)} item(s))"
