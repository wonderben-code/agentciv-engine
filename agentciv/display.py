"""Rich terminal display — making the invisible visible.

Every extraordinary thing the engine does (agents communicating, voting,
restructuring, resolving conflicts, developing specialisations) needs to
come alive in the terminal. This module is the single source of all
terminal rendering.

Design principles:
  - Agent names get consistent colours — you can visually track who's who
  - Events are formatted for human reading, not debugging
  - Auto mode votes/proposals are visual events, not log lines
  - The run summary tells a story, not a data dump
  - Errors teach, not just report
  - Jargon translated to plain English (dimension values, event types)
"""

from __future__ import annotations

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.padding import Padding

# Shared console — stderr=False means stdout (rich defaults to stderr in some contexts)
console = Console(highlight=False)

# ── Agent colour palette ──────────────────────────────────────────────
# Each agent name maps to a consistent colour so users can visually
# track who's doing what across the entire run.

AGENT_COLOURS: dict[str, str] = {
    "Atlas": "bold blue",
    "Nova": "bold magenta",
    "Sage": "bold green",
    "Flux": "bold yellow",
    "Echo": "bold cyan",
    "Drift": "bold bright_blue",
    "Pulse": "bold bright_red",
    "Cinder": "bold bright_yellow",
    "Wren": "bold bright_green",
    "Quill": "bold bright_magenta",
    "Ember": "bold red",
    "Loom": "bold bright_cyan",
    "Haze": "bold blue",
    "Strider": "bold green",
    "Crux": "bold yellow",
    "Rune": "bold magenta",
    "Fern": "bold bright_green",
    "Glyph": "bold cyan",
    "Shard": "bold bright_blue",
    "Tide": "bold bright_cyan",
}

# Fallback colours for unknown agent names
_FALLBACK_COLOURS = [
    "bold blue", "bold magenta", "bold green", "bold yellow",
    "bold cyan", "bold red", "bold bright_blue", "bold bright_magenta",
]


def agent_style(name: str) -> str:
    """Get the consistent colour style for an agent name."""
    if name in AGENT_COLOURS:
        return AGENT_COLOURS[name]
    # Deterministic fallback based on name hash
    return _FALLBACK_COLOURS[hash(name) % len(_FALLBACK_COLOURS)]


def agent_text(name: str) -> Text:
    """Render an agent name in its signature colour."""
    return Text(name, style=agent_style(name))


# ── Plain English translations ────────────────────────────────────────
# Dimension values are internal shorthand. Users should see human language.

DIMENSION_LABELS: dict[str, str] = {
    "authority": "Leadership",
    "communication": "How agents talk",
    "roles": "How roles work",
    "decisions": "How decisions are made",
    "incentives": "What drives agents",
    "information": "What agents can see",
    "conflict": "How disagreements resolve",
    "groups": "How teams form",
    "adaptation": "How the org evolves",
}

VALUE_LABELS: dict[str, dict[str, str]] = {
    "authority": {
        "hierarchy": "one agent leads",
        "flat": "everyone is equal",
        "distributed": "authority is shared",
        "rotating": "leadership rotates",
        "consensus": "group agreement required",
        "anarchic": "no formal authority",
    },
    "communication": {
        "hub-spoke": "messages go through the lead",
        "mesh": "everyone talks directly",
        "clustered": "small group conversations",
        "broadcast": "announcements to all",
        "whisper": "private 1-on-1 only",
    },
    "roles": {
        "assigned": "roles are pre-assigned",
        "emergent": "roles develop naturally",
        "rotating": "roles rotate between agents",
        "fixed": "roles never change",
        "fluid": "roles shift as needed",
    },
    "decisions": {
        "top-down": "the lead decides",
        "consensus": "everyone must agree",
        "majority": "majority vote wins",
        "meritocratic": "best track record decides",
        "autonomous": "each agent decides for themselves",
    },
    "incentives": {
        "collaborative": "shared team success",
        "competitive": "individual performance",
        "reputation": "earned credibility",
        "market": "bid for tasks",
    },
    "information": {
        "transparent": "everyone sees everything",
        "need-to-know": "only what's relevant to you",
        "curated": "filtered by the lead",
        "filtered": "filtered by role",
    },
    "conflict": {
        "authority": "the lead resolves it",
        "negotiated": "agents work it out together",
        "voted": "the team votes",
        "adjudicated": "a neutral party decides",
    },
    "groups": {
        "imposed": "groups are pre-assigned",
        "self-selected": "agents choose their groups",
        "task-based": "groups form around tasks",
        "persistent": "groups stay the same",
        "temporary": "groups are temporary",
    },
    "adaptation": {
        "static": "structure never changes",
        "evolving": "structure changes gradually",
        "cyclical": "periodic restructuring",
        "real-time": "structure changes constantly",
    },
}


def humanise_dimension(dimension: str) -> str:
    """Translate a dimension name to plain English."""
    return DIMENSION_LABELS.get(dimension, dimension)


