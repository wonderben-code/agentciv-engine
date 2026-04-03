"""
run_tests.py — Pytest-free test runner for the Todo app.

Provides a minimal pytest compatibility shim so that tests/test_store.py
(which uses `pytest.raises`) can be executed with plain Python 3:

    python3 run_tests.py

No external dependencies required.
"""

import sys
import os
import traceback
import types
import importlib
import importlib.util          # ← must be imported explicitly
from datetime import datetime

# ---------------------------------------------------------------------------
# 0.  Make sure the project root is on sys.path so todo/store are importable
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ---------------------------------------------------------------------------
# 1.  Minimal pytest compatibility shim
#     Installs a fake `pytest` module that supports pytest.raises()
# ---------------------------------------------------------------------------

class _RaisesContext:
    """Context manager returned by pytest.raises(exc_type)."""

    def __init__(self, expected_exception):
        self.expected_exception = expected_exception
        self.value = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            raise AssertionError(
                f"Expected {self.expected_exception.__name__} to be raised, "
                "but no exception was raised."
            )
        if not issubclass(exc_type, self.expected_exception):
            # Let unexpected exceptions propagate unchanged
            return False
        self.value = exc_val
        return True  # suppress the expected exception


def _raises(expected_exception):
    """Drop-in replacement for pytest.raises()."""
    return _RaisesContext(expected_exception)


# Build and register the fake pytest module
_pytest_shim = types.ModuleType("pytest")
_pytest_shim.raises = _raises
sys.modules.setdefault("pytest", _pytest_shim)

# ---------------------------------------------------------------------------
# 2.  ANSI colour helpers (auto-disabled on non-TTY)
# ---------------------------------------------------------------------------
_USE_COLOUR = sys.stdout.isatty()

def _green(s):  return f"\033[32m{s}\033[0m" if _USE_COLOUR else s
def _red(s):    return f"\033[31m{s}\033[0m" if _USE_COLOUR else s
def _yellow(s): return f"\033[33m{s}\033[0m" if _USE_COLOUR else s
def _bold(s):   return f"\033[1m{s}\033[0m"  if _USE_COLOUR else s
def _dim(s):    return f"\033[2m{s}\033[0m"  if _USE_COLOUR else s

# ---------------------------------------------------------------------------
# 3.  Test discovery helpers
# ---------------------------------------------------------------------------

def _collect_test_classes(module):
    """Yield (class_name, class) for every class whose name starts with Test."""
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and name.startswith("Test"):
            yield name, obj


def _collect_test_methods(cls):
    """Yield method names that start with 'test_', sorted by line number."""
    return sorted(
        [name for name in dir(cls) if name.startswith("test_")],
        key=lambda n: getattr(getattr(cls, n), "__code__", None) and
                      getattr(cls, n).__code__.co_firstlineno or 0,
    )

# ---------------------------------------------------------------------------
# 4.  Module runner
# ---------------------------------------------------------------------------

def run_module(module_path: str) -> tuple:
    """
    Import and run all Test* classes from *module_path*.

    Returns
    -------
    (passed, failed, errors, failures)
        failures is a list of (test_id, traceback_str) pairs.
    """
    rel = os.path.relpath(module_path, PROJECT_ROOT)
    module_name = rel.replace(os.sep, ".").removesuffix(".py")

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    passed = failed = errors = 0
    failures = []

    for class_name, cls in _collect_test_classes(module):
        method_names = _collect_test_methods(cls)
        for method_name in method_names:
            test_id = f"{class_name}::{method_name}"
            instance = cls()
            method = getattr(instance, method_name)

            setup    = getattr(instance, "setUp",    None)
            teardown = getattr(instance, "tearDown", None)

            try:
                if setup:
                    setup()
                method()
                if teardown:
                    teardown()
                print(f"  {_green('PASS')}  {_dim(test_id)}")
                passed += 1
            except AssertionError:
                tb = traceback.format_exc()
                print(f"  {_red('FAIL')}  {test_id}")
                failures.append((test_id, tb))
                failed += 1
            except Exception:
                tb = traceback.format_exc()
                print(f"  {_red('ERR ')}  {test_id}")
                failures.append((test_id, tb))
                errors += 1

    return passed, failed, errors, failures

# ---------------------------------------------------------------------------
# 5.  Entry point
# ---------------------------------------------------------------------------

def main():
    test_file = os.path.join(PROJECT_ROOT, "tests", "test_store.py")

    print(_bold("=" * 60))
    print(_bold("  Todo App — Test Suite"))
    print(_bold("=" * 60))
    print(f"  File : {os.path.relpath(test_file)}")
    print(f"  Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    passed, failed, errors, failures = run_module(test_file)
    total = passed + failed + errors

    if failures:
        print()
        print(_bold(_red("─── Failures / Errors " + "─" * 38)))
        for test_id, tb in failures:
            print(f"\n{_red('FAILED')} {test_id}")
            for line in tb.splitlines():
                print(f"    {line}")

    print()
    print(_bold("=" * 60))
    summary_parts = [f"{passed} passed"]
    if failed:
        summary_parts.append(_red(f"{failed} failed"))
    if errors:
        summary_parts.append(_red(f"{errors} errors"))
    status_icon = _green("✓ OK") if (failed + errors) == 0 else _red("✗ FAILED")
    print(f"  {status_icon}  —  {', '.join(summary_parts)}  ({total} total)")
    print(_bold("=" * 60))

    sys.exit(0 if (failed + errors) == 0 else 1)


if __name__ == "__main__":
    main()
