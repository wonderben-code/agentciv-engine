"""City Grid scoring — 5 automated dimensions for measuring city quality.

Each scorer returns a float in [0, 100]. The aggregate is the harmonic
mean of all 5, which penalises any dimension near zero.

Dimensions:
  1. Coverage     — how much of the grid is used
  2. Accessibility — how well the road network connects buildings
  3. Zoning Logic  — adjacency bonuses/penalties (good/bad neighbours)
  4. Diversity     — Shannon entropy of building type distribution
  5. Connectivity  — road network coherence (components, dead-ends, paths)
"""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass

from .city_grid import BuildingType, CityGrid, GRID_SIZE


@dataclass
class CityScore:
    """Scores for a city grid across all 5 dimensions + aggregate."""
    coverage: float
    accessibility: float
    zoning: float
    diversity: float
    connectivity: float
    aggregate: float  # harmonic mean

    def to_dict(self) -> dict:
        return {
            "coverage": round(self.coverage, 2),
            "accessibility": round(self.accessibility, 2),
            "zoning": round(self.zoning, 2),
            "diversity": round(self.diversity, 2),
            "connectivity": round(self.connectivity, 2),
            "aggregate": round(self.aggregate, 2),
        }


# ── Dimension 1: Coverage ──────────────────────────────────────────────

def score_coverage(grid: CityGrid) -> float:
    """Percentage of grid cells that are not empty.

    Simple but foundational — a city that uses 30% of its land
    scores 30. A fully built city scores 100.
    """
    used = grid.count_non_empty()
    total = GRID_SIZE * GRID_SIZE
    return (used / total) * 100.0


# ── Dimension 2: Accessibility ─────────────────────────────────────────

def score_accessibility(grid: CityGrid) -> float:
    """Percentage of buildings reachable from the road network.

    BFS from all road cells simultaneously. A building is "accessible"
    if it is adjacent (4-connected) to a road cell that is part of the
    main road network. Buildings not adjacent to any road are inaccessible.
    """
    # Find all road cells
    road_cells: set[tuple[int, int]] = set()
    building_cells: set[tuple[int, int]] = set()

    for r, c, bt in grid.iter_cells():
        if bt == BuildingType.ROAD:
            road_cells.add((r, c))
        elif bt != BuildingType.EMPTY:
            building_cells.add((r, c))

    if not building_cells:
        return 100.0  # No buildings to be inaccessible
    if not road_cells:
        return 0.0  # No roads at all

    # BFS from all road cells to find the connected road network
    visited_roads: set[tuple[int, int]] = set()
    queue: deque[tuple[int, int]] = deque()

    # Start from all road cells (find largest connected component)
    # First, find all connected components of roads
    components: list[set[tuple[int, int]]] = []
    unvisited = set(road_cells)

    while unvisited:
        start = next(iter(unvisited))
        component: set[tuple[int, int]] = set()
        bfs: deque[tuple[int, int]] = deque([start])
        while bfs:
            pos = bfs.popleft()
            if pos in component:
                continue
            component.add(pos)
            unvisited.discard(pos)
            r, c = pos
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in unvisited and (nr, nc) not in component:
                    bfs.append((nr, nc))
        components.append(component)

    # Use all road cells (not just largest component) for accessibility
    all_road_positions = road_cells

    # A building is accessible if adjacent to any road cell
    accessible = 0
    for br, bc in building_cells:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = br + dr, bc + dc
            if (nr, nc) in all_road_positions:
                accessible += 1
                break

    return (accessible / len(building_cells)) * 100.0


# ── Dimension 3: Zoning Logic ──────────────────────────────────────────

# Adjacency scores: (type_a, type_b) -> bonus/penalty
# Symmetric — checked both ways
_ADJACENCY_SCORES: dict[tuple[BuildingType, BuildingType], float] = {
    # Good adjacencies
    (BuildingType.RESIDENTIAL, BuildingType.PARK): 3.0,
    (BuildingType.RESIDENTIAL, BuildingType.SCHOOL): 2.0,
    (BuildingType.COMMERCIAL, BuildingType.ROAD): 2.0,
    (BuildingType.COMMERCIAL, BuildingType.RESIDENTIAL): 1.0,
    (BuildingType.INDUSTRIAL, BuildingType.INDUSTRIAL): 1.0,
    (BuildingType.INDUSTRIAL, BuildingType.ROAD): 1.5,
    (BuildingType.HOSPITAL, BuildingType.ROAD): 2.0,
    (BuildingType.HOSPITAL, BuildingType.RESIDENTIAL): 1.5,
    (BuildingType.SCHOOL, BuildingType.PARK): 1.5,
    # Bad adjacencies
    (BuildingType.RESIDENTIAL, BuildingType.INDUSTRIAL): -3.0,
    (BuildingType.HOSPITAL, BuildingType.INDUSTRIAL): -2.0,
    (BuildingType.SCHOOL, BuildingType.INDUSTRIAL): -2.0,
    (BuildingType.PARK, BuildingType.INDUSTRIAL): -1.5,
}


def _get_adjacency_score(a: BuildingType, b: BuildingType) -> float:
    """Get adjacency score for a pair, checking both orderings."""
    return _ADJACENCY_SCORES.get((a, b), 0.0) or _ADJACENCY_SCORES.get((b, a), 0.0)


