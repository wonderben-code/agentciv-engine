"""
main.py — CLI interface for the Todo app.

Usage:
    python main.py add "Buy groceries"
    python main.py list
    python main.py toggle 1
    python main.py remove 2
    python main.py get 1
"""

import sys
from store import TodoStore, TodoNotFoundError

# Single shared store for this session
_store = TodoStore()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_index(raw: str) -> int:
    """Parse a 1-based integer index from a string, or exit with an error."""
    try:
        index = int(raw)
    except ValueError:
        print(f"Error: '{raw}' is not a valid integer index.", file=sys.stderr)
        sys.exit(1)
    return index


def _fmt_todo(index: int, todo) -> str:
    """Format a single todo for display."""
    status = "✓" if todo.done else "○"
    created = todo.created_at.strftime("%Y-%m-%d %H:%M")
    return f"  {index}. [{status}] {todo.title}  (added: {created})"


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def cmd_add(args: list) -> None:
    """Add a new todo item.

    Usage: python main.py add <title>
    """
    if not args:
        print("Usage: python main.py add <title>", file=sys.stderr)
        sys.exit(1)
    title = " ".join(args)
    try:
        todo = _store.add(title)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    index = len(_store)
    print(f"Added todo {index}:")
    print(_fmt_todo(index, todo))


def cmd_list(_args: list) -> None:
    """List all todo items.

    Usage: python main.py list
    """
    todos = _store.list()
    if not todos:
        print("No todos yet. Add one with: python main.py add <title>")
        return
    print(f"Todos ({len(todos)}):")
    for i, todo in enumerate(todos, start=1):
        print(_fmt_todo(i, todo))


def cmd_toggle(args: list) -> None:
    """Toggle the done state of a todo.

    Usage: python main.py toggle <index>
    """
    if not args:
        print("Usage: python main.py toggle <index>", file=sys.stderr)
        sys.exit(1)
    index = _parse_index(args[0])
    try:
        todo = _store.toggle(index)
    except TodoNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    state = "done ✓" if todo.done else "not done ○"
    print(f"Toggled todo {index} → {state}:")
    print(_fmt_todo(index, todo))


def cmd_remove(args: list) -> None:
    """Remove a todo item.

    Usage: python main.py remove <index>
    """
    if not args:
        print("Usage: python main.py remove <index>", file=sys.stderr)
        sys.exit(1)
    index = _parse_index(args[0])
    try:
        todo = _store.remove(index)
    except TodoNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    print(f"Removed todo: '{todo.title}'")


def cmd_get(args: list) -> None:
    """Get a single todo by index.

    Usage: python main.py get <index>
    """
    if not args:
        print("Usage: python main.py get <index>", file=sys.stderr)
        sys.exit(1)
    index = _parse_index(args[0])
    try:
        todo = _store.get(index)
    except TodoNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    print(f"Todo {index}:")
    print(_fmt_todo(index, todo))


def cmd_help(_args: list) -> None:
    """Show help text."""
    print(
        "Todo CLI — manage your tasks from the command line\n"
        "\n"
        "Commands:\n"
        "  add <title>     Add a new todo item\n"
        "  list            List all todo items\n"
        "  toggle <index>  Toggle done/not-done for a todo\n"
        "  remove <index>  Remove a todo item\n"
        "  get <index>     Show a single todo item\n"
        "  help            Show this help message\n"
        "\n"
        "Indices are 1-based (the first todo is index 1)."
    )


# ---------------------------------------------------------------------------
# Dispatch table
# ---------------------------------------------------------------------------

COMMANDS = {
    "add": cmd_add,
    "list": cmd_list,
    "toggle": cmd_toggle,
    "remove": cmd_remove,
    "get": cmd_get,
    "help": cmd_help,
}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list = None) -> None:
    """Parse arguments and dispatch to the appropriate command handler."""
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        cmd_help([])
        return

    command, *args = argv
    handler = COMMANDS.get(command)

    if handler is None:
        print(
            f"Unknown command: '{command}'. "
            f"Available commands: {', '.join(COMMANDS)}",
            file=sys.stderr,
        )
        sys.exit(1)

    handler(args)


if __name__ == "__main__":
    main()
