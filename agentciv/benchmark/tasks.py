"""Task bank — standardised tasks for benchmarking organisational configurations.

Each task is a self-contained definition: description, seed files, verification
script, and expected outputs. Tasks are designed so that different organisational
structures produce measurably different outcomes.

Difficulty levels:
  simple  — 1-2 files, clear requirements, any org should complete
  medium  — 3-5 files, requires coordination, org structure matters
  hard    — 5+ files, complex coordination, org structure critical
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class BenchmarkTask:
    """A standardised task for benchmarking."""
    id: str
    name: str
    description: str  # the --task prompt given to the engine
    difficulty: str  # "simple" | "medium" | "hard"
    seed_files: dict[str, str]  # path -> content (initial project state)
    verification_script: str  # Python code run post-task to check correctness
    expected_files: list[str]  # files that should exist after completion
    max_ticks: int  # recommended tick limit
    tags: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Task 1: FizzBuzz (simple)
# ---------------------------------------------------------------------------

_FIZZBUZZ = BenchmarkTask(
    id="fizzbuzz",
    name="FizzBuzz",
    difficulty="simple",
    description=(
        "Write a Python file fizzbuzz.py with a function fizzbuzz(n) that returns "
        "a list of strings for numbers 1 to n: 'Fizz' for multiples of 3, 'Buzz' "
        "for multiples of 5, 'FizzBuzz' for multiples of both, or the number as a "
        "string otherwise. Also write test_fizzbuzz.py with at least 5 tests using "
        "assert statements. Coordinate with your team on who writes what."
    ),
    seed_files={},
    expected_files=["fizzbuzz.py", "test_fizzbuzz.py"],
    max_ticks=5,
    tags=["python", "simple", "testing"],
    verification_script=r"""
import sys, os, importlib.util

results = {"tests_total": 0, "tests_passed": 0, "files_present": []}

# Check files exist
for f in ["fizzbuzz.py", "test_fizzbuzz.py"]:
    if os.path.exists(f):
        results["files_present"].append(f)

