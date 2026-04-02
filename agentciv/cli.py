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

    # Create and run engine
    engine = Engine(
        config=config,
        workspace=workspace,
        agents=agents,
        event_bus=event_bus,
        enforcer=enforcer,
        attention=attention,
    )

    await engine.run()

    # Print chronicle report
    if engine.chronicle:
        report = engine.chronicle.generate_report()
        print(report.to_terminal())


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

    elif args.command == "info":
        show_info()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
