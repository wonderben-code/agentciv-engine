"""CLI entry point — agentciv solve --task "..." --org collaborative

This is how users interact with the engine from the terminal.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from pathlib import Path

from .core.agent import Agent
from .core.attention import AttentionMap
from .core.engine import Engine
from .core.event_bus import EventBus
from .core.types import AgentIdentity, AgentState, Event, EventType
from .gardener import Gardener
from .llm.client import create_client
from .org.config import EngineConfig
from .org.enforcer import OrgEnforcer
from .workspace.executor import WorkspaceExecutor
from .workspace.workspace import Workspace

# Agent names — they earn their identity through work, not assignment
AGENT_NAMES = [
    "Atlas", "Nova", "Sage", "Flux", "Echo",
    "Drift", "Pulse", "Cinder", "Wren", "Quill",
    "Ember", "Loom", "Haze", "Strider", "Crux",
    "Rune", "Fern", "Glyph", "Shard", "Tide",
]


def build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentciv",
        description="AgentCiv Engine — organisational arrangement as a design parameter",
    )
    sub = parser.add_subparsers(dest="command")

    # --- solve ---
    solve = sub.add_parser("solve", help="Spawn a community to solve a task")
    solve.add_argument("--task", "-t", required=True, help="What the community should build/solve")
    solve.add_argument("--org", "-o", default="collaborative", help="Organisational preset (collaborative, competitive, meritocratic, auto)")
    solve.add_argument("--agents", "-a", type=int, default=4, help="Number of agents")
    solve.add_argument("--model", "-m", default="claude-sonnet-4-6", help="LLM model")
    solve.add_argument("--dir", "-d", default=".", help="Project directory")
    solve.add_argument("--config", "-c", help="YAML config file (overrides other flags)")
    solve.add_argument("--max-ticks", type=int, default=50, help="Maximum ticks")
    solve.add_argument("--verbose", "-v", action="store_true", help="Show agent reasoning")
    solve.add_argument("--gardener", "-g", action="store_true", help="Enable mid-run human intervention")

    # --- experiment ---
    exp = sub.add_parser("experiment", help="Run same task under multiple org configs and compare")
    exp.add_argument("--task", "-t", required=True, help="What the community should build/solve")
    exp.add_argument("--orgs", required=True, help="Comma-separated org presets to compare")
    exp.add_argument("--runs", type=int, default=1, help="Runs per org config (for statistical validity)")
    exp.add_argument("--agents", "-a", type=int, default=4, help="Number of agents")
    exp.add_argument("--model", "-m", default="claude-sonnet-4-6", help="LLM model")
    exp.add_argument("--dir", "-d", default=".", help="Source project directory")
    exp.add_argument("--max-ticks", type=int, default=30, help="Maximum ticks per run")
    exp.add_argument("--output", "-O", help="Save JSON results to file")
    exp.add_argument("--verbose", "-v", action="store_true", help="Show details")

    # --- benchmark ---
    bench = sub.add_parser("benchmark", help="Run standardised tasks across all presets with statistical analysis")
    bench.add_argument("--tasks", default="all", help="Comma-separated task IDs, difficulty level (simple/medium/hard), or 'all'")
    bench.add_argument("--presets", default="all", help="Comma-separated preset names or 'all'")
    bench.add_argument("--runs", type=int, default=3, help="Runs per (task, preset) combination (default: 3)")
    bench.add_argument("--agents", "-a", type=int, default=4, help="Number of agents (default: 4)")
    bench.add_argument("--model", "-m", default="claude-sonnet-4-6", help="LLM model")
    bench.add_argument("--max-ticks", type=int, default=None, help="Override per-task tick limits")
    bench.add_argument("--output", "-O", help="Save JSON results to file")
    bench.add_argument("--dry-run", action="store_true", help="Print execution plan without running")
    bench.add_argument("--mock", action="store_true", help="Use mock LLM (no API calls, for testing the pipeline)")
    bench.add_argument("--verbose", "-v", action="store_true", help="Show per-run details")
    bench.add_argument("--list-tasks", action="store_true", help="List available benchmark tasks and exit")

    # --- info ---
    sub.add_parser("info", help="Show available presets and dimensions")

    # --- mcp ---
    sub.add_parser("mcp", help="Start the MCP server (for Claude Code, Cursor, etc.)")

    return parser


def print_event(event: Event, verbose: bool = False) -> None:
    """Pretty-print an event to the terminal."""
    tick = f"[tick {event.tick:3d}]"
    agent = f" {event.agent_id}" if event.agent_id else ""

    match event.type:
        case EventType.ENGINE_STARTED:
            agents = event.data.get("agents", "?")
            org = event.data.get("config", "?")
            print(f"\n  AgentCiv Engine")
            print(f"  {agents} agents | org: {org}")
            print(f"  {'─' * 40}\n")

        case EventType.TICK_START:
            meta = " [META-TICK]" if event.data.get("is_meta_tick") else ""
            print(f"  {tick} ────────────────────{meta}")

        case EventType.TICK_END:
            actions = event.data.get("actions", 0)
            print(f"  {tick} {actions} actions taken\n")

        case EventType.FILE_CREATED:
            f = event.data.get("file", "?")
            print(f"  {tick}{agent} created {f}")

        case EventType.FILE_MODIFIED:
            f = event.data.get("file", "?")
            print(f"  {tick}{agent} modified {f}")

        case EventType.MESSAGE_SENT:
            targets = event.data.get("targets", [])
            preview = event.data.get("content_preview", "")
            print(f"  {tick}{agent} → {', '.join(targets)}: {preview}")

        case EventType.BROADCAST_SENT:
            preview = event.data.get("content_preview", "")
            print(f"  {tick}{agent} → all: {preview}")

        case EventType.TASK_CLAIMED:
            preview = event.data.get("content_preview", "")
            print(f"  {tick}{agent} claimed: {preview}")

        case EventType.TESTS_PASSED:
            print(f"  {tick} ✓ tests passing")

        case EventType.TESTS_FAILED:
            print(f"  {tick} ✗ tests failing")

        case EventType.BUILD_SUCCEEDED:
            print(f"  {tick} ✓ build passing")

        case EventType.BUILD_FAILED:
            print(f"  {tick} ✗ build failing")

        case EventType.BRANCH_MERGED:
            count = event.data.get("count", 0)
            print(f"  {tick}{agent} merged ({count} files)")

        case EventType.MERGE_CONFLICT:
            conflicts = event.data.get("conflicts", [])
            print(f"  {tick}{agent} ✗ MERGE CONFLICT: {', '.join(conflicts)}")

        case EventType.RESTRUCTURE_PROPOSED:
            preview = event.data.get("content_preview", "")
            print(f"  {tick}{agent} proposes restructure: {preview}")

        case EventType.RESTRUCTURE_ADOPTED:
            dim = event.data.get("dimension", "?")
            old = event.data.get("old_value", "?")
            new = event.data.get("new_value", "?")
            yes = event.data.get("yes_votes", 0)
            no = event.data.get("no_votes", 0)
            print(f"  {tick} ★ RESTRUCTURED: {dim} '{old}' → '{new}' ({yes}-{no})")

        case EventType.ENGINE_STOPPED:
            print(f"\n  Engine stopped at tick {event.tick}")
            print(f"  {'─' * 40}\n")

        case _:
            if verbose:
                print(f"  {tick}{agent} {event.type.name}")


async def run_solve(args: argparse.Namespace) -> None:
    """Execute the solve command."""
    # Load config
    if args.config:
        config = EngineConfig.from_yaml(args.config)
    else:
        config = EngineConfig.from_preset(args.org)

    # Override with CLI flags
    config.task = args.task
    config.project_dir = args.dir
    config.agent_count = args.agents
    config.model = args.model
    config.max_ticks = args.max_ticks

    # Set up workspace
    workspace = Workspace(
        project_dir=Path(config.project_dir).resolve(),
        task_description=config.task,
    )
    workspace.scan()
    print(f"  Scanned project: {len(workspace.files)} files\n")

    # Set up event bus with CLI printer
    event_bus = EventBus()
    event_bus.subscribe(None, lambda e: print_event(e, verbose=args.verbose))

    # Create attention map
    attention = AttentionMap()

    # Create agents (with per-agent model overrides from config.models)
    agents: list[Agent] = []
    for i in range(config.agent_count):
        name = AGENT_NAMES[i % len(AGENT_NAMES)]
        agent_id = f"agent_{i}"
        # Per-agent model: check by agent_id, then by name, then fall back to default
        agent_model = config.models.get(agent_id) or config.models.get(name) or config.model
        identity = AgentIdentity(id=agent_id, name=name, model=agent_model)
        state = AgentState(
            identity=identity,
            token_budget_remaining=config.parameters.token_budget_per_agent,
        )
        llm = create_client(agent_model, max_tokens=4096)
        executor = WorkspaceExecutor(workspace, attention=attention)
        agent = Agent(state=state, llm=llm, executor=executor)
        workspace.register_agent(state)
        agents.append(agent)

    # Create org enforcer
    enforcer = OrgEnforcer(
        dimensions=config.org_dimensions,
        parameters=config.parameters,
    )
    enforcer.assign_initial_roles([a.state.identity.id for a in agents])

    if enforcer.lead_agent_id:
        lead_name = next(
            a.state.identity.name for a in agents
            if a.state.identity.id == enforcer.lead_agent_id
        )
        print(f"  Lead agent: {lead_name}\n")

    # Set up gardener if requested
    gardener = None
    if args.gardener:
        gardener = Gardener()
        gardener.enable()
        print(f"  Gardener mode: ON (type instructions between ticks, Enter to continue)\n")

    # Create and run engine
    engine = Engine(
        config=config,
        workspace=workspace,
        agents=agents,
        event_bus=event_bus,
        enforcer=enforcer,
        attention=attention,
        gardener=gardener,
    )

    if gardener:
        # Gardener mode: run tick by tick with prompts between
        await _run_with_gardener(engine, gardener)
    else:
        await engine.run()

    # Print chronicle report
    if engine.chronicle:
        report = engine.chronicle.generate_report()
        print(report.to_terminal())


async def _run_with_gardener(engine: Engine, gardener: Gardener) -> None:
    """Run engine tick by tick with gardener prompts between ticks.

    After each tick, the user can type an instruction:
      <text>              → message to all agents
      /redirect <text>    → change task focus
      /meta               → force a meta-tick
      /set <param> <val>  → adjust a parameter
      /stop               → stop the engine
      (Enter)             → continue to next tick
    """
    import sys

    # Manual engine initialisation (normally done inside engine.run)
    engine.running = True
    # Trigger the initialisation that run() does
    await engine.run.__wrapped__(engine) if hasattr(engine.run, '__wrapped__') else None

    # We need to replicate the init from run() without the tick loop
    if engine.enforcer is None:
        from .org.enforcer import OrgEnforcer
        engine.enforcer = OrgEnforcer(
            dimensions=engine.config.org_dimensions,
            parameters=engine.config.parameters,
        )
        engine.enforcer.assign_initial_roles(
            [a.state.identity.id for a in engine.agents]
        )

    # Init subsystems (same as engine.run)
    from .core.types import Event, EventType
    from .org.auto import AutoOrgManager
    from .chronicle.observer import Chronicle
    from .workspace.git import GitManager

    if engine.config.parameters.meta_tick_interval > 0 and engine.auto_org is None:
        engine.auto_org = AutoOrgManager(
            dimensions=engine.config.org_dimensions,
            parameters=engine.config.parameters,
            agent_count=len(engine.agents),
        )

    if engine.config.parameters.enable_git_branches and engine.git is None:
        if await GitManager.is_available():
            engine.git = GitManager(engine.workspace.project_dir)
            await engine.git.init()

    if engine.config.enable_chronicle and engine.chronicle is None:
        agent_names = {
            a.state.identity.id: a.state.identity.name
            for a in engine.agents
        }
        engine.chronicle = Chronicle(
            task=engine.config.task,
            org_preset=engine.config.org_preset,
            agent_count=len(engine.agents),
            agent_names=agent_names,
        )
        engine.event_bus.subscribe(None, engine.chronicle.observe)

    for agent in engine.agents:
        engine.attention.register_agent(
            agent.state.identity.id,
            agent.state.identity.name,
        )

    engine.event_bus.emit(Event(
        type=EventType.ENGINE_STARTED,
        tick=0,
        data={"config": engine.config.org_preset, "agents": engine.config.agent_count},
    ))

    try:
        for engine.tick in range(1, engine.config.max_ticks + 1):
            if not engine.running:
                break

            await engine._execute_tick()

            # Gardener prompt
            try:
                raw = input("  gardener> ")
            except (EOFError, KeyboardInterrupt):
                print("\n  Gardener ended the run.")
                break

            intervention = Gardener.parse_input(raw, tick=engine.tick)
            if intervention:
                if intervention.type == "stop":
                    print("  Stopping engine...")
                    break
                gardener.submit(intervention)
                print(f"  → {intervention.type}: queued for next tick")
    finally:
        engine.running = False
        if engine.git:
            await engine.git.cleanup_all()
        engine.event_bus.emit(Event(
            type=EventType.ENGINE_STOPPED,
            tick=engine.tick,
        ))


async def run_experiment_cmd(args: argparse.Namespace) -> None:
    """Execute the experiment command."""
    import json
    from .experiment import run_experiment

    orgs = [o.strip() for o in args.orgs.split(",")]

    result = await run_experiment(
        task=args.task,
        orgs=orgs,
        runs_per_org=args.runs,
        agent_count=args.agents,
        model=args.model,
        max_ticks=args.max_ticks,
        source_dir=args.dir,
        verbose=args.verbose,
    )

    # Print comparison report
    print(result.to_terminal())

    # Save JSON if requested
    if args.output:
        with open(args.output, "w") as f:
            json.dump(result.to_dict(), f, indent=2)
        print(f"  Results saved to {args.output}\n")


async def run_benchmark_cmd(args: argparse.Namespace) -> None:
    """Execute the benchmark command."""
    from .benchmark import run_benchmark, BenchmarkConfig, get_all_tasks

    # Handle --list-tasks
    if args.list_tasks:
        print("\n  Available Benchmark Tasks:")
        print(f"  {'─' * 60}")
        for task in get_all_tasks():
            print(
                f"  {task.id:20s} {task.difficulty:8s} "
                f"{task.max_ticks:3d} ticks  "
                f"files: {', '.join(task.expected_files)}"
            )
        print(f"\n  Use --tasks fizzbuzz,todo-cli or --tasks simple or --tasks all\n")
        return

    config = BenchmarkConfig(
        tasks=[t.strip() for t in args.tasks.split(",")],
        presets=[p.strip() for p in args.presets.split(",")],
        runs_per_combo=args.runs,
        agent_count=args.agents,
        model=args.model,
        max_ticks_override=args.max_ticks,
        dry_run=args.dry_run,
        mock=args.mock,
        output_path=args.output,
        verbose=args.verbose,
    )

    result = await run_benchmark(config)

    # Dry run returns a dict, not a BenchmarkResult
    if isinstance(result, dict) and result.get("dry_run"):
        return

    # Print terminal report
    print(result.to_terminal())

    # Save JSON if requested
    if args.output:
        result.to_json(args.output)
        print(f"  Results saved to {args.output}\n")


def show_info() -> None:
    """Show available presets, dimensions, and feature toggles."""
    import yaml
    from .org.config import KNOWN_DIMENSIONS

    print("\n  AgentCiv Engine — Organisational Configurations\n")

    # Presets with descriptions (read from YAML comments)
    print("  Presets:")
    presets_dir = Path(__file__).parent.parent / "presets"
    if presets_dir.exists():
        for p in sorted(presets_dir.glob("*.yaml")):
            # Extract description from comment block (skip title and blank comment lines)
            desc = ""
            with open(p) as f:
                for line in f:
                    line = line.strip()
                    if not line or line == "#":
                        continue
                    if "AgentCiv Engine" in line:
                        continue
                    if line.startswith("#"):
                        desc = line.lstrip("# ").strip()
                        break
                    else:
                        break
            print(f"    --org {p.stem:20s} {desc}")
    print()

    # Dimensions
    print("  Organisational Dimensions (9 built-in, community-expandable):")
    for dim, values in KNOWN_DIMENSIONS.items():
        print(f"    {dim:16s} {' → '.join(values)}")
    print()

    # Feature toggles
    print("  Feature Toggles (all configurable in YAML):")
    toggles = [
        ("enable_specialisation", "Agents develop skills through practice"),
        ("specialisation_visible", "Other agents can see your skills"),
        ("enable_relationships", "Track collaboration history and trust"),
        ("prefer_known_collaborators", "Agents prefer past partners"),
        ("enable_attention_map", "Shared view of who's working on what"),
        ("enable_git_branches", "Branch-per-agent with auto-merge"),
        ("enable_gardener_mode", "Human-in-the-loop mid-run intervention"),
        ("require_review", "Mandatory peer review before merge"),
    ]
    for name, desc in toggles:
        print(f"    {name:32s} {desc}")
    print()

    print("  Add custom dimensions, presets, and parameters in your YAML config.")
    print("  Everything is expandable. See presets/ directory for examples.\n")


def main() -> None:
    parser = build_cli()
    args = parser.parse_args()

    if args.command == "solve":
        logging.basicConfig(
            level=logging.DEBUG if args.verbose else logging.WARNING,
            format="%(name)s: %(message)s",
        )
        asyncio.run(run_solve(args))

    elif args.command == "experiment":
        logging.basicConfig(
            level=logging.DEBUG if args.verbose else logging.WARNING,
            format="%(name)s: %(message)s",
        )
        asyncio.run(run_experiment_cmd(args))

    elif args.command == "benchmark":
        logging.basicConfig(
            level=logging.DEBUG if args.verbose else logging.WARNING,
            format="%(name)s: %(message)s",
        )
        asyncio.run(run_benchmark_cmd(args))

    elif args.command == "info":
        show_info()

    elif args.command == "mcp":
        from .mcp import run_server
        run_server()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
