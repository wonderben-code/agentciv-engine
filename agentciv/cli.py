"""CLI entry point — agentciv solve --task "..." --org collaborative

This is how users interact with the engine from the terminal.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from pathlib import Path

import os

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
    solve.add_argument("--no-tips", action="store_true", help="Suppress contextual feature tips")

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
    exp.add_argument("--no-tips", action="store_true", help="Suppress contextual feature tips")

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

    # --- history ---
    hist = sub.add_parser("history", help="View or manage the learning history")
    hist.add_argument("--clear", action="store_true", help="Clear all run history")
    hist.add_argument("--similar", help="Find similar runs to a task description")
    hist.add_argument("--json", action="store_true", help="Output as JSON")

    # --- setup ---
    setup = sub.add_parser("setup", help="Configure AgentCiv for your environment (Claude Code, API key, etc.)")
    setup.add_argument("--dir", "-d", default=".", help="Project directory to configure (default: current)")
    setup.add_argument("--global", dest="global_config", action="store_true", help="Configure globally in ~/.claude.json instead of project-level")

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

        # Contextual tip
        if not args.no_tips:
            from .discovery import FeatureTracker, generate_post_run_tip
            tracker = FeatureTracker()
            tracker.mark_used("solve")
            if args.org == "auto":
                tracker.mark_used("auto")
            if args.gardener:
                tracker.mark_used("gardener")
            tip = generate_post_run_tip(
                org_preset=args.org,
                merge_conflicts=report.merge_conflicts,
                total_messages=report.total_messages,
                restructures_adopted=report.restructures_adopted,
                agent_count=args.agents,
                tracker=tracker,
            )
            if tip:
                print(f"  {tip.text}\n")


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

    # Contextual tip
    if not args.no_tips:
        from .discovery import FeatureTracker, generate_post_experiment_tip
        tracker = FeatureTracker()
        tracker.mark_used("experiment")
        tip = generate_post_experiment_tip(orgs_tested=orgs, tracker=tracker)
        if tip:
            print(f"  {tip.text}\n")

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


def show_history(args: argparse.Namespace) -> None:
    """Show or manage learning history."""
    import json as json_mod
    from .learning.history import RunHistory
    from .learning.insights import generate_insights

    history = RunHistory()

    if args.clear:
        history.clear()
        print("  Run history cleared.\n")
        return

    if args.similar:
        insights = generate_insights(args.similar, history)
        if args.json:
            print(json_mod.dumps(insights.to_dict(), indent=2))
        else:
            print(f"\n  Learning Insights for: \"{args.similar}\"")
            print(f"  {'─' * 50}")
            print(f"  Keywords: {', '.join(insights.task_keywords)}")
            print(f"  Matching runs: {insights.matching_runs} / {insights.total_history}")
            if insights.preset_rankings:
                print(f"\n  Preset rankings:")
                for p in insights.preset_rankings[:10]:
                    print(f"    {p.preset:20s} quality: {p.avg_quality:.3f} ({p.run_count} runs)")
            if insights.dimension_insights:
                print(f"\n  Best dimension values:")
                for d in insights.dimension_insights:
                    print(f"    {d.dimension:20s} → {d.value} (quality: {d.avg_quality:.3f})")
            if not insights.has_data():
                print(f"\n  Not enough similar runs for recommendations yet.")
            print()
        return

    # Default: show stats
    stats = history.get_stats()
    if args.json:
        print(json_mod.dumps(stats, indent=2))
    else:
        print(f"\n  AgentCiv Learning History")
        print(f"  {'─' * 40}")
        print(f"  Total runs: {stats['total_runs']}")
        if stats['total_runs'] > 0:
            print(f"  Successful: {stats['successful_runs']}")
            print(f"  Unique presets: {stats['unique_presets']}")
            print(f"\n  Average quality by preset:")
            for preset, avg in stats['preset_avg_quality'].items():
                print(f"    {preset:20s} {avg:.3f}")
        else:
            print(f"  No runs recorded yet. Run some tasks to build up learning data.")
        print()


def run_setup(args: argparse.Namespace) -> None:
    """Configure AgentCiv for the user's environment.

    Interactive setup that:
    1. Checks the environment
    2. Explains the two modes clearly (free vs paid)
    3. Writes the config
    4. Celebrates success with clear next steps
    """
    import json as json_mod
    import shutil
    import sys

    print()
    print(f"  ╔══════════════════════════════════════════════════════╗")
    print(f"  ║                                                      ║")
    print(f"  ║   Welcome to AgentCiv Engine!                        ║")
    print(f"  ║   Let's get your custom AI agent team set up.        ║")
    print(f"  ║                                                      ║")
    print(f"  ╚══════════════════════════════════════════════════════════╝")
    print()

    # 1. Environment check
    print(f"  Checking your environment...")
    agentciv_path = shutil.which("agentciv")
    if agentciv_path:
        print(f"  ✓ CLI installed: {agentciv_path}")
    else:
        print(f"  ✓ Running via Python module")

    import platform
    print(f"  ✓ Python {platform.python_version()}")
    print(f"  ✓ 13 team structures ready to go")
    print(f"  ✓ 9 organisational dimensions available")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        masked = api_key[:12] + "..." + api_key[-4:]
        print(f"  ✓ Anthropic API key detected: {masked}")

    print()

    # 2. Mode selection — user explicitly chooses, no auto-detection
    print(f"  How would you like to run your agent teams?")
    print()
    print(f"  [1] MAX PLAN — Free")
    print(f"      Works inside Claude Code / Cursor via MCP.")
    print(f"      Your AI assistant drives the agents — no API key needed.")
    print(f"      Zero additional cost beyond your existing subscription.")
    print()
    print(f"  [2] API MODE — Uses your Anthropic API key")
    print(f"      Run from the command line: agentciv solve --task \"...\"")
    print(f"      The engine makes its own LLM calls. You pay per token.")
    print(f"      Requires ANTHROPIC_API_KEY environment variable.")
    print()
    print(f"  [3] BOTH — Set up both modes")
    print()

    try:
        choice = input("  Your choice [1]: ").strip() or "1"
    except (EOFError, KeyboardInterrupt):
        choice = "1"
        print("1")

    if choice not in ("1", "2", "3"):
        choice = "1"

    wants_mcp = choice in ("1", "3")
    wants_api = choice in ("2", "3")

    print()

    # 3. Configure based on choice
    project_dir = Path(args.dir).resolve()
    project_dir.mkdir(parents=True, exist_ok=True)

    if wants_mcp:
        mcp_config = {
            "mcpServers": {
                "agentciv": {
                    "command": agentciv_path or "python3",
                    "args": ["mcp"] if agentciv_path else ["-m", "agentciv.mcp"],
                }
            }
        }

        if args.global_config:
            config_path = Path.home() / ".claude.json"
            if config_path.exists():
                existing = json_mod.loads(config_path.read_text())
                if "mcpServers" not in existing:
                    existing["mcpServers"] = {}
                existing["mcpServers"]["agentciv"] = mcp_config["mcpServers"]["agentciv"]
                config_path.write_text(json_mod.dumps(existing, indent=2))
                print(f"  ✓ MCP configured globally: ~/.claude.json")
            else:
                print(f"  ✗ ~/.claude.json not found — is Claude Code installed?")
                print(f"    Install: https://docs.anthropic.com/en/docs/claude-code")
        else:
            config_path = project_dir / ".mcp.json"
            if config_path.exists():
                existing = json_mod.loads(config_path.read_text())
                existing.setdefault("mcpServers", {})
                existing["mcpServers"]["agentciv"] = mcp_config["mcpServers"]["agentciv"]
                config_path.write_text(json_mod.dumps(existing, indent=2) + "\n")
            else:
                config_path.write_text(json_mod.dumps(mcp_config, indent=2) + "\n")
            print(f"  ✓ MCP server configured: {config_path}")

    if wants_mcp and not args.global_config:
        # Write CLAUDE.md with factual agentciv knowledge so Claude Code
        # is naturally knowledgeable — no scripts, just facts
        claude_md = project_dir / "CLAUDE.md"
        agentciv_block = (
            "\n# AgentCiv Engine\n\n"
            "This project has AgentCiv Engine configured (MCP tools available).\n\n"
            "AgentCiv spawns communities of 2-20 AI agents under configurable "
            "organisational structures. 13 presets, 9 dimensions, two modes "
            "(Max Plan and API).\n\n"
            "Presets: collaborative (default), competitive, meritocratic, auto, "
            "hierarchical, startup, pair-programming, open-source, military, "
            "research-lab, swarm, hackathon, code-review.\n\n"
            "org='auto' — agents design their own structure through proposals "
            "and votes. Restructures live during the run.\n\n"
            "Dimensions (each overridable): authority, communication, roles, "
            "decisions, incentives, information, conflict, groups, adaptation.\n\n"
            "Defaults: org='collaborative', agents=4, max_ticks=50. "
            "Only 'task' is required.\n\n"
            "agentciv_info() returns full details on all presets and dimensions.\n"
        )
        if claude_md.exists():
            existing = claude_md.read_text()
            if "AgentCiv Engine" not in existing:
                claude_md.write_text(existing.rstrip() + "\n" + agentciv_block)
                print(f"  ✓ AgentCiv knowledge added to: {claude_md}")
            else:
                print(f"  ✓ CLAUDE.md already has AgentCiv info: {claude_md}")
        else:
            claude_md.write_text(agentciv_block.lstrip())
            print(f"  ✓ CLAUDE.md created: {claude_md}")

    if wants_api:
        if api_key:
            print(f"  ✓ API key detected — API mode ready")
        else:
            print(f"  ! API mode selected but no ANTHROPIC_API_KEY found.")
            print(f"    Set it in your shell profile:")
            print(f"    export ANTHROPIC_API_KEY=\"sk-ant-...\"")

    # 4. Celebration and next steps
    print()
    print(f"  ╔══════════════════════════════════════════════════════╗")
    print(f"  ║                                                      ║")
    print(f"  ║   CONGRATULATIONS! AgentCiv Engine is installed.     ║")
    print(f"  ║                                                      ║")
    print(f"  ║   13 team structures at your fingertips — including  ║")
    print(f"  ║   one where your agents design their own team        ║")
    print(f"  ║   through proposals and votes.                       ║")
    print(f"  ║                                                      ║")
    print(f"  ║   Time to spawn your first agent team!               ║")
    print(f"  ║                                                      ║")
    print(f"  ╚══════════════════════════════════════════════════════════╝")
    print()

    if wants_mcp:
        print(f"  YOUR FIRST RUN")
        print(f"  ─────────────────────────────────────")
        print(f"  Open Claude Code in this directory and say:")
        print()
        print(f"    \"Use agentciv to build a REST API with 4 agents\"")
        print()
        print(f"  You can shape your team however you want:")
        print()
        print(f"    \"Use a meritocratic team to refactor this module\"")
        print(f"    \"Set up a pair-programming duo for this bug\"")
        print(f"    \"Use --org auto and let the agents figure it out\"")
        print()

    if wants_api:
        print(f"  YOUR FIRST RUN")
        print(f"  ─────────────────────────────────────")
        print(f"  agentciv solve --task \"Build a REST API\" --org collaborative")
        print(f"  agentciv solve --task \"Build a CLI tool\" --org auto")
        print(f"  agentciv experiment --task \"Build X\" --orgs collaborative,meritocratic,auto")
        print()

    print(f"  THE CROWN JEWEL: --org auto")
    print(f"    Agents design their own team structure through proposals")
    print(f"    and votes. Self-organisation in real time. Try it.")
    print()
    print(f"  Run 'agentciv info' to explore all 13 team structures.")
    print(f"  ══════════════════════════════════════════════════════")


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

    elif args.command == "history":
        show_history(args)

    elif args.command == "setup":
        run_setup(args)

    elif args.command == "info":
        show_info()

    elif args.command == "mcp":
        from .mcp import run_server
        run_server()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
