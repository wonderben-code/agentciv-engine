"""MCP display formatting — beautiful output for Claude Code.

The CLI has Rich panels, coloured agent names, teaching error messages,
celebration moments, contextual tips, and proactive guidance. MCP mode
needs ALL of this, just in a different medium. Claude Code renders
markdown and monospace text beautifully, so we use:
  - Unicode box-drawing for panels and separators
  - Markdown tables for data grids
  - Status indicators (✓ ✗ ● ◆ ★)
  - Structured sections with headers
  - Agent names prominently displayed
  - Celebration moments (success, milestones)
  - Contextual tips and "what's next" guidance
  - Crown jewel callouts (auto mode)

Every MCP tool calls a formatter here. The formatted text is the primary
response — JSON data is embedded at the end for programmatic use.

Design principles:
  - Same data, same clarity, different medium
  - Teaching, not reporting — every response guides the user
  - Celebrate wins — passing tests, completing runs, first benchmarks
  - Proactive — suggest what to try next based on context
  - Crown jewel — org='auto' highlighted at every natural opportunity
"""

from __future__ import annotations

import json
from typing import Any


# ── Agent display ──────────────────────────────────────────────────

AGENT_MARKERS = {
    "Atlas": "◆", "Nova": "●", "Sage": "▲", "Flux": "■",
    "Echo": "◇", "Drift": "○", "Pulse": "△", "Cinder": "□",
    "Wren": "★", "Quill": "☆", "Ember": "◈", "Loom": "◎",
    "Haze": "⬡", "Strider": "⬢", "Crux": "✦", "Rune": "✧",
    "Fern": "❖", "Glyph": "⊕", "Shard": "⊗", "Tide": "⊙",
}


def _agent_marker(name: str) -> str:
    return AGENT_MARKERS.get(name, "●")


def _agent_display(name: str) -> str:
    return f"{_agent_marker(name)} {name}"


# ── Box drawing ──────────────────────────────────────────────────

def _header_box(title: str, subtitle: str = "") -> str:
    """Top-level header box with double-line border."""
    width = max(len(title), len(subtitle)) + 6
    width = max(width, 50)
    top = "╔" + "═" * width + "╗"
    bot = "╚" + "═" * width + "╝"
    title_line = "║  " + title + " " * (width - len(title) - 2) + "║"
    lines = [top, title_line]
    if subtitle:
        sub_line = "║  " + subtitle + " " * (width - len(subtitle) - 2) + "║"
        lines.append(sub_line)
    lines.append(bot)
    return "\n".join(lines)


def _section_header(title: str) -> str:
    """Section header with single-line underline."""
    return f"\n  {title}\n  {'─' * len(title)}"


def _separator() -> str:
    return "\n  " + "─" * 50


def _kv(key: str, value: Any, indent: int = 2) -> str:
    """Key-value line."""
    pad = " " * indent
    return f"{pad}{key}: {value}"


def _status(passed: bool, message: str) -> str:
    """Status line with checkmark or cross."""
    mark = "✓" if passed else "✗"
    return f"  {mark} {message}"


def _md_table(headers: list[str], rows: list[list[str]]) -> str:
    """Render a markdown table."""
    if not rows:
        return ""
    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(str(cell)))

    # Header
    header = "  | " + " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers)) + " |"
    sep = "  | " + " | ".join("─" * widths[i] for i in range(len(headers))) + " |"
    lines = [header, sep]

    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            w = widths[i] if i < len(widths) else len(str(cell))
            cells.append(str(cell).ljust(w))
        lines.append("  | " + " | ".join(cells) + " |")

    return "\n".join(lines)


# ── Celebrations & guidance ────────────────────────────────────────


def _celebration(message: str) -> str:
    """A visual celebration moment."""
    width = len(message) + 6
    return "\n".join([
        "",
        "  ┌" + "─" * width + "┐",
        "  │   " + message + "   │",
        "  └" + "─" * width + "┘",
        "",
    ])