def humanise_value(dimension: str, value: str) -> str:
    """Translate a dimension value to plain English."""
    dim_values = VALUE_LABELS.get(dimension, {})
    return dim_values.get(value, value)


def humanise_change(dimension: str, old_value: str, new_value: str) -> str:
    """Describe an org change in plain English."""
    dim_label = humanise_dimension(dimension)
    old_label = humanise_value(dimension, old_value)
    new_label = humanise_value(dimension, new_value)
    return f"{dim_label}: {old_label} → {new_label}"


# ── Engine lifecycle ──────────────────────────────────────────────────

def show_engine_start(
    task: str,
    agent_count: int,
    org_preset: str,
    max_ticks: int,
    agent_names: list[str],
    model: str = "",
    lead_agent: str | None = None,
    gardener: bool = False,
) -> None:
    """Display the engine start header — the first thing users see."""
    # Build agent name display with colours
    names = Text()
    for i, name in enumerate(agent_names):
        if i > 0:
            names.append("  ", style="dim")
        names.append(name, style=agent_style(name))

    # Build info lines
    content = Text()
    content.append("Task: ", style="dim")
    content.append(task, style="bold white")
    content.append("\n")
    content.append(f"Team: {agent_count} agents", style="dim")
    content.append(" │ ", style="dim")
    content.append("Org: ", style="dim")
    content.append(org_preset, style="bold")
    content.append(" │ ", style="dim")
    content.append(f"Max: {max_ticks} ticks", style="dim")
    if model:
        content.append(" │ ", style="dim")
        content.append(model, style="dim")
    content.append("\n\n")
    content.append(names)

    if lead_agent:
        content.append("\n")
        content.append("Lead: ", style="dim")
        content.append(lead_agent, style=agent_style(lead_agent))

    if gardener:
        content.append("\n")
        content.append("🌱 Gardener mode ON", style="bold green")
        content.append(" — type instructions between ticks", style="dim")

    panel = Panel(
        content,
        title="[bold]AgentCiv Engine[/bold]",
        border_style="bright_blue",
        padding=(1, 2),
    )
    console.print()
    console.print(panel)
    console.print()


def show_engine_stopped(tick: int) -> None:
    """Display engine completion."""
    console.print()
    console.print(
        f"  [dim]Engine stopped at tick {tick}[/dim]"
    )
    console.print()


# ── Tick display ──────────────────────────────────────────────────────

def show_tick_start(tick: int, is_meta_tick: bool = False) -> None:
    """Display tick separator."""
    if is_meta_tick:
        console.print(
            f"\n  [bold bright_yellow]── tick {tick:3d} ── ★ Team discussion ──"
            f"──────────────────────[/bold bright_yellow]"
        )
        console.print(
            "  [dim bright_yellow]  Agents are discussing how to restructure their team[/dim bright_yellow]"
        )
    else:
        console.print(f"\n  [dim]── tick {tick:3d} ──────────────────────────────────────────[/dim]")


def show_tick_end(tick: int, actions: int) -> None:
    """Display tick summary."""
    console.print(f"  [dim]{actions} actions[/dim]")


# ── Agent events ──────────────────────────────────────────────────────

def show_file_created(tick: int, agent_name: str, file_path: str) -> None:
    """Agent created a file."""
    name = Text(f"  {agent_name:>8s}", style=agent_style(agent_name))
    console.print(name, Text(" created  ", style="green"), Text(file_path, style="bold"))


def show_file_modified(tick: int, agent_name: str, file_path: str) -> None:
    """Agent modified a file."""
    name = Text(f"  {agent_name:>8s}", style=agent_style(agent_name))
    console.print(name, Text(" modified ", style="yellow"), Text(file_path, style="bold"))


def show_message_sent(tick: int, sender_name: str, target_names: list[str], preview: str) -> None:
    """Agent sent a direct message."""
    sender = Text(f"  {sender_name:>8s}", style=agent_style(sender_name))
    arrow = Text(" → ", style="dim")
    targets = Text(", ".join(target_names), style="bold")
    content = Text(f": {preview}", style="italic")
    console.print(sender, arrow, targets, content)


def show_broadcast(tick: int, sender_name: str, preview: str) -> None:
    """Agent broadcast to all."""
    sender = Text(f"  {sender_name:>8s}", style=agent_style(sender_name))
    arrow = Text(" → ", style="dim")
    target = Text("all", style="bold dim")
    content = Text(f": {preview}", style="italic")
    console.print(sender, arrow, target, content)


def show_task_claimed(tick: int, agent_name: str, preview: str) -> None:
    """Agent claimed a task."""
    name = Text(f"  {agent_name:>8s}", style=agent_style(agent_name))
    console.print(name, Text(" claimed ", style="cyan"), Text(preview, style="bold"))


def show_tests_passed(tick: int) -> None:
    console.print("  [bold green]       ✓ tests passing[/bold green]")


