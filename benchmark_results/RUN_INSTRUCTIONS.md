# Benchmark Run Instructions

Paste the prompt below into a Claude Code session launched from this directory.
The AgentCiv MCP server will auto-connect via `.mcp.json`.

## Quick Pilot (start here)

```
Run the AgentCiv internal benchmark: fizzbuzz task, collaborative preset, 4 agents.
Use agentciv_benchmark_start to set up the task, then drive all agents through
their ticks using agentciv_orchestrate_act and agentciv_orchestrate_tick.
When the run finishes, call agentciv_benchmark_verify to score and save results.
```

## After pilot works, scale up

```
Run the full internal benchmark suite. For each combination of:
- Tasks: fizzbuzz, kv-store, todo-cli, calculator, chat-server
- Presets: collaborative, competitive, meritocratic, auto, hierarchical
- Plus single-agent baseline (agents=1) for each task

Use agentciv_benchmark_start for each (task, preset) combo. Drive agents through
all ticks. Call agentciv_benchmark_verify after each run. Save everything to
benchmark_results/internal. Do one run at a time, report results as you go.
```

## Results location

All per-run JSON files save to: `benchmark_results/internal/runs/`
Each file contains: metrics, analysis (network + temporal), verification, full chronicle.

## If you need to resume

Results auto-save after each run. If the session ends, just start a new one
and pick up where you left off. Check what's already been run:
```
ls benchmark_results/internal/runs/
```
