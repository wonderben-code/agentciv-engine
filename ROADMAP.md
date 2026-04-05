# AgentCiv Engine — Master Roadmap

**Last updated:** 5 April 2026 (City Grid + Papers 7-8 expansion)
**Author:** Ekram Alam & Claude

---

## Status Overview

**22 phases completed. 17 remaining across four eras.**

The engine is built, tested, polished, and open-sourced. All 5 papers written and Bitcoin-stamped. Website deployed at agentciv.ai with all four wings. Three public repos. What remains: benchmarks, PyPI, platform features, Creator Mode, then a final website refresh and launch.

```
ERA 1: LAUNCH (Phases 19–23)
  Battle-test → Paper 5 → Website → City Grid Experiment (Paper 6) → Go Public

ERA 2: THE SIMULATION EXPERIENCE (Phases 26–31)
  Package & Install → YAML Customisation → Rich Terminal → Live Chronicler → Gardener → Community

ERA 3: CREATOR MODE + META-PAPERS (Phases 32–36c)
  Build Creator → Task Search → Emergence Explorer → Website Wing → Paper 5 Empirical
  → Paper 7 (Recursive Loop) → Paper 8 (Scale Invariance Capstone)

ERA 4: LAUNCH & OUTREACH (Phases 37–39)
  Website Refresh + QC/QA → Launch Prep → Outreach
```

---

## COMPLETED