def show_tests_failed(tick: int) -> None:
    console.print("  [bold red]       ✗ tests failing[/bold red]")


def show_build_passed(tick: int) -> None:
    console.print("  [bold green]       ✓ build passing[/bold green]")


def show_build_failed(tick: int) -> None:
    console.print("  [bold red]       ✗ build failing[/bold red]")


# ── Git events ────────────────────────────────────────────────────────

def show_branch_merged(tick: int, agent_name: str, file_count: int) -> None:
    """Agent's branch was merged."""
    name = Text(f"  {agent_name:>8s}", style=agent_style(agent_name))
    console.print(name, Text(" merged ", style="green"), Text(f"({file_count} files)", style="dim"))


def show_merge_conflict(tick: int, agent_name: str, conflicts: list[str]) -> None:
    """Merge conflict detected."""
    name = Text(f"  {agent_name:>8s}", style=agent_style(agent_name))
    files = ", ".join(conflicts) if conflicts else "unknown files"
    console.print(name, Text(" ✗ CONFLICT ", style="bold red"), Text(files, style="red"))


# ── Organisation events ──────────────────────────────────────────────

def show_restructure_proposed(tick: int, agent_name: str, preview: str) -> None:
    """Agent proposed an organisational restructure."""
    name = Text(f"  {agent_name:>8s}", style=agent_style(agent_name))
    console.print(
        name,
        Text(" proposes ", style="bright_yellow"),
        Text(preview, style="bold bright_yellow"),
    )


def show_restructure_adopted(
    tick: int,
    dimension: str,
    old_value: str,
    new_value: str,
    yes_votes: int,
    no_votes: int,
    proposer: str = "",
) -> None:
    """An organisational restructure was adopted by vote."""
    # This is a big moment — make it visually distinct
    # Translate to plain English
    change_text = humanise_change(dimension, old_value, new_value)

    content = Text()
    content.append(change_text, style="bold")
    content.append("\n")
    content.append(f"{yes_votes} agreed", style="green")
    if no_votes > 0:
        content.append(f", {no_votes} disagreed", style="red")
    if proposer:
        content.append(" │ Proposed by ", style="dim")
        content.append(proposer, style=agent_style(proposer))

    panel = Panel(
        content,
        title="[bold bright_yellow]★ The team restructured[/bold bright_yellow]",
        border_style="bright_yellow",
        padding=(0, 1),
    )
    console.print(Padding(panel, (0, 2)))


# ── Chronicle report (run summary) ───────────────────────────────────

