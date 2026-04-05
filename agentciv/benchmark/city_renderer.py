"""City Grid rendering — ASCII, PNG, heatmap, and radar chart outputs.

Produces the visual evidence for Paper 6: five cities side by side,
contribution heatmaps, and radar quality profiles.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from .city_grid import (
    BuildingType,
    BUILDING_COLOURS,
    BUILDING_NAMES,
    CityGrid,
    ContributionGrid,
    GRID_SIZE,
)
from .city_scorer import CityScore


# ── Terminal colours for ASCII rendering ───────────────────────────────

# ANSI colour codes per building type
_ANSI_COLOURS: dict[BuildingType, str] = {
    BuildingType.RESIDENTIAL: "\033[92m",   # Bright green
    BuildingType.COMMERCIAL: "\033[94m",    # Bright blue
    BuildingType.INDUSTRIAL: "\033[37m",    # White/grey
    BuildingType.PARK: "\033[32m",          # Green
    BuildingType.ROAD: "\033[90m",          # Dark grey
    BuildingType.HOSPITAL: "\033[91m",      # Red
    BuildingType.SCHOOL: "\033[93m",        # Yellow
    BuildingType.EMPTY: "\033[90m",         # Dark grey
}
_RESET = "\033[0m"


# ── ASCII Renderer ─────────────────────────────────────────────────────

def render_ascii(grid: CityGrid, colour: bool = True) -> str:
    """Render a city grid as colour-coded terminal text.

    Returns a string with ANSI colour codes (if colour=True),
    row/column labels, and a legend.
    """
    lines = []

    # Column headers
    header = "    " + " ".join(f"{c}" for c in range(GRID_SIZE))
    lines.append(header)
    lines.append("    " + "─" * (GRID_SIZE * 2 - 1))

    for r in range(GRID_SIZE):
        row_parts = []
        for c in range(GRID_SIZE):
            bt = grid.get(r, c)
            ch = bt.value
            if colour:
                row_parts.append(f"{_ANSI_COLOURS[bt]}{ch}{_RESET}")
            else:
                row_parts.append(ch)
        lines.append(f" {r:2d}│ " + " ".join(row_parts))

    # Legend
    lines.append("")
    legend_parts = []
    for bt in BuildingType:
        name = BUILDING_NAMES[bt]
        if colour:
            legend_parts.append(f"{_ANSI_COLOURS[bt]}{bt.value}{_RESET}={name}")
        else:
            legend_parts.append(f"{bt.value}={name}")
    lines.append("  " + "  ".join(legend_parts))

    return "\n".join(lines)


# ── PNG Renderer ───────────────────────────────────────────────────────

def render_png(
    grid: CityGrid,
    path: str | Path,
    cell_size: int = 60,
    title: str | None = None,
    scores: CityScore | None = None,
) -> Path:
    """Render a city grid as a colour PNG image.

    Each cell is a coloured square with a building type label.
    Optionally includes a title and score bar.

    Returns the output path.
    """
    from PIL import Image, ImageDraw, ImageFont

    path = Path(path)
    margin = 20
    label_height = 30 if title else 0
    score_height = 25 if scores else 0
    legend_height = 30

    width = margin * 2 + GRID_SIZE * cell_size
    height = (
        margin * 2
        + label_height
        + GRID_SIZE * cell_size
        + score_height
        + legend_height
    )

    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Try to get a reasonable font, fall back to default
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 11)
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except (OSError, IOError):
        font = ImageFont.load_default()
        small_font = font
        title_font = font

    y_offset = margin

    # Title
    if title:
        draw.text((margin, y_offset), title, fill=(0, 0, 0), font=title_font)
        y_offset += label_height

    # Grid cells
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            bt = grid.get(r, c)
            colour = BUILDING_COLOURS[bt]

            x = margin + c * cell_size
            y = y_offset + r * cell_size

            # Cell fill
            draw.rectangle(
                [x, y, x + cell_size - 1, y + cell_size - 1],
                fill=colour,
                outline=(200, 200, 200),
            )

            # Cell label (building type char)
            text_colour = (255, 255, 255) if bt in (
                BuildingType.ROAD, BuildingType.INDUSTRIAL
            ) else (0, 0, 0)
            bbox = draw.textbbox((0, 0), bt.value, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            tx = x + (cell_size - tw) // 2
            ty = y + (cell_size - th) // 2
            draw.text((tx, ty), bt.value, fill=text_colour, font=font)

    y_offset += GRID_SIZE * cell_size + 5

    # Score bar
    if scores:
        score_text = (
            f"Coverage: {scores.coverage:.0f}  "
            f"Access: {scores.accessibility:.0f}  "
            f"Zoning: {scores.zoning:.0f}  "
            f"Diversity: {scores.diversity:.0f}  "
            f"Connect: {scores.connectivity:.0f}  "
            f"│ Aggregate: {scores.aggregate:.1f}"
        )
        draw.text((margin, y_offset), score_text, fill=(80, 80, 80), font=small_font)
        y_offset += score_height

    # Legend
    legend_x = margin
    for bt in BuildingType:
        if bt == BuildingType.EMPTY:
            continue
        colour = BUILDING_COLOURS[bt]
        draw.rectangle(
            [legend_x, y_offset, legend_x + 12, y_offset + 12],
            fill=colour,
            outline=(150, 150, 150),
        )
        draw.text(
            (legend_x + 16, y_offset - 1),
            BUILDING_NAMES[bt],
            fill=(80, 80, 80),
            font=small_font,
        )
        bbox = draw.textbbox((0, 0), BUILDING_NAMES[bt], font=small_font)
        legend_x += 16 + (bbox[2] - bbox[0]) + 12

    img.save(path)
    return path


# ── Contribution Heatmap Renderer ──────────────────────────────────────

# Distinct colours for up to 10 agents
_AGENT_COLOURS = [
    (76, 175, 80),    # Green
    (33, 150, 243),   # Blue
    (255, 152, 0),    # Orange
    (156, 39, 176),   # Purple
    (0, 188, 212),    # Cyan
    (244, 67, 54),    # Red
    (255, 235, 59),   # Yellow
    (121, 85, 72),    # Brown
    (233, 30, 99),    # Pink
    (96, 125, 139),   # Blue-grey
]


def render_heatmap(
    contributions: ContributionGrid,
    path: str | Path,
    cell_size: int = 60,
    title: str | None = None,
) -> Path:
    """Render a contribution heatmap showing which agent placed each cell.

    Each agent gets a distinct colour. Unmodified cells are white.
    Returns the output path.
    """
    from PIL import Image, ImageDraw, ImageFont

    path = Path(path)
    margin = 20
    label_height = 30 if title else 0
    legend_height = 35

    width = margin * 2 + GRID_SIZE * cell_size
    height = margin * 2 + label_height + GRID_SIZE * cell_size + legend_height

    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except (OSError, IOError):
        font = ImageFont.load_default()
        title_font = font

    y_offset = margin

    if title:
        draw.text((margin, y_offset), title, fill=(0, 0, 0), font=title_font)
        y_offset += label_height

    # Map agent IDs to colours
    unique_agents = sorted(contributions.get_unique_agents())
    agent_colour_map: dict[str, tuple[int, int, int]] = {}
    for i, agent_id in enumerate(unique_agents):
        agent_colour_map[agent_id] = _AGENT_COLOURS[i % len(_AGENT_COLOURS)]

    # Draw cells
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            agent_id = contributions.agents[r][c]
            colour = agent_colour_map.get(agent_id, (240, 240, 240)) if agent_id else (240, 240, 240)

            x = margin + c * cell_size
            y = y_offset + r * cell_size

            draw.rectangle(
                [x, y, x + cell_size - 1, y + cell_size - 1],
                fill=colour,
                outline=(200, 200, 200),
            )

            # Label with agent name (truncated)
            if agent_id:
                label = agent_id[:6]
                text_colour = (255, 255, 255) if _luminance(colour) < 128 else (0, 0, 0)
                bbox = draw.textbbox((0, 0), label, font=font)
                tw = bbox[2] - bbox[0]
                tx = x + (cell_size - tw) // 2
                ty = y + (cell_size - 18) // 2
                draw.text((tx, ty), label, fill=text_colour, font=font)

    y_offset += GRID_SIZE * cell_size + 8

    # Legend
    legend_x = margin
    for agent_id, colour in agent_colour_map.items():
        draw.rectangle(
            [legend_x, y_offset, legend_x + 14, y_offset + 14],
            fill=colour,
            outline=(150, 150, 150),
        )
        draw.text((legend_x + 18, y_offset), agent_id, fill=(80, 80, 80), font=font)
        bbox = draw.textbbox((0, 0), agent_id, font=font)
        legend_x += 18 + (bbox[2] - bbox[0]) + 16

    img.save(path)
    return path


def _luminance(rgb: tuple[int, int, int]) -> float:
    """Perceived luminance (0-255)."""
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


# ── Radar Chart ────────────────────────────────────────────────────────

def render_radar(
    scores_by_preset: dict[str, CityScore],
    path: str | Path,
    title: str = "Quality Profile by Organisation",
) -> Path:
    """Render a 5-axis radar chart overlaying all preset quality profiles.

    Each preset is a coloured polygon on the same axes.
    Axes: Coverage, Accessibility, Zoning, Diversity, Connectivity.

    Returns the output path.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    path = Path(path)
    dimensions = ["Coverage", "Accessibility", "Zoning", "Diversity", "Connectivity"]
    n_dims = len(dimensions)

    # Angles for each axis
    angles = [n * 2 * math.pi / n_dims for n in range(n_dims)]
    angles.append(angles[0])  # Close the polygon

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection="polar"))

    # Colours for presets
    preset_colours = [
        "#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#00BCD4",
        "#F44336", "#FFEB3B", "#795548", "#E91E63", "#607D8B",
        "#8BC34A", "#3F51B5", "#FF5722",
    ]

    for i, (preset, score) in enumerate(scores_by_preset.items()):
        values = [
            score.coverage,
            score.accessibility,
            score.zoning,
            score.diversity,
            score.connectivity,
        ]
        values.append(values[0])  # Close polygon

        colour = preset_colours[i % len(preset_colours)]
        ax.plot(angles, values, "o-", linewidth=2, label=preset, color=colour)
        ax.fill(angles, values, alpha=0.1, color=colour)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dimensions, size=11)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], size=8, color="grey")
    ax.set_title(title, size=14, y=1.08)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=9)

    plt.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return path