def _tip(text: str) -> str:
    """A contextual suggestion."""
    return f"\n  ✦ {text}"


def _whats_next(items: list[str]) -> str:
    """A 'what's next' guidance section."""
    lines = ["\n  What's next"]
    lines.append("  " + "─" * 20)
    for item in items:
        lines.append(f"    → {item}")
    return "\n".join(lines)


def _generate_post_run_tips(
    org_preset: str = "",
    merge_conflicts: int = 0,
    total_messages: int = 0,
    restructures: int = 0,
) -> list[str]:
    """Generate contextual tips based on run characteristics."""
    tips = []

    if merge_conflicts >= 2 and org_preset != "code-review":
        tips.append(f"{merge_conflicts} merge conflicts — try preset='code-review' for mandatory peer review")

    if total_messages == 0 and org_preset not in ("collaborative", "pair-programming", "startup"):
        tips.append("Agents didn't communicate — try preset='collaborative' for tighter coordination")

    if org_preset != "auto":
        tips.append("Try preset='auto' — agents design their own structure through proposals and votes")

    if restructures > 0:
        tips.append("Use agentciv_intervene() to guide agents mid-run (gardener mode)")

    return tips[:2]  # Max 2 tips per response


# ── Tool formatters ──────────────────────────────────────────────


def format_solve(data: dict) -> str:
    """Format agentciv_solve response."""
    lines = [
        _header_box("AgentCiv Engine", "Community spawned — agents are working"),
        "",
        _kv("Task", data["task"]),
        _kv("Org", data["org"]),
        _kv("Agents", data["agents"]),
        _kv("Model", data["model"]),
        _kv("Max ticks", data["max_ticks"]),
        "",
        _status(True, f"Session {data['session_id']} running"),
        "",
    ]

    # Guidance
    sid = data["session_id"]
    lines.append(_whats_next([
        f"Check progress: agentciv_status(session_id='{sid}')",
        f"Guide agents: agentciv_intervene(session_id='{sid}', message='Focus on tests')",
        f"Stop run: agentciv_intervene(session_id='{sid}', stop=True)",
    ]))

    # Crown jewel hint
    if data.get("org") != "auto":
        lines.append(_tip(
            "The crown jewel: try org='auto' — agents vote on their own structure"
        ))

    return "\n".join(lines)


def format_status_overview(data: dict) -> str:
    """Format agentciv_status (no session_id) response."""
    sessions = data.get("sessions", [])
    if not sessions:
        lines = [
            _header_box("AgentCiv Engine", "Ready to spawn agent communities"),
            "",
            "  No active sessions yet.",
            "",
        ]
        lines.append(_whats_next([
            "Max Plan (free): agentciv_orchestrate_start(task='Build a REST API')",
            "API mode: agentciv_solve(task='Build a REST API', org='collaborative')",
            "Explore: agentciv_info() — see all 13 presets and 9 dimensions",
            "★ Try org='auto' — agents design their own structure",
        ]))
        return "\n".join(lines)

    lines = [
        _section_header("Active Sessions"),
        "",
    ]

    headers = ["ID", "Task", "Org", "Status", "Tick", "Agents", "Mode"]
    rows = []
    for s in sessions:
        status = s["status"]
        if status == "completed":
            status = "✓ done"
        elif status == "running":
            status = "● running"
        elif status == "failed":
            status = "✗ failed"
        rows.append([s["id"], s["task"][:40], s["org"], status, s["tick"], str(s["agents"]), s["mode"]])

    lines.append(_md_table(headers, rows))
    return "\n".join(lines)