def show_chronicle_report(report: Any) -> None:
    """Render a beautiful run summary from a ChronicleReport.

    This is the moment users learn what their agents did. It should
    read like a story, not a data dump.
    """
    # Header
    status_parts = []
    if report.final_build_status == "passing":
        status_parts.append("[green]✓ build[/green]")
    elif report.final_build_status == "failing":
        status_parts.append("[red]✗ build[/red]")
    if report.final_test_status == "passing":
        status_parts.append("[green]✓ tests[/green]")
    elif report.final_test_status == "failing":
        status_parts.append("[red]✗ tests[/red]")
    status = " │ ".join(status_parts) if status_parts else ""

    header = Text()
    header.append(f"\"{report.task}\"", style="italic")
    header.append(f"\n{report.org_preset}", style="bold")
    header.append(f" │ {report.agent_count} agents │ {report.total_ticks} ticks", style="dim")
    if status:
        header.append(" │ ")
    header_line = Text.from_markup(
        f"[italic]\"{report.task}\"[/italic]\n"
        f"[bold]{report.org_preset}[/bold]"
        f"[dim] │ {report.agent_count} agents │ {report.total_ticks} ticks[/dim]"
        + (f" │ {status}" if status else "")
    )

    # Agent contributions table
    agent_table = Table(show_header=True, header_style="bold dim", box=None, padding=(0, 1))
    agent_table.add_column("Agent", style="bold", min_width=10)
    agent_table.add_column("Files", justify="right")
    agent_table.add_column("Messages", justify="right")
    agent_table.add_column("Focus", max_width=40)

    for c in report.contributions:
        created = len(c.files_created)
        modified = len(c.files_modified)
        file_str = f"{created} new, {modified} mod" if (created or modified) else "—"
        msg_str = str(c.messages_sent + c.broadcasts_sent) if (c.messages_sent or c.broadcasts_sent) else "—"
        focus = ", ".join(c.tasks_claimed[:2]) if c.tasks_claimed else "—"
        if len(focus) > 40:
            focus = focus[:37] + "..."

        name_text = Text(c.agent_name, style=agent_style(c.agent_name))
        agent_table.add_row(name_text, file_str, msg_str, focus)

    # Communication summary — human-friendly
    comm_lines = []
    if report.total_messages or report.total_broadcasts:
        total = report.total_messages + report.total_broadcasts
        comm_lines.append(
            f"[dim]{total} total conversations "
            f"({report.total_messages} direct, {report.total_broadcasts} to the whole team)[/dim]"
        )
    if report.communication_pairs:
        sorted_pairs = sorted(
            report.communication_pairs.items(),
            key=lambda x: x[1], reverse=True,
        )
        top = sorted_pairs[0]
        exchange_word = "exchange" if top[1] == 1 else "exchanges"
        comm_lines.append(f"[dim]Most active pair: {top[0]} ({top[1]} {exchange_word})[/dim]")

    # Git summary — plain language
    git_lines = []
    if report.merges_succeeded or report.merge_conflicts:
        parts = []
        if report.merges_succeeded:
            parts.append(f"[green]{report.merges_succeeded} successful merges[/green]")
        if report.merge_conflicts:
            parts.append(
                f"[red]{report.merge_conflicts} conflict"
                f"{'s' if report.merge_conflicts != 1 else ''} "
                f"(agents edited the same file)[/red]"
            )
        git_lines.append(" │ ".join(parts))

    # Org dynamics — in plain English
    org_lines = []
    if report.restructures_proposed:
        org_lines.append(
            f"The team discussed {report.restructures_proposed} change"
            f"{'s' if report.restructures_proposed != 1 else ''} to how they work — "
            f"[bold]{report.restructures_adopted} adopted[/bold]"
        )
        for r in report.restructure_log:
            dim = r.get("dimension", "?")
            old_val = r.get("old_value", "?")
            new_val = r.get("new_value", "?")
            yes = r.get("yes_votes", 0)
            no = r.get("no_votes", 0)
            change = humanise_change(dim, old_val, new_val)
            org_lines.append(
                f"  [dim]tick {r.get('tick', '?')}:[/dim] "
                f"[bold bright_yellow]{change}[/bold bright_yellow] "
                f"[dim]({yes} agreed, {no} disagreed)[/dim]"
            )

    # Compose the full report
    sections = []
    sections.append(header_line)
    sections.append(Text(""))

    # Agent contributions
    sections.append(Text.from_markup("[bold]Who did what[/bold]"))
    sections.append(agent_table)

    if comm_lines:
        sections.append(Text(""))
        sections.append(Text.from_markup("[bold]How they communicated[/bold]"))
        for line in comm_lines:
            sections.append(Text.from_markup(f"  {line}"))

    if git_lines:
        sections.append(Text(""))
        sections.append(Text.from_markup("[bold]Code integration[/bold]"))
        for line in git_lines:
            sections.append(Text.from_markup(f"  {line}"))

    if org_lines:
        sections.append(Text(""))
        sections.append(Text.from_markup("[bold]How the team evolved[/bold]"))
        for line in org_lines:
            sections.append(Text.from_markup(f"  {line}"))

    # Timeline highlights (top 10)
    if report.timeline:
        sections.append(Text(""))
        sections.append(Text.from_markup("[bold]Key moments[/bold]"))
        for entry in report.timeline[:12]:
            agent_str = f" {entry.agent}" if entry.agent else ""
            sections.append(Text.from_markup(
                f"  [dim]tick {entry.tick:3d}[/dim]{agent_str} {entry.summary}"
            ))

    # Build the renderables into a single group
    from rich.console import Group
    panel = Panel(
        Group(*sections),
        title="[bold]Run Complete[/bold]",
        border_style="bright_blue",
        padding=(1, 2),
    )
    console.print()
    console.print(panel)
    console.print()


# ── Experiment report ────────────────────────────────────────────────

