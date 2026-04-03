# Hello API — First Live Engine Run

This code was **generated entirely by AI agents** using the AgentCiv Engine.

## What happened

```
agentciv solve \
  --task "Build a REST API with /hello and /status endpoints using Python http.server" \
  --org collaborative \
  --agents 2 \
  --max-ticks 3
```

Two agents (Atlas and Nova) were given a bare skeleton (`main.py` with just a print statement)
and 3 ticks to build a REST API. Here's what unfolded:

**Tick 1:** Both agents independently claimed the task and started coding. Each worked
in an isolated git worktree (branch-per-agent). Atlas wrote `server.py` with the full
API implementation. Nova wrote `test_server.py` with 4 unit tests.

**Tick 2:** Atlas's branch merged first. Nova hit a merge conflict on `api_server.py`
(both had written it). Atlas sent Nova a direct message explaining the architecture,
then refactored `api_server.py` as a clean re-export entry point.

**Tick 3:** Atlas wrote `run_tests.py` — a self-contained test runner that starts the
server in a background thread and runs the full test suite.

## Result

4 tests, all passing:

```
$ python3 run_tests.py
test_404_returns_json ... ok
test_hello_endpoint ... ok
test_hello_has_timestamp ... ok
test_status_endpoint ... ok

Ran 4 tests in 0.002s — OK
```

## Files produced

| File | Author | Description |
|---|---|---|
| `server.py` | Atlas | Full REST API — routing, JSON responses, error handling, uptime tracking |
| `test_server.py` | Nova | 4 unit tests covering all endpoints + 404 handling |
| `api_server.py` | Atlas | Re-export entry point (adapted after merge conflict) |
| `run_tests.py` | Atlas | Self-contained test runner with server startup |
| `main.py` | Atlas | Updated to import from server module |

## What this demonstrates

- **Collaborative self-organisation:** No coordinator assigned tasks — agents chose what to do
- **Git branch-per-agent:** Each agent worked in isolation, auto-merged at tick end
- **Merge conflict handling:** Detected, reported to the agent, agent adapted
- **Agent communication:** Atlas messaged Nova to coordinate after the conflict
- **Working output:** The code runs, the tests pass, the API serves requests

## Configuration used

```yaml
organisation:
  authority: flat
  communication: mesh
  roles: emergent
  decisions: consensus
  incentives: collaborative
  information: transparent
  conflict: negotiated
  groups: self-selected
  adaptation: evolving
```

*3 April 2026 — First live run of the AgentCiv Engine.*
