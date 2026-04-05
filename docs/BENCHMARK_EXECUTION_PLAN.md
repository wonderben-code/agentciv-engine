# Benchmark Execution Plan — City Grid Experiment (Paper 6)

**Created:** 5 April 2026
**Updated:** 5 April 2026 — replaced SWE-bench with City Grid
**Goal:** Run the City Grid experiment, capture all data, write Paper 6.
**Budget:** ~$50-70 API costs
**Paper plan:** `docs/PAPER_PLAN.md`

---

## Status Tracker

| Step | What | Status | Notes |
|------|------|--------|-------|
| 0 | Engine preparation | DONE | All infrastructure built. |
| 0.5 | MCP display parity | DONE | 15 formatters, all tools wired. |
| 1 | Pipeline validation (smoke test) | DONE | 4 real runs. Data capture verified. |
| 2 | Build City Grid infrastructure | NEXT | ~5 hours. Grid model, 5 scorers, renderers, task def. |
| 3 | Run City Grid experiment | TODO | ~$50-70. 18 automated runs. |
| 4 | Analysis + figures | TODO | ~2 hours. Tools already built + new renderers. |
| 5 | Write Paper 6 | TODO | ~4-6 hours. Structure in PAPER_PLAN.md. |

---

## Step 0: Engine Preparation — DONE