def show_experiment_report(result: Any) -> None:
    """Render a beautiful experiment comparison."""
    header = Text.from_markup(
        f"[italic]\"{result.task}\"[/italic]\n"
        f"[dim]{result.agent_count} agents │ {result.max_ticks} max ticks │ "
        f"{len(result.orgs)} configs × {result.runs_per_org} runs │ {result.model}[/dim]"
    )

    # Comparison table
    table = Table(show_header=True, header_style="bold", box=None, padding=(0, 1))
    table.add_column("Org", style="bold", min_width=14)
    table.add_column("Ticks", justify="right")
    table.add_column("Files", justify="right")
    table.add_column("Messages", justify="right")
    table.add_column("Broadcasts", justify="right")
    table.add_column("Merges", justify="right")
    table.add_column("Conflicts", justify="right")

    for org in result.orgs:
        org_runs = [r for r in result.runs if r.org_preset == org and r.success]
        if not org_runs:
            table.add_row(org, "[red]FAILED[/red]", "", "", "", "", "")
            continue

        for run in org_runs:
            r = run.report
            label = org
            if result.runs_per_org > 1:
                label += f" (run {run.run_index + 1})"
            conflict_style = "red" if r.merge_conflicts > 0 else "dim"
            table.add_row(
                label,
                str(r.total_ticks),
                str(len(r.files_created)),
                str(r.total_messages),
                str(r.total_broadcasts),
                str(r.merges_succeeded),
                Text(str(r.merge_conflicts), style=conflict_style),
            )

        # Average row for multiple runs
        if len(org_runs) > 1:
            avg_ticks = sum(r.report.total_ticks for r in org_runs) / len(org_runs)
            avg_files = sum(len(r.report.files_created) for r in org_runs) / len(org_runs)
            avg_msgs = sum(r.report.total_messages for r in org_runs) / len(org_runs)
            table.add_row(
                Text("  ↳ average", style="dim italic"),
                Text(f"{avg_ticks:.1f}", style="dim"),
                Text(f"{avg_files:.1f}", style="dim"),
                Text(f"{avg_msgs:.1f}", style="dim"),
                "", "", "",
            )

    sections = [header, Text(""), table]

    # Auto-org dynamics — plain English
    auto_runs = [r for r in result.runs if r.org_preset == "auto" and r.success]
    if auto_runs:
        sections.append(Text(""))
        sections.append(Text.from_markup(
            "[bold bright_yellow]How auto-mode teams self-organised[/bold bright_yellow]"
        ))
        for run in auto_runs:
            r = run.report
            if r.restructures_adopted:
                for change in r.restructure_log:
                    dim = change.get("dimension", "?")
                    old_val = change.get("old_value", "?")
                    new_val = change.get("new_value", "?")
                    human_change = humanise_change(dim, old_val, new_val)
                    sections.append(Text.from_markup(
                        f"  [dim]run {run.run_index + 1}:[/dim] "
                        f"[bold bright_yellow]{human_change}[/bold bright_yellow]"
                    ))
            else:
                sections.append(Text.from_markup(
                    f"  [dim]run {run.run_index + 1}: team kept their initial structure[/dim]"
                ))

    from rich.console import Group
    panel = Panel(
        Group(*sections),
        title="[bold]Experiment Results[/bold]",
        border_style="bright_blue",
        padding=(1, 2),
    )
    console.print()
    console.print(panel)
    console.print()


# ── Info display ──────────────────────────────────────────────────────

def show_info(presets: list[tuple[str, str]], dimensions: dict[str, list[str]], toggles: list[tuple[str, str]]) -> None:
    """Display available presets, dimensions, and toggles beautifully."""
    # Presets table
    preset_table = Table(show_header=True, header_style="bold", box=None, padding=(0, 1))
    preset_table.add_column("Preset", style="bold cyan", min_width=20)
    preset_table.add_column("Description")
    for name, desc in presets:
        preset_table.add_row(f"--org {name}", desc)

    # Dimensions table
    dim_table = Table(show_header=True, header_style="bold", box=None, padding=(0, 1))
    dim_table.add_column("Dimension", style="bold", min_width=16)
    dim_table.add_column("Values", style="dim")
    for dim, values in dimensions.items():
        dim_table.add_row(dim, " → ".join(values))

    # Toggles table
    toggle_table = Table(show_header=True, header_style="bold", box=None, padding=(0, 1))
    toggle_table.add_column("Toggle", style="bold", min_width=30)
    toggle_table.add_column("Description")
    for name, desc in toggles:
        toggle_table.add_row(name, desc)

    from rich.console import Group
    panel = Panel(
        Group(
            Text.from_markup("[bold]13 Organisational Presets[/bold]"),
            preset_table,
            Text(""),
            Text.from_markup("[bold]9 Dimensions[/bold] [dim](community-expandable)[/dim]"),
            dim_table,
            Text(""),
            Text.from_markup("[bold]Feature Toggles[/bold] [dim](configurable in YAML)[/dim]"),
            toggle_table,
            Text(""),
            Text.from_markup("[dim]Add custom dimensions, presets, and parameters in your YAML config.[/dim]"),
        ),
        title="[bold]AgentCiv Engine[/bold]",
        border_style="bright_blue",
        padding=(1, 2),
    )
    console.print()
    console.print(panel)
    console.print()


# ── History display ──────────────────────────────────────────────────

def show_history_stats(stats: dict[str, Any]) -> None:
    """Display learning history stats."""
    content = []
    content.append(Text.from_markup(f"Total runs: [bold]{stats['total_runs']}[/bold]"))

    if stats["total_runs"] > 0:
        content.append(Text.from_markup(
            f"Successful: [green]{stats['successful_runs']}[/green]"
        ))
        content.append(Text.from_markup(
            f"Unique presets: {stats['unique_presets']}"
        ))
        content.append(Text(""))
        content.append(Text.from_markup("[bold]Quality by preset[/bold]"))

        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Preset", style="bold", min_width=20)
        table.add_column("Quality", justify="right")
        for preset, avg in stats["preset_avg_quality"].items():
            # Colour code quality
            quality_style = "green" if avg >= 0.7 else "yellow" if avg >= 0.4 else "red"
            table.add_row(preset, Text(f"{avg:.3f}", style=quality_style))
        content.append(table)
    else:
        content.append(Text.from_markup(
            "[dim]No runs recorded yet. Run some tasks to build learning data.[/dim]"
        ))

    from rich.console import Group
    panel = Panel(
        Group(*content),
        title="[bold]Learning History[/bold]",
        border_style="bright_blue",
        padding=(1, 2),
    )
    console.print()
    console.print(panel)
    console.print()