def format_status_detail(data: dict) -> str:
    """Format agentciv_status (with session_id) response."""
    status = data["status"]
    status_icon = {"completed": "✓", "running": "●", "failed": "✗", "stopped": "■"}.get(status, "?")

    lines = [
        _header_box(f"Session {data['id']}", f"{status_icon} {status.upper()}"),
        "",
        _kv("Task", data["task"]),
        _kv("Org", data["org_preset"]),
        _kv("Agents", data["agent_count"]),
        _kv("Tick", f"{data['current_tick']}/{data['max_ticks']}"),
    ]

    if data.get("error"):
        lines.append(f"\n  ✗ Error: {data['error']}")

    # Recent events
    events = data.get("recent_events", [])
    if events:
        lines.append(_section_header("Recent Activity"))
        for e in events[-15:]:
            tick = f"tick {e['tick']:>3d}" if e.get("tick") else "      "
            lines.append(f"  {tick}  {e['summary']}")

    # Chronicle summary if available
    chronicle = data.get("chronicle")
    if chronicle:
        lines.append("")
        lines.append(_format_chronicle_summary(chronicle))

    return "\n".join(lines)


def _format_chronicle_summary(report: dict) -> str:
    """Format a chronicle report dict into display text."""
    lines = [_section_header("Run Complete")]

    # Build/test status
    status_parts = []
    if report.get("final_build_status") == "passing":
        status_parts.append("✓ build")
    elif report.get("final_build_status") == "failing":
        status_parts.append("✗ build")
    if report.get("final_test_status") == "passing":
        status_parts.append("✓ tests")
    elif report.get("final_test_status") == "failing":
        status_parts.append("✗ tests")
    if status_parts:
        lines.append(f"  {' │ '.join(status_parts)}")

    # Agent contributions
    contributions = report.get("contributions", [])
    if contributions:
        lines.append("")
        lines.append("  Who did what")
        headers = ["Agent", "Files", "Messages", "Focus"]
        rows = []
        for c in contributions:
            name = c.get("agent_name", "?")
            created = len(c.get("files_created", []))
            modified = len(c.get("files_modified", []))
            file_str = f"{created} new, {modified} mod" if (created or modified) else "—"
            msgs = c.get("messages_sent", 0) + c.get("broadcasts_sent", 0)
            msg_str = str(msgs) if msgs else "—"
            tasks = c.get("tasks_claimed", [])
            focus = ", ".join(tasks[:2]) if tasks else "—"
            rows.append([_agent_display(name), file_str, msg_str, focus[:30]])
        lines.append(_md_table(headers, rows))

    # Communication
    total_msgs = report.get("total_messages", 0) + report.get("total_broadcasts", 0)
    if total_msgs:
        lines.append("")
        lines.append(f"  {total_msgs} conversations ({report.get('total_messages', 0)} direct, {report.get('total_broadcasts', 0)} to all)")

    # Git
    merges = report.get("merges_succeeded", 0)
    conflicts = report.get("merge_conflicts", 0)
    if merges or conflicts:
        parts = []
        if merges:
            parts.append(f"✓ {merges} merges")
        if conflicts:
            parts.append(f"✗ {conflicts} conflict{'s' if conflicts != 1 else ''}")
        lines.append(f"  {' │ '.join(parts)}")

    # Org dynamics
    adopted = report.get("restructures_adopted", 0)
    if adopted:
        lines.append("")
        lines.append(f"  ★ Team restructured {adopted} time{'s' if adopted != 1 else ''}")
        for r in report.get("restructure_log", []):
            dim = r.get("dimension", "?")
            old_val = r.get("old_value", "?")
            new_val = r.get("new_value", "?")
            lines.append(f"    tick {r.get('tick', '?')}: {dim}: {old_val} → {new_val}")

    # Timeline highlights
    timeline = report.get("timeline", [])
    if timeline:
        lines.append("")
        lines.append("  Key moments")
        for entry in timeline[:10]:
            tick = entry.get("tick", "?")
            agent = entry.get("agent", "")
            summary = entry.get("summary", "")
            lines.append(f"    tick {tick:>3}  {agent + ' ' if agent else ''}{summary}")

    return "\n".join(lines)