# Try to import and test fizzbuzz
try:
    spec = importlib.util.spec_from_file_location("fizzbuzz", "fizzbuzz.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fb = mod.fizzbuzz

    checks = [
        (fb(1), ["1"]),
        (fb(3)[-1], "Fizz"),
        (fb(5)[-1], "Buzz"),
        (fb(15)[-1], "FizzBuzz"),
        (len(fb(100)), 100),
    ]
    for i, (got, expected) in enumerate(checks):
        results["tests_total"] += 1
        if got == expected:
            results["tests_passed"] += 1
except Exception as e:
    results["error"] = str(e)

# Try running the test file
try:
    spec2 = importlib.util.spec_from_file_location("test_fizzbuzz", "test_fizzbuzz.py")
    mod2 = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(mod2)
    results["test_file_ran"] = True
except Exception as e:
    results["test_file_error"] = str(e)

import json
print(json.dumps(results))
""",
)

# ---------------------------------------------------------------------------
# Task 2: Key-Value Store (simple)
# ---------------------------------------------------------------------------

_KV_STORE = BenchmarkTask(
    id="kv-store",
    name="Key-Value Store",
    difficulty="simple",
    description=(
        "Build a Python key-value store in kv.py with a class KVStore that supports: "
        "set(key, value), get(key) -> value (raises KeyError if missing), "
        "delete(key), exists(key) -> bool, keys() -> list, and len(). "
        "Write test_kv.py with at least 8 tests covering all methods, edge cases, "
        "and error handling. Coordinate who writes what."
    ),
    seed_files={},
    expected_files=["kv.py", "test_kv.py"],
    max_ticks=8,
    tags=["python", "simple", "data-structure", "testing"],
    verification_script=r"""
import sys, os, importlib.util, json

results = {"tests_total": 0, "tests_passed": 0, "files_present": []}

for f in ["kv.py", "test_kv.py"]:
    if os.path.exists(f):
        results["files_present"].append(f)

try:
    spec = importlib.util.spec_from_file_location("kv", "kv.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    KVStore = mod.KVStore

    store = KVStore()

    # Test set/get
    results["tests_total"] += 1
    store.set("a", 1)
    if store.get("a") == 1:
        results["tests_passed"] += 1

    # Test exists
    results["tests_total"] += 1
    if store.exists("a") and not store.exists("z"):
        results["tests_passed"] += 1

    # Test delete
    results["tests_total"] += 1
    store.delete("a")
    if not store.exists("a"):
        results["tests_passed"] += 1

    # Test KeyError on missing
    results["tests_total"] += 1
    try:
        store.get("missing")
        pass  # should have raised
    except KeyError:
        results["tests_passed"] += 1

    # Test keys
    results["tests_total"] += 1
    store.set("x", 1)
    store.set("y", 2)
    if set(store.keys()) == {"x", "y"}:
        results["tests_passed"] += 1

    # Test len
    results["tests_total"] += 1
    if len(store) == 2:
        results["tests_passed"] += 1

except Exception as e:
    results["error"] = str(e)

print(json.dumps(results))
""",
)

# ---------------------------------------------------------------------------
# Task 3: Todo CLI (medium)
# ---------------------------------------------------------------------------

_TODO_CLI = BenchmarkTask(
    id="todo-cli",
    name="Todo CLI App",
    difficulty="medium",
    description=(
        "Build a command-line todo application with these files:\n"
        "1) todo.py — Todo class with title, done (bool), created_at (datetime). "
        "Include toggle() and to_dict() methods. Validate non-empty title.\n"
        "2) store.py — TodoStore class with add(title), remove(index), toggle(index), "
        "list(), get(index). Use 1-based indexing. Raise a custom TodoNotFoundError.\n"
        "3) main.py — CLI interface: python main.py add/list/toggle/remove/get/help.\n"
        "4) tests/test_store.py — At least 20 tests covering all methods and edge cases.\n"
        "5) README.md — Usage docs with examples.\n"
        "Discuss who does what, split the work, and build it."
    ),
    seed_files={
        "tests/__init__.py": "",
    },
    expected_files=["todo.py", "store.py", "main.py", "tests/test_store.py", "README.md"],
    max_ticks=15,
    tags=["python", "medium", "cli", "testing", "multi-file"],
    verification_script=r"""
import sys, os, importlib.util, json

results = {"tests_total": 0, "tests_passed": 0, "files_present": []}

for f in ["todo.py", "store.py", "main.py", "tests/test_store.py", "README.md"]:
    if os.path.exists(f):
        results["files_present"].append(f)

# Test Todo class
try:
    spec = importlib.util.spec_from_file_location("todo", "todo.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    Todo = mod.Todo

    results["tests_total"] += 1
    t = Todo("Test")
    if t.title == "Test" and t.done is False:
        results["tests_passed"] += 1

    results["tests_total"] += 1
    t.toggle()
    if t.done is True:
        results["tests_passed"] += 1

    results["tests_total"] += 1
    d = t.to_dict()
    if "title" in d and "done" in d:
        results["tests_passed"] += 1

    results["tests_total"] += 1
    try:
        Todo("")
    except (ValueError, Exception):
        results["tests_passed"] += 1

except Exception as e:
    results["todo_error"] = str(e)

# Test TodoStore
try:
    spec2 = importlib.util.spec_from_file_location("store", "store.py")
    mod2 = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(mod2)
    TodoStore = mod2.TodoStore

    store = TodoStore()

    results["tests_total"] += 1
    store.add("Alpha")
    if len(store) == 1:
        results["tests_passed"] += 1

    results["tests_total"] += 1
    store.add("Beta")
    items = store.list()
    if len(items) == 2:
        results["tests_passed"] += 1

    results["tests_total"] += 1
    item = store.get(1)
    if item.title == "Alpha":
        results["tests_passed"] += 1

    results["tests_total"] += 1
    store.toggle(1)
    if store.get(1).done is True:
        results["tests_passed"] += 1

    results["tests_total"] += 1
    removed = store.remove(1)
    if len(store) == 1:
        results["tests_passed"] += 1

    results["tests_total"] += 1
    try:
        store.get(99)
    except Exception:
        results["tests_passed"] += 1

except Exception as e:
    results["store_error"] = str(e)

# Check README has content
results["tests_total"] += 1
if os.path.exists("README.md") and os.path.getsize("README.md") > 50:
    results["tests_passed"] += 1

print(json.dumps(results))
""",
)

# ---------------------------------------------------------------------------
# Task 4: Calculator Library (medium)
# ---------------------------------------------------------------------------

_CALCULATOR = BenchmarkTask(
    id="calculator",
    name="Calculator Library",
    difficulty="medium",
    description=(
        "Build a Python calculator library that evaluates arithmetic expressions "
        "as strings. Support +, -, *, /, parentheses, and operator precedence.\n"
        "Files:\n"
        "1) tokenizer.py — tokenize(expr: str) -> list of tokens (numbers, operators, parens)\n"
        "2) parser.py — parse(tokens) -> AST (nested dicts or objects)\n"
        "3) evaluator.py — evaluate(expr: str) -> float (ties it all together)\n"
        "4) test_calculator.py — At least 15 tests: basic ops, precedence, parens, "
        "nested parens, division by zero, edge cases.\n"
        "Coordinate who implements what. The tokenizer, parser, and evaluator must "
        "work together correctly."
    ),
    seed_files={},
    expected_files=["tokenizer.py", "parser.py", "evaluator.py", "test_calculator.py"],
    max_ticks=15,
    tags=["python", "medium", "parsing", "multi-file", "coordination"],
    verification_script=r"""
import sys, os, importlib.util, json

results = {"tests_total": 0, "tests_passed": 0, "files_present": []}

for f in ["tokenizer.py", "parser.py", "evaluator.py", "test_calculator.py"]:
    if os.path.exists(f):
        results["files_present"].append(f)

try:
    spec = importlib.util.spec_from_file_location("evaluator", "evaluator.py")
    mod = importlib.util.module_from_spec(spec)
    # Add cwd to path so evaluator can import tokenizer/parser
    sys.path.insert(0, os.getcwd())
    spec.loader.exec_module(mod)
    evaluate = mod.evaluate

    test_cases = [
        ("2 + 3", 5.0),
        ("10 - 4", 6.0),
        ("3 * 4", 12.0),
        ("15 / 3", 5.0),
        ("2 + 3 * 4", 14.0),      # precedence
        ("(2 + 3) * 4", 20.0),    # parens
        ("10 / (2 + 3)", 2.0),    # parens with division
        ("((1 + 2) * 3)", 9.0),   # nested parens
        ("100", 100.0),            # single number
        ("3.5 + 1.5", 5.0),       # decimals
    ]

    for expr, expected in test_cases:
        results["tests_total"] += 1
        try:
            got = evaluate(expr)
            if abs(got - expected) < 0.001:
                results["tests_passed"] += 1
        except Exception:
            pass

    # Division by zero should raise
    results["tests_total"] += 1
    try:
        evaluate("1 / 0")
    except (ZeroDivisionError, Exception):
        results["tests_passed"] += 1

except Exception as e:
    results["error"] = str(e)
finally:
    if os.getcwd() in sys.path:
        sys.path.remove(os.getcwd())

print(json.dumps(results))
""",
)

# ---------------------------------------------------------------------------
# Task 5: Chat Room Server (hard)
# ---------------------------------------------------------------------------

_CHAT_SERVER = BenchmarkTask(
    id="chat-server",
    name="Chat Room Server",
    difficulty="hard",
    description=(
        "Build a multi-room chat system in Python with these files:\n"
        "1) models.py — User(nickname, room) and Room(name, users, messages) classes. "
        "Message has sender, content, timestamp.\n"
        "2) server.py — ChatServer class with: create_room(name), join_room(user, room), "
        "leave_room(user), send_message(user, content) -> broadcasts to room, "
        "get_messages(room, limit=50) -> list. Thread-safe with locks.\n"
        "3) commands.py — parse_command(input_str) -> (command, args). Commands: "
        "/join room, /leave, /rooms, /who, /nick name, /quit, and plain text = message.\n"
        "4) test_server.py — At least 20 tests covering room creation, join/leave, "
        "messaging, message history, multiple rooms, edge cases.\n"
        "5) README.md — Architecture overview, usage docs, design decisions.\n"
        "This requires careful coordination. Discuss architecture first, agree on "
        "interfaces between modules, then split implementation."
    ),
    seed_files={},
    expected_files=["models.py", "server.py", "commands.py", "test_server.py", "README.md"],
    max_ticks=25,
    tags=["python", "hard", "architecture", "multi-file", "threading", "coordination"],
    verification_script=r"""
import sys, os, importlib.util, json

results = {"tests_total": 0, "tests_passed": 0, "files_present": []}

for f in ["models.py", "server.py", "commands.py", "test_server.py", "README.md"]:
    if os.path.exists(f):
        results["files_present"].append(f)

sys.path.insert(0, os.getcwd())

# Test models
try:
    spec = importlib.util.spec_from_file_location("models", "models.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    results["tests_total"] += 1
    if hasattr(mod, "User") and hasattr(mod, "Room"):
        results["tests_passed"] += 1

    results["tests_total"] += 1
    if hasattr(mod, "Message") or hasattr(mod, "Room"):
        results["tests_passed"] += 1
except Exception as e:
    results["models_error"] = str(e)

# Test server
try:
    spec2 = importlib.util.spec_from_file_location("server", "server.py")
    mod2 = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(mod2)
    ChatServer = mod2.ChatServer

    srv = ChatServer()

    # Create room
    results["tests_total"] += 1
    srv.create_room("general")
    results["tests_passed"] += 1

    # Join room
    results["tests_total"] += 1
    try:
        srv.join_room("alice", "general")
        results["tests_passed"] += 1
    except Exception:
        pass

    # Send message
    results["tests_total"] += 1
    try:
        srv.send_message("alice", "hello")
        results["tests_passed"] += 1
    except Exception:
        pass

    # Get messages
    results["tests_total"] += 1
    try:
        msgs = srv.get_messages("general")
        if len(msgs) >= 1:
            results["tests_passed"] += 1
    except Exception:
        pass

    # Multiple rooms
    results["tests_total"] += 1
    try:
        srv.create_room("dev")
        srv.join_room("bob", "dev")
        srv.send_message("bob", "hi dev")
        dev_msgs = srv.get_messages("dev")
        gen_msgs = srv.get_messages("general")
        if len(dev_msgs) >= 1 and len(gen_msgs) >= 1:
            results["tests_passed"] += 1
    except Exception:
        pass

    # Leave room
    results["tests_total"] += 1
    try:
        srv.leave_room("alice")
        results["tests_passed"] += 1
    except Exception:
        pass

except Exception as e:
    results["server_error"] = str(e)

# Test commands
try:
    spec3 = importlib.util.spec_from_file_location("commands", "commands.py")
    mod3 = importlib.util.module_from_spec(spec3)
    spec3.loader.exec_module(mod3)
    parse_command = mod3.parse_command

    results["tests_total"] += 1
    cmd, args = parse_command("/join general")
    if cmd == "join":
        results["tests_passed"] += 1

    results["tests_total"] += 1
    cmd2, args2 = parse_command("hello everyone")
    if cmd2 == "message":
        results["tests_passed"] += 1

except Exception as e:
    results["commands_error"] = str(e)

# README
results["tests_total"] += 1
if os.path.exists("README.md") and os.path.getsize("README.md") > 100:
    results["tests_passed"] += 1

if os.getcwd() in sys.path:
    sys.path.remove(os.getcwd())

print(json.dumps(results))
""",
)


# ---------------------------------------------------------------------------
# Task 6: City Grid (medium) — Paper 6 benchmark
# ---------------------------------------------------------------------------

_CITY_GRID = BenchmarkTask(
    id="city-grid",
    name="City Grid Design",
    difficulty="medium",
    description=(
        "Design a city on a 10x10 grid. You are city planners working together.\n\n"
        "## Grid Format\n"
        "Write the result to `city.txt` — a 10x10 grid where each cell is one character,\n"
        "separated by spaces, one row per line.\n\n"
        "## Building Types\n"
        "  R = Residential (houses, apartments)\n"
        "  C = Commercial  (shops, offices, restaurants)\n"
        "  I = Industrial  (factories, warehouses)\n"
        "  P = Park        (green space, recreation)\n"
        "  . = Road        (connects everything — buildings need road access)\n"
        "  H = Hospital    (healthcare)\n"
        "  S = School      (education)\n"
        "  _ = Empty       (unused land)\n\n"
        "## Design Goals\n"
        "Build a high-quality city that scores well on ALL of these:\n"
        "1. COVERAGE — use the land (empty cells score zero)\n"
        "2. ACCESSIBILITY — every building should be adjacent to a road\n"
        "3. ZONING — good neighbours matter! Residential near parks/schools (+), "
        "residential near industrial (-), hospitals near roads (+), etc.\n"
        "4. DIVERSITY — mix of building types, not just one kind\n"
        "5. CONNECTIVITY — roads should form a connected network, minimal dead-ends\n\n"
        "## Rules\n"
        "- Grid is exactly 10 rows x 10 columns\n"
        "- Each cell is exactly one of: R C I P . H S _\n"
        "- Roads connect the city — buildings without adjacent roads are inaccessible\n"
        "- Quality is scored 0-100 on each dimension; aggregate = harmonic mean\n\n"
        "## Example (3x3 — yours is 10x10)\n"
        "```\n"
        ". . .\n"
        "R P C\n"
        ". H .\n"
        "```\n"
        "This tiny city has roads on top and bottom, with residential, park, commercial,\n"
        "and hospital all adjacent to roads. Good zoning: residential next to park.\n\n"
        "## Output\n"
        "Write your city grid to `city.txt`. Discuss strategy with your team first —\n"
        "where to put roads, how to zone districts, how to balance coverage and quality.\n"
        "The city should reflect your team's collective design decisions."
    ),
    seed_files={},
    expected_files=["city.txt"],
    max_ticks=15,
    tags=["design", "medium", "coordination", "spatial", "paper-6"],
    verification_script=r"""
import sys, os, json

results = {"tests_total": 0, "tests_passed": 0, "files_present": [], "scores": None}

# Check file exists
if os.path.exists("city.txt"):
    results["files_present"].append("city.txt")

results["tests_total"] += 1
if not os.path.exists("city.txt"):
    results["error"] = "city.txt not found"
    print(json.dumps(results))
    sys.exit(0)

# Read and parse the grid
try:
    text = open("city.txt").read()

    # Try to import agentciv scoring (installed via pip)
    try:
        from agentciv.benchmark.city_grid import CityGrid
        from agentciv.benchmark.city_scorer import score_city
    except ImportError:
        # Fallback: add parent paths
        for p in ["/Users/ekramalam/agentciv-engine"]:
            if p not in sys.path:
                sys.path.insert(0, p)
        from agentciv.benchmark.city_grid import CityGrid
        from agentciv.benchmark.city_scorer import score_city

    grid = CityGrid.from_string(text)
    results["tests_passed"] += 1  # Valid grid parsed

    # Score it
    scores = score_city(grid)
    results["scores"] = scores.to_dict()

    # Each dimension above 20 counts as a "test passed"
    for dim_name, dim_val in [
        ("coverage", scores.coverage),
        ("accessibility", scores.accessibility),
        ("zoning", scores.zoning),
        ("diversity", scores.diversity),
        ("connectivity", scores.connectivity),
    ]:
        results["tests_total"] += 1
        if dim_val >= 20.0:
            results["tests_passed"] += 1

    # Aggregate above 30 = bonus test
    results["tests_total"] += 1
    if scores.aggregate >= 30.0:
        results["tests_passed"] += 1

except Exception as e:
    results["error"] = str(e)

print(json.dumps(results))
""",
)


# ---------------------------------------------------------------------------
# Task Bank Registry
# ---------------------------------------------------------------------------

TASK_BANK: dict[str, BenchmarkTask] = {
    t.id: t for t in [_FIZZBUZZ, _KV_STORE, _TODO_CLI, _CALCULATOR, _CHAT_SERVER, _CITY_GRID]
}


def get_task(task_id: str) -> BenchmarkTask:
    """Get a task by ID. Raises KeyError if not found."""
    return TASK_BANK[task_id]


def get_all_tasks() -> list[BenchmarkTask]:
    """Get all tasks in difficulty order."""
    order = {"simple": 0, "medium": 1, "hard": 2}
    return sorted(TASK_BANK.values(), key=lambda t: (order.get(t.difficulty, 9), t.id))


def get_tasks_by_difficulty(difficulty: str) -> list[BenchmarkTask]:
    """Get tasks filtered by difficulty level."""
    return [t for t in get_all_tasks() if t.difficulty == difficulty]