def show_learning_insights(insights: Any) -> None:
    """Display learning insights for a task."""
    content = []
    content.append(Text.from_markup(
        f"[italic]\"{insights.task_keywords}\"[/italic]"
    ))
    content.append(Text.from_markup(
        f"[dim]{insights.matching_runs} matching runs / {insights.total_history} total[/dim]"
    ))

    if insights.preset_rankings:
        content.append(Text(""))
        content.append(Text.from_markup("[bold]Best presets[/bold]"))
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Preset", style="bold", min_width=20)
        table.add_column("Quality", justify="right")
        table.add_column("Runs", justify="right", style="dim")
        for p in insights.preset_rankings[:8]:
            quality_style = "green" if p.avg_quality >= 0.7 else "yellow" if p.avg_quality >= 0.4 else "red"
            table.add_row(p.preset, Text(f"{p.avg_quality:.3f}", style=quality_style), f"({p.run_count})")
        content.append(table)

    if insights.dimension_insights:
        content.append(Text(""))
        content.append(Text.from_markup("[bold]Best dimensions[/bold]"))
        for d in insights.dimension_insights:
            quality_style = "green" if d.avg_quality >= 0.7 else "yellow" if d.avg_quality >= 0.4 else "red"
            content.append(Text.from_markup(
                f"  {d.dimension:16s} → [bold]{d.value}[/bold] "
                f"[{quality_style}]({d.avg_quality:.3f})[/{quality_style}]"
            ))

    if not insights.has_data():
        content.append(Text(""))
        content.append(Text.from_markup(
            "[dim]Not enough similar runs for recommendations yet.[/dim]"
        ))

    from rich.console import Group
    panel = Panel(
        Group(*content),
        title="[bold]Learning Insights[/bold]",
        border_style="bright_blue",
        padding=(1, 2),
    )
    console.print()
    console.print(panel)
    console.print()


# ── Setup display ────────────────────────────────────────────────────

def show_setup_welcome() -> None:
    """Display setup welcome banner."""
    console.print()
    panel = Panel(
        Text.from_markup(
            "[bold white]Welcome to AgentCiv Engine![/bold white]\n"
            "[dim]Let's get your custom AI agent team set up.[/dim]"
        ),
        border_style="bright_blue",
        padding=(1, 2),
    )
    console.print(panel)
    console.print()


def show_setup_check(label: str, value: str = "", success: bool = True) -> None:
    """Display a setup check result."""
    mark = "[green]✓[/green]" if success else "[red]✗[/red]"
    suffix = f" [dim]{value}[/dim]" if value else ""
    console.print(f"  {mark} {label}{suffix}")


def show_setup_celebration() -> None:
    """Display the post-setup celebration."""
    content = Text.from_markup(
        "[bold bright_green]CONGRATULATIONS![/bold bright_green] "
        "[bold white]AgentCiv Engine is installed.[/bold white]\n\n"
        "[bold]13 team structures[/bold] await you — with [bold]9 dimensions[/bold] to\n"
        "shape how your agents communicate, make decisions,\n"
        "and resolve conflicts.\n\n"
        "The crown jewel: [bold bright_yellow]auto mode[/bold bright_yellow] — "
        "your agents self-organise,\n"
        "proposing and voting on their own structure in real\n"
        "time. You just set the goal.\n\n"
        "[bold]Time to spawn your first team![/bold]"
    )
    panel = Panel(
        content,
        border_style="bright_green",
        padding=(1, 2),
    )
    console.print()
    console.print(panel)
    console.print()


def show_setup_next_steps_mcp() -> None:
    """Display MCP mode next steps."""
    console.print(Text.from_markup("[bold]YOUR FIRST RUN[/bold]"))
    console.print(Text.from_markup("[dim]─────────────────────────────────────[/dim]"))
    console.print(Text.from_markup("Open Claude Code in this directory and say:"))
    console.print()
    console.print(Text.from_markup('  [bold cyan]"Use agentciv to build a REST API with 4 agents"[/bold cyan]'))
    console.print()
    console.print(Text.from_markup("Shape your team however you want:"))
    console.print()
    console.print(Text.from_markup('  [dim]"Use a meritocratic team to refactor this module"[/dim]'))
    console.print(Text.from_markup('  [dim]"Set up a pair-programming duo for this bug"[/dim]'))
    console.print(Text.from_markup('  [dim]"Use --org auto and let the agents figure it out"[/dim]'))
    console.print()