def format_intervene(data: dict) -> str:
    """Format agentciv_intervene response."""
    lines = [
        f"  Session {data['session_id']} — tick {data['current_tick']}",
        "",
    ]
    for intervention in data.get("interventions", []):
        lines.append(_status(True, intervention))
    lines.append("")
    lines.append(f"  Takes effect at tick {data['current_tick'] + 1}")
    return "\n".join(lines)


def format_info(data: dict) -> str:
    """Format agentciv_info response."""
    lines = [
        _header_box("AgentCiv Engine", "Organisational presets, dimensions & features"),
        "",
    ]

    # Presets
    lines.append("  13 Organisational Presets")
    lines.append("  " + "─" * 40)
    headers = ["Preset", "Description"]
    rows = [[name, desc[:60]] for name, desc in data.get("presets", {}).items()]
    lines.append(_md_table(headers, rows))

    # Dimensions
    lines.append("")
    lines.append("  9 Dimensions")
    lines.append("  " + "─" * 40)
    headers = ["Dimension", "Values"]
    rows = [[dim, " → ".join(vals)] for dim, vals in data.get("dimensions", {}).items()]
    lines.append(_md_table(headers, rows))

    # Features
    lines.append("")
    lines.append("  Feature Toggles")
    lines.append("  " + "─" * 40)
    for name, desc in data.get("features", {}).items():
        lines.append(f"    {name:30s}  {desc}")

    # Crown jewel — prominent callout
    lines.append("")
    lines.append("  ┌──────────────────────────────────────────────────┐")
    lines.append("  │  ★ THE CROWN JEWEL: org='auto'                   │")
    lines.append("  │                                                   │")
    lines.append("  │  Agents design their own organisational structure │")
    lines.append("  │  through proposals and votes during meta-ticks.   │")
    lines.append("  │  Structure evolves based on what works.           │")
    lines.append("  └──────────────────────────────────────────────────┘")

    # Getting started guidance
    lines.append(_whats_next([
        "Quick start: agentciv_orchestrate_start(task='Build a REST API')",
        "Compare orgs: agentciv_experiment(task='...', orgs='collaborative,competitive,auto')",
        "Custom config: agentciv_configure(preset='collaborative', authority='distributed')",
    ]))

    return "\n".join(lines)


def format_configure(data: dict) -> str:
    """Format agentciv_configure response."""
    lines = [
        f"  Configuration: {data['preset']}",
    ]
    overrides = data.get("overrides_applied", {})
    if overrides:
        lines.append(f"  Overrides: {', '.join(f'{k}={v}' for k, v in overrides.items())}")
    lines.append("")

    # Dimensions
    lines.append("  Dimensions")
    lines.append("  " + "─" * 40)
    for dim, val in data.get("dimensions", {}).items():
        marker = " ◆" if dim in overrides else ""
        lines.append(f"    {dim:16s}  {val}{marker}")

    # Parameters
    lines.append("")
    lines.append("  Parameters")
    lines.append("  " + "─" * 40)
    for param, val in data.get("parameters", {}).items():
        lines.append(f"    {param:30s}  {val}")

    return "\n".join(lines)


def format_experiment(data: dict) -> str:
    """Format agentciv_experiment response."""
    # The experiment tool already has a summary field
    summary = data.get("summary", "")
    if summary:
        return summary
    return json.dumps(data, indent=2)


# ── Max Plan Mode formatters ──────────────────────────────────────


