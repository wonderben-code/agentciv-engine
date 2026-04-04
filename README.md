# AgentCiv Engine

**Spawn a team of AI agents. Choose how they organise. Watch them build.**

AgentCiv Engine treats organisational arrangement as a first-class design parameter for multi-agent AI systems. Instead of hard-coding how agents coordinate, you choose from 13 team structures — or let the agents design their own.

```bash
pip install -e .
agentciv setup
# That's it. Open Claude Code and say: "Use agentciv to build a REST API"
```

## Why this exists

Every multi-agent framework hard-codes a single coordination strategy. AgentCiv asks: *what if the organisational structure itself was the variable?*

The same task solved by a **hierarchical** team (top-down, assigned roles, chain of command) produces fundamentally different code than a **meritocratic** team (earned influence, mandatory review, reputation-based authority) or a **swarm** (no communication, stigmergic coordination, like ants).

13 team structures. 9 organisational dimensions. Every combination produces a different society of agents working on your code.

## Quick start

```bash
# Install
git clone https://github.com/wonderben-code/agentciv-engine.git
cd agentciv-engine
pip install -e .

# Set up for your project
cd /path/to/your/project
agentciv setup
```

Setup configures Claude Code (or Cursor) with AgentCiv's MCP server and writes a knowledge file so your AI assistant understands all 13 team structures. Then just talk naturally:

> "Use agentciv to build a REST API with a meritocratic team"
>
> "Set up a pair-programming duo for this bug"
>
> "Use --org auto and let the agents figure it out"

### API mode (for researchers and power users)

```bash
export ANTHROPIC_API_KEY="sk-ant-..."

# Single run
agentciv solve --task "Build a REST API" --org collaborative --agents 4

# Compare team structures
agentciv experiment --task "Build a CLI tool" --orgs collaborative,meritocratic,auto

# See all options
agentciv info
```

## 13 team structures

| Preset | How agents work |
|--------|----------------|
| **collaborative** | Flat, open, emergent roles. Everyone sees everything. The default. |
| **competitive** | Agents race independently. Best solution wins. No collaboration. |
| **meritocratic** | Influence earned through quality. Mandatory peer review. Reputation builds. |
| **hierarchical** | Top-down. Lead assigns tasks, coordinates, reviews. Chain of command. |
| **startup** | Move fast. Flat, minimal process, no review gates. Speed over polish. |
| **pair-programming** | Two agents, tight loop. One writes, one reviews. Roles rotate. |
| **open-source** | Distributed authority, earned reputation, transparent everything. Maintainers emerge. |
| **military** | Strict chain of command. Need-to-know information. No autonomous decisions. |
| **research-lab** | Divergent exploration. Agents pursue different approaches, then converge. |
| **swarm** | No communication. Agents observe file changes and adapt. Like ants. |
| **hackathon** | Maximum speed, maximum parallelism. Broadcast-heavy. Ship fast. |
| **code-review** | Quality over speed. Every change reviewed by 2+ agents. |
| **auto** | **The crown jewel.** See below. |

## The crown jewel: `--org auto`

Set the goal. The agents do the rest.

In auto mode, agents self-organise: they propose changes to team structure, vote on them, and restructure in real time. Authority, communication patterns, role assignment, decision-making — all evolve based on what the agents discover works.

You define the task. They design the team.

```bash
agentciv solve --task "Build a REST API" --org auto --agents 6
```

Every N ticks, agents enter a meta-tick: a restructuring discussion where any agent can propose changes to any of the 9 organisational dimensions. The team votes, and the winning proposal reshapes how they work together — live, mid-task.

Auto mode also learns. Every run's outcome is saved, and future auto runs consult history for similar tasks. The more you use it, the smarter it gets.

## 9 organisational dimensions

Every preset configures these. Any can be overridden individually.

| Dimension | Spectrum |
|-----------|----------|
| **Authority** | hierarchy · flat · distributed · rotating · consensus · anarchic |
| **Communication** | hub-spoke · mesh · clustered · broadcast · whisper |
| **Roles** | assigned · emergent · rotating · fixed · fluid |
| **Decisions** | top-down · consensus · majority · meritocratic · autonomous |
| **Incentives** | collaborative · competitive · reputation · market |
| **Information** | transparent · need-to-know · curated · filtered |
| **Conflict** | authority · negotiated · voted · adjudicated |
| **Groups** | imposed · self-selected · task-based · persistent · temporary |
| **Adaptation** | static · evolving · cyclical · real-time |

Override any dimension on the fly:

```bash
agentciv solve \
  --task "Build auth module" \
  --org collaborative \
  --override authority=hierarchy \
  --override information=need-to-know
```