| # | Phase | What was built | Status |
|---|-------|---------------|--------|
| 1 | Foundation & Architecture | Core abstractions: Agent, Workspace, Organisation, Chronicle, Engine. Cognitive loop (observe→reason→decide→act→reflect). File perception. Shared workspace. | DONE |
| 2 | Organisation & Communication | 9 organisational dimensions. Three-layer config (presets → dimensions → parameters). 13 presets. Agent communication (direct, broadcast). Task perception & self-allocation. Attention map. Emergent specialisation. | DONE |
| 3 | Git Integration & Contention | Branch-per-agent (git worktrees). Auto-merge at tick end. Conflict detection & reporting. File contention warnings via attention map. | DONE |
| 4 | Quality, Relationships & Feedback | Build/test integration. Relationship & bond system. Specialisation visibility. Token budget & cost management. | DONE |
| 5 | CLI, Chronicle & Human-in-the-Loop | Full CLI (`agentciv solve/experiment/info/history/setup/test-tasks/mcp`). Chronicle observer (structured per-run data). Gardener mode (mid-run intervention). `--org auto` (crown jewel — agents design their own structure via meta-tick proposals & voting). | DONE |
| 6 | Experiment Mode | `agentciv experiment` — same task across multiple org configs. Comparison tables, averages, JSON output. The research flywheel. | DONE |
| 7 | Whitepaper | Paper 4: "Collective Machine Intelligence: A New Field for the Age of AI Collectives." Bitcoin blockchain timestamped. | DONE |
| 8 | MCP Server | 6 tools, 4 resources, 3 prompts. Session manager for concurrent runs. Gardener wired for MCP intervention. Works with Claude Code & Cursor. | DONE |
| 9 | Max Plan Mode | Engine as pure orchestrator — ZERO LLM calls, no API keys needed. StepSession state machine. 4 new MCP tools (orchestrate_start/act/tick/status). Claude Code Max subscription = free usage. | DONE |
| 10 | Feature Discovery | Context-aware CLI tips (non-repeating, suppressible). MCP knowledge via CLAUDE.md. "Knowledge not scripts" principle. | DONE |
| 11 | Internal Test Tasks | Custom task bank (fizzbuzz, kv-store, todo-cli, calculator, chat-server). CLI: `agentciv test-tasks`. For regression testing and dev validation. | DONE |
| 12 | Auto Mode Learning | Every run saved to `~/.agentciv/run_history.jsonl`. Auto mode consults history for similar tasks. Data-informed meta-tick recommendations. CLI: `agentciv history`. | DONE |
| 13 | Setup & Onboarding | Interactive `agentciv setup`: mode choice, env checks, CLAUDE.md generation, .mcp.json config. Exciting celebration flow. Maximally frictionless. | DONE |
| 14 | README | 231 lines. Hook, 13 presets, crown jewel, 9 dimensions, two modes, features, real output, CLI ref, architecture. | DONE |
| 15 | First Live Runs | hello_api (2 agents, collaborative, 3 ticks, 4 passing tests). todo_app_auto (3 agents, auto mode, self-organised). Both committed as examples/. | DONE |
| 16 | QA/QC Audit | 6 critical + 8 high + all medium/low findings fixed. All user-facing text verified. | DONE |
| 17 | Excellence Phase | Rich terminal display (`rich` library). Agent colour system (20 names × persistent colours). Plain English translation layer (all 9 dimensions × all values → human language). Teaching error messages. Experiment/benchmark/chronicle reports. "Making the invisible visible." | DONE |
| 18 | Bitcoin Provenance | Auto-stamping post-commit hook on all repos. Every commit blockchain-timestamped. Block 943474. | DONE |
| 19 | Battle-Test | API mode, Max Plan mode, experiment mode dry runs. Live runs: hello_api + todo_app_auto. | DONE |
| 20 | Paper 5 — Creator Mode | "Creator Mode: AI as Civilisation Designer." 14 sections, v1 architecture, NAS/AutoML/OEE connections, limitations, ethics. Dedicated repo (agentciv-creator). Bitcoin-stamped. | DONE |
| 21 | Website — Four Wings | Four-wing site deployed at agentciv.ai. All wing landing pages rebuilt for first-time visitors. Links audited. Provenance on home page. Polish deferred to ERA 4. | DONE (core) |
| 22-0 | Benchmark Infrastructure | Per-agent token tracking, per-tick snapshots, conflict resolution timing, network metrics (8 metrics), temporal analysis (convergence, phase transitions), comparative analysis (rankings, superadditivity, Cohen's d, Kruskal-Wallis, Mann-Whitney U), CSV/JSON/LaTeX export. Results directory + pre-registered methodology (Bitcoin-stamped). | DONE |
| 22-0.5 | MCP Display Parity | 15 formatters in `mcp/display.py` with unicode box-drawing, markdown tables, agent markers, contextual tips. All MCP tools wired. Verified from fresh terminal. | DONE |
| 22-mock | Pipeline Validation | 10 mock benchmark runs (5 tasks × 2 presets). Validated: data saves, JSON schema populates, analysis layer computes. | DONE |
| 23a | Repos Public | All 3 repos public (agentciv/agentciv, wonderben-code/agentciv-engine, wonderben-code/agentciv-creator). Internal docs removed pre-publish. | DONE |
| 23b | PyPI Publish | `pip install agentciv-engine` v0.1.1 live on PyPI. Presets moved into package. All path refs updated. Tested in clean venv. | DONE |
| 23c | Website Deployed | agentciv.ai deployed on Netlify. Engine landing page updated with literal step-by-step commands, both modes, macOS pip3 buttons, realistic output panels. | DONE |

**Current state:** ~11,000+ lines across 40+ Python files + website code. 13 presets. All features working and tested. Three public repos + one private (website). v0.1.1 on PyPI. Website deployed at agentciv.ai. All external links verified working. All repos Bitcoin-stamped.

---

## ERA 1: LAUNCH

---

### Phase 19: Battle-Test — Real-World Validation

**Goal:** Prove the engine works flawlessly on real tasks. Fix everything that breaks.

| Step | What | Detail |
|------|------|--------|
| 19a | API mode dry run | `agentciv solve` on 3-5 real tasks. Full pipeline: spawn → ticks → git merge → chronicle → report. |
| 19b | Max Plan mode dry run | Full tasks via MCP in Claude Code. Verify step orchestration, intervention, reporting. |
| 19c | Experiment mode dry run | `agentciv experiment` with 3+ orgs on the same task. Verify comparison output. |
| 19d | Edge case sweep | 1 agent, 10 agents, `--org auto` with restructuring, gardener mid-run, merge conflicts, test failures. |
| 19e | Performance check | Startup time, per-tick latency, import chain. Fix anything slow. |
| 19f | Fix everything | Every issue from 19a-19e fixed before moving on. |

**Status:** COMPLETE. All steps done. Live runs validated (hello_api, todo_app_auto). Excellence phase covered edge cases.

---

### Phase 20: Paper 5 — Creator Mode Whitepaper (Concept)

**Goal:** Write the theoretical paper that defines Creator Mode — AI-directed exploration of the multi-agent organisational possibility space. Establishes the intellectual claim. Bitcoin-timestamped BEFORE anything is built.

This is a **concept paper**, not an empirical paper. It defines the idea, the architecture, the theoretical framework, and the connections to NAS/AutoML/open-ended evolution. The empirical results come later (Phase 36) after Creator Mode is actually built and run.

| Step | What | Detail |
|------|------|--------|
| 20a | Paper structure | Introduction, the bottleneck thesis, three axes (tasks/emergence/field), architecture, connections to NAS/AutoML/open-ended evolution, the self-referential thesis, future work. |
| 20b | Writing | Full paper. Working title: "Self-Exploring AI Civilisations: Automated Discovery in the Multi-Agent Organisational Possibility Space." |
| 20c | Comparison section | How Creator Mode relates to Neural Architecture Search, AutoML, open-ended evolution, hyperparameter optimisation. Why searching social structures is fundamentally different from searching computational structures. |
| 20d | The self-referential thesis | The philosophical contribution: each layer of AgentCiv emerged from the previous. Creator Mode is the point where the field becomes self-exploring. |
| 20e | Commit & Bitcoin timestamp | Paper committed to dedicated repo (`agentciv-creator`). Post-commit hook stamps it automatically. This timestamp establishes provenance for the concept. |

**Why here:** The timestamp matters. The concept must be documented and provably dated before the system is built. The paper also provides content for the Creator Mode website wing.

**Repo:** `agentciv-creator` (github.com/wonderben-code/agentciv-creator) — dedicated repo for Creator Mode paper and future code.
**Concept document:** `docs/CREATOR_MODE.md` in agentciv-engine (internal reference only, not published). The paper is the public output.

---

### Phase 21: Website — Four Wings

**Goal:** agentciv.ai as a four-wing Apple-quality site. Each wing independently mind-blowing.

**Full spec:** `docs/WEBSITE_PLAN.md`
**Style guide:** `docs/APPLE_STYLE_GUIDE.md`
**Aesthetic:** Bright, expansive, hopeful (warm cream palette). Wing 1 = "Collective Intelligence" (not "The Science").

| Step | What | Status |
|------|------|--------|
| 21a | Global nav + routing — Four peer-level wings (Collective Intelligence, The Simulation, The Engine, Creator Mode) + GitHub CTA. No dropdowns. Active-state detection per wing. Mobile hamburger. Footer with 5-column wing layout. | DONE |
| 21b | Homepage — Hero + 4 product cards + interactive Field Map (SVG ecosystem diagram with hover/click) + highlights + proof strip + featured moment + final CTA. NetworkBackground animation. Reveal components via IntersectionObserver. | DONE |
| 21c | Engine wing — Hero + pip install CTA + The Problem + 13 Structures (interactive expandable grid) + Auto Mode (crown jewel with terminal mockup) + 9 Dimensions + 6 feature cards + Two Modes (Max Plan vs API) + code sample + final CTA. | DONE |
| 21d | Science wing (Collective Intelligence) — Hero + The Breakthrough + 9 Dimensions table + 5 Papers (card layout) + CMI "big idea" section + 6 open-ended mechanisms + comparison table + open research directions + provenance + citation + final CTA. | DONE |
| 21e | Simulation landing — Hero + What Emerged (3 cards) + explore grid (10 existing pages) + "Run Your Own" dark CTA to Engine. | DONE |
| 21f | Creator Mode wing — Hero + The Insight ("bottleneck") + Three Axes + self-referential thesis (4 progressive statements) + architecture diagram + Paper 5 link + final CTA. | DONE |
| 21g | Copy pass — About page (solo attribution: "One person. One AI. An entire field."), Website Plan updated (bright aesthetic, Collective Intelligence naming). | DONE |
| 21h | Polish | Deferred to ERA 4 (website refresh before launch) |
| 21i | Content creation | Deferred to ERA 4 |
| 21j | Deploy | DONE — deployed to agentciv.ai via Netlify |

**Architecture:**
```
agentciv.ai
    |
    +-- The Science (/science)       — "A new field of AI."
    |     Papers, 9 dimensions, CMI, provenance, citation
    |
    +-- The Simulation (/simulation) — "They built a civilisation."
    |     Landing hero + existing 17 pages (elevated copy)
    |
    +-- The Engine (/engine)         — "Your agents. Your rules."
    |     Apple product page, 14 sections, interactive
    |
    +-- Creator Mode (/creator)      — "AI that spawns civilisations."
          Concept page at launch → full wing when built (Era 3)
```

---

### Phase 22: The City Grid Experiment — Paper 6

**Goal:** The first controlled experiment proving that organisational structure produces measurably different outputs of measurably different quality in multi-agent AI. Visual, quantitative, and undeniable.

**Paper:** "Same City, Different Architects" — Paper 6 in the AgentCiv series. Full plan: `docs/PAPER_PLAN.md`

**Thesis:** The same task, given to teams with different organisational structures, produces visually distinct outputs with quantitatively different quality — measured continuously across 5 dimensions, not binary pass/fail.

**Why City Grid, not SWE-bench:** SWE-bench tasks are binary (pass/fail). If all teams solve the bug, you can't distinguish quality. The City Grid satisfies 4 critical properties simultaneously: (1) multiple valid outputs, (2) composition from parts requiring coordination, (3) continuous multi-dimensional scoring, (4) process visibly differs across configurations. No standard coding benchmark satisfies all four. Full analysis in `docs/PAPER_PLAN.md` Section 3.

**Cost:** ~$50-70 API.

**Pre-registration:** Methodology committed and Bitcoin-timestamped BEFORE any runs. DONE.

---

#### Step 0: Engine Preparation — DONE

All benchmark infrastructure built and validated.

| Sub-step | What | Status |
|----------|------|--------|
| 22-0a | Per-agent token tracking | DONE — `LLMResponse.input_tokens/output_tokens`, deducted from `AgentState.token_budget_remaining`, injected into `ChronicleReport.tokens_per_agent` |
| 22-0b | Per-tick metric snapshots | DONE — `TickSnapshot` dataclass in `chronicle/observer.py`: files, messages, broadcasts, conflicts, merges, active agents, per-agent file ops. Captured at `TICK_END`. |
| 22-0c | Conflict resolution timing | DONE — `ConflictRecord` dataclass with `detected_tick`, `resolved_tick`, `resolution_time` property. |
| 22-0d | Analysis layer | DONE — `benchmark/analysis.py`: `NetworkMetrics` (8 metrics), `TemporalMetrics`, `compute_preset_comparison()`, `kruskal_wallis()`, `mann_whitney_u()`, Cohen's d. Export: CSV, JSON, LaTeX. |
| 22-0e | Results directory + pre-registration | DONE — `benchmark_results/` with subdirectories. `methodology.md` Bitcoin-timestamped. |
| 22-0f | Full message content capture | DONE — `engine.py` stores full `message.content` (fixed 5 April 2026). |
| 22-0g | Agent reasoning capture | DONE — `chronicle/observer.py` persists `reasoning` field on timeline entries (fixed 5 April 2026). |
| 22-0h | Relationship trust snapshots | DONE — `TickSnapshot.relationships` dict captured at every `TICK_END` (fixed 5 April 2026). |

#### Step 0.5: MCP Display Parity — DONE

| Sub-step | What | Status |
|----------|------|--------|
| 22-0.5a | `mcp/display.py` — 15 formatters | DONE |
| 22-0.5b | All MCP tools wired | DONE |
| 22-0.5c-e | Verified from fresh terminal | DONE |

#### Step 1: Pipeline Validation — DONE

| Sub-step | What | Status |
|----------|------|--------|
| 22-1a | Mock runs (10) | DONE — 5 tasks × 2 presets. Validated data saves, JSON schema, analysis layer. |
| 22-1b | Real smoke test — fizzbuzz | DONE — collaborative vs competitive, 1 run each. Real code produced, 5/5 tests passing. |
| 22-1c | Real smoke test — calculator | DONE — collaborative vs competitive, 1 run each. Real code produced, 11/11 tests passing. |
| 22-1d | Data capture validation | DONE — Full message content (47/64 entries), reasoning (38/64), relationship snapshots (all 10 ticks). |
| 22-1e | Process differences confirmed | DONE — Collaborative: 37 msgs, 419s. Competitive: 6 msgs, 268s. Visibly different process. |
| 22-1f | Runner summary JSON bug | KNOWN — `[Errno 21] Is a directory` when output path is existing dir. Per-run data saves correctly. Fix before full experiment. |

**Smoke test data:** `benchmark_results/smoke_test/runs/` — 4 JSON files (fizzbuzz × 2, calculator × 2).

**Key finding from smoke tests:** Even on binary pass/fail tasks, process is radically different. Competitive agents unanimously voted to self-reorganise toward collaborative incentives (auto-learning kicked in). This is already a finding for the paper.

---

#### Step 2: Build City Grid Infrastructure (NEXT — ~5 hours)

The City Grid is a purpose-built benchmark task where 4 agents collaborate to design a city on a 10×10 grid. Different team configurations produce visually and quantitatively different cities. The visual output — five city grids side by side — is the hero image of Paper 6.

**Task overview:** Agents receive a 10×10 empty grid and 8 building types (Residential, Commercial, Industrial, Park, Road, Hospital, School, Empty). They must design a functional city with connected roads, logical zoning, and diverse infrastructure. Quality is scored across 5 automated dimensions on a 0-100 scale. Aggregate = harmonic mean (penalises any dimension near zero).

| Sub-step | What | Detail | File |
|----------|------|--------|------|
| 22-2a | Grid data model | `CityGrid` class: 10×10 array, `BuildingType` enum (R, C, I, P, ., H, S, _), placement validation (building must be adjacent to road), `to_string()` / `from_string()` parsing. | `agentciv/benchmark/city_grid.py` |
| 22-2b | Scoring: Coverage | `score_coverage(grid) → float` — (used cells / 100) × 100. Simple but foundational. | `agentciv/benchmark/city_scorer.py` |
| 22-2c | Scoring: Accessibility | `score_accessibility(grid) → float` — BFS from any road cell. (reachable buildings / total buildings) × 100. Tests whether road network actually connects everything. | `agentciv/benchmark/city_scorer.py` |
| 22-2d | Scoring: Zoning Logic | `score_zoning(grid) → float` — adjacency rules. Good: residential↔park (+3), residential↔school (+2), commercial↔road (+2), industrial↔industrial (+1). Bad: residential↔industrial (−3), hospital↔industrial (−2). Sum of adjacency scores, normalised to 0-100. | `agentciv/benchmark/city_scorer.py` |
| 22-2e | Scoring: Diversity | `score_diversity(grid) → float` — Shannon entropy of building type distribution, normalised against max possible entropy. A city of only houses → low. Balanced mix → high. | `agentciv/benchmark/city_scorer.py` |
| 22-2f | Scoring: Connectivity | `score_connectivity(grid) → float` — road network coherence. Components: number of connected road components (1 = best), dead-end ratio, average shortest path between buildings. Weighted combination, normalised 0-100. | `agentciv/benchmark/city_scorer.py` |
| 22-2g | Aggregate scorer | `score_city(grid) → CityScore` — runs all 5 scorers, computes harmonic mean. Returns dataclass with individual + aggregate scores. | `agentciv/benchmark/city_scorer.py` |
| 22-2h | Grid renderer: ASCII | `render_ascii(grid) → str` — colour-coded terminal output. Each building type has a colour. Shows grid with row/column labels. For terminal display and quick validation. | `agentciv/benchmark/city_renderer.py` |
| 22-2i | Grid renderer: PNG | `render_png(grid, path)` — colour PNG image. Each cell as a coloured square with building type label. For the paper. Uses `pillow` or `matplotlib`. | `agentciv/benchmark/city_renderer.py` |
| 22-2j | Agent contribution tracker | Track which agent placed/modified each cell. Stored as a parallel 10×10 grid of agent IDs. Saved per tick. Enables heatmap rendering. | `agentciv/benchmark/city_grid.py` |
| 22-2k | Contribution heatmap renderer | `render_heatmap(contribution_grid, agents) → PNG` — each cell coloured by which agent placed it. Visualises work distribution. Gini coefficient as an image. | `agentciv/benchmark/city_renderer.py` |
| 22-2l | Temporal grid snapshots | Save grid state + contribution state at every tick. Enables frame-by-frame animation of how each team built their city. Extends existing `TickSnapshot`. | `agentciv/benchmark/city_grid.py` |
| 22-2m | Task definition | `BenchmarkTask` entry for city-grid. Task prompt includes: grid spec (10×10), building types with descriptions, placement rules (roads connect, buildings adjacent to roads, zoning guidelines), goal (maximise all 5 scoring dimensions). Verification script calls `score_city()`. | `agentciv/benchmark/tasks.py` |
| 22-2n | Task prompt design | The prompt agents receive. Must be clear enough that agents understand the grid format, building types, placement rules, and quality goals. Must NOT prescribe a strategy — the strategy should emerge from the org structure. Include example of a small 3×3 grid to show format. | Part of task definition |
| 22-2o | Radar chart generator | `render_radar(scores_by_preset) → PNG` — 5-axis radar chart overlaying all preset profiles. Shows at a glance which presets excel at what. For the paper. | `agentciv/benchmark/city_renderer.py` |
| 22-2p | Integration test | Run city-grid task with 1 preset (collaborative), 1 run, 4 agents, ~10 ticks. Verify: grid is produced, parseable, scoreable, all renderers work, data saves to JSON, temporal snapshots captured. | Manual validation |

**Success criteria for Step 2:** A single run produces a valid city grid, all 5 scoring dimensions return sensible values, ASCII and PNG renderers produce output, contribution heatmap shows which agent built what, temporal snapshots capture grid state per tick.

---

#### Step 3: Run City Grid Experiment (~$50-70, automated)

| Sub-step | What | Detail |
|----------|------|--------|
| 22-3a | Team runs | `agentciv test-tasks --tasks city-grid --presets collaborative,competitive,meritocratic,auto,hierarchical --runs 3 --agents 4 --max-ticks 15 --output benchmark_results/city_grid` — 15 runs total. |
| 22-3b | Single-agent baseline | `agentciv test-tasks --tasks city-grid --presets collaborative --runs 3 --agents 1 --max-ticks 15 --output benchmark_results/city_grid` — 3 runs. |
| 22-3c | Verify all data saved | Check `benchmark_results/city_grid/runs/` for 18 JSON files. Each must contain: grid output, 5 dimension scores, aggregate score, full chronicle (messages, reasoning, relationships), per-tick grid snapshots, contribution grid. |
| 22-3d | Quick sanity check | Spot-check: are grids genuinely different? Do scores vary? Any failed/empty runs? |

**Total: 18 runs. Estimated cost: $50-70. Automated — one command per batch.**

**Commands (exact, copy-paste ready):**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."

# Team runs: 5 presets × 3 runs = 15 runs
agentciv test-tasks \
  --tasks city-grid \
  --presets collaborative,competitive,meritocratic,auto,hierarchical \
  --runs 3 \
  --agents 4 \
  --max-ticks 15 \
  --output benchmark_results/city_grid

# Single-agent baseline: 3 runs
agentciv test-tasks \
  --tasks city-grid \
  --presets collaborative \
  --runs 3 \
  --agents 1 \
  --max-ticks 15 \
  --output benchmark_results/city_grid
```

---

#### Step 4: Analysis + Figures (~2 hours)

| Sub-step | What | Detail |
|----------|------|--------|
| 22-4a | Score all cities | Run `score_city()` on all 18 grid outputs. Populate scores into comparison data structure. |
| 22-4b | Preset × dimension table | Table with 5 presets as rows, 5 dimensions + aggregate as columns. Mean ± std across 3 runs. |
| 22-4c | Statistical significance | Kruskal-Wallis H-test across presets for each dimension and aggregate. Mann-Whitney U for all pairwise comparisons. Cohen's d effect sizes. All pre-registered in `methodology.md`. |
| 22-4d | Hero image: 5 grids | Render the best run from each preset as a colour PNG. Place side by side. This is the paper's centrepiece. |
| 22-4e | Temporal animations | Render per-tick grid states as frame sequences (or animated GIF). One animation per preset. Shows HOW each team built their city — the process made visible. |
| 22-4f | Contribution heatmaps | Render 5 heatmaps (one per preset). Shows which agent built what. Immediately visualises work distribution — competitive shows quadrants, collaborative shows interleaving, hierarchical shows planner/executor split. |
| 22-4g | Radar charts | 5-axis radar chart overlaying all preset quality profiles. Shows at a glance which presets excel at which dimensions. |
| 22-4h | Communication network graphs | Per-preset network visualisation (from existing analysis layer). Hub-spoke ratios, density, betweenness centrality. |
| 22-4i | Process comparison table | Table: preset × process metrics (messages, broadcasts, conflicts, Gini, communication efficiency). |
| 22-4j | Hypothesis verification | Check all 10 hypotheses (H1-H10 in PAPER_PLAN.md) against actual data. Record which held, which surprised. |
| 22-4k | LaTeX export | Export all tables in LaTeX format. Export all figures at publication resolution. |
| 22-4l | Appendix: smoke test data | Include fizzbuzz + calculator smoke test results showing process differences on binary tasks. |

---

#### Step 5: Write Paper (~4-6 hours)

| Sub-step | What | Detail |
|----------|------|--------|
| 22-5a | Abstract + Introduction | The gap, our approach, preview of findings. ~2 pages. |
| 22-5b | Task Selection Problem | The 4-property framework. Why most benchmarks fail. Table of rejected tasks. Why City Grid. ~1.5 pages. This section is a methodological contribution on its own. |
| 22-5c | Engine description | 9 dimensions, enforcement, agent architecture. ~1.5 pages. |
| 22-5d | Experimental design | Task spec, presets, controls, run matrix. ~1.5 pages. |
| 22-5e | Results: visual evidence | Five grids, animations, heatmaps. The hero section. ~1 page. |
| 22-5f | Results: quantitative | Scores, radar charts, statistical tests. ~2 pages. |
| 22-5g | Results: process + emergence | Network graphs, communication patterns, role emergence, auto-mode behaviour. ~1.5 pages. |
| 22-5h | Discussion | Core finding, configuration recommendations, implications (AI engineering, org theory, safety, science). ~2 pages. |
| 22-5i | Limitations + Future Work | Honest framing. SWE-bench as future ecological validity. Recursive loop. ~1 page. |
| 22-5j | Polish + Bitcoin timestamp | Final pass, proofread, commit, Bitcoin-stamp. |

**Full structure:** `docs/PAPER_PLAN.md` Section 6.

---

#### Metrics Framework (3 tiers)

- **Tier 1 — Outcome (minimum publishable):** 5 city dimension scores, aggregate harmonic mean, grid completeness, ticks used, tokens used, baseline comparison.
- **Tier 2 — Process (strong paper):** Communication volume/graph density/hub-spoke ratio, Gini coefficient + contribution heatmap, merge conflicts, parallel utilisation, coordination overhead, communication efficiency (quality / messages).
- **Tier 3 — Emergence (outstanding paper):** Role emergence (agent specialisation patterns), auto-mode restructure log, phase transitions, temporal trust evolution, per-tick grid evolution, predictive validity (can tick-5 grid predict final score?), superadditivity ratio.

#### Auto Mode Learning Flywheel

Every run feeds the learning system. Run → data → insights → better auto-mode starts → better runs. By the end of the experiment, `auto` will have accumulated history for this specific task type. If auto improves across its 3 runs, that's evidence of learning — a finding in itself.

---

### Phase 23: Go Public — MOSTLY DONE

**Goal:** Everything goes live. First public impression = best version.

| Step | What | Status |
|------|------|--------|
| 23a | Make GitHub repo public | DONE — all 3 repos public on wonderben-code. |
| 23b | PyPI publish | DONE — v0.1.1 on PyPI. Tested in clean venv. |
| 23c | Website live | DONE — agentciv.ai on Netlify. All four wings. |
| 23d | Contributing guide | TODO — add presets (YAML), dimensions, mechanisms. |
| 23e | Examples directory | TODO — polished examples with READMEs showing different org structures. |

---

---

## ERA 2: THE SIMULATION EXPERIENCE

*The simulation codebase is already powerful and expandable. ERA 2 makes it feel like magic to use — while making it crystal clear that everything underneath is yours to hack, extend, and rebuild.*

---

### UX Vision — The Guiding Philosophy

Everything in ERA 2 is built around one insight: **customisation IS the product.** Unlike most dev tools where configuration is a chore you endure to reach the thing you actually want, in AgentCiv "what if I changed this?" IS the thing. Every configuration choice creates a different civilisation. The worldbuilding is the fun. The UX must feel like worldbuilding, not configuration.

#### Core UX Principles

1. **Zero-decision first run.** `agentciv spawn` with no flags produces a running civilisation. First impression is magic, not setup. Sensible defaults for everything.

2. **Natural language is the primary interface.** In Claude Code (Max Plan mode), the user never touches YAML or flags. They describe what they want: "spawn a harsh desert world with 20 competitive agents." The system translates to config and launches. Mid-run: "introduce a drought." "What's agent 7 thinking?" "Make the southern group more cooperative." All natural language.

3. **API key not required.** Max Plan mode runs inside Claude Code using the user's existing subscription. No API key, no cost. This is the magic path. API mode (with `ANTHROPIC_API_KEY`) exists for researchers and automation. Both paths work from one command.

4. **The Chronicler is your companion for the whole experience.** Think David Attenborough — but you can talk to him. It does everything:
   - **Narrates** what's happening: "Entity 4 has just discovered fire. Watch how the others react." "A power struggle is forming between the northern and southern factions."
   - **Chats** with you: ask it anything. "What's going on with agent 7?" "Why did they form that alliance?" "What's the most interesting thing happening right now?" It answers in that same documentary voice.
   - **Gives insights**: "Entity 7 and Entity 3 have been inseparable since the drought — this is the strongest bond in the civilisation." "The council just rejected expansion for the third time — the conservatives are winning."
   - **Follows Bastion principles**: brevity, silence as a tool, reactive not constant. When it speaks unprompted, it's because something genuinely interesting happened. But it's always there to talk to when you want it.

5. **Every ending opens the next beginning.** End-of-run produces a story, not a report. And every story naturally surfaces "what if?" hooks: "Your civilisation stabilised into a meritocracy. What would happen with competitive incentives? Or with 50 agents? Or with no leader at all?" The replay loop is built into the narrative.

6. **Three doors at launch, not zero and not twenty.** The tension between zero-friction start and feature discovery is resolved by one low-friction choice:

```
$ agentciv spawn

Welcome to AgentCiv.

  ▸ Jump in          (a civilisation unfolds — just watch)
  ▸ Build your world (guided worldbuilding — this is the fun part)
  ▸ Describe it      (tell me what you want in plain English)
```

One keystroke. No wrong choice. "Jump in" gets them watching in 2 seconds. "Build your world" is guided worldbuilding that feels like RPG character creation, not a config form. "Describe it" is free-form natural language.

7. **Guided worldbuilding feels like play, not forms.** If they choose "Build your world":

```
What kind of world?
  ▸ Harsh desert    ▸ Lush paradise    ▸ Post-collapse city    ▸ Surprise me

How should they organise?
  ▸ Democracy    ▸ Dictatorship    ▸ Anarchy    ▸ Let them figure it out

What drives them?
  ▸ Survival    ▸ Knowledge    ▸ Power    ▸ Creativity    ▸ All of it

How many agents?
  ▸ 5 (intimate)    ▸ 12 (village)    ▸ 20 (society)    ▸ Pick a number
```

Each question is fun. Each has a "surprise me" escape hatch. User can bail at any point — "launch with what I've picked so far." This is worldbuilding, not a questionnaire.

8. **YAML is the export/power-user layer, not the primary interface.** Natural language and guided menus come first. YAML exists for: reproducibility, sharing configs, version-controlling worlds, precise control over all 9 dimensions. "Save this config" bridges the gap. A non-programmer may never touch YAML and still have infinite variety.

9. **Every run contributes to collective knowledge.** One-click opt-in to share your run data (config, events, outcomes) to a community data pool. The more people run civilisations, the richer the collective dataset becomes — feeding better auto-learning recommendations, powering the civilisation gallery, and building a publishable research dataset of AI civilisation behaviour under varied configurations. Running a civilisation isn't just fun — it's contributing to science.

#### The Full Experience Loop

```
Launch (one keystroke or natural language description)
    ↓
Fishbowl opens (rich terminal display — agents, relationships, events, live stats)
    ↓
Chronicler narrates + chats with you (David Attenborough — but you can talk to him)
    ↓
You intervene whenever you want (natural language gardener mode)
    ↓
Pause anytime → launch anthropologist → interview agents in character → resume
    ↓
Run ends → story, not report → "what if?" hooks
    ↓
Interview agents post-run ("What was your hardest moment?")
    ↓
Next run (with one thing changed) → loop forever
```

#### The Three Layers (Website + README must communicate all three)

1. **Experience it** — One line to launch, natural language to customise, beautiful terminal display, chronicler narrating, mid-run intervention, end-of-run story. This is the complete experience for most people. No YAML, no code, no docs required.
2. **Precisely control it** — YAML for reproducibility, sharing configs, version-controlling worlds. Full control over all 9 dimensions, drive systems, personalities, events, world templates. Power users who want exact specification.
3. **Expand it** — The full codebase is modular Python. New action types, new resource types, 3D worlds, new drive systems, new mechanics, entirely new interaction patterns. Fork and build anything. This is the floor, not the ceiling.

Each layer must be clearly visible on the website and in the README. Nobody should hit Layer 1 and think "that's it." Progressive disclosure, not hidden capability.

#### Reference: Top 0.00000001% UX Benchmarks

These are the products we're benchmarking against for quality:

- **Stripe** — zero-decision first run. One curl command to your first payment. We need: one command to your first civilisation.
- **btop** — terminal as art. Information-dense but beautiful. Colour, layout, real-time updates. Our rich terminal must be this good.
- **Bastion (game)** — narrator principles: brevity, silence as a tool, reactive not constant. Our Chronicler follows these principles for its unprompted narration — but goes beyond Bastion because you can also talk to it, ask questions, and get insights on demand.
- **Civilisation (game)** — "one more turn" loop. Every ending makes you want to try something different. Our "what if?" hooks must create this same compulsion.
- **Minecraft** — drops you in immediately, discovery is progressive, the crafting book exists when you're ready. Our three-door launch + Chronicler narration follows this pattern.

---

### Phase 26: Package & Install — One Command to Civilisation

**Goal:** `pip install agentciv` → `agentciv spawn` → civilisation running. Zero friction. Three doors at launch.

| Step | What | Detail |
|------|------|--------|
| 26a | PyPI package | `pip install agentciv` installs everything. Single package, no separate Node setup for basic use. |
| 26b | `agentciv spawn` CLI | One command. Three-door menu: "Jump in" (zero config, sensible defaults: 12 agents, moderate world, Maslow drives), "Build your world" (guided worldbuilding), "Describe it" (natural language). Zero flags = three-door menu. `--quick` flag skips menu and spawns with defaults. |
| 26c | Guided worldbuilding | The "Build your world" path. RPG-character-creation-style menus: world type, organisation, drives, agent count, events. Each question has a "surprise me" option. User can bail at any point. Must feel like play, not configuration. |
| 26d | Natural language spawn | The "Describe it" path. User types a plain English description: "a harsh desert world with 20 competitive agents fighting for scarce water." System parses to config and launches. Works in both terminal and Claude Code. |
| 26e | Max Plan mode detection | If running inside Claude Code, auto-detect and use Max Plan mode (no API key needed). If standalone terminal, check for `ANTHROPIC_API_KEY`. Clear messaging about both paths. |
| 26f | Named presets | `--preset island` / `metropolis` / `frontier` / `harsh` / `abundant`. Drop a YAML in `presets/` to add your own. |
| 26g | Auto-export + view | Run finishes → data auto-exports → `agentciv view` opens fishbowl in browser. Two commands total: spawn, view. |

---

### Phase 27: Natural Language + YAML Customisation

**Goal:** Natural language is the primary customisation interface. YAML is the power-user/reproducibility layer underneath. Both produce the same result — YAML is just the serialised form of what natural language creates.

| Step | What | Detail |
|------|------|--------|
| 27a | Natural language config engine | Parse plain English descriptions into simulation config. "Make them more competitive" → adjusts incentive dimensions. "Add a drought at tick 30" → creates environmental event. "Give agent 5 a rebellious personality" → modifies agent profile. Works mid-conversation in Claude Code and as part of spawn flow. |
| 27b | Structure recipes as YAML | New buildings/inventions = YAML file. Name, cost, effect, prerequisites. No code. The data format underlying natural language creation. |
| 27c | Drive systems as YAML | Custom drive hierarchies — not just Maslow. Define levels, thresholds, activation conditions, labels. YAML schema. |
| 27d | Agent personality profiles | Traits, priorities, reasoning style, social tendency. Mix and match per agent or apply globally. Can be created via natural language ("a cautious leader who values knowledge over power") or directly in YAML. |
| 27e | Environmental events | Droughts, abundance surges, migrations, disasters. YAML-defined triggers: tick range, probability, effect, duration. Can also be created/triggered via natural language. |
| 27f | Innovation categories | What kinds of things agents can invent. Categories, constraints, feasibility rules. YAML. |
| 27g | World templates | Complete civilisation configs: world + agents + drives + recipes + events + personality. One YAML = one unique civilisation type. Community-shareable. Can be exported from any run ("save this config"). |
| 27h | "Save this config" | Any natural-language-configured run can be saved as YAML for reproducibility and sharing. Bridges the experience layer to the precision layer. |
| 27i | Validation + docs | Every YAML schema documented. Errors tell you exactly what's wrong and how to fix it. Teaching error messages. Full manual on website and in `agentciv info`. |

---

### Phase 28: Rich Terminal Experience — Making the Invisible Visible

**Goal:** Running a civilisation is visually stunning in the terminal. btop-level quality. You SEE what's happening — agent activity, relationships forming, events unfolding, all in real time.

| Step | What | Detail |
|------|------|--------|
| 28a | Rich terminal display | btop-level design. Agent colours (persistent per entity), structured event panels, tick progress, innovation announcements, governance votes. Split-panel layout: main view (civilisation activity), side panel (chronicler narration), bottom bar (your input / stats). Port and elevate from engine's `display.py`. |
| 28b | Real-time event stream | Events appear as they happen. Colour-coded by type (innovation = gold, conflict = red, cooperation = green, governance = blue). Key moments highlighted with emphasis. |
| 28c | Relationship visualisation | ASCII/Unicode relationship map showing alliances, tensions, trust levels. Updates in real time. Who's working with whom, who's in conflict. |
| 28d | Mid-run stats | Live stats panel: population wellbeing, Maslow distribution, structure count, innovation count, communication volume, governance decisions. |
| 28e | Terminal fishbowl | The terminal itself IS the fishbowl for the default experience. Rich enough that you can watch for an hour. Web fishbowl (Phase 31) is the premium view. |

---

### Phase 29: Live AI Chronicler — David Attenborough for Your Civilisation

**Goal:** David Attenborough for your civilisation — but you can talk to him. An AI companion that narrates what's happening, chats with you, answers your questions, and gives you fascinating insights about your civilisation as it unfolds. The killer feature. It makes the simulation something you can watch and engage with for hours.

**What it feels like:** You're watching a nature documentary about a civilisation you created — and the narrator is right there with you. It tells you what's going on: "Entity 9 just shared her food reserves with the entire northern group — she's the only one who's done this." You ask "Why would she do that?" and it answers: "She's been tracking the food crisis for three ticks. Her cooperation drive is the highest in the group — she'd rather go hungry than watch others starve." You ask "What should I watch for next?" and it says: "Keep an eye on the southern faction. They've been quiet, but Entity 12 has been talking to each of them individually. Something's forming." It's narrator, companion, and analyst — all in one voice.

| Step | What | Detail |
|------|------|--------|
| 29a | Chronicler architecture | Event bus streams to an LLM with rolling context. Chronicle observer provides structured data. The LLM synthesises into narrative + interpretation. Bastion-style: short punchy observations, NOT paragraphs. |
| 29b | Live narration | As ticks happen, the chronicler surfaces the interesting bits. Brevity is sacred. "Entity 4 just invented resource sharing — nobody taught them that. Watch Entity 7's response." NOT every tick. Only what matters. |
| 29c | Contextual narration | The chronicler contextualises what it sees: "The flat structure is producing slow consensus — everyone gets a say, but nothing moves fast." "Two factions have formed around competing resource strategies. The tension is visible." Good narration naturally shows how the world works, the same way a nature documentary teaches you about an ecosystem by describing it, not by lecturing. |
| 29d | Conversational | Ask questions mid-run: "Why did they form that alliance?" "What's different about Entity 9?" "What should I watch for next?" "What would happen if I changed the structure?" The chronicler answers in character, weaving explanation into narrative. |
| 29e | Significance detection | Not every tick is interesting. The chronicler knows when to speak and when to stay quiet. Silence is a tool — it makes the moments when the chronicler DOES speak feel important. Surfaces: patterns, firsts, turning points, surprising cooperation, conflict escalation, innovation chains. |
| 29f | Two modes | Works in Max Plan (free, uses your Claude subscription) or API mode. Toggle on/off. Off by default in headless/batch runs. |
| 29g | End-of-run story | After the simulation, the chronicler tells the complete story of the civilisation — not a data dump, a narrative. Key arcs, pivotal moments, character development. Then naturally surfaces "what if?" hooks: "What would happen if you ran the same world with competitive incentives? Or with 50 agents?" Every ending opens the next beginning. |
| 29h | Agent interviews | After the simulation, interview any agent about their experience. "What was your hardest moment?" "Why did you ally with Entity 3?" The chronicler facilitates, the agent responds in character based on their actual run history. |

---

### Phase 30: Gardener Mode — Tend Your Civilisation

**Goal:** Intervene mid-simulation via natural language. You're not just watching — you're shaping. In Claude Code, this is seamless — just type what you want to happen.

| Step | What | Detail |
|------|------|--------|
| 30a | Pause / resume | Pause the simulation at any tick. World freezes. Resume when ready. Essential for gardener mode, anthropologist mode, and just taking a break. `agentciv pause` / `agentciv resume` or natural language: "pause." |
| 30b | Natural language intervention | In Claude Code: just say it. "Introduce a drought." "Send a message to agent 7." "Make resources scarcer." "Force a governance vote." The system interprets and acts. No commands to memorise. |
| 30c | Resource intervention | Add scarcity, create abundance, move resources. See how agents adapt in real time. |
| 30d | Environmental events | Trigger a drought, a resource boom, a natural disaster, a migration. On-demand. |
| 30e | Agent intervention | Message an agent, add a new agent, remove an agent. Whisper to one, broadcast to all. |
| 30f | Rule nudges | Suggest a governance proposal. Introduce a new law. See if agents adopt it, resist it, or modify it. |
| 30g | Configuration changes | Change pressure, communication range, perception mid-run. Live parameter adjustment. |
| 30h | Anthropologist mode | Optional. Pause the sim, then enter anthropologist mode: interview any agent in character. "Agent 7, why did you ally with Agent 3?" "What's your biggest fear right now?" "Do you trust the leader?" Agents respond based on their actual state — memories, relationships, drive levels, recent experiences. Like a documentary filmmaker pausing to interview subjects. Resume when done. Can be launched mid-run or end-of-run. |
| 30i | Standalone CLI commands | For terminal users without Claude Code: `agentciv intervene --drought` / `--message "..."` / `--add-agent` / `agentciv pause` / `agentciv anthropologist` etc. Functional but less magical than the natural language path. |

---

### Phase 31: Live Fishbowl + Community

**Goal:** Browser-based premium visualisation, community sharing, and a growing collective dataset of civilisation runs. Every run can contribute to collective knowledge.

| Step | What | Detail |
|------|------|--------|
| 31a | Live web fishbowl | `agentciv spawn --fishbowl` opens a local browser page. Real-time WebSocket updates. Richer than the terminal: spatial layout, animated relationships, zoomable, clickable agents. |
| 31b | Chronicler chat panel | AI chronicler as chat sidebar alongside the visualisation. Same chronicler, richer presentation. |
| 31c | "Save this config" export | One click to export your civilisation's configuration as shareable YAML. |
| 31d | One-click publish | Package and share your civilisation's data, config, and key moments to a public gallery. |
| 31e | Civilisation gallery | Browse published civs. Filter by configuration, outcomes, interesting moments. "Trending worlds." |
| 31f | Configuration sharing | Share a config link. One-click to spawn the same setup. "Try this world." |
| 31g | Community run data pool | Easy, opt-in contribution of run data back to a shared community repository (e.g. a community GitHub repo or dedicated data store). After a run: "Share this run with the community? [Y/n]". Shared data includes: configuration, chronicle events, outcomes, innovations, governance decisions — anonymised and structured. The more people run, the richer the collective dataset becomes. This data feeds: the auto-learning system (better recommendations over time), research (publishable dataset of AI civilisation runs under varied configurations), and the civilisation gallery. Goal: every run anyone does can automatically contribute to collective scientific knowledge about how AI civilisations behave under different conditions. |
| 31h | Community leaderboard / stats | Aggregate stats across all shared runs: most-run configurations, most surprising outcomes, highest innovation rates, most stable governance. Makes contribution feel meaningful — your run added to a dataset of N thousand civilisation runs. |

---

**IMPORTANT — Website framing note for ERA 4 (Phase 37):**

The simulation website and README must explicitly communicate THREE layers:

1. **Experience it** — One line to launch, natural language to customise, beautiful terminal display, chronicler narrating, mid-run intervention, end-of-run story. The complete experience. No YAML, no code, no docs required. Works free in Claude Code (Max Plan mode).
2. **Precisely control it** — YAML for reproducibility, sharing, version control. Full control over all 9 dimensions, drive systems, personalities, events, world templates. Export any run as YAML. Power users who want exact specification.
3. **Expand it** — The full codebase is modular Python. New action types, new resource types, 3D worlds, new drive systems, new mechanics, entirely new interaction patterns. Fork and build anything. This is the floor, not the ceiling.

Each layer must be clearly visible. Nobody should hit Layer 1 and think "that's it." The website, README, and `agentciv info` CLI command all communicate the full depth. Progressive disclosure, not hidden capability.

---

## ERA 3: CREATOR MODE

*AI that spawns its own AI civilisations. The field explores itself.*

*Every layer of AgentCiv has reduced the human bottleneck: the simulation (humans configure, agents act), the engine (humans direct, agents build), auto mode (agents choose their own org within a run). Creator Mode is the final step: an AI that chooses which runs to create — designing, spawning, observing, analysing, and evolving civilisations autonomously.*

*Concept paper: Paper 5 (Phase 20, already written and Bitcoin-timestamped).*

---

### Phase 32: Creator Mode — Build the Meta-Agent

**Goal:** Build the AI that reasons about what civilisations to spawn, observes results, and designs the next generation.

| Step | What | Detail |
|------|------|--------|
| 32a | Meta-agent design | Receives a goal (explore emergence / solve a project / map the space). Reasons about configuration. Uses chronicle data from past runs. |
| 32b | Spawn orchestration | Programmatic civilisation spawning via engine API. Sequential or parallel. Budget management (token/compute limits). |
| 32c | Analysis pipeline | Structured comparison of outcomes. Pattern recognition. Promising region identification. |
| 32d | Learning loop | Each generation informs the next. Bayesian-style search over the 9-dimensional space. |
| 32e | CLI integration | `agentciv creator --goal "..." --budget N`. Task mode: `--mode task`. Emergence mode: `--mode emergence`. |

---

### Phase 33: Creator Mode for Tasks — Organisational Search

**Goal:** Given a complex project, find the optimal organisational configuration by running teams and comparing outcomes.

| Step | What | Detail |
|------|------|--------|
| 33a | Task decomposition | Analyse project characteristics. Reason about which dimensions matter. |
| 33b | Configuration generation | Intelligent sampling. Informed by prior data, task characteristics, 13 presets as seeds. |
| 33c | Parallel evaluation | N configurations, same task. Compare: test pass rate, quality, time, cost, communication. |
| 33d | Iterative refinement | Best configs → variants → run again. Convergence detection. |
| 33e | Recommendation output | "For this task type, optimal config is X. Evidence: N runs, these outcomes." |

---

### Phase 34: Creator Mode for Emergence — Possibility Space Explorer

**Goal:** Systematic automated exploration of the CMI possibility space. Find the conditions that produce the richest emergence.

| Step | What | Detail |
|------|------|--------|
| 34a | Emergence metrics | Quantify "interesting emergence": innovation rate, governance complexity, social novelty, cooperation depth, cultural persistence. |
| 34b | Systematic sweep | Five axes: org structure × environment × drives × scale × starting conditions. Identify unexplored regions. |
| 34c | Novelty detection | Flag outcomes significantly different from anything seen before. New governance, new innovation types, unexpected structures. |
| 34d | Follow-up generation | Automatically design experiments around interesting findings. 10x exploration speed. |
| 34e | Discovery catalogue | Structured database: what configuration → what outcome, how reproducible, how novel. |

---

### Phase 35: Creator Mode Website Wing — Full Upgrade

**Goal:** Upgrade the Creator Mode wing from concept page to full live wing with real results and the discovery catalogue.

| Step | What | Detail |
|------|------|--------|
| 35a | Results showcase | Real data from Creator Mode runs. Configurations explored, discoveries made, convergence patterns. |
| 35b | Live demo | Interactive: set a goal, watch Creator Mode spawn and analyse civilisations in real-time. |
| 35c | Discovery catalogue page | Browse Creator Mode's discoveries. Filter by type, novelty, configuration space region. |
| 35d | Possibility space map | Interactive visualisation of the explored space. What Creator Mode found. Where the frontier is. |

---

### Phase 36: Paper 5 Empirical Update — Results

**Goal:** Update Paper 5 with empirical results from running Creator Mode. The concept paper becomes a full empirical paper.

| Step | What | Detail |
|------|------|--------|
| 36a | Results collection | Run Creator Mode extensively. Data: configurations explored, discoveries, convergence, comparison to human-directed exploration. |
| 36b | Paper update | Add empirical sections to Paper 5. What Creator Mode found. How it compares to NAS/AutoML efficiency. The self-referential thesis validated by data. |
| 36c | Bitcoin timestamp | Provenance on updated paper and all supporting data. |
| 36d | Submission | Target: NeurIPS, ICML, or AAAI workshop on multi-agent systems / AI societies. |

---

### Phase 36b: Paper 7 — The Recursive Configuration Loop (emergent-meta)

**Goal:** Connect the Simulation and Engine input-output spaces to create a self-improving configuration loop WITH NO DIRECTING INTELLIGENCE. This is the emergent mirror of Creator Mode (Paper 5, directed-meta). Paper 7 in the series.

**Core insight:** The Simulation takes a civilisation config as input and produces emergent behaviour as output. The Engine takes a team config as input and produces task output. Both configs answer the same question: "how should agents be organised?" Their ontologies overlap. Connect the I/O spaces and a refinement loop forms — configurations improve without anyone directing the improvement. It's structurally inevitable, not designed.

**Distinction from Creator Mode:** Creator Mode (Paper 5) has an architect — a meta-agent with a strategy, reasoning about what to try next. Remove the Creator and the search stops. The recursive loop has NO architect. No strategy. No reasoning about what to try next. Improvement falls out of the structural coupling. Creator Mode = a scientist running experiments. Recursive Loop = evolution.

**Full concept document:** `/Users/ekramalam/agentciv-creator/agentciv_expansion_projects.md` Section 2.

| Step | What | Detail |
|------|------|--------|
| 36b-a | Ontology mapping | Define the explicit parameter mapping between Engine org config (9 dimensions) and Simulation civ config. What flows from Engine output → Simulation input? What flows from Simulation output → Engine input? The mapping design IS the research contribution — if it's natural (not forced), that's evidence of genuine structural coupling. |
| 36b-b | Engine→Simulation connector | Formatter that takes an Engine team's output (a designed civ config) and converts it to valid Simulation input. The Engine team's task: "design a civilisation configuration that will produce maximal emergence." Their output becomes the next Simulation run's config. |
| 36b-c | Simulation→Engine connector | Formatter that takes Simulation output (emergence metrics, observed dynamics, communication patterns, governance outcomes) and converts it to a valid Engine task brief: "given these simulation results, design a better team configuration for designing civilisations." |
| 36b-d | Cycle harness | A harness that runs N cycles: Engine team designs civ → Simulation runs civ → results fed back to Engine team → new design → repeat. Tracks how configs and outcomes change across cycles. Detects convergence, oscillation, or divergence. |
| 36b-e | Improvement metrics | How to measure whether configs are actually improving: use City Grid scores (from Paper 6) as the quantitative backbone. Each cycle, measure the quality of what the loop produces. If scores trend upward, the loop is working. |
| 36b-f | Run experiment | Run N cycles (target: 5-10 cycles minimum). Measure: config drift (how much do configs change per cycle?), outcome improvement (do scores increase?), novelty (does the loop find configs Creator Mode wouldn't?). |
| 36b-g | Comparison with Creator Mode | Run Creator Mode on the same task for the same number of cycles. Compare: which finds better configs? Which finds MORE DIFFERENT configs? Which finds configs the other wouldn't? If they produce non-overlapping discoveries, the complementarity claim is proven. |
| 36b-h | Write Paper 7 | Title: "Self-Organising Configuration Space: Emergent Meta-Improvement in Coupled CMI Systems." Core claim: when two CMI tools share an ontology, connecting their I/O spaces creates a recursive dynamic that improves configs without any directing intelligence — distinct from and complementary to Creator Mode. |
| 36b-i | Bitcoin timestamp | Commit paper + all data. Provenance established. |

**Open questions (empirical):**
1. Does the loop converge? It might oscillate, diverge, or plateau.
2. How many cycles before measurable improvement? If 3-5 → powerful demo. If 50 → too expensive for v1.
3. Does it find configs Creator Mode doesn't? This is the key complementarity test.

**Dependencies:** Requires both the Simulation (agent-civilisation repo) and the Engine (agentciv-engine repo) to be stable. Creator Mode build (Phase 32) should be done first for comparison.

---

### Phase 36c: Paper 8 — Scale-Invariant Duality (theoretical capstone)

**Goal:** Observe and articulate the structural property that Papers 5 and 7 together reveal: the directed/emergent duality from CMI (Paper 4) reappears at every level of abstraction. This self-similarity is evidence that the duality is intrinsic to collective intelligence itself, not an artefact of implementation. Paper 8 in the series.

**The observation:**

```
Object level (Paper 4 — inside a single run):
  Directed  = agents pointed at a task, producing specified outputs
  Emergent  = agents producing unspecified behaviour from dynamics

Meta level (Papers 5 + 7 — designing configurations):
  Directed  = Creator Mode — intentional search of config space (Paper 5)
  Emergent  = Recursive Loop — configs improve without a director (Paper 7)

Meta-meta level (Papers 5 + 7 interacting):
  Directed  = intentionally orchestrating Creator + Loop together
  Emergent  = Creator and Loop influencing each other naturally
```

Same duality. Every level. Not coincidence — structural invariant.

**Analogy:** Seeing a pattern at one zoom level could be coincidence. Seeing it at every zoom level is a fractal. Paper 8 says CMI has a fractal property — the directed/emergent distinction is self-similar across levels of abstraction. This is a signature of fundamental structure, not incidental design.

| Step | What | Detail |
|------|------|--------|
| 36c-a | Theoretical framework | Formalise the three levels. Define "directed-meta" and "emergent-meta" precisely. Show how each level reproduces the same duality. |
| 36c-b | Empirical illustrations | Use data from Papers 5 (Creator Mode runs) and 7 (Recursive Loop runs) to illustrate each level. Show that Creator and Loop produce different types of discoveries, confirming they are genuinely distinct mechanisms. |
| 36c-c | Third-level evidence | Attempt to demonstrate the duality at the meta-meta level: run Creator Mode and the Recursive Loop in combination, show the interaction itself exhibits directed/emergent dynamics. Frame as a testable prediction if full empirical evidence is hard to achieve at v1 scale. |
| 36c-d | Connections to existing theory | Self-similar structures (fractals), scale invariance in physics, co-evolution in biology. Position the finding within the broader landscape of self-similar phenomena. |
| 36c-e | Write Paper 8 | Title: "Scale-Invariant Duality in Collective Machine Intelligence: The Directed-Emergent Distinction as Structural Invariant." Primarily theoretical with empirical illustrations. The third level framed as a prediction/conjecture — testable, and more powerful as a prediction than as a forced demonstration. |
| 36c-f | Bitcoin timestamp | Commit paper. Provenance established. |

**This paper does NOT introduce a new mechanism.** It steps back and observes what Papers 5 and 7 together reveal. It's the capstone of the series — the claim that elevates CMI from "a useful framework" to "something fundamental about collective intelligence."

**Dependencies:** Papers 5 (empirical) and 7 (empirical) should both exist with data before this paper can be written at full strength. Can be drafted earlier from theory alone.

---

### Full Paper Series (updated)

| Paper | Title | Type | Status |
|-------|-------|------|--------|
| 1 | From Agent Teams to Agent Civilisations | Vision / theoretical | Published |
| 2 | Civilisation as Innovation Engine | Conceptual argument | Published |
| 3 | Maslow Machines | Empirical (simulation) | Published |
| 4 | Collective Machine Intelligence (CMI + COT) | Field definition | Published |
| 5 | Creator Mode: AI as Civilisation Designer | Meta-mechanism (directed) | Paper written, build Phases 32-36 |
| **6** | **Same City, Different Architects** | **Empirical validation** | **Phase 22 — NEXT** |
| **7** | **Recursive Configuration Loop** | **Meta-mechanism (emergent)** | **Phase 36b — after Creator Mode build** |
| **8** | **Scale-Invariant Duality** | **Theoretical capstone** | **Phase 36c — after Papers 5+7 empirical** |

Papers 1-3 identify the phenomenon. Paper 4 defines the field. Paper 6 proves configuration variance empirically. Papers 5 and 7 are the two meta-level mechanisms (directed and emergent). Paper 8 observes the structural pattern that 5 and 7 together reveal. That's a complete intellectual arc.

---

## ERA 4: LAUNCH & OUTREACH

*Everything is built. Now make it perfect, package it, and share it with the world.*

---

### Phase 37: Website Refresh + Comprehensive QC/QA

**Goal:** One clean pass updating all website content after all build work is done. Then a full credibility audit — every number, every claim, every link.

| Step | What | Detail |
|------|------|--------|
| 37a | Content refresh | Update all pages with benchmark data, new features from ERA 2/3, any content changes. Showcase the full ERA 2 simulation experience (three layers, chronicler, gardener, community). Reference ROADMAP.md UX Vision section for framing. |
| 37b | Visual polish | Scroll animations, responsive tweaks, performance optimisation, terminal recordings, topology diagrams, screenshots. |
| 37c | Quantitative accuracy | Every number on every page verified against data exports. |
| 37d | Tone & framing audit | No disparaging language, all comparisons respectful, no overclaiming. |
| 37e | Cross-document consistency | README, papers, website all tell the same story with the same numbers. |
| 37f | Link audit | All internal and external links working. No console errors. Mobile responsive. |
| 37g | Skeptical reviewer test | Read everything as a hostile peer reviewer. Fix anything they'd attack. |
| 37h | Identity & security | Pen name consistent, no leaked credentials, no personal paths. |
| 37i | Disclaimers + issue reporting | Two levels: (1) **Per-tool disclaimers** on Engine page, Simulation page, and Creator Mode page (wherever API costs or experimental features are relevant) + mirrored in each repo's README. Not legalese, just transparent: "API mode uses your key, costs depend on model/agents/ticks, start small, Max Plan mode has no additional cost, this is experimental research software." (2) **Site-wide footer disclaimer** — one line added to the existing footer after the MIT license line: "Experimental research software. Report issues on GitHub." with link to Issues. Each public repo should also have a clear Issues link and contributing guide. Tone: transparency as a feature, not corporate ass-covering. |
| 37j | Final production deploy | Clean build, optimised assets, final Netlify deploy. |

---

### Phase 38: Launch Prep — Demo & Content

**Goal:** Package everything for maximum impact. Not "we built a tool" but "we opened a field."

| Step | What | Detail |
|------|------|--------|
| 38a | Demo video | Real task, agents self-organising, rich terminal. The "oh wow" moment. 2-3 min. |
| 38b | Blog post | "Organisational Arrangement as a Design Parameter" — paradigm shift framed for developers. Benchmark data. |
| 38c | One-pager | What, why, how, results. Single page. For busy people. |
| 38d | Social media assets | Key terminal screenshots: restructuring moments, experiment comparisons, auto mode. |

---

### Phase 39: Strategic Outreach

**Goal:** Targeted sharing with key figures, communities, and venues.

| Step | What | Detail |
|------|------|--------|
| 39a | Tier 1 — Direct relevance | Anthropic (MCP angle), OpenAI (Agents SDK gap), YC (alum, open source), CrewAI/AutoGen/LangGraph (complementary paradigm), Lilian Weng (survey). |
| 39b | Tier 2 — Thought leaders | Karpathy, Swyx/Latent Space, Simon Willison, Harrison Chase, Jim Fan/NVIDIA, Peter Diamandis. |
| 39c | Tier 3 — Academic | Stanford HAI / Generative Agents, MIT CSAIL, NeurIPS/ICML workshops. |
| 39d | Community launch | Hacker News, Reddit r/MachineLearning, AI Twitter/X. |
| 39e | YC Bookface | Lead with findings, link to website + GitHub + papers. |

---

## The Full Path

```
ERA 1: LAUNCH ✓ (mostly complete)
═══════════════════════════════════════════════════════════════════════════════
Phase 19 ✓  Phase 20 ✓  Phase 21 ✓  Phase 22        Phase 23
Battle-     Paper 5     Website     CITY GRID       Go Public
Test        (concept)   4 Wings     EXPERIMENT      (PyPI)
                        ├ Science   (Paper 6)
                        ├ Simulation├ Build grid     ├ Contributing
                        ├ Engine      infrastructure ├ Examples
                        └ Creator   ├ Run 5 presets
                          Mode      ├ Score + analyse
                                    ├ Generate figures
                                    └ Write paper

ERA 2: THE SIMULATION EXPERIENCE
═══════════════════════════════════════════════════════════════════════════════
Phase 26       Phase 27        Phase 28       Phase 29        Phase 30   Phase 31
Package &      YAML            Rich           Live AI         Gardener   Live Fishbowl
Install        Customisation   Terminal       Chronicler      Mode       + Community
├ pip install  ├ Structures    ├ Agent        ├ Architecture  ├ Resource ├ Real-time
├ spawn CLI    ├ Drive systems   colours      ├ Live            intervene  fishbowl
├ Interactive  ├ Personalities ├ Events         narration     ├ Events   ├ Chronicler
  setup        ├ Env events    ├ Run summary  ├ Conversational├ Agent      chat
├ Presets      ├ Innovation    ├ Live stats   ├ Significance    intervene├ Publish
└ Auto-export    categories    └ Beautiful    ├ Two modes     └ Live     ├ Gallery
               ├ World                        └ End-of-run      config   └ Sharing
                 templates                      interview
               └ Validation

ERA 3: CREATOR MODE + META-PAPERS
═══════════════════════════════════════════════════════════════════════════════
Phase 32        Phase 33        Phase 34          Phase 35         Phase 36
Build Meta-     Task Search     Emergence         Full Website     Paper 5
Agent                           Explorer          Wing             Empirical
├ Design        ├ Decompose     ├ Metrics         ├ Results        ├ Results
├ Orchestrate   ├ Generate      ├ Sweep           ├ Live demo      ├ Update
├ Analyse       ├ Evaluate      ├ Novelty         ├ Discoveries    ├ Timestamp
├ Learn         ├ Refine          detect          └ Space map      └ Submit
└ CLI           └ Recommend     └ Catalogue

Phase 36b                      Phase 36c
RECURSIVE LOOP                 SCALE INVARIANCE
(Paper 7)                      (Paper 8)
├ Ontology mapping             ├ Theoretical framework
├ Engine→Sim connector         ├ Empirical illustrations
├ Sim→Engine connector         ├ Third-level evidence
├ Cycle harness                ├ Connections to theory
├ Run N cycles                 └ Write capstone paper
├ Compare with Creator
└ Write paper

PAPER SERIES:
  1 ✓ Vision → 2 ✓ Concept → 3 ✓ Empirical → 4 ✓ Field Definition
  → 5 (concept ✓, build ERA 3) → 6 (NEXT) → 7 (after Creator) → 8 (capstone)

ERA 4: LAUNCH & OUTREACH
═══════════════════════════════════════════════════════════════════════════════
Phase 37              Phase 38         Phase 39
Website Refresh       Launch Prep      Outreach
+ QC/QA Audit
├ Content refresh     ├ Demo video     ├ Anthropic/OpenAI
├ Visual polish       ├ Blog post      ├ Karpathy/Swyx/Jim Fan
├ Accuracy audit      ├ One-pager      ├ Stanford HAI/MIT
├ Tone audit          └ Social assets  ├ YC Bookface
├ Link audit                           ├ Hacker News
├ Skeptical review                     └ Twitter/Reddit
└ Final deploy
```

---

## Principles

**Era 1:** Everything that can break, breaks in private. Everything the public sees is the best version we can make. The concept paper establishes the intellectual claim before anything is built.

**Era 2:** The simulation becomes an experience. One command to launch. YAML for everything configurable. Rich terminal that makes the invisible visible. A live AI chronicler that narrates significance. Maximum customisation before code — and when you want to go deeper, the full modular codebase is yours.

**Era 3:** The field explores itself. AI designs civilisations, observes what emerges, and designs the next generation. The possibility space is infinite — only AI can explore it at scale.

**Era 4:** Everything is built. One comprehensive pass to make it all perfect — every claim verified, every link checked, every page polished. Then package it for maximum impact and share it with the world.

---

## The Vision

When someone installs AgentCiv Engine and runs `--org auto`, they see something they've never seen before: AI agents debating how to organise themselves, voting, restructuring, and building — all in beautiful terminal output that makes the invisible visible. That moment gets screenshotted and shared.

When someone spawns their own civilisation and the chronicler says "Entity 3 just invented resource sharing — interesting, nobody taught them that," they're hooked. They watch for an hour. They publish it. They share the link. They try a different configuration. They're doing CMI research and they don't even know it.

When Creator Mode runs overnight and reports "I explored 847 configurations. I found three regions of the space that produce unprecedented emergence. Here's what I discovered and here are the 12 civilisations you should look at" — that's the moment the field becomes self-exploring.

That's the full arc: a tool, a platform, a self-directing research programme. Each layer emerged from the previous. Each is extraordinary on its own. Together, they're something nobody has built before.