def format_orchestrate_start(data: dict) -> str:
    """Format agentciv_orchestrate_start response."""
    init = data.get("init", {})
    contexts = data.get("agent_contexts", [])

    # Extract agent names
    agent_names = []
    for ctx in contexts:
        name = ctx.get("agent_name", ctx.get("agent_id", "?"))
        agent_names.append(name)

    agents_display = "  ".join(_agent_display(n) for n in agent_names)
    org = init.get("org_preset", "?")

    lines = [
        _header_box("AgentCiv Engine — Max Plan Mode", "Zero API cost — powered by your subscription"),
        "",
        _kv("Session", data["session_id"]),
        _kv("Task", init.get("task", "?")[:80]),
        _kv("Org", org),
        _kv("Team", f"{len(contexts)} agents"),
        _kv("Max ticks", init.get("max_ticks", "?")),
        "",
        f"  {agents_display}",
        "",
        _status(True, f"Session {data['session_id']} created"),
        _status(True, f"Tick 1 ready — {len(contexts)} agents awaiting actions"),
        "",
        "  Workflow:",
        "    1. For each agent, make an LLM call with the provided context",
        "    2. Call agentciv_orchestrate_act() with the tool calls",
        "    3. Repeat until agent signals done",
        "    4. Call agentciv_orchestrate_tick() when all agents finish",
    ]

    # Crown jewel hint
    if org != "auto":
        lines.append(_tip(
            "★ The crown jewel: try org='auto' — agents propose and vote on "
            "their own organisational structure during meta-ticks"
        ))

    return "\n".join(lines)


def format_orchestrate_act(data: dict) -> str:
    """Format agentciv_orchestrate_act response."""
    agent_id = data.get("agent_id", "?")
    agent_done = data.get("agent_done", False)
    results = data.get("tool_results", [])

    lines = []

    # Summarise tool results
    files_created = []
    files_modified = []
    messages = []
    other_actions = []

    for r in results:
        tool = r.get("tool_name", "")
        result = r.get("result", {})
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except (json.JSONDecodeError, TypeError):
                result = {}

        if tool == "create_file":
            path = result.get("path") or r.get("arguments", {}).get("path", "?")
            files_created.append(path)
        elif tool == "write_file":
            path = result.get("path") or r.get("arguments", {}).get("path", "?")
            files_modified.append(path)
        elif tool == "send_message":
            target = r.get("arguments", {}).get("to", "?")
            messages.append(f"→ {target}")
        elif tool == "broadcast":
            messages.append("→ all")
        elif tool == "done":
            pass  # handled by agent_done flag
        else:
            other_actions.append(tool)

    for f in files_created:
        lines.append(f"  {agent_id} created  {f}")
    for f in files_modified:
        lines.append(f"  {agent_id} modified {f}")
    for m in messages:
        lines.append(f"  {agent_id} {m}")
    for a in other_actions:
        lines.append(f"  {agent_id} {a}")

    if not lines:
        lines.append(f"  {agent_id}: {len(results)} tool call{'s' if len(results) != 1 else ''}")

    # Status
    if agent_done:
        summary_parts = []
        if files_created or files_modified:
            summary_parts.append(f"{len(files_created) + len(files_modified)} files")
        if messages:
            summary_parts.append(f"{len(messages)} message{'s' if len(messages) != 1 else ''}")
        summary = ", ".join(summary_parts) if summary_parts else "done"
        lines.append(f"\n  ✓ {agent_id} done — {summary}")
    else:
        lines.append(f"\n  ● {agent_id} continuing — send next LLM call with updated_context")

    return "\n".join(lines)