# ── Side-by-Side Comparison ────────────────────────────────────────────

def render_comparison(
    grids: dict[str, CityGrid],
    path: str | Path,
    scores: dict[str, CityScore] | None = None,
    cell_size: int = 40,
) -> Path:
    """Render multiple city grids side by side for comparison.

    This is the hero image of Paper 6: five cities, one per preset,
    visually demonstrating that different org structures → different cities.

    Returns the output path.
    """
    from PIL import Image, ImageDraw, ImageFont

    path = Path(path)
    n_grids = len(grids)
    if n_grids == 0:
        raise ValueError("No grids to render")

    gap = 15
    margin = 20
    label_height = 25
    score_height = 20 if scores else 0

    grid_width = GRID_SIZE * cell_size
    total_width = margin * 2 + n_grids * grid_width + (n_grids - 1) * gap
    total_height = margin * 2 + label_height + GRID_SIZE * cell_size + score_height

    img = Image.new("RGB", (total_width, total_height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
        label_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except (OSError, IOError):
        font = ImageFont.load_default()
        label_font = font

    for idx, (preset_name, grid) in enumerate(grids.items()):
        x_origin = margin + idx * (grid_width + gap)
        y_origin = margin

        # Preset label
        draw.text(
            (x_origin, y_origin),
            preset_name.upper(),
            fill=(60, 60, 60),
            font=label_font,
        )
        y_origin += label_height

        # Grid cells
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                bt = grid.get(r, c)
                colour = BUILDING_COLOURS[bt]
                x = x_origin + c * cell_size
                y = y_origin + r * cell_size

                draw.rectangle(
                    [x, y, x + cell_size - 1, y + cell_size - 1],
                    fill=colour,
                    outline=(220, 220, 220),
                )

                # Cell label
                text_colour = (255, 255, 255) if bt in (
                    BuildingType.ROAD, BuildingType.INDUSTRIAL
                ) else (0, 0, 0)
                bbox = draw.textbbox((0, 0), bt.value, font=font)
                tw = bbox[2] - bbox[0]
                th = bbox[3] - bbox[1]
                tx = x + (cell_size - tw) // 2
                ty = y + (cell_size - th) // 2
                draw.text((tx, ty), bt.value, fill=text_colour, font=font)

        # Score below grid
        if scores and preset_name in scores:
            sc = scores[preset_name]
            score_text = f"Aggregate: {sc.aggregate:.1f}"
            draw.text(
                (x_origin, y_origin + GRID_SIZE * cell_size + 4),
                score_text,
                fill=(100, 100, 100),
                font=font,
            )

    img.save(path)
    return path
