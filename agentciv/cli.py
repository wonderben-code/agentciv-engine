"""CLI entry point — agentciv solve --task "..." --org collaborative

This is how users interact with the engine from the terminal.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
from pathlib import Path

import os

from .core.agent import Agent
from .core.attention import AttentionMap
from .core.engine import Engine
from .core.event_bus import EventBus
from .core.types import AgentIdentity, AgentState, Event, EventType
from . import display
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
    solve.add_argument("--org", "-o", default="collaborative", help="Organisational preset — 13 available. Run 'agentciv info' to see all. Examples: collaborative, hierarchical, meritocratic, swarm, auto")
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

    # --- test-tasks ---
    bench = sub.add_parser("test-tasks", help="Run built-in test tasks across org presets and compare results")
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
    bench.add_argument("--list-tasks", action="store_true", help="List available test tasks and exit")

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


def make_event_handler(agent_names: dict[str, str], verbose: bool = False):
    """Create an event handler that resolves agent IDs to names and uses rich display.

    Returns a callable suitable for event_bus.subscribe().
    """
    def _resolve(agent_id: str | None) -> str:
        if not agent_id:
            return ""
        return agent_names.get(agent_id, agent_id)

    def handle_event(event: Event) -> None:
        name = _resolve(event.agent_id)

        match event.type:
            # Engine lifecycle — handled by show_engine_start, not here
            case EventType.ENGINE_STARTED:
                pass  # displayed by run_solve directly

            case EventType.TICK_START:
                display.show_tick_start(event.tick, event.data.get("is_meta_tick", False))

            case EventType.TICK_END:
                display.show_tick_end(event.tick, event.data.get("actions", 0))

            case EventType.FILE_CREATED:
                display.show_file_created(event.tick, name, event.data.get("file", "?"))

            case EventType.FILE_MODIFIED:
                display.show_file_modified(event.tick, name, event.data.get("file", "?"))

            case EventType.MESSAGE_SENT:
                targets = event.data.get("targets", [])
                target_names = [_resolve(t) for t in targets]
                display.show_message_sent(
                    event.tick, name, target_names,
                    event.data.get("content_preview", ""),
                )

            case EventType.BROADCAST_SENT:
                display.show_broadcast(
                    event.tick, name,
                    event.data.get("content_preview", ""),
                )

            case EventType.TASK_CLAIMED:
                display.show_task_claimed(
                    event.tick, name,
                    event.data.get("content_preview", ""),
                )

            case EventType.TESTS_PASSED:
                display.show_tests_passed(event.tick)

            case EventType.TESTS_FAILED:
                display.show_tests_failed(event.tick)

            case EventType.BUILD_SUCCEEDED:
                display.show_build_passed(event.tick)

            case EventType.BUILD_FAILED:
                display.show_build_failed(event.tick)

            case EventType.BRANCH_MERGED:
                display.show_branch_merged(event.tick, name, event.data.get("count", 0))

            case EventType.MERGE_CONFLICT:
                display.show_merge_conflict(event.tick, name, event.data.get("conflicts", []))

            case EventType.RESTRUCTURE_PROPOSED:
                display.show_restructure_proposed(
                    event.tick, name,
                    event.data.get("content_preview", ""),
                )

            case EventType.RESTRUCTURE_ADOPTED:
                display.show_restructure_adopted(
                    event.tick,
                    dimension=event.data.get("dimension", "?"),
                    old_value=event.data.get("old_value", "?"),
                    new_value=event.data.get("new_value", "?"),
                    yes_votes=event.data.get("yes_votes", 0),
                    no_votes=event.data.get("no_votes", 0),
                    proposer=_resolve(event.data.get("proposer", "")),
                )

            case EventType.ENGINE_STOPPED:
                display.show_engine_stopped(event.tick)

            case _:
                if verbose:
                    display.console.print(
                        f"  [dim][tick {event.tick:3d}] {name} {event.type.name}[/dim]"
                    )

    return handle_event


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
    display.show_scan_result(len(workspace.files))

    # Build agent name mapping (agent_id → display name)
    agent_name_map: dict[str, str] = {}
    agent_display_names: list[str] = []

    # Create attention map
    attention = AttentionMap()

    # Create agents (with per-agent model overrides from config.models)
    agents: list[Agent] = []
    for i in range(config.agent_count):
        name = AGENT_NAMES[i % len(AGENT_NAMES)]
        agent_id = f"agent_{i}"
        agent_name_map[agent_id] = name
        agent_display_names.append(name)
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

    lead_name = None
    if enforcer.lead_agent_id:
        lead_name = agent_name_map.get(enforcer.lead_agent_id)

    # Set up gardener if requested
    gardener = None
    if args.gardener:
        gardener = Gardener()
        gardener.enable()

    # Set up event bus with rich display handler
    event_bus = EventBus()
    event_handler = make_event_handler(agent_name_map, verbose=args.verbose)
    event_bus.subscribe(None, event_handler)

    # Show the beautiful engine start header
    display.show_engine_start(
        task=config.task,
        agent_count=config.agent_count,
        org_preset=args.org,
        max_ticks=config.max_ticks,
        agent_names=agent_display_names,
        model=config.model,
        lead_agent=lead_name,
        gardener=args.gardener,
    )

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

    # Print chronicle report (rich version)
    if engine.chronicle:
        report = engine.chronicle.generate_report()
        display.show_chronicle_report(report)

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
                display.show_tip(tip.text)


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
    # Use engine.initialize() — the same init path that Max Plan Mode uses
    await engine.initialize()

    try:
        for engine.tick in range(1, engine.config.max_ticks + 1):
            if not engine.running:
                break

            await engine._execute_tick()

            # Gardener prompt (rich display)
            raw = display.show_gardener_prompt()
            if not raw:
                break

            intervention = Gardener.parse_input(raw, tick=engine.tick)
            if intervention:
                if intervention.type == "stop":
                    display.console.print("  [dim]Stopping engine...[/dim]")
                    break
                gardener.submit(intervention)
                display.show_gardener_queued(intervention.type)
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

    # Rich comparison report
    display.show_experiment_report(result)

    # Contextual tip
    if not args.no_tips:
        from .discovery import FeatureTracker, generate_post_experiment_tip
        tracker = FeatureTracker()
        tracker.mark_used("experiment")
        tip = generate_post_experiment_tip(orgs_tested=orgs, tracker=tracker)
        if tip:
            display.show_tip(tip.text)

    # Save JSON if requested
    if args.output:
        with open(args.output, "w") as f:
            json.dump(result.to_dict(), f, indent=2)
        display.show_success(f"Results saved to {args.output}")


async def run_benchmark_cmd(args: argparse.Namespace) -> None:
    """Execute the benchmark command."""
    from .benchmark import run_benchmark, BenchmarkConfig, get_all_tasks

    # Handle --list-tasks
    if args.list_tasks:
        display.show_benchmark_tasks_list(get_all_tasks())
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

    # Print terminal report (rich)
    display.show_test_tasks_report(result)

    # Save JSON if requested
    if args.output:
        result.to_json(args.output)
        display.show_success(f"Results saved to {args.output}")


def show_info() -> None:
    """Show available presets, dimensions, and feature toggles."""
    from .org.config import KNOWN_DIMENSIONS

    # Presets with descriptions (read from YAML comments)
    presets: list[tuple[str, str]] = []
    presets_dir = Path(__file__).parent / "presets"
    if presets_dir.exists():
        for p in sorted(presets_dir.glob("*.yaml")):
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
            presets.append((p.stem, desc))

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

    display.show_info(presets, dict(KNOWN_DIMENSIONS), toggles)


def show_history(args: argparse.Namespace) -> None:
    """Show or manage learning history."""
    import json as json_mod
    from .learning.history import RunHistory
    from .learning.insights import generate_insights

    history = RunHistory()

    if args.clear:
        history.clear()
        display.show_success("Run history cleared.")
        return

    if args.similar:
        insights = generate_insights(args.similar, history)
        if args.json:
            print(json_mod.dumps(insights.to_dict(), indent=2))
        else:
            display.show_learning_insights(insights)
        return

    # Default: show stats
    stats = history.get_stats()
    if args.json:
        print(json_mod.dumps(stats, indent=2))
    else:
        display.show_history_stats(stats)


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

    display.show_setup_welcome()

    # 1. Environment check
    display.console.print("  [dim]Checking your environment...[/dim]")
    agentciv_path = shutil.which("agentciv")
    if agentciv_path:
        display.show_setup_check("CLI installed", agentciv_path)
    else:
        display.show_setup_check("Running via Python module")

    import platform
    display.show_setup_check(f"Python {platform.python_version()}")
    display.show_setup_check("13 team structures ready to go")
    display.show_setup_check("9 organisational dimensions available")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        masked = api_key[:12] + "..." + api_key[-4:]
        display.show_setup_check("Anthropic API key detected", masked)

    display.console.print()

    # 2. Mode selection — user explicitly chooses, no auto-detection
    display.console.print("  How would you like to run your agent teams?")
    display.console.print()
    display.console.print("  [bold][1] MAX PLAN[/bold] [green]— Free[/green]")
    display.console.print("      [dim]Works inside Claude Code / Cursor via MCP.[/dim]")
    display.console.print("      [dim]Your AI assistant drives the agents — no API key needed.[/dim]")
    display.console.print("      [dim]Zero additional cost beyond your existing subscription.[/dim]")
    display.console.print()
    display.console.print("  [bold][2] API MODE[/bold] [yellow]— Uses your Anthropic API key[/yellow]")
    display.console.print("      [dim]Run from the command line: agentciv solve --task \"...\"[/dim]")
    display.console.print("      [dim]The engine makes its own LLM calls. You pay per token.[/dim]")
    display.console.print("      [dim]Requires ANTHROPIC_API_KEY environment variable.[/dim]")
    display.console.print()
    display.console.print("  [bold][3] BOTH[/bold] [dim]— Set up both modes[/dim]")
    display.console.print()

    try:
        choice = input("  Your choice [1]: ").strip() or "1"
    except (EOFError, KeyboardInterrupt):
        choice = "1"
        print("1")

    if choice not in ("1", "2", "3"):
        choice = "1"

    wants_mcp = choice in ("1", "3")
    wants_api = choice in ("2", "3")

    display.console.print()

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
                display.show_setup_check("MCP configured globally", "~/.claude.json")
            else:
                display.show_setup_check("~/.claude.json not found — is Claude Code installed?", success=False)
                display.console.print("    [dim]Install: https://docs.anthropic.com/en/docs/claude-code[/dim]")
        else:
            config_path = project_dir / ".mcp.json"
            if config_path.exists():
                existing = json_mod.loads(config_path.read_text())
                existing.setdefault("mcpServers", {})
                existing["mcpServers"]["agentciv"] = mcp_config["mcpServers"]["agentciv"]
                config_path.write_text(json_mod.dumps(existing, indent=2) + "\n")
            else:
                config_path.write_text(json_mod.dumps(mcp_config, indent=2) + "\n")
            display.show_setup_check("MCP server configured", str(config_path))

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
                display.show_setup_check("AgentCiv knowledge added to", str(claude_md))
            else:
                display.show_setup_check("CLAUDE.md already has AgentCiv info", str(claude_md))
        else:
            claude_md.write_text(agentciv_block.lstrip())
            display.show_setup_check("CLAUDE.md created", str(claude_md))

    if wants_api:
        if api_key:
            display.show_setup_check("API key detected — API mode ready")
        else:
            display.show_warning("API mode selected but no ANTHROPIC_API_KEY found.")
            display.console.print("    [dim]Set it in your shell profile:[/dim]")
            display.console.print('    [dim]export ANTHROPIC_API_KEY="sk-ant-..."[/dim]')

    # 4. Celebration and next steps
    display.show_setup_celebration()

    if wants_mcp:
        display.show_setup_next_steps_mcp()

    if wants_api:
        display.show_setup_next_steps_api()

    display.show_setup_crown_jewel()


def main() -> None:
    parser = build_cli()
    args = parser.parse_args()

    try:
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

        elif args.command == "test-tasks":
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

    except KeyboardInterrupt:
        display.console.print("\n  [dim]Run interrupted.[/dim]")
    except RuntimeError as e:
        # Teaching errors from LLM client, engine, etc.
        error_msg = str(e)
        if "\n" in error_msg:
            # Multi-line error = already a teaching message
            title = error_msg.split("\n")[0]
            body = "\n".join(error_msg.split("\n")[1:]).strip()
            display.show_error(title, body)
        else:
            display.show_error("Error", error_msg)
        raise SystemExit(1)
    except Exception as e:
        display.show_error(
            "Unexpected error",
            str(e),
            suggestion="Run with --verbose for more details, or report this issue.",
        )
        raise SystemExit(1)


if __name__ == "__main__":
    main()