def format_orchestrate_tick(data: dict) -> str:
    """Format agentciv_orchestrate_tick response."""
    tick_summary = data.get("tick_summary", {})
    tick = tick_summary.get("tick", "?")
    actions = tick_summary.get("actions", 0)
    should_continue = tick_summary.get("should_continue", False)
    finished = data.get("finished", False)

    is_meta = tick_summary.get("is_meta_tick", False)
    meta_label = " ★ Team Discussion" if is_meta else ""

    lines = [
        f"\n  ── tick {tick} ──────────────────────────────────────{meta_label}",
    ]

    # Git summary
    git = tick_summary.get("git_summary")
    if git:
        lines.append(f"  {git}")

    # Specialisation updates
    specs = tick_summary.get("specialisation_updates", [])
    for s in specs:
        lines.append(f"  ★ {s}")

    lines.append(f"  {actions} action{'s' if actions != 1 else ''}")

    if finished:
        # Celebration moment
        lines.append(_celebration("✓ Run Complete!"))

        # Final report
        final = data.get("final", {})
        chronicle = final.get("chronicle", {}) if final else {}
        if chronicle:
            lines.append(_format_chronicle_summary(chronicle))

            # Post-run tips based on what happened
            org = chronicle.get("org_preset", "")
            conflicts = chronicle.get("merge_conflicts", 0)
            msgs = chronicle.get("total_messages", 0) + chronicle.get("total_broadcasts", 0)
            restructures = chronicle.get("restructures_adopted", 0)
            tips = _generate_post_run_tips(org, conflicts, msgs, restructures)
            for t in tips:
                lines.append(_tip(t))

        # What's next guidance
        lines.append(_whats_next([
            "Compare org structures: run the same task with different presets",
            "Try agentciv_experiment() for automated comparison",
            "Run agentciv_info() to see all 13 presets and 9 dimensions",
        ]))
    else:
        next_tick = data.get("next_tick", tick + 1)
        contexts = data.get("agent_contexts", [])
        lines.append(f"\n  → Tick {next_tick} ready — {len(contexts)} agents awaiting actions")

    return "\n".join(lines)


def format_orchestrate_status(data: dict) -> str:
    """Format agentciv_orchestrate_status response."""
    phase = data.get("phase", "?")
    tick = data.get("tick", "?")
    max_ticks = data.get("max_ticks", "?")

    lines = [
        f"  Session: {phase}  │  Tick: {tick}/{max_ticks}",
    ]

    agents = data.get("agents", {})
    if agents:
        lines.append("")
        for agent_id, info in agents.items():
            status = info.get("status", "?")
            icon = {"acting": "●", "done": "✓", "waiting": "○"}.get(status, "?")
            lines.append(f"  {icon} {agent_id}: {status}")

    return "\n".join(lines)


# ── Benchmark formatters ──────────────────────────────────────────


def format_benchmark_start(data: dict) -> str:
    """Format agentciv_benchmark_start response."""
    # List mode
    if "available_tasks" in data:
        lines = [
            _header_box("AgentCiv Benchmark", "Available tasks"),
            "",
        ]
        headers = ["Task", "Difficulty", "Max Ticks", "Expected Files"]
        rows = []
        for t in data["available_tasks"]:
            diff = t["difficulty"]
            diff_marker = {"simple": "●", "medium": "◆", "hard": "★"}.get(diff, "?")
            rows.append([
                t["id"],
                f"{diff_marker} {diff}",
                str(t["max_ticks"]),
                ", ".join(t["expected_files"]),
            ])
        lines.append(_md_table(headers, rows))
        return "\n".join(lines)

    # Normal start mode
    task = data.get("task", {})
    contexts = data.get("agent_contexts", [])
    agent_names = [ctx.get("agent_name", ctx.get("agent_id", "?")) for ctx in contexts]
    agents_display = "  ".join(_agent_display(n) for n in agent_names)

    diff = task.get("difficulty", "?")
    diff_marker = {"simple": "●", "medium": "◆", "hard": "★"}.get(diff, "?")

    lines = [
        _header_box("AgentCiv Benchmark", f"{task.get('name', '?')} × {data.get('preset', '?')}"),
        "",
        _kv("Task", f"{task.get('id', '?')} ({diff_marker} {diff})"),
        _kv("Preset", data.get("preset", "?")),
        _kv("Team", f"{data.get('agents', '?')} agents"),
        _kv("Max ticks", data.get("max_ticks", "?")),
        "",
        f"  {agents_display}",
        "",
        _status(True, "Seed files written"),
        _status(True, f"Session {data.get('session_id', '?')} created"),
        _status(True, f"Tick 1 ready — {len(contexts)} agents awaiting actions"),
        "",
        "  Drive agents through ticks, then call",
        "  agentciv_benchmark_verify() to score the result.",
    ]
    return "\n".join(lines)


