# ✅ Todo App

A clean, minimal command-line todo application written in Python 3.

---

## Features

- Add, list, toggle, remove, and retrieve todo items
- 1-based indexing for a natural user experience
- Timestamps on every item (creation time)
- Fully unit-tested with `pytest`
- Zero external dependencies

---

## Project Structure

```
todo-app/
├── todo.py               # Todo data model
├── store.py              # TodoStore — manages a collection of todos
├── main.py               # CLI entry point
├── tests/
│   ├── __init__.py
│   └── test_store.py     # Unit tests for Todo + TodoStore
└── README.md
```

---

## Quick Start

### Prerequisites

- Python 3.8 or newer

### Run the CLI

```bash
python main.py help
```

---

## CLI Usage

```
python main.py <command> [arguments]
```

| Command              | Description                             |
|----------------------|-----------------------------------------|
| `add <title>`        | Add a new todo item                     |
| `list`               | List all todo items                     |
| `toggle <index>`     | Toggle done / not-done for an item      |
| `remove <index>`     | Permanently remove an item              |
| `get <index>`        | Display a single item by index          |
| `help`               | Show usage information                  |

> **Note:** Indices are **1-based** — the first todo is index `1`.

### Examples

```bash
# Add some todos
python main.py add "Buy groceries"
python main.py add "Write unit tests"
python main.py add "Ship the feature"

# List everything
python main.py list
# Todos (3):
#   1. [○] Buy groceries       (added: 2024-01-15 09:30)
#   2. [○] Write unit tests    (added: 2024-01-15 09:30)
#   3. [○] Ship the feature    (added: 2024-01-15 09:30)

# Mark item 2 as done
python main.py toggle 2
# Toggled todo 2 → done ✓

# List again — item 2 is now marked
python main.py list
# Todos (3):
#   1. [○] Buy groceries       (added: 2024-01-15 09:30)
#   2. [✓] Write unit tests    (added: 2024-01-15 09:30)
#   3. [○] Ship the feature    (added: 2024-01-15 09:30)

# Get a single item
python main.py get 1
# Todo 1:
#   1. [○] Buy groceries  (added: 2024-01-15 09:30)

# Remove an item
python main.py remove 1
# Removed todo: 'Buy groceries'
```

---

## API Reference

### `todo.py` — `Todo`

```python
from todo import Todo

todo = Todo("Buy milk")
todo.title       # "Buy milk"   (str, whitespace stripped)
todo.done        # False        (bool)
todo.created_at  # datetime.now() at creation time

todo.toggle()    # flip done ↔ not done
todo.to_dict()   # {"title": ..., "done": ..., "created_at": "<ISO string>"}
repr(todo)       # "[○] 'Buy milk' (created: 2024-01-15 09:30)"
```

**Raises `ValueError`** if the title is empty or whitespace-only.

---

### `store.py` — `TodoStore`

```python
from store import TodoStore, TodoNotFoundError

store = TodoStore()
```

| Method                    | Returns       | Description                                      |
|---------------------------|---------------|--------------------------------------------------|
| `store.add(title)`        | `Todo`        | Create and store a new todo; returns it          |
| `store.list()`            | `List[Todo]`  | Return a copy of all todos in insertion order    |
| `store.get(index)`        | `Todo`        | Return todo at 1-based index (non-destructive)   |
| `store.toggle(index)`     | `Todo`        | Flip done state of todo at index; return it      |
| `store.remove(index)`     | `Todo`        | Remove and return todo at 1-based index          |
| `len(store)`              | `int`         | Number of todos currently stored                 |

**Raises `TodoNotFoundError`** (from `store.py`) when an index is out of range.

---

## Running Tests

```bash
pytest tests/test_store.py -v
```

Example output:

```
tests/test_store.py::TestTodo::test_create_todo_sets_title PASSED
tests/test_store.py::TestTodo::test_create_todo_strips_whitespace PASSED
tests/test_store.py::TestTodo::test_create_todo_done_is_false_by_default PASSED
...
tests/test_store.py::TestTodoStoreMisc::test_full_workflow PASSED
tests/test_store.py::TestTodoStoreMisc::test_independent_stores_dont_share_state PASSED

xx passed in 0.xxs
```

---

## Design Notes

- **In-memory storage**: todos are held in a plain Python list for the current session. There is no persistence between runs — by design for simplicity.
- **1-based indexing**: matches what users expect from CLI tools (like `cut`, numbered lists, etc.).
- **Immutable timestamps**: `created_at` is set once at construction and never mutated.
- **Defensive validation**: both `Todo` and `TodoStore` validate inputs immediately and raise descriptive exceptions.

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b my-feature`
3. Make your changes and add tests
4. Run `pytest tests/ -v` to confirm everything passes
5. Open a pull request

---

## License

MIT — free to use, modify, and distribute.
