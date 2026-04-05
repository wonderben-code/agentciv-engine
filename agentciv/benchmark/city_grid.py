"""City Grid — data model for the city design benchmark task.

A 10x10 grid where agents place building types to design a city.
Different organisational configurations produce visually and
quantitatively different cities. The hero benchmark of Paper 6.

Building types:
  R = Residential    C = Commercial    I = Industrial
  P = Park           . = Road          H = Hospital
  S = School         _ = Empty (unused)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator


class BuildingType(Enum):
    """Building types for the city grid."""
    RESIDENTIAL = "R"
    COMMERCIAL = "C"
    INDUSTRIAL = "I"
    PARK = "P"
    ROAD = "."
    HOSPITAL = "H"
    SCHOOL = "S"
    EMPTY = "_"

    @classmethod
    def from_char(cls, char: str) -> BuildingType:
        """Parse a single character into a BuildingType."""
        for bt in cls:
            if bt.value == char:
                return bt
        raise ValueError(f"Unknown building type: {char!r}")


# Display names for each building type
BUILDING_NAMES: dict[BuildingType, str] = {
    BuildingType.RESIDENTIAL: "Residential",
    BuildingType.COMMERCIAL: "Commercial",
    BuildingType.INDUSTRIAL: "Industrial",
    BuildingType.PARK: "Park",
    BuildingType.ROAD: "Road",
    BuildingType.HOSPITAL: "Hospital",
    BuildingType.SCHOOL: "School",
    BuildingType.EMPTY: "Empty",
}

# Colours for rendering (RGB)
BUILDING_COLOURS: dict[BuildingType, tuple[int, int, int]] = {
    BuildingType.RESIDENTIAL: (76, 175, 80),     # Green
    BuildingType.COMMERCIAL: (33, 150, 243),      # Blue
    BuildingType.INDUSTRIAL: (158, 158, 158),     # Grey
    BuildingType.PARK: (139, 195, 74),            # Light green
    BuildingType.ROAD: (66, 66, 66),              # Dark grey
    BuildingType.HOSPITAL: (244, 67, 54),         # Red
    BuildingType.SCHOOL: (255, 193, 7),           # Amber
    BuildingType.EMPTY: (245, 245, 245),          # Near-white
}

GRID_SIZE = 10


@dataclass
class CityGrid:
    """A 10x10 city grid.

    cells[row][col] is a BuildingType. Row 0 is the top.
    """
    cells: list[list[BuildingType]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.cells:
            self.cells = [
                [BuildingType.EMPTY for _ in range(GRID_SIZE)]
                for _ in range(GRID_SIZE)
            ]

    @property
    def size(self) -> int:
        return GRID_SIZE

    def get(self, row: int, col: int) -> BuildingType:
        """Get the building type at (row, col)."""
        return self.cells[row][col]

    def set(self, row: int, col: int, bt: BuildingType) -> None:
        """Set the building type at (row, col)."""
        self.cells[row][col] = bt

    def iter_cells(self) -> Iterator[tuple[int, int, BuildingType]]:
        """Iterate over all cells yielding (row, col, building_type)."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                yield r, c, self.cells[r][c]

    def neighbours(self, row: int, col: int) -> list[tuple[int, int, BuildingType]]:
        """Get 4-connected neighbours of (row, col)."""
        result = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                result.append((nr, nc, self.cells[nr][nc]))
        return result

    def count(self, bt: BuildingType) -> int:
        """Count cells of a given building type."""
        return sum(1 for _, _, cell in self.iter_cells() if cell == bt)

    def count_non_empty(self) -> int:
        """Count all non-empty cells."""
        return sum(1 for _, _, cell in self.iter_cells() if cell != BuildingType.EMPTY)

    def to_string(self) -> str:
        """Serialize to text format (space-separated chars, one row per line)."""
        lines = []
        for row in self.cells:
            lines.append(" ".join(cell.value for cell in row))
        return "\n".join(lines)

    @classmethod
    def from_string(cls, text: str) -> CityGrid:
        """Parse from text format.

        Accepts:
          - Space-separated chars (R C I P . H S _)
          - Or compact chars without spaces (RCI.PHS_)
        One row per line. Blank lines and comment lines (starting with #) are skipped.
        """
        grid = cls()
        rows = []
        for line in text.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Try space-separated first
            parts = line.split()
            if len(parts) == GRID_SIZE:
                rows.append([BuildingType.from_char(ch) for ch in parts])
            elif len(line.replace(" ", "")) >= GRID_SIZE:
                # Compact format — take first GRID_SIZE non-space chars
                chars = [ch for ch in line if ch != " "][:GRID_SIZE]
                rows.append([BuildingType.from_char(ch) for ch in chars])
            else:
                raise ValueError(
                    f"Row has {len(parts)} columns, expected {GRID_SIZE}: {line!r}"
                )

        if len(rows) != GRID_SIZE:
            raise ValueError(f"Grid has {len(rows)} rows, expected {GRID_SIZE}")

        grid.cells = rows
        return grid

    def to_dict(self) -> dict:
        """Serialize to a JSON-friendly dict."""
        return {
            "size": GRID_SIZE,
            "cells": [[cell.value for cell in row] for row in self.cells],
        }

    @classmethod
    def from_dict(cls, data: dict) -> CityGrid:
        """Deserialize from a JSON dict."""
        grid = cls()
        grid.cells = [
            [BuildingType.from_char(ch) for ch in row]
            for row in data["cells"]
        ]
        return grid


@dataclass
class ContributionGrid:
    """Tracks which agent placed/modified each cell.

    agents[row][col] is the agent ID string, or None if unmodified.
    """
    agents: list[list[str | None]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.agents:
            self.agents = [
                [None for _ in range(GRID_SIZE)]
                for _ in range(GRID_SIZE)
            ]

    def record(self, row: int, col: int, agent_id: str) -> None:
        """Record that an agent placed/modified a cell."""
        self.agents[row][col] = agent_id

    def get_agent_cells(self, agent_id: str) -> list[tuple[int, int]]:
        """Get all cells placed by a given agent."""
        return [
            (r, c)
            for r in range(GRID_SIZE)
            for c in range(GRID_SIZE)
            if self.agents[r][c] == agent_id
        ]

    def get_unique_agents(self) -> set[str]:
        """Get set of all agent IDs that contributed."""
        return {
            self.agents[r][c]
            for r in range(GRID_SIZE)
            for c in range(GRID_SIZE)
            if self.agents[r][c] is not None
        }

    def to_dict(self) -> dict:
        return {"agents": self.agents}

    @classmethod
    def from_dict(cls, data: dict) -> ContributionGrid:
        cg = cls()
        cg.agents = data["agents"]
        return cg


@dataclass
class GridSnapshot:
    """A snapshot of the grid state at a specific tick."""
    tick: int
    grid: CityGrid
    contributions: ContributionGrid

    def to_dict(self) -> dict:
        return {
            "tick": self.tick,
            "grid": self.grid.to_dict(),
            "contributions": self.contributions.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> GridSnapshot:
        return cls(
            tick=data["tick"],
            grid=CityGrid.from_dict(data["grid"]),
            contributions=ContributionGrid.from_dict(data["contributions"]),
        )
