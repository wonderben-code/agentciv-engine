"""
tests/test_store.py — Unit tests for the Todo model and TodoStore.

Run with:
    pytest tests/test_store.py -v
"""

import pytest
from datetime import datetime

from todo import Todo
from store import TodoStore, TodoNotFoundError


# ===========================================================================
# Todo model tests
# ===========================================================================

class TestTodo:
    """Tests for the Todo data model."""

    def test_create_todo_sets_title(self):
        todo = Todo("Buy milk")
        assert todo.title == "Buy milk"

    def test_create_todo_strips_whitespace(self):
        todo = Todo("  Buy milk  ")
        assert todo.title == "Buy milk"

    def test_create_todo_done_is_false_by_default(self):
        todo = Todo("Buy milk")
        assert todo.done is False

    def test_create_todo_created_at_is_datetime(self):
        todo = Todo("Buy milk")
        assert isinstance(todo.created_at, datetime)

    def test_create_todo_created_at_is_recent(self):
        before = datetime.now()
        todo = Todo("Buy milk")
        after = datetime.now()
        assert before <= todo.created_at <= after

    def test_create_todo_empty_title_raises(self):
        with pytest.raises(ValueError):
            Todo("")

    def test_create_todo_whitespace_only_raises(self):
        with pytest.raises(ValueError):
            Todo("   ")

    def test_toggle_false_to_true(self):
        todo = Todo("Buy milk")
        todo.toggle()
        assert todo.done is True

    def test_toggle_true_to_false(self):
        todo = Todo("Buy milk")
        todo.toggle()
        todo.toggle()
        assert todo.done is False

    def test_toggle_multiple_times(self):
        todo = Todo("Buy milk")
        for i in range(5):
            todo.toggle()
        assert todo.done is True  # odd number of toggles → True

    def test_repr_contains_title(self):
        todo = Todo("Buy milk")
        assert "Buy milk" in repr(todo)

    def test_repr_shows_undone_marker(self):
        todo = Todo("Buy milk")
        assert "○" in repr(todo)

    def test_repr_shows_done_marker(self):
        todo = Todo("Buy milk")
        todo.toggle()
        assert "✓" in repr(todo)

    def test_to_dict_keys(self):
        todo = Todo("Buy milk")
        d = todo.to_dict()
        assert set(d.keys()) == {"title", "done", "created_at"}

    def test_to_dict_values(self):
        todo = Todo("Buy milk")
        d = todo.to_dict()
        assert d["title"] == "Buy milk"
        assert d["done"] is False
        assert isinstance(d["created_at"], str)  # ISO format string

    def test_to_dict_done_true_after_toggle(self):
        todo = Todo("Buy milk")
        todo.toggle()
        assert todo.to_dict()["done"] is True


# ===========================================================================
# TodoStore tests
# ===========================================================================

class TestTodoStoreAdd:
    """Tests for TodoStore.add()."""

    def test_add_returns_todo(self):
        store = TodoStore()
        result = store.add("Buy milk")
        assert isinstance(result, Todo)

    def test_add_sets_title(self):
        store = TodoStore()
        todo = store.add("Buy milk")
        assert todo.title == "Buy milk"

    def test_add_increases_length(self):
        store = TodoStore()
        assert len(store) == 0
        store.add("Task 1")
        assert len(store) == 1
        store.add("Task 2")
        assert len(store) == 2

    def test_add_empty_title_raises(self):
        store = TodoStore()
        with pytest.raises(ValueError):
            store.add("")

    def test_add_whitespace_title_raises(self):
        store = TodoStore()
        with pytest.raises(ValueError):
            store.add("   ")

    def test_add_multiple_todos_in_order(self):
        store = TodoStore()
        store.add("First")
        store.add("Second")
        store.add("Third")
        todos = store.list()
        assert [t.title for t in todos] == ["First", "Second", "Third"]


class TestTodoStoreList:
    """Tests for TodoStore.list()."""

    def test_list_empty_store(self):
        store = TodoStore()
        assert store.list() == []

    def test_list_returns_all_todos(self):
        store = TodoStore()
        store.add("Task A")
        store.add("Task B")
        todos = store.list()
        assert len(todos) == 2

    def test_list_returns_copy_not_reference(self):
        store = TodoStore()
        store.add("Task A")
        todos = store.list()
        todos.clear()
        assert len(store) == 1  # original store unaffected

    def test_list_preserves_insertion_order(self):
        store = TodoStore()
        titles = ["Alpha", "Beta", "Gamma", "Delta"]
        for t in titles:
            store.add(t)
        assert [todo.title for todo in store.list()] == titles


