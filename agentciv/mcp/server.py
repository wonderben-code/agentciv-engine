"""AgentCiv MCP Server — spawn agent communities from any AI assistant.

This is the bridge between Claude Code / Cursor / any MCP client and
the AgentCiv Engine. Every tool call spawns, monitors, or shapes a
living agent community.

Usage:
  agentciv mcp                    # stdio transport (for Claude Code)
  python -m agentciv.mcp          # same thing

Claude Code config (~/.claude.json or project .mcp.json):
  {
    "mcpServers": {
      "agentciv": {
        "command": "agentciv",
        "args": ["mcp"]
      }
    }
  }
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from ..gardener import Intervention
from ..org.config import KNOWN_DIMENSIONS, EngineConfig
from .session import SessionManager

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# MCP server instance
# ---------------------------------------------------------------------------

mcp = FastMCP(
    "AgentCiv Engine",
    instructions=(
        "AgentCiv Engine — organisational arrangement as a first-class design "
        "parameter for multi-agent AI systems.\n\n"
        "Spawns communities of 2-20 AI agents under configurable organisational "
        "structures to solve tasks. 13 presets, each defining 9 dimensions "
        "(authority, communication, roles, decisions, incentives, information, "
        "conflict, groups, adaptation).\n\n"
        "MODES (confirm with user before proceeding — never auto-select API mode):\n"
        "- Max Plan: agentciv_orchestrate_start(). You drive agent cognition. "
        "No API key needed, no cost beyond existing subscription.\n"
        "- API: agentciv_solve(). Engine makes its own LLM calls via "
        "ANTHROPIC_API_KEY. User pays per token.\n\n"
        "DEFAULTS: org='collaborative', agents=4, max_ticks=50. "
        "Only 'task' is required — everything else is optional.\n\n"
        "PRESETS: collaborative, competitive, meritocratic, auto, hierarchical, "
        "startup, pair-programming, open-source, military, research-lab, swarm, "
        "hackathon, code-review. org='auto' lets agents design their own "
        "structure through proposals and votes.\n\n"
        "CAPABILITIES: single runs, comparative experiments across org structures, "
        "mid-run intervention (gardener mode), custom configs via dimension "
        "overrides. agentciv_info() has full details."
    ),
)

# Global session manager — lives for the server process lifetime
manager = SessionManager()


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
async def agentciv_solve(
    task: str,
    org: str = "collaborative",
    agents: int = 4,
    model: str = "claude-sonnet-4-6",
    max_ticks: int = 50,
    project_dir: str = ".",
    overrides: dict[str, str] | None = None,
) -> str:
    """Spawn an agent community to solve a task.

    The community self-organises according to the chosen organisational
    preset. Each agent gets tools (read/write files, run commands,
    communicate, claim tasks) and works concurrently in the project directory.

    Available presets: collaborative, competitive, meritocratic, auto,
    hierarchical, startup, pair-programming, open-source, military,
    research-lab, swarm, hackathon, code-review

    The crown jewel is org='auto' — agents design their own organisational
    structure through proposals and votes during meta-ticks.

    Returns a session ID for monitoring and intervention.

    Args:
        task: What the community should build or solve
        org: Organisational preset name (default: collaborative)
        agents: Number of agents, 2-20 (default: 4)
        model: LLM model for agents (default: claude-sonnet-4-6)
        max_ticks: Maximum execution rounds (default: 50)
        project_dir: Working directory for the community (default: current dir)
        overrides: Optional dimension overrides, e.g. {"authority": "distributed", "communication": "mesh"}
    """
    agents = max(2, min(20, agents))

    session = await manager.create_session(
        task=task,
        org_preset=org,
        agent_count=agents,
        model=model,
        max_ticks=max_ticks,
        project_dir=project_dir,
        dimension_overrides=overrides,
    )

    return json.dumps({
        "session_id": session.id,
        "status": "running",
        "task": task,
        "org": org,
        "agents": agents,
        "model": model,
        "max_ticks": max_ticks,
        "project_dir": str(session.project_dir),
    }, indent=2)


@mcp.tool()
async def agentciv_status(session_id: str | None = None) -> str:
    """Check the status of running agent communities.

    Without a session_id, lists all sessions (active and completed).
    With a session_id, returns detailed status: current tick, recent
    events, agent activity, and full chronicle report if completed.

    Args:
        session_id: Specific session to check (omit for overview of all sessions)
    """
    if session_id is None:
        sessions = manager.list_sessions()
        if not sessions:
            return json.dumps({
                "sessions": [],
                "message": "No active sessions. Use agentciv_solve() to spawn a community.",
            }, indent=2)
        return json.dumps({"sessions": sessions}, indent=2)

    session = manager.get_session(session_id)
    if not session:
        return json.dumps({"error": f"Session '{session_id}' not found"}, indent=2)

    result = session.to_dict()

    # Include chronicle report if the engine has one and run is complete
    if (
        session.engine
        and session.engine.chronicle
        and session.status.value in ("completed", "stopped")
    ):
        report = session.engine.chronicle.generate_report()
        result["chronicle"] = report.to_dict()

    return json.dumps(result, indent=2)


@mcp.tool()
async def agentciv_intervene(
    session_id: str,
    message: str | None = None,
    redirect: str | None = None,
    force_meta_tick: bool = False,
    adjust: dict[str, str] | None = None,
    stop: bool = False,
) -> str:
    """Intervene in a running agent community (gardener mode).

    You don't command the garden — you shape conditions and prune.
    Agents see your interventions as events and messages. They don't
    know a human (or AI assistant) is gardening.

    Multiple interventions can be applied in a single call. They are
    queued and take effect at the start of the next tick.

    Args:
        session_id: The session to intervene in
        message: Broadcast a message visible to all agents (e.g. "Focus on tests first")
        redirect: Change the task focus entirely (e.g. "Prioritise the auth module")
        force_meta_tick: Force agents to discuss and vote on org restructuring
        adjust: Dict of parameter adjustments (e.g. {"max_messages_per_tick": "5"})
        stop: Gracefully stop the engine after the current tick
    """
    session = manager.get_session(session_id)
    if not session:
        return json.dumps({"error": f"Session '{session_id}' not found"}, indent=2)

    if session.status.value != "running":
        return json.dumps({
            "error": f"Session is {session.status.value}, not running. Cannot intervene.",
        }, indent=2)

    interventions_applied = []

    if stop:
        await manager.stop_session(session_id)
        interventions_applied.append("stop: engine will halt after current tick")

    if message:
        manager.intervene(session_id, Intervention(
            type="message",
            content=message,
            tick=session.current_tick,
        ))
        interventions_applied.append(f"message: \"{message[:80]}\"")

    if redirect:
        manager.intervene(session_id, Intervention(
            type="redirect",
            content=redirect,
            tick=session.current_tick,
        ))
        interventions_applied.append(f"redirect: \"{redirect[:80]}\"")

    if force_meta_tick:
        manager.intervene(session_id, Intervention(
            type="meta_tick",
            tick=session.current_tick,
        ))
        interventions_applied.append("force_meta_tick: agents will discuss org restructuring")

    if adjust:
        manager.intervene(session_id, Intervention(
            type="adjust",
            parameters=adjust,
            tick=session.current_tick,
        ))
        interventions_applied.append(f"adjust: {adjust}")

    if not interventions_applied:
        return json.dumps({
            "error": (
                "No intervention specified. Provide at least one of: "
                "message, redirect, force_meta_tick, adjust, or stop."
            ),
        }, indent=2)

    return json.dumps({
        "session_id": session_id,
        "current_tick": session.current_tick,
        "interventions": interventions_applied,
        "message": (
            f"Applied {len(interventions_applied)} intervention(s). "
            f"Will take effect at the start of tick {session.current_tick + 1}."
        ),
    }, indent=2)


@mcp.tool()
async def agentciv_info() -> str:
    """Full reference: all organisational presets, dimensions, and features."""
    # Load preset descriptions from YAML files
    presets_dir = Path(__file__).parent.parent.parent / "presets"
    presets: dict[str, str] = {}
    if presets_dir.exists():
        for p in sorted(presets_dir.glob("*.yaml")):
            lines = []
            with open(p) as f:
                for line in f:
                    line = line.strip()
                    if not line or line == "#":
                        continue
                    if "AgentCiv Engine" in line:
                        continue
                    if line.startswith("#"):
                        lines.append(line.lstrip("# ").strip())
                    else:
                        break
            presets[p.stem] = " ".join(lines)

    return json.dumps({
        "presets": presets,
        "dimensions": {
            dim: values for dim, values in KNOWN_DIMENSIONS.items()
        },
        "features": {
            "enable_specialisation": "Agents develop skills through practice",
            "enable_relationships": "Track collaboration history and trust",
            "enable_attention_map": "Shared view of who's working on what",
            "enable_git_branches": "Branch-per-agent with auto-merge",
            "require_review": "Mandatory peer review before merge",
            "meta_tick_interval": "How often agents discuss org restructuring (0=never, default 10 for auto)",
        },
        "auto_mode": (
            "org='auto' — agents design their own organisational structure. "
            "Starts with a meta-tick where agents discuss how to organise. "
            "Every N ticks they can propose and vote on restructuring any "
            "of the 9 dimensions. Structure evolves based on what works."
        ),
        "defaults": {
            "org": "collaborative",
            "agents": 4,
            "max_ticks": 50,
        },
    }, indent=2)


@mcp.tool()
async def agentciv_configure(
    preset: str = "collaborative",
    authority: str | None = None,
    communication: str | None = None,
    roles: str | None = None,
    decisions: str | None = None,
    incentives: str | None = None,
    information: str | None = None,
    conflict: str | None = None,
    groups: str | None = None,
    adaptation: str | None = None,
) -> str:
    """Preview an organisational configuration before spawning.

    Start from a preset and override specific dimensions. Returns the
    full configuration that would be used, so you can check it before
    committing to a run.

    Valid values for each dimension can be found via agentciv_info().

    Args:
        preset: Base preset to start from (default: collaborative)
        authority: Override authority model (hierarchy, flat, distributed, rotating, consensus, anarchic)
        communication: Override communication pattern (hub-spoke, mesh, clustered, broadcast, whisper)
        roles: Override role assignment (assigned, emergent, rotating, fixed, fluid)
        decisions: Override decision making (top-down, consensus, majority, meritocratic, autonomous)
        incentives: Override incentive structure (collaborative, competitive, reputation, market)
        information: Override information sharing (transparent, need-to-know, curated, filtered)
        conflict: Override conflict resolution (authority, negotiated, voted, adjudicated)
        groups: Override group formation (imposed, self-selected, task-based, persistent, temporary)
        adaptation: Override adaptation strategy (static, evolving, cyclical, real-time)
    """
    config = EngineConfig.from_preset(preset)
    dims = config.org_dimensions

    overrides_applied = {}
    for dim_name, dim_value in [
        ("authority", authority), ("communication", communication),
        ("roles", roles), ("decisions", decisions),
        ("incentives", incentives), ("information", information),
        ("conflict", conflict), ("groups", groups),
        ("adaptation", adaptation),
    ]:
        if dim_value is not None:
            setattr(dims, dim_name, dim_value)
            overrides_applied[dim_name] = dim_value

    return json.dumps({
        "preset": preset,
        "overrides_applied": overrides_applied,
        "dimensions": {
            "authority": dims.authority,
            "communication": dims.communication,
            "roles": dims.roles,
            "decisions": dims.decisions,
            "incentives": dims.incentives,
            "information": dims.information,
            "conflict": dims.conflict,
            "groups": dims.groups,
            "adaptation": dims.adaptation,
        },
        "parameters": {
            "meta_tick_interval": config.parameters.meta_tick_interval,
            "enable_git_branches": config.parameters.enable_git_branches,
            "enable_specialisation": config.parameters.enable_specialisation,
            "require_review": config.parameters.require_review,
            "task_claim_mode": config.parameters.task_claim_mode,
            "communication_range": config.parameters.communication_range,
        },
        "message": (
            f"Configuration preview for '{preset}'"
            + (f" with {len(overrides_applied)} override(s)" if overrides_applied else "")
            + ". Pass these as overrides to agentciv_solve()."
        ),
    }, indent=2)


@mcp.tool()
async def agentciv_experiment(
    task: str,
    orgs: str = "collaborative,competitive,meritocratic",
    runs_per_org: int = 1,
    agents: int = 4,
    model: str = "claude-sonnet-4-6",
    max_ticks: int = 30,
    project_dir: str = ".",
) -> str:
    """Run the same task under multiple org configs and compare results.

    This is the research flywheel for Computational Organisational Theory.
    Compare how different organisational structures affect task completion,
    communication patterns, file output, and emergent behaviour.

    WARNING: This runs synchronously and can take a long time depending
    on the number of orgs, runs, and ticks. For quick experiments, use
    low max_ticks (10-15) and few runs.

    Args:
        task: What the community should build or solve
        orgs: Comma-separated org presets to compare (default: collaborative,competitive,meritocratic)
        runs_per_org: Runs per config for statistical validity (default: 1)
        agents: Number of agents per run (default: 4)
        model: LLM model (default: claude-sonnet-4-6)
        max_ticks: Maximum ticks per run (default: 30)
        project_dir: Source project directory (default: current dir)
    """
    from ..experiment import run_experiment

    org_list = [o.strip() for o in orgs.split(",")]

    result = await run_experiment(
        task=task,
        orgs=org_list,
        runs_per_org=runs_per_org,
        agent_count=agents,
        model=model,
        max_ticks=max_ticks,
        source_dir=project_dir,
    )

    return json.dumps({
        "summary": result.to_terminal(),
        "data": result.to_dict(),
    }, indent=2)


# ---------------------------------------------------------------------------
# Max Plan Mode — step-by-step orchestration tools
# ---------------------------------------------------------------------------


@mcp.tool()
async def agentciv_orchestrate_start(
    task: str,
    org: str = "collaborative",
    agents: int = 4,
    max_ticks: int = 50,
    project_dir: str = ".",
    overrides: dict[str, str] | None = None,
) -> str:
    """Start a Max Plan Mode session — NO API key needed.

    In Max Plan Mode, the engine is a pure orchestrator. It does NOT make
    LLM calls — YOU (the MCP client) drive agent cognition. This means
    users on a Claude Max subscription can run AgentCiv with zero API costs.

    The flow:
      1. orchestrate_start → returns session_id and agent contexts
      2. For each agent context, YOU make the LLM call and get tool calls
      3. orchestrate_act → engine executes tool calls, returns results
      4. Repeat 2-3 until agent signals 'done'
      5. orchestrate_tick → engine does post-tick processing
      6. Repeat 2-5 until should_continue is False

    Args:
        task: What the community should build or solve
        org: Organisational preset (default: collaborative)
        agents: Number of agents, 2-20 (default: 4)
        max_ticks: Maximum execution rounds (default: 50)
        project_dir: Working directory (default: current dir)
        overrides: Dimension overrides, e.g. {"authority": "distributed"}
    """
    agents = max(2, min(20, agents))

    session_id, init_result = await manager.create_step_session(
        task=task,
        org_preset=org,
        agent_count=agents,
        max_ticks=max_ticks,
        project_dir=project_dir,
        dimension_overrides=overrides,
    )

    # Prepare the first tick and return agent contexts
    step = manager.get_step_session(session_id)
    contexts = await step.prepare_tick()

    return json.dumps({
        "session_id": session_id,
        "mode": "max_plan",
        "init": init_result,
        "tick": 1,
        "agent_contexts": contexts,
        "instructions": (
            "For each agent_context above:\n"
            "1. Send system_prompt + user_prompt + tools to your LLM\n"
            "2. Extract tool_use blocks from the response\n"
            "3. Call agentciv_orchestrate_act(session_id, agent_id, tool_calls)\n"
            "4. If agent_done is False, repeat with the updated context\n"
            "5. When all agents are done, call agentciv_orchestrate_tick(session_id)"
        ),
    }, indent=2)


@mcp.tool()
async def agentciv_orchestrate_act(
    session_id: str,
    agent_id: str,
    tool_calls: list[dict] | None = None,
    tokens_used: int = 0,
) -> str:
    """Submit tool calls for an agent in Max Plan Mode.

    After making an LLM call with the agent's context, extract the tool_use
    blocks and submit them here. The engine executes the tools and returns
    results that you feed back into the next LLM call.

    Each tool_call dict should have:
      - tool_call_id (or id): unique ID from the LLM response
      - tool_name (or name): the tool that was called
      - arguments (or input): the tool's input parameters

    Args:
        session_id: The step session ID
        agent_id: Which agent is acting (e.g. "agent_0")
        tool_calls: List of tool calls from the LLM response
        tokens_used: Tokens consumed by the LLM call (optional, for budget tracking)
    """
    step = manager.get_step_session(session_id)
    if not step:
        return json.dumps({"error": f"Step session '{session_id}' not found"}, indent=2)

    if not tool_calls:
        return json.dumps({"error": "No tool_calls provided"}, indent=2)

    result = await step.act(
        agent_id=agent_id,
        tool_calls=tool_calls,
        tokens_used=tokens_used,
    )

    return json.dumps(result, indent=2)


@mcp.tool()
async def agentciv_orchestrate_tick(session_id: str) -> str:
    """Complete the current tick and prepare the next one.

    Call this after all agents have finished acting. The engine does
    post-tick processing (git merge, attention map, relationships,
    auto-org proposals, chronicle) and prepares agent contexts for
    the next tick.

    Returns tick summary + next tick's agent contexts (if continuing).

    Args:
        session_id: The step session ID
    """
    step = manager.get_step_session(session_id)
    if not step:
        return json.dumps({"error": f"Step session '{session_id}' not found"}, indent=2)

    # Complete current tick
    tick_result = await step.complete_tick()

    response: dict = {
        "tick_summary": tick_result,
    }

    # Prepare next tick if we should continue
    if tick_result.get("should_continue", True):
        next_contexts = await step.prepare_tick()
        if next_contexts:
            response["next_tick"] = step.engine.tick
            response["agent_contexts"] = next_contexts
        else:
            response["finished"] = True
            final = await step.finish()
            response["final"] = final
    else:
        response["finished"] = True
        final = await step.finish()
        response["final"] = final

    return json.dumps(response, indent=2)


@mcp.tool()
async def agentciv_orchestrate_status(session_id: str) -> str:
    """Check the status of a Max Plan Mode step session.

    Shows current phase, tick, and per-agent progress.

    Args:
        session_id: The step session ID
    """
    step = manager.get_step_session(session_id)
    if not step:
        return json.dumps({"error": f"Step session '{session_id}' not found"}, indent=2)

    return json.dumps(step.get_status(), indent=2)


# ---------------------------------------------------------------------------
# Benchmark Mode — run established benchmarks via Max Plan
# ---------------------------------------------------------------------------


@mcp.tool()
async def agentciv_benchmark_start(
    task_id: str,
    preset: str = "collaborative",
    agents: int = 4,
    max_ticks: int | None = None,
    output_dir: str = "benchmark_results/internal",
) -> str:
    """Start a benchmark task in Max Plan Mode.

    Sets up the task (seed files, working directory), creates a step session,
    and returns agent contexts for the first tick. Drive agents using the
    standard orchestrate_act/orchestrate_tick flow. When done, call
    agentciv_benchmark_verify() to score the result.

    Available internal tasks: fizzbuzz, kv_store, todo_api, calculator,
    data_pipeline, web_scraper. Use 'all' to list them.

    Args:
        task_id: Benchmark task ID (e.g. 'fizzbuzz') or 'all' to list tasks
        preset: Organisational preset (default: collaborative)
        agents: Number of agents (default: 4)
        max_ticks: Override max ticks (default: task-specific)
        output_dir: Where to save results (default: benchmark_results/internal)
    """
    from ..benchmark.tasks import TASK_BANK, get_all_tasks

    # List mode
    if task_id == "all":
        tasks = get_all_tasks()
        return json.dumps({
            "available_tasks": [
                {
                    "id": t.id,
                    "name": t.name,
                    "difficulty": t.difficulty,
                    "max_ticks": t.max_ticks,
                    "expected_files": t.expected_files,
                }
                for t in tasks
            ],
        }, indent=2)

    # Look up task
    if task_id not in TASK_BANK:
        return json.dumps({"error": f"Unknown task: {task_id}. Use task_id='all' to list."}, indent=2)

    task = TASK_BANK[task_id]
    ticks = max_ticks or task.max_ticks

    # Create temp project directory with seed files
    import tempfile
    tmpdir = tempfile.mkdtemp(prefix=f"agentciv_bench_{task_id}_")
    project = Path(tmpdir) / "project"
    project.mkdir()

    for fpath, content in task.seed_files.items():
        full = project / fpath
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content)

    # Create step session
    session_id, init_result = await manager.create_step_session(
        task=task.description,
        org_preset=preset,
        agent_count=agents,
        max_ticks=ticks,
        project_dir=str(project),
    )

    # Store benchmark context for verify step
    manager.store_benchmark_context(session_id, {
        "task_id": task_id,
        "task": task,
        "preset": preset,
        "project_dir": str(project),
        "tmpdir": tmpdir,
        "output_dir": output_dir,
        "agent_count": agents,
    })

    # Prepare first tick
    step = manager.get_step_session(session_id)
    contexts = await step.prepare_tick()

    return json.dumps({
        "session_id": session_id,
        "mode": "benchmark_max_plan",
        "task": {
            "id": task_id,
            "name": task.name,
            "difficulty": task.difficulty,
            "description": task.description[:200],
        },
        "preset": preset,
        "agents": agents,
        "max_ticks": ticks,
        "project_dir": str(project),
        "tick": 1,
        "agent_contexts": contexts,
        "instructions": (
            "Drive agents using agentciv_orchestrate_act() and "
            "agentciv_orchestrate_tick() as normal. When the run finishes "
            "(should_continue=False), call agentciv_benchmark_verify(session_id) "
            "to score the result and save data."
        ),
    }, indent=2)


@mcp.tool()
async def agentciv_benchmark_verify(session_id: str, run_index: int = 0) -> str:
    """Verify and score a completed benchmark run.

    Runs the task's verification script, extracts metrics, computes analysis
    (network + temporal), and saves all data to the output directory.

    Call this after the orchestrate loop finishes (should_continue=False).

    Args:
        session_id: The benchmark step session ID
        run_index: Run index for this (task, preset) combo (default: 0)
    """
    import time
    from ..benchmark.metrics import VerificationResult, extract_metrics
    from ..benchmark.analysis import analyse_run
    from ..benchmark.runner import _verify

    step = manager.get_step_session(session_id)
    if not step:
        return json.dumps({"error": f"Session '{session_id}' not found"}, indent=2)

    ctx = manager.get_benchmark_context(session_id)
    if not ctx:
        return json.dumps({"error": "No benchmark context — was this started with agentciv_benchmark_start?"}, indent=2)

    task = ctx["task"]
    project = Path(ctx["project_dir"])

    # Generate chronicle report
    report = None
    if step.engine.chronicle:
        report = step.engine.chronicle.generate_report()

        # Inject per-agent token consumption
        initial_budget = step.engine.config.parameters.token_budget_per_agent
        report.tokens_per_agent = {
            a.state.identity.id: max(0, initial_budget - a.state.token_budget_remaining)
            for a in step.engine.agents
        }

    if not report:
        return json.dumps({"error": "No chronicle report available"}, indent=2)

    # Run verification
    verification = _verify(task, project)

    # Extract metrics
    metrics = extract_metrics(
        report, verification,
        wall_time=0.0,  # wall time not tracked in Max Plan mode
        agent_tokens=report.tokens_per_agent,
    )

    # Run analysis
    analysis = analyse_run(report, metrics)

    # Save per-run JSON
    output_dir = Path(ctx["output_dir"])
    runs_dir = output_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{ctx['task_id']}_{ctx['preset']}_run{run_index}.json"
    data = {
        "task_id": ctx["task_id"],
        "preset": ctx["preset"],
        "run_index": run_index,
        "mode": "max_plan",
        "agent_count": ctx["agent_count"],
        "success": verification.passed,
        "metrics": {
            "completion_rate": metrics.completion_rate,
            "ticks_used": metrics.ticks_used,
            "files_produced": metrics.files_produced,
            "test_pass_rate": metrics.test_pass_rate,
            "communication_volume": metrics.communication_volume,
            "merge_conflicts": metrics.merge_conflicts,
            "emergent_specialisation": round(metrics.emergent_specialisation, 4),
            "file_completeness": metrics.file_completeness,
            "total_tokens": metrics.total_tokens,
            "tokens_per_agent": metrics.tokens_per_agent,
        },
        "analysis": analysis.to_dict(),
        "verification": {
            "passed": verification.passed,
            "tests_total": verification.tests_total,
            "tests_passed": verification.tests_passed,
            "tests_failed": verification.tests_failed,
            "output": verification.output,
        },
        "report": report.to_dict(),
    }

    filepath = runs_dir / filename
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    # Clean up step session
    await step.finish()

    return json.dumps({
        "session_id": session_id,
        "task_id": ctx["task_id"],
        "preset": ctx["preset"],
        "run_index": run_index,
        "verification": {
            "passed": verification.passed,
            "tests_total": verification.tests_total,
            "tests_passed": verification.tests_passed,
        },
        "metrics": {
            "completion_rate": metrics.completion_rate,
            "ticks_used": metrics.ticks_used,
            "test_pass_rate": metrics.test_pass_rate,
            "total_tokens": metrics.total_tokens,
            "communication_volume": metrics.communication_volume,
            "merge_conflicts": metrics.merge_conflicts,
            "emergent_specialisation": round(metrics.emergent_specialisation, 4),
        },
        "analysis_summary": {
            "network_density": analysis.network.graph_density,
            "hub_spoke_ratio": analysis.network.hub_spoke_ratio,
            "convergence_tick": analysis.temporal.convergence_tick,
        },
        "saved_to": str(filepath),
        "message": (
            f"{'PASSED' if verification.passed else 'FAILED'}: "
            f"{verification.tests_passed}/{verification.tests_total} tests. "
            f"Data saved to {filepath}"
        ),
    }, indent=2)


# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------


@mcp.resource("agentciv://presets")
async def list_presets() -> str:
    """List all available organisational presets."""
    presets_dir = Path(__file__).parent.parent.parent / "presets"
    presets = []
    if presets_dir.exists():
        for p in sorted(presets_dir.glob("*.yaml")):
            presets.append(p.stem)
    return json.dumps({"presets": presets}, indent=2)


@mcp.resource("agentciv://presets/{name}")
async def get_preset(name: str) -> str:
    """Get the full YAML configuration for a specific preset."""
    presets_dir = Path(__file__).parent.parent.parent / "presets"
    preset_file = presets_dir / f"{name}.yaml"
    if not preset_file.exists():
        return json.dumps({"error": f"Preset '{name}' not found"}, indent=2)
    return preset_file.read_text()


@mcp.resource("agentciv://dimensions")
async def list_dimensions() -> str:
    """List all 9 organisational dimensions and their possible values."""
    return json.dumps(KNOWN_DIMENSIONS, indent=2)


@mcp.resource("agentciv://sessions")
async def get_sessions_resource() -> str:
    """List all engine sessions (active and completed)."""
    return json.dumps({"sessions": manager.list_sessions()}, indent=2)


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------


@mcp.prompt()
def solve_task(task: str, org: str = "collaborative") -> str:
    """Template for spawning an agent community."""
    return (
        f"Spawn an AgentCiv community to work on this task:\n\n"
        f"Task: {task}\n"
        f"Organisation: {org}\n\n"
        f"Steps:\n"
        f"1. Use agentciv_solve(task='{task}', org='{org}') to start\n"
        f"2. Monitor with agentciv_status(session_id='...')\n"
        f"3. Guide with agentciv_intervene(session_id='...', message='...')\n"
        f"4. Check final results when status shows 'completed'"
    )


@mcp.prompt()
def compare_orgs(task: str) -> str:
    """Template for running a comparative organisational experiment."""
    return (
        f"Run a comparative experiment to find the best org structure for:\n\n"
        f"Task: {task}\n\n"
        f"Use agentciv_experiment(task='{task}', "
        f"orgs='collaborative,competitive,meritocratic,auto') to compare "
        f"how different organisational structures handle this task. "
        f"Analyse the results: ticks to completion, file output, "
        f"communication patterns, and org dynamics (for auto runs)."
    )


@mcp.prompt()
def design_org(goal: str) -> str:
    """Template for designing a custom organisational configuration."""
    return (
        f"Design a custom organisational structure optimised for:\n\n"
        f"Goal: {goal}\n\n"
        f"Steps:\n"
        f"1. Use agentciv_info() to see available dimensions and values\n"
        f"2. Use agentciv_configure() to preview configurations\n"
        f"3. Choose a base preset and override dimensions as needed\n"
        f"4. Spawn with agentciv_solve(task='...', org='preset', "
        f"overrides={{...}})"
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def run_server() -> None:
    """Start the MCP server on stdio transport."""
    mcp.run()