All benchmark infrastructure built and validated:
- Per-agent token tracking
- Per-tick metric snapshots (files, messages, broadcasts, conflicts, merges, per-agent file ops)
- Full message content capture (fixed 5 April)
- Agent reasoning text capture (fixed 5 April)
- Relationship trust snapshots per tick (fixed 5 April)
- Conflict resolution timing
- Network metrics (8 metrics: density, in/out/betweenness centrality, reciprocity, hub-spoke ratio, communication efficiency, clustering)
- Temporal analysis (convergence, phase transitions, activity curves, cumulative progress)
- Statistical tests (Kruskal-Wallis, Mann-Whitney U, Cohen's d)
- Export (CSV, JSON, LaTeX)
- Auto-save per run (crash resilient)
- Pre-registered methodology (Bitcoin-timestamped)

## Step 0.5: MCP Display Parity — DONE

15 formatters in `mcp/display.py`. All MCP tools wired. Verified.

## Step 1: Pipeline Validation — DONE

| What | Result |
|------|--------|
| Mock runs (10) | Data saves, JSON populates, analysis computes. |
| Fizzbuzz smoke test | Collaborative: 5/5 tests, 37 msgs. Competitive: 5/5 tests, 6 msgs. |
| Calculator smoke test | Collaborative: 11/11 tests, 37 msgs, 419s. Competitive: 11/11 tests, 6 msgs, 268s. |
| Data capture | Full content: 47/64 entries. Reasoning: 38/64. Relationships: all 10 ticks. |
| Finding | Process radically different even on binary tasks. Competitive agents self-reorganised toward collaborative (auto-learning). |

Smoke test data: `benchmark_results/smoke_test/runs/` (4 JSON files).

**Known bug:** Runner summary JSON fails when output path is existing directory (`[Errno 21]`). Per-run data saves correctly. Fix before Step 3.

---

## Step 2: Build City Grid Infrastructure (~5 hours)

### The Task

Agents receive a 10×10 empty grid and 8 building types. They must design a functional city with connected roads, logical zoning, and diverse infrastructure. Quality is scored across 5 automated dimensions on a 0-100 scale.

**Building types:** Residential (R), Commercial (C), Industrial (I), Park (P), Road (.), Hospital (H), School (S), Empty (_)

### 2a. Grid Data Model
- **File:** `agentciv/benchmark/city_grid.py`
- **What:** `CityGrid` class (10×10 array), `BuildingType` enum, `from_string()` parser (agents output text → we parse), `to_string()` serialiser, `is_valid()` checker (basic structural validation)
- **Why:** Everything downstream depends on parsing agent output into a scoreable grid

### 2b. Scoring: Coverage
- **File:** `agentciv/benchmark/city_scorer.py`
- **What:** `score_coverage(grid) → float` — (non-empty cells / 100) × 100
- **Why:** Penalises wasted space. Simplest dimension.

### 2c. Scoring: Accessibility
- **File:** `agentciv/benchmark/city_scorer.py`
- **What:** `score_accessibility(grid) → float` — BFS from road cells, count reachable buildings
- **Why:** Tests whether road network actually connects everything

### 2d. Scoring: Zoning Logic
- **File:** `agentciv/benchmark/city_scorer.py`
- **What:** `score_zoning(grid) → float` — adjacency rules with weighted scoring
  - Good: residential↔park (+3), residential↔school (+2), commercial↔road (+2), industrial↔industrial (+1)
  - Bad: residential↔industrial (−3), hospital↔industrial (−2)
  - Normalised to 0-100

### 2e. Scoring: Diversity
- **File:** `agentciv/benchmark/city_scorer.py`
- **What:** `score_diversity(grid) → float` — Shannon entropy of building type distribution, normalised
- **Why:** Catches "all houses" or "all roads" degenerate solutions

### 2f. Scoring: Connectivity
- **File:** `agentciv/benchmark/city_scorer.py`
- **What:** `score_connectivity(grid) → float` — road network coherence
  - Components: connected road components (1 = best), dead-end ratio, average path length between buildings
  - Weighted combination, normalised 0-100

### 2g. Aggregate Scorer
- **File:** `agentciv/benchmark/city_scorer.py`
- **What:** `score_city(grid) → CityScore` — runs all 5, computes harmonic mean
- **Why:** Harmonic mean penalises any dimension near zero — can't compensate for no roads with great zoning

### 2h. Grid Renderer: ASCII
- **File:** `agentciv/benchmark/city_renderer.py`
- **What:** `render_ascii(grid) → str` — colour-coded terminal output with row/column labels
- **Why:** Quick validation during development and runs

### 2i. Grid Renderer: PNG
- **File:** `agentciv/benchmark/city_renderer.py`
- **What:** `render_png(grid, path)` — colour image, each cell as coloured square with building type label
- **Why:** For the paper. Uses matplotlib.

### 2j. Agent Contribution Tracker
- **File:** `agentciv/benchmark/city_grid.py`
- **What:** Parallel 10×10 grid of agent IDs. Updated when agent writes to a cell. Saved per tick.
- **Why:** Enables contribution heatmap — who built what

### 2k. Contribution Heatmap Renderer
- **File:** `agentciv/benchmark/city_renderer.py`
- **What:** `render_heatmap(contribution_grid, agents) → PNG` — cells coloured by agent
- **Why:** Visualises work distribution. Competitive = quadrants. Collaborative = interleaved.

### 2l. Temporal Grid Snapshots
- **File:** Extension to existing tick snapshot system
- **What:** Save grid state + contribution state at every tick
- **Why:** Enables frame-by-frame animation of how each team built their city

### 2m. Task Definition
- **File:** `agentciv/benchmark/tasks.py`
- **What:** `BenchmarkTask` for city-grid. Task prompt + verification script (calls `score_city()`)
- **Prompt must include:** Grid spec, building types with descriptions, placement rules, quality goals, small 3×3 example showing format. Must NOT prescribe strategy.

### 2n. Radar Chart Generator
- **File:** `agentciv/benchmark/city_renderer.py`
- **What:** `render_radar(scores_by_preset) → PNG` — 5-axis radar overlaying all presets
- **Why:** Shows at a glance which presets excel at what

### 2o. Integration Test
- **What:** Run city-grid with collaborative, 1 run, 4 agents, ~10 ticks
- **Verify:** Grid produced, parseable, scoreable, renderers work, data saves

**Success criteria:** Valid city grid produced → all 5 scores return → ASCII + PNG render → heatmap renders → temporal snapshots captured → data saves to JSON.

---

## Step 3: Run City Grid Experiment (~$50-70)

### Team runs (15)
```bash
export ANTHROPIC_API_KEY="sk-ant-..."

agentciv test-tasks \
  --tasks city-grid \
  --presets collaborative,competitive,meritocratic,auto,hierarchical \
  --runs 3 \
  --agents 4 \
  --max-ticks 15 \
  --output benchmark_results/city_grid
```

### Single-agent baseline (3)
```bash
agentciv test-tasks \
  --tasks city-grid \
  --presets collaborative \
  --runs 3 \
  --agents 1 \
  --max-ticks 15 \
  --output benchmark_results/city_grid
```

### Total: 18 runs. Estimated cost: $50-70. Automated.

### Verify after runs:
- 18 JSON files in `benchmark_results/city_grid/runs/`
- Each contains: grid output, 5 dimension scores, aggregate, full chronicle, per-tick grid snapshots, contribution grid
- Grids are genuinely different between presets
- Scores vary meaningfully

---

## Step 4: Analysis + Figures (~2 hours)

| What | Tool | Output |
|------|------|--------|
| Score all cities | `city_scorer.py` | Scores per run |
| Preset × dimension table | `analysis.py` + new code | LaTeX table (mean ± std) |
| Statistical tests | `analysis.py` (existing) | Kruskal-Wallis, Mann-Whitney, Cohen's d |
| Hero image: 5 grids | `city_renderer.py` | 5 PNG grids side by side |
| Temporal animations | `city_renderer.py` | Frame sequences / animated GIF per preset |
| Contribution heatmaps | `city_renderer.py` | 5 PNG heatmaps |
| Radar charts | `city_renderer.py` | Overlay radar chart |
| Network graphs | `analysis.py` (existing) | Per-preset communication topology |
| Process comparison table | `analysis.py` (existing) | Messages, conflicts, Gini, efficiency |
| Hypothesis check | Manual | H1-H10 against data |

---

## Step 5: Write Paper 6 (~4-6 hours)

Full structure in `docs/PAPER_PLAN.md`. Key sections:
1. Introduction — the gap nobody is filling
2. Task Selection Problem — the 4-property framework (methodological contribution)
3. The AgentCiv Engine — 9 dimensions, enforcement
4. Experimental Design — city grid task, 5 presets, controls
5. Results — visual evidence (5 grids) + quantitative (scores, stats) + process (networks, Gini) + emergence
6. Discussion — core finding, configuration recommendations, implications
7. Limitations + Future Work — SWE-bench extension, recursive loop, Creator Mode
8. Conclusion

---

## The 5 Presets

| # | Preset | Authority | Communication | Decisions | Why |
|---|--------|-----------|--------------|-----------|-----|
| 1 | collaborative | flat | mesh | consensus | Baseline "normal" team |
| 2 | hierarchical | hierarchy | hub-spoke | top-down | Classic management |
| 3 | competitive | anarchic | whisper | autonomous | No collaboration, agents race |
| 4 | meritocratic | distributed | mesh | meritocratic | Quality-focused, mandatory review |
| 5 | auto | (agents choose) | (agents choose) | (agents choose) | Crown jewel — self-organisation |
| B | single-agent | n/a | n/a | n/a | Baseline: is a team even helpful? |

---

## Cost Breakdown

| What | Runs | Est. Cost |
|------|------|-----------|
| City Grid team runs | 15 | ~$30-45 |
| City Grid baseline | 3 | ~$6-9 |
| Buffer / retries | — | ~$15 |
| **Total** | **18** | **~$50-70** |

---

## Data Output

All saved to `benchmark_results/city_grid/runs/` as individual JSON files.

Each run JSON contains:
- Meta: task, preset, agents, model, timestamps
- **City Grid output:** raw grid text, parsed grid, 5 dimension scores, aggregate harmonic mean
- **Visual assets:** per-tick grid snapshots, contribution grid
- Efficiency: tokens per agent
- Communication: volume, pairs, network metrics
- Coordination: conflicts, resolution times, Gini
- Organisation: initial/final state, restructure log (auto mode)
- Temporal: tick snapshots, convergence, phase transitions
- Full message content
- Agent reasoning text
- Relationship snapshots per tick

---

## Hypotheses (pre-registered, H1-H10)

See `docs/PAPER_PLAN.md` Section 8 for all 10 hypotheses with rationale and measurement method.

Summary: If even 4-5 hold, the paper is strong. Surprises are even MORE interesting.