Community-expandable: add your own dimensions, values, and presets by dropping a YAML file in `presets/`.

## Two modes

| | Max Plan | API |
|--|---------|-----|
| **How** | Inside Claude Code / Cursor via MCP | CLI: `agentciv solve` |
| **Cost** | Free (uses your existing subscription) | Pay per token (your API key) |
| **Who drives** | Your AI assistant drives agent cognition | Engine makes its own LLM calls |
| **Best for** | Everyday use | Research, experiments, test tasks |
| **Setup** | `agentciv setup` | `export ANTHROPIC_API_KEY=...` |

## Features

- **Git branch-per-agent** — each agent works in an isolated git worktree. Auto-merge at tick end. Conflict detection and reporting.
- **Gardener mode** — intervene mid-run. Broadcast messages, redirect focus, force restructuring discussions, adjust parameters live. `--gardener`
- **Experiments** — run the same task under multiple team structures and compare. `agentciv experiment --orgs collaborative,meritocratic,auto`
- **Specialisation** — agents develop skills through practice. A testing-focused agent gets better at testing.
- **Relationships** — collaboration history and trust tracked between agents across ticks.
- **Attention map** — shared awareness of who's working on what, preventing duplicate work.
- **Chronicle** — every run produces structured data: per-agent contributions, communication patterns, git stats, org dynamics, full timeline.
- **Learning** — run outcomes persist to history. Auto mode consults past runs for similar tasks. `agentciv history`
- **Peer review** — optional mandatory review before merge. Configurable per-preset.
- **MCP server** — full tool suite for AI assistants: solve, experiment, configure, intervene, monitor.

## Real output

This REST API was built by 2 agents in collaborative mode, 3 ticks:

```
agentciv solve \
  --task "Build a REST API with /hello and /status endpoints" \
  --org collaborative --agents 2 --max-ticks 3
```

**Tick 1:** Both agents independently claimed the task. Atlas wrote `server.py` (full API). Nova wrote `test_server.py` (4 tests). Each in isolated git branches.

**Tick 2:** Atlas's branch merged first. Nova hit a merge conflict. Atlas messaged Nova explaining the architecture, then refactored the entry point.

**Tick 3:** Atlas wrote a self-contained test runner. All 4 tests pass.

```
$ python3 run_tests.py
test_404_returns_json ... ok
test_hello_endpoint ... ok
test_hello_has_timestamp ... ok
test_status_endpoint ... ok

Ran 4 tests in 0.002s — OK
```

See [`examples/`](examples/) for full output including auto mode runs.

## CLI reference

```
agentciv solve        Spawn an agent team to solve a task
agentciv experiment   Compare team structures on the same task
agentciv info         Show all presets, dimensions, and features
agentciv history      View learning data from past runs
agentciv setup        Configure AgentCiv for your project
agentciv test-tasks   Run built-in test tasks across org presets
agentciv mcp          Start the MCP server (for Claude Code / Cursor)
```

## How it works

```
You define the task
        ↓
Engine spawns N agents with tools (read, write, run, communicate, claim)
        ↓
Each agent gets a system prompt shaped by the organisational config
        ↓
Per tick: agents act → git merge → chronicle → repeat
        ↓
Auto mode: every N ticks, agents discuss + vote on restructuring
        ↓
Output: working code + structured run data
```

The organisational structure isn't decoration — it fundamentally shapes agent behaviour. Authority determines who can override whom. Communication patterns control who can talk to whom. Information sharing decides what each agent can see. These aren't suggestions — they're enforced constraints that produce genuinely different emergent behaviour.

## Extending

**Add a preset:** Drop a YAML file in `presets/`. It's immediately available as `--org your-preset`.

**Add a dimension:** Add values to `KNOWN_DIMENSIONS` in `org/config.py` and reference them in `org/enforcer.py`. Existing presets keep working.

**Add a mechanism:** The engine is designed for community extension. Custom dimensions in YAML flow through to agent prompts automatically.

## Architecture

```
agentciv/
├── core/           Engine, agents, tick loop, tool execution
├── org/            Dimensions, presets, enforcement, auto-org
├── mcp/            MCP server, session management, step orchestration
├── learning/       Run history, insights, quality scoring
├── benchmark/      Task bank, verification, metrics
├── chronicle.py    Structured observer — every run produces data
├── gardener.py     Mid-run intervention system
├── experiment.py   Multi-org comparison runner
└── discovery.py    Contextual feature tips
```

~11,500 lines of Python across 40 files.

## License

MIT — see [LICENSE](LICENSE).

## Author

Mark E. Mala