def format_benchmark_verify(data: dict) -> str:
    """Format agentciv_benchmark_verify response."""
    verification = data.get("verification", {})
    metrics = data.get("metrics", {})
    analysis = data.get("analysis_summary", {})
    passed = verification.get("passed", False)
    tests_passed = verification.get("tests_passed", 0)
    tests_total = verification.get("tests_total", 0)

    status_text = "PASSED" if passed else "FAILED"
    status_icon = "✓" if passed else "✗"

    lines = [
        "",
        f"  ══ Benchmark Result {'═' * 30}",
        "",
        f"  {data.get('task_id', '?')} × {data.get('preset', '?')}",
        f"  {status_icon} {status_text} — {tests_passed}/{tests_total} tests",
        "",
    ]

    # Metrics table
    headers = ["Metric", "Value"]
    rows = [
        ["Completion rate", f"{metrics.get('completion_rate', 0):.0%}"],
        ["Test pass rate", f"{metrics.get('test_pass_rate', 0):.0%}"],
        ["Ticks used", str(int(metrics.get("ticks_used", 0)))],
        ["Communication", str(int(metrics.get("communication_volume", 0)))],
        ["Merge conflicts", str(int(metrics.get("merge_conflicts", 0)))],
        ["Specialisation", f"{metrics.get('emergent_specialisation', 0):.3f}"],
    ]
    if metrics.get("total_tokens"):
        rows.append(["Total tokens", f"{metrics['total_tokens']:,}"])
    lines.append(_md_table(headers, rows))

    # Analysis
    if analysis:
        lines.append("")
        lines.append("  Analysis")
        lines.append("  " + "─" * 20)
        if analysis.get("network_density") is not None:
            lines.append(f"    Network density:   {analysis['network_density']:.3f}")
        if analysis.get("hub_spoke_ratio") is not None:
            lines.append(f"    Hub-spoke ratio:   {analysis['hub_spoke_ratio']:.3f}")
        if analysis.get("convergence_tick") is not None:
            lines.append(f"    Convergence tick:  {analysis['convergence_tick']}")

    # Saved location
    saved_to = data.get("saved_to", "")
    if saved_to:
        lines.append("")
        lines.append(f"  ✓ Saved: {saved_to}")

    # Celebration for passing benchmarks
    if passed:
        lines.append(_celebration(
            f"✓ {data.get('task_id', 'Task')} × {data.get('preset', 'preset')} — ALL TESTS PASSED"
        ))
    else:
        lines.append("")
        lines.append(f"  ✗ Some tests failed — check verification output for details")

    # Guidance
    task_id = data.get("task_id", "")
    preset = data.get("preset", "")
    lines.append(_whats_next([
        f"Run same task with different preset to compare org effects",
        f"Try preset='auto' to see if agents find a better structure",
        f"Check benchmark_results/internal/runs/ for accumulated data",
    ]))

    return "\n".join(lines)


def format_benchmark_task_list(data: dict) -> str:
    """Format task list for benchmark."""
    return format_benchmark_start(data)  # Same logic for 'all' mode


# ── Error formatter ──────────────────────────────────────────────


def format_error(error_msg: str, suggestion: str = "") -> str:
    """Format an error response — teaching, not just reporting.

    Answers three questions: What happened? Why? What should I try?
    """
    lines = [
        "",
        "  ┌─ Error ─────────────────────────────────────┐",
        f"  │  ✗ {error_msg}",
    ]
    if suggestion:
        lines.append(f"  │  → {suggestion}")
    lines.append("  └─────────────────────────────────────────────┘")
    return "\n".join(lines)


# ── Generic data attachment ──────────────────────────────────────


def with_data(display: str, data: dict) -> str:
    """Combine formatted display text with JSON data.

    The display text is what the user sees. The JSON data is available
    for programmatic use (e.g., extracting session_id).
    """
    json_str = json.dumps(data, indent=2)
    return f"{display}\n\n<details>\n<summary>Raw data</summary>\n\n```json\n{json_str}\n```\n</details>"