def show_setup_next_steps_api() -> None:
    """Display API mode next steps."""
    console.print(Text.from_markup("[bold]YOUR FIRST RUN[/bold]"))
    console.print(Text.from_markup("[dim]─────────────────────────────────────[/dim]"))
    console.print(Text.from_markup(
        '  [bold cyan]agentciv solve --task "Build a REST API" --org collaborative[/bold cyan]'
    ))
    console.print(Text.from_markup(
        '  [dim]agentciv solve --task "Build a CLI tool" --org auto[/dim]'
    ))
    console.print(Text.from_markup(
        '  [dim]agentciv experiment --task "Build X" --orgs collaborative,meritocratic,auto[/dim]'
    ))
    console.print()


def show_setup_crown_jewel() -> None:
    """Display the crown jewel callout."""
    console.print(Text.from_markup(
        "[bold bright_yellow]THE CROWN JEWEL: --org auto[/bold bright_yellow]"
    ))
    console.print(Text.from_markup(
        "  Agents design their own team structure through proposals"
    ))
    console.print(Text.from_markup(
        "  and votes. Self-organisation in real time. Try it."
    ))
    console.print()
    console.print(Text.from_markup(
        "[dim]Run 'agentciv info' to explore all 13 team structures.[/dim]"
    ))
    console.print()


# ── Error display ────────────────────────────────────────────────────

def show_error(title: str, message: str, suggestion: str = "") -> None:
    """Display a teaching error message.

    Errors should answer three questions:
      1. What happened?
      2. Why?
      3. What should I try?
    """
    content = Text()
    content.append(message, style="white")
    if suggestion:
        content.append("\n\n", style="")
        content.append("Try: ", style="bold green")
        content.append(suggestion, style="green")

    panel = Panel(
        content,
        title=f"[bold red]{title}[/bold red]",
        border_style="red",
        padding=(0, 2),
    )
    console.print()
    console.print(panel)
    console.print()


def show_warning(message: str) -> None:
    """Display a warning."""
    console.print(f"  [yellow]⚠ {message}[/yellow]")


def show_success(message: str) -> None:
    """Display a success message."""
    console.print(f"  [green]✓ {message}[/green]")


def show_tip(text: str) -> None:
    """Display a contextual tip."""
    console.print(f"  [dim italic]💡 {text}[/dim italic]")


# ── Progress (for API mode and experiments) ──────────────────────────

def show_scan_result(file_count: int) -> None:
    """Display workspace scan result."""
    console.print(f"  [dim]Scanned project: {file_count} files[/dim]")
    console.print()


def show_experiment_progress(current: int, total: int, org: str, run_idx: int) -> None:
    """Display experiment run progress."""
    console.print(
        f"  [dim][{current}/{total}][/dim] "
        f"[bold]{org}[/bold] [dim](run {run_idx + 1})...[/dim]",
        end="",
    )


def show_experiment_run_done(ticks: int) -> None:
    """Display experiment run completion."""
    console.print(f" [green]done[/green] [dim]({ticks} ticks)[/dim]")


def show_experiment_run_failed(error: str) -> None:
    """Display experiment run failure."""
    console.print(f" [red]FAILED: {error}[/red]")


# ── Test tasks report ─────────────────────────────────────────────────

def _completion_style(rate: float) -> str:
    """Return a colour style based on completion rate thresholds."""
    if rate > 0.8:
        return "green"
    if rate > 0.5:
        return "yellow"
    return "red"


