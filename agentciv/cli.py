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
from .core.engine import Engine
from .core.event_bus import EventBus
from .core.types import AgentIdentity, AgentState, Event, EventType
from .llm.client import create_client
from .org.config import EngineConfig
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

    # --- info ---
    sub.add_parser("info", help="Show available presets and dimensions")

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
            print(f"  {tick} ────────────────────")

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

        case EventType.RESTRUCTURE_PROPOSED:
            preview = event.data.get("content_preview", "")
            print(f"  {tick}{agent} proposes restructure: {preview}")

        case EventType.RESTRUCTURE_ADOPTED:
            print(f"  {tick} ★ organisation restructured")

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

    # Create agents
    agents: list[Agent] = []
    for i in range(config.agent_count):
        name = AGENT_NAMES[i % len(AGENT_NAMES)]
        identity = AgentIdentity(id=f"agent_{i}", name=name, model=config.model)
        state = AgentState(
            identity=identity,
            token_budget_remaining=config.parameters.token_budget_per_agent,
        )
        llm = create_client(config.model, max_tokens=1024)
        executor = WorkspaceExecutor(workspace)
        agent = Agent(state=state, llm=llm, executor=executor)
        workspace.register_agent(state)
        agents.append(agent)

    # Create and run engine
    engine = Engine(
        config=config,
        workspace=workspace,
        agents=agents,
        event_bus=event_bus,
    )

    await engine.run()


def show_info() -> None:
    """Show available presets and dimensions."""
    from .org.config import KNOWN_DIMENSIONS

    print("\n  AgentCiv Engine — Organisational Configurations\n")
    print("  Presets:")
    presets_dir = Path(__file__).parent.parent / "presets"
    if presets_dir.exists():
        for p in sorted(presets_dir.glob("*.yaml")):
            print(f"    --org {p.stem}")
    print()

    print("  Organisational Dimensions:")
    for dim, values in KNOWN_DIMENSIONS.items():
        print(f"    {dim}: {' → '.join(values)}")
    print()
    print("  All dimensions are community-expandable. Add your own in YAML config.\n")


def main() -> None:
    parser = build_cli()
    args = parser.parse_args()

    if args.command == "solve":
        logging.basicConfig(
            level=logging.DEBUG if args.verbose else logging.WARNING,
            format="%(name)s: %(message)s",
        )
        asyncio.run(run_solve(args))

    elif args.command == "info":
        show_info()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