def score_zoning(grid: CityGrid) -> float:
    """Score based on adjacency quality of building placements.

    Each pair of adjacent cells contributes a bonus or penalty.
    The raw score is normalised to 0-100 based on the theoretical
    min/max for a grid of this size.

    A perfectly zoned city (all good adjacencies, no bad ones) scores ~100.
    A terribly zoned city (hospitals next to factories) scores near 0.
    """
    raw_score = 0.0
    pairs_checked = 0

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            cell = grid.get(r, c)
            if cell == BuildingType.EMPTY:
                continue
            # Check right and down neighbours (avoid double-counting)
            for dr, dc in [(0, 1), (1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                    neighbour = grid.get(nr, nc)
                    if neighbour == BuildingType.EMPTY:
                        continue
                    adj_score = _get_adjacency_score(cell, neighbour)
                    raw_score += adj_score
                    pairs_checked += 1

    if pairs_checked == 0:
        return 50.0  # Neutral — no adjacent pairs

    # Normalise: theoretical range is roughly [-3, +3] per pair.
    # Map raw average from [-3, 3] to [0, 100]
    avg = raw_score / pairs_checked
    # Clamp to [-3, 3] range
    avg = max(-3.0, min(3.0, avg))
    # Linear map: -3 → 0, 0 → 50, 3 → 100
    return ((avg + 3.0) / 6.0) * 100.0


# ── Dimension 4: Diversity ─────────────────────────────────────────────

def score_diversity(grid: CityGrid) -> float:
    """Shannon entropy of building type distribution, normalised.

    A city with only houses → low diversity. A balanced mix of all
    types → high diversity. Empty cells are excluded from the count.

    Normalised against max possible entropy (log2 of number of
    building types present, up to 7 non-empty types).
    """
    counts: dict[BuildingType, int] = {}
    total = 0

    for _, _, bt in grid.iter_cells():
        if bt == BuildingType.EMPTY:
            continue
        counts[bt] = counts.get(bt, 0) + 1
        total += 1

    if total == 0:
        return 0.0

    # Shannon entropy
    entropy = 0.0
    for count in counts.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)

    # Max entropy = log2(num_types_used), but normalise against
    # log2(7) since there are 7 non-empty building types
    max_entropy = math.log2(7)  # ~2.807
    if max_entropy == 0:
        return 100.0

    return min(100.0, (entropy / max_entropy) * 100.0)


# ── Dimension 5: Connectivity ──────────────────────────────────────────

def score_connectivity(grid: CityGrid) -> float:
    """Road network coherence.

    Three sub-metrics combined:
    1. Connected components (1 = best, more = worse) — weight 40%
    2. Dead-end ratio (fewer dead-ends = better) — weight 30%
    3. Road coverage (roads should be ~15-30% of grid) — weight 30%

    Returns 0-100.
    """
    road_cells: set[tuple[int, int]] = set()
    for r, c, bt in grid.iter_cells():
        if bt == BuildingType.ROAD:
            road_cells.add((r, c))

    if not road_cells:
        return 0.0

    # Sub-metric 1: Connected components
    components = _count_road_components(road_cells)
    # 1 component = 100, 2 = 50, 3+ = diminishing
    component_score = 100.0 / components

    # Sub-metric 2: Dead-end ratio
    dead_ends = 0
    for r, c in road_cells:
        road_neighbours = sum(
            1 for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if (r + dr, c + dc) in road_cells
        )
        if road_neighbours <= 1:
            dead_ends += 1

    dead_end_ratio = dead_ends / len(road_cells) if road_cells else 0
    # 0% dead-ends = 100, 50%+ dead-ends = 0
    dead_end_score = max(0.0, (1.0 - 2.0 * dead_end_ratio) * 100.0)

    # Sub-metric 3: Road coverage
    # Ideal road coverage is ~15-30% of total grid
    road_pct = len(road_cells) / (GRID_SIZE * GRID_SIZE)
    if road_pct < 0.05:
        coverage_score = road_pct / 0.05 * 50.0  # Too few roads
    elif road_pct <= 0.35:
        coverage_score = 100.0  # Sweet spot
    elif road_pct <= 0.60:
        # Too many roads, diminishing
        coverage_score = 100.0 - ((road_pct - 0.35) / 0.25) * 60.0
    else:
        coverage_score = max(0.0, 40.0 - (road_pct - 0.60) * 200.0)

    # Weighted combination
    return (
        component_score * 0.40
        + dead_end_score * 0.30
        + coverage_score * 0.30
    )


def _count_road_components(road_cells: set[tuple[int, int]]) -> int:
    """Count connected components in the road network."""
    if not road_cells:
        return 0

    visited: set[tuple[int, int]] = set()
    components = 0

    for start in road_cells:
        if start in visited:
            continue
        components += 1
        queue: deque[tuple[int, int]] = deque([start])
        while queue:
            pos = queue.popleft()
            if pos in visited:
                continue
            visited.add(pos)
            r, c = pos
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in road_cells and (nr, nc) not in visited:
                    queue.append((nr, nc))

    return components


# ── Aggregate ──────────────────────────────────────────────────────────

def score_city(grid: CityGrid) -> CityScore:
    """Score a city across all 5 dimensions + harmonic mean aggregate.

    The harmonic mean penalises any dimension near zero — a city
    cannot compensate for terrible zoning with great diversity.
    """
    scores = {
        "coverage": score_coverage(grid),
        "accessibility": score_accessibility(grid),
        "zoning": score_zoning(grid),
        "diversity": score_diversity(grid),
        "connectivity": score_connectivity(grid),
    }

    # Harmonic mean (with floor to avoid division by zero)
    values = [max(0.01, v) for v in scores.values()]
    harmonic = len(values) / sum(1.0 / v for v in values)

    return CityScore(
        coverage=scores["coverage"],
        accessibility=scores["accessibility"],
        zoning=scores["zoning"],
        diversity=scores["diversity"],
        connectivity=scores["connectivity"],
        aggregate=harmonic,
    )