def _fmt_time(seconds: float) -> str:
    """Format seconds as human-readable time."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    if minutes < 60:
        return f"{minutes}m {secs}s"
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours}h {minutes}m"


def _fmt_stat_rich(stat: Any, is_rate: bool = False) -> Text:
    """Format a StatSummary as a rich Text object.

    If is_rate is True, colour-codes based on completion thresholds.
    """
    if stat.std > 0.005:
        label = f"{stat.mean:.2f}\u00b1{stat.std:.2f}"
    else:
        label = f"{stat.mean:.2f}"

    if is_rate:
        return Text(label, style=_completion_style(stat.mean))
    return Text(label)


def show_test_tasks_report(result: Any) -> None:
    """Render a beautiful benchmark report using rich panels and tables.

    Takes a BenchmarkResult and displays:
      - Metadata summary
      - Per-task comparison tables with colour-coded completion rates
      - Overall rankings
    """
    from rich.console import Group

    total_runs = len(result.runs)
    successful = sum(1 for r in result.runs if r.success)
    failed = total_runs - successful

    # Metadata section
    model_label = "mock" if result.config.mock else result.config.model
    meta = Text()
    meta.append("Tasks: ", style="dim")
    meta.append(str(len(result.tasks)), style="bold")
    meta.append(" │ ", style="dim")
    meta.append("Presets: ", style="dim")
    meta.append(str(len(result.presets)), style="bold")
    meta.append(" │ ", style="dim")
    meta.append("Runs per combo: ", style="dim")
    meta.append(str(result.config.runs_per_combo), style="bold")
    meta.append("\n")
    meta.append("Total runs: ", style="dim")
    meta.append(str(total_runs), style="bold")
    meta.append(" (", style="dim")
    if successful:
        meta.append(f"{successful} succeeded", style="green")
    if failed:
        if successful:
            meta.append(", ", style="dim")
        meta.append(f"{failed} failed", style="red")
    meta.append(")", style="dim")
    meta.append("\n")
    meta.append("Model: ", style="dim")
    meta.append(model_label, style="bold")
    meta.append(" │ ", style="dim")
    meta.append("Agents: ", style="dim")
    meta.append(str(result.config.agent_count), style="bold")
    meta.append(" │ ", style="dim")
    meta.append("Wall time: ", style="dim")
    meta.append(_fmt_time(result.total_wall_time), style="bold")

    sections: list[Any] = [meta, Text("")]

    # Per-task comparison tables
    for task_id in result.tasks:
        sections.append(Text.from_markup(f"[bold]{task_id}[/bold]"))

        table = Table(show_header=True, header_style="bold dim", box=None, padding=(0, 1))
        table.add_column("Preset", style="bold", min_width=20)
        table.add_column("Completion", justify="right", min_width=10)
        table.add_column("Ticks", justify="right", min_width=8)
        table.add_column("Files", justify="right", min_width=7)
        table.add_column("Tests", justify="right", min_width=8)
        table.add_column("Messages", justify="right", min_width=9)
        table.add_column("Conflicts", justify="right", min_width=9)
        table.add_column("Specialisation", justify="right", min_width=12)

        for preset in result.presets:
            key = (task_id, preset)
            agg = result.aggregated.get(key)
            if not agg:
                table.add_row(
                    preset,
                    Text("FAILED", style="red"),
                    "", "", "", "", "", "",
                )
                continue

            table.add_row(
                preset,
                _fmt_stat_rich(agg.completion_rate, is_rate=True),
                _fmt_stat_rich(agg.ticks_used),
                _fmt_stat_rich(agg.files_produced),
                _fmt_stat_rich(agg.test_pass_rate, is_rate=True),
                _fmt_stat_rich(agg.communication_volume),
                _fmt_stat_rich(agg.merge_conflicts),
                _fmt_stat_rich(agg.emergent_specialisation),
            )

        sections.append(table)
        sections.append(Text(""))

    # Overall rankings
    rankings = result._compute_rankings()
    if rankings:
        sections.append(Text.from_markup(
            "[bold]Overall Results[/bold] [dim](by completion rate, then average ticks)[/dim]"
        ))

        for i, (preset, score) in enumerate(rankings[:10], 1):
            comp = score["avg_completion"]
            style = _completion_style(comp)
            line = Text()
            line.append(f"  {i:2d}. ", style="dim")
            line.append(f"{preset:20s} ", style="bold")
            line.append("completion: ", style="dim")
            line.append(f"{comp:.2f}", style=style)
            line.append("  average ticks: ", style="dim")
            line.append(f"{score['avg_ticks']:.1f}")
            sections.append(line)

        sections.append(Text(""))

    panel = Panel(
        Group(*sections),
        title="[bold]Test Tasks Report[/bold]",
        border_style="bright_blue",
        padding=(1, 2),
    )
    console.print()
    console.print(panel)
    console.print()


def show_benchmark_tasks_list(tasks: list[Any]) -> None:
    """Render available test tasks as a rich table."""
    from rich.console import Group

    table = Table(show_header=True, header_style="bold", box=None, padding=(0, 1))
    table.add_column("Task ID", style="bold cyan", min_width=20)
    table.add_column("Difficulty", min_width=10)
    table.add_column("Max Ticks", justify="right", min_width=9)
    table.add_column("Expected Files")

    for task in tasks:
        # Colour-code difficulty
        diff_style = {
            "simple": "green",
            "medium": "yellow",
            "hard": "red",
        }.get(task.difficulty, "dim")
        diff_text = Text(task.difficulty, style=diff_style)
        files_str = ", ".join(task.expected_files)

        table.add_row(task.id, diff_text, str(task.max_ticks), files_str)

    hint = Text.from_markup(
        "[dim]Use --tasks fizzbuzz,todo-cli or --tasks simple or --tasks all[/dim]"
    )

    panel = Panel(
        Group(table, Text(""), hint),
        title="[bold]Available Test Tasks[/bold]",
        border_style="bright_blue",
        padding=(1, 2),
    )
    console.print()
    console.print(panel)
    console.print()


# ── Gardener mode ────────────────────────────────────────────────────

def show_gardener_prompt() -> str:
    """Display gardener prompt and get input. Returns the raw input string."""
    try:
        return console.input("[bold green]  🌱 gardener> [/bold green]")
    except (EOFError, KeyboardInterrupt):
        console.print("\n  [dim]Gardener ended the run.[/dim]")
        return ""


def show_gardener_queued(intervention_type: str) -> None:
    """Display queued intervention."""
    console.print(f"  [dim]→ {intervention_type}: queued for next tick[/dim]")
