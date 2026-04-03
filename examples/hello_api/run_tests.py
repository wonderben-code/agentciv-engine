#!/usr/bin/env python3
"""
run_tests.py — self-contained test runner.

Starts the REST API server in a background daemon thread on port 8080,
waits for it to be ready, runs the full unittest suite from test_server.py,
then exits.  No external dependencies required.
"""

import sys
import threading
import time
import unittest
import urllib.request
import urllib.error

# ── Start the server in a background thread ───────────────────────────────────
from server import run as _run_server

_server_thread = threading.Thread(
    target=_run_server,
    kwargs={"host": "localhost", "port": 8080},
    daemon=True,   # killed automatically when the main thread exits
)
_server_thread.start()

# ── Wait until the server is accepting connections (max 5 s) ─────────────────
_deadline = time.time() + 5.0
while time.time() < _deadline:
    try:
        urllib.request.urlopen("http://localhost:8080/status", timeout=1)
        break   # server is up
    except (urllib.error.URLError, ConnectionRefusedError):
        time.sleep(0.1)
else:
    print("ERROR: server did not start within 5 seconds", file=sys.stderr)
    sys.exit(1)

print("Server is up — running tests...\n")

# ── Discover and run tests ────────────────────────────────────────────────────
loader = unittest.TestLoader()
suite  = loader.loadTestsFromName("test_server")   # imports test_server.py

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

sys.exit(0 if result.wasSuccessful() else 1)