class TestTodoStoreGet:
    """Tests for TodoStore.get()."""

    def test_get_first_item(self):
        store = TodoStore()
        store.add("First")
        todo = store.get(1)
        assert todo.title == "First"

    def test_get_last_item(self):
        store = TodoStore()
        store.add("First")
        store.add("Second")
        store.add("Third")
        todo = store.get(3)
        assert todo.title == "Third"

    def test_get_middle_item(self):
        store = TodoStore()
        store.add("A")
        store.add("B")
        store.add("C")
        assert store.get(2).title == "B"

    def test_get_does_not_remove_item(self):
        store = TodoStore()
        store.add("Stay")
        store.get(1)
        assert len(store) == 1

    def test_get_index_zero_raises(self):
        store = TodoStore()
        store.add("Task")
        with pytest.raises(TodoNotFoundError):
            store.get(0)

    def test_get_negative_index_raises(self):
        store = TodoStore()
        store.add("Task")
        with pytest.raises(TodoNotFoundError):
            store.get(-1)

    def test_get_out_of_range_raises(self):
        store = TodoStore()
        store.add("Task")
        with pytest.raises(TodoNotFoundError):
            store.get(2)

    def test_get_empty_store_raises(self):
        store = TodoStore()
        with pytest.raises(TodoNotFoundError):
            store.get(1)

    def test_get_non_integer_raises(self):
        store = TodoStore()
        store.add("Task")
        with pytest.raises(TodoNotFoundError):
            store.get("1")  # type: ignore


class TestTodoStoreRemove:
    """Tests for TodoStore.remove()."""

    def test_remove_returns_todo(self):
        store = TodoStore()
        store.add("Task")
        removed = store.remove(1)
        assert isinstance(removed, Todo)

    def test_remove_returns_correct_todo(self):
        store = TodoStore()
        store.add("Keep")
        store.add("Remove me")
        removed = store.remove(2)
        assert removed.title == "Remove me"

    def test_remove_decreases_length(self):
        store = TodoStore()
        store.add("A")
        store.add("B")
        store.remove(1)
        assert len(store) == 1

    def test_remove_first_item_shifts_rest(self):
        store = TodoStore()
        store.add("First")
        store.add("Second")
        store.add("Third")
        store.remove(1)
        todos = store.list()
        assert [t.title for t in todos] == ["Second", "Third"]

    def test_remove_middle_item(self):
        store = TodoStore()
        store.add("A")
        store.add("B")
        store.add("C")
        store.remove(2)
        assert [t.title for t in store.list()] == ["A", "C"]

    def test_remove_last_item(self):
        store = TodoStore()
        store.add("A")
        store.add("B")
        store.remove(2)
        assert [t.title for t in store.list()] == ["A"]

    def test_remove_until_empty(self):
        store = TodoStore()
        store.add("Only one")
        store.remove(1)
        assert len(store) == 0

    def test_remove_out_of_range_raises(self):
        store = TodoStore()
        store.add("Task")
        with pytest.raises(TodoNotFoundError):
            store.remove(2)

    def test_remove_empty_store_raises(self):
        store = TodoStore()
        with pytest.raises(TodoNotFoundError):
            store.remove(1)

    def test_remove_zero_index_raises(self):
        store = TodoStore()
        store.add("Task")
        with pytest.raises(TodoNotFoundError):
            store.remove(0)


class TestTodoStoreToggle:
    """Tests for TodoStore.toggle()."""

    def test_toggle_returns_todo(self):
        store = TodoStore()
        store.add("Task")
        result = store.toggle(1)
        assert isinstance(result, Todo)

    def test_toggle_marks_undone_as_done(self):
        store = TodoStore()
        store.add("Task")
        todo = store.toggle(1)
        assert todo.done is True

    def test_toggle_marks_done_as_undone(self):
        store = TodoStore()
        store.add("Task")
        store.toggle(1)
        todo = store.toggle(1)
        assert todo.done is False

    def test_toggle_mutates_stored_todo(self):
        store = TodoStore()
        store.add("Task")
        store.toggle(1)
        assert store.get(1).done is True

    def test_toggle_only_affects_target(self):
        store = TodoStore()
        store.add("A")
        store.add("B")
        store.add("C")
        store.toggle(2)
        assert store.get(1).done is False
        assert store.get(2).done is True
        assert store.get(3).done is False

    def test_toggle_out_of_range_raises(self):
        store = TodoStore()
        store.add("Task")
        with pytest.raises(TodoNotFoundError):
            store.toggle(5)

    def test_toggle_empty_store_raises(self):
        store = TodoStore()
        with pytest.raises(TodoNotFoundError):
            store.toggle(1)


class TestTodoStoreMisc:
    """Miscellaneous / integration-style store tests."""

    def test_len_empty(self):
        store = TodoStore()
        assert len(store) == 0

    def test_repr_contains_count(self):
        store = TodoStore()
        store.add("A")
        store.add("B")
        assert "2" in repr(store)

    def test_full_workflow(self):
        """Add → list → toggle → get → remove → list again."""
        store = TodoStore()

        # Add three items
        store.add("Buy milk")
        store.add("Write tests")
        store.add("Ship it")
        assert len(store) == 3

        # Toggle the second
        todo = store.toggle(2)
        assert todo.done is True

        # Get confirms state
        assert store.get(2).done is True

        # Remove the first
        removed = store.remove(1)
        assert removed.title == "Buy milk"
        assert len(store) == 2

        # Remaining items shifted
        remaining = store.list()
        assert remaining[0].title == "Write tests"
        assert remaining[1].title == "Ship it"

    def test_add_after_remove_uses_correct_index(self):
        store = TodoStore()
        store.add("Alpha")
        store.add("Beta")
        store.remove(1)
        store.add("Gamma")
        # Now: Beta(1), Gamma(2)
        assert store.get(1).title == "Beta"
        assert store.get(2).title == "Gamma"

    def test_independent_stores_dont_share_state(self):
        store_a = TodoStore()
        store_b = TodoStore()
        store_a.add("Only in A")
        assert len(store_b) == 0
