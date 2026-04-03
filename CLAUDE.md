# AgentCiv Engine

Organisational arrangement as a first-class design parameter for multi-agent AI systems.

## What it does

Spawns communities of 2-20 AI agents under configurable organisational structures. Agents get tools (read/write files, run commands, communicate, claim tasks) and work concurrently in the project directory. The organisational structure shapes how they coordinate, communicate, make decisions, and resolve conflicts.

## Two modes

- **Max Plan Mode** — `agentciv_orchestrate_start()`. The MCP client drives agent cognition. No API key needed, no cost beyond existing subscription.
- **API Mode** — `agentciv_solve()` or `agentciv solve` CLI. The engine makes its own LLM calls via `ANTHROPIC_API_KEY`. User pays per token.

Never auto-select API mode. Confirm with the user which mode they want.

## 13 organisational presets

| Preset | What it is |
|--------|-----------|
| `collaborative` | Flat authority, mesh communication, emergent roles, shared reward. Everyone sees everything. Default. |
| `competitive` | Agents race independently. Each works the full problem in isolation. Best solution wins. |
| `meritocratic` | Influence earned through demonstrated quality. Mandatory peer review. Reputation builds over time. |
| `auto` | Agents design their own organisational structure through proposals and votes. Restructures live during the run. |
| `hierarchical` | Top-down. First agent leads, assigns tasks, coordinates. Communication flows through the lead. |
| `startup` | Move fast. Flat, rapid iteration, minimal process. No review gates. Speed over polish. |
| `pair-programming` | Two agents, tight feedback loop. One writes, one reviews. Roles rotate. Designed for 2 agents. |
| `open-source` | Distributed authority, earned reputation, mandatory review. Maintainers emerge through quality contributions. |
| `military` | Strict chain of command. Need-to-know information. No freelancing, no autonomous decisions. |
| `research-lab` | Exploratory. Agents pursue different approaches in parallel, then converge to share findings. |
| `swarm` | Stigmergic coordination. No explicit communication. Agents observe file changes and adapt. Like ants. |
| `hackathon` | Maximum speed, maximum parallelism. Broadcast-heavy. No review gates. Ship fast. |
| `code-review` | Quality over speed. Every change reviewed by 2+ agents. Meritocratic review authority. |

## 9 organisational dimensions

Each preset configures these dimensions. Any can be overridden individually.

| Dimension | Values |
|-----------|--------|
| `authority` | hierarchy, flat, distributed, rotating, consensus, anarchic |
| `communication` | hub-spoke, mesh, clustered, broadcast, whisper |
| `roles` | assigned, emergent, rotating, fixed, fluid |
| `decisions` | top-down, consensus, majority, meritocratic, autonomous |
| `incentives` | collaborative, competitive, reputation, market |
| `information` | transparent, need-to-know, curated, filtered |
| `conflict` | authority, negotiated, voted, adjudicated |
| `groups` | imposed, self-selected, task-based, persistent, temporary |
| `adaptation` | static, evolving, cyclical, real-time |

## Features

- **Specialisation** — agents develop skills through practice
- **Relationships** — collaboration history and trust tracked between agents
- **Attention map** — shared view of who's working on what
- **Git branches** — branch-per-agent with auto-merge
- **Peer review** — optional mandatory review before merge
- **Meta-ticks** — periodic org restructuring discussions (auto mode)
- **Gardener mode** — intervene mid-run: broadcast messages, redirect focus, force meta-ticks, adjust parameters
- **Experiments** — run the same task under multiple org configs and compare results
- **Learning** — every run persists outcomes; `--org auto` consults history for similar past tasks

## Defaults

Only `task` is required. Everything else has sensible defaults:
- `org`: collaborative
- `agents`: 4
- `max_ticks`: 50

## CLI commands

```
agentciv solve --task "..." --org collaborative
agentciv experiment --task "..." --orgs collaborative,meritocratic,auto
agentciv info
agentciv history
agentciv setup
```
