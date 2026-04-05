# Paper 6: "Same City, Different Architects"

**Full title:** Same City, Different Architects: How Organisational Structure Shapes Collective AI Output Quality, Process, and Emergent Behaviour

**Authors:** Mark E. Mala

**Target:** NeurIPS 2026 / ICML Multi-Agent Systems / standalone arXiv preprint

**Status:** Pre-execution. Methodology pre-registered and Bitcoin-timestamped.

---

## 1. THE THESIS (one sentence)

Organisational structure is a significant, underexplored design parameter for multi-agent AI systems — the same task solved by teams with different authority, communication, and decision-making structures produces measurably different outputs of measurably different quality, via measurably different processes, with measurably different emergent behaviours.

## 2. WHY THIS MATTERS

Every multi-agent AI framework (CrewAI, AutoGen, LangGraph, Agents SDK) hardcodes a single coordination strategy. Nobody is asking: **what if the team structure itself was the variable?**

Organisational theory has known for 60 years that structure shapes performance in human teams (Burns & Stalker 1961, Mintzberg 1979, Galbraith 1973). Yet AI research treats multi-agent coordination as a fixed engineering choice, not an experimental variable.

This paper introduces the first controlled experiment measuring the effect of organisational structure on multi-agent AI team performance — not on binary pass/fail coding tasks, but on an open-ended collaborative design task where output quality varies on a continuous spectrum and is visible to the naked eye.

**What makes this publishable even with small N:**
- The QUESTION is novel (nobody is asking it)
- The TASK is purpose-built to maximise configuration variance visibility
- The METHODOLOGY is rigorous (pre-registered, controlled, reproducible)
- The OUTPUT is visual — five city grids side by side is undeniable
- The SCORING is multi-dimensional and continuous (not binary pass/fail)
- The PROCESS DATA is rich (how teams actually behave differently)
- The IMPLICATIONS are enormous (opens an entire research programme)
- The INFRASTRUCTURE is open-source (anyone can reproduce and extend)

## 3. THE TASK SELECTION PROBLEM

### 3.1 The Four Properties

Most candidate tasks for benchmarking multi-agent teams fail to reveal configuration effects because they lack one or more of four critical properties. Any task used to measure configuration variance must satisfy ALL FOUR simultaneously:

**Property 1: Multiple valid outputs.** The task cannot have a single correct answer. If it does (e.g., fizzbuzz), every team converges to the same output regardless of configuration, and the experiment proves nothing. The solution space must be combinatorial — different teams should produce genuinely different outputs.

**Property 2: Composition from parts.** Each agent must contribute a piece, and those pieces must integrate. If agents work independently on isolated subtasks, configuration doesn't matter. Coordination (or lack thereof) must be directly visible in the output.

**Property 3: Measurable quality on a continuous spectrum.** Not binary pass/fail, but multi-dimensional scoring where you can say "this output scored 74, that one scored 91." Quality dimensions must be automatable — no subjective human judgment.

**Property 4: The process visibly differs.** An observer watching the agents work should see different behaviour patterns across configurations, not just different outputs. The organisational structure should manifest in HOW the team works, not just WHAT they produce.

### 3.2 Why Common Tasks Fail

| Task | P1: Multiple outputs | P2: Composition | P3: Continuous scoring | P4: Visible process | Verdict |
|------|---------------------|-----------------|----------------------|--------------------|---------|
| Fizzbuzz | No — one answer | No | No — binary | No | Fails 4/4 |
| Calculator | No — one answer | Partial | No — binary | Partial | Fails 2/4 |
| Todo CLI | No — converges | Low coordination | No — binary | Partial | Fails 2/4 |
| Chat server | No — works or doesn't | Partial | No — binary | Partial | Fails 2/4 |
| SWE-bench bugs | No — one fix | Low for most | No — tests pass or don't | Partial | Fails 2/4 |
| API spec design | Yes | Yes | Hard to automate | Yes | Fails 1/4 |
| Research briefing | Yes | Yes | Subjective | Yes | Fails 1/4 |
| **City Grid** | **Yes — combinatorial** | **Yes — integration critical** | **Yes — 5 automated dimensions** | **Yes — territory vs coordination** | **Passes 4/4** |

This framework is itself a contribution. It explains why most multi-agent benchmarks fail to reveal configuration effects and provides a principled basis for designing tasks that do.

## 4. THE CITY GRID TASK

### 4.1 Task Description

Agents are given a 10×10 grid and a set of building types. Their task: design and build a functional city. The city must have roads connecting buildings, logical zoning (residential near parks, not industrial), diverse infrastructure, and efficient use of space.

**Building types:**
- Residential (R) — houses, apartments
- Commercial (C) — shops, offices
- Industrial (I) — factories, workshops
- Park (P) — green spaces, recreation
- Road (.) — transportation network
- Hospital (H) — healthcare
- School (S) — education
- Empty (_) — unused space

**Placement rules (provided to agents):**
- Roads must form a connected network (no isolated segments)
- Every building must be adjacent to at least one road
- Residential should be near parks and schools (good), away from industrial (bad)
- Commercial benefits from road frontage and residential proximity
- Industrial should be clustered and away from residential
- Hospitals and schools serve surrounding area — placement matters

**Output format:** A 10×10 grid as a text file, where each cell contains a building type code. Plus a brief city plan document explaining design decisions.

### 4.2 Why City Grid Is Ideal

The solution space is enormous. A 10×10 grid with 8 cell types has 8^100 possible configurations. Even restricting to "valid" cities (connected roads, all buildings reachable), the space is combinatorial. Different teams WILL produce different cities.

The task requires composition: agents must coordinate road networks, agree on zoning, and integrate their contributions. A road placed by Agent A must connect to buildings placed by Agent B. This is where team dynamics become visible in the output.

Quality is measurable on a continuous spectrum across five automated dimensions (Section 4.3). And the process visibly differs — competitive teams claim territory and duplicate infrastructure, collaborative teams coordinate zones, hierarchical teams follow a lead architect.

### 4.3 Scoring Dimensions (5)

Each dimension is scored 0–100. All scoring is automated — no human judgment.

**1. Coverage (0–100)**
- Percentage of grid cells utilised (non-empty)
- Score = (used cells / 100) × 100
- Penalises wasted space. A half-empty grid scores 50.

**2. Accessibility (0–100)**
- Can all buildings be reached via the road network?
- Score = (reachable buildings / total buildings) × 100
- Uses BFS/DFS from any road cell. Isolated buildings score 0.

**3. Zoning Logic (0–100)**
- Measures quality of adjacency relationships
- Good adjacencies: residential↔park (+), residential↔school (+), commercial↔road (+), industrial↔industrial (+)
- Bad adjacencies: residential↔industrial (−), hospital↔industrial (−)
- Score = weighted sum of good adjacencies minus penalties, normalised to 0–100

**4. Diversity (0–100)**
- Distribution of building types
- Shannon entropy of building type distribution, normalised
- A city of only houses scores low. A balanced mix scores high.
- Score = (observed entropy / max entropy) × 100

**5. Connectivity (0–100)**
- Coherence of the road network
- Measures: connected components (fewer = better), dead ends (fewer = better), average path length between buildings (shorter = better)
- Score = weighted combination, normalised to 0–100

**Aggregate score:** Harmonic mean of all 5 dimensions. This penalises any dimension being near zero — a city can't compensate for no roads by having excellent zoning. Individual dimension scores are also reported for analysis.

### 4.4 Visual Outputs

The city grid produces three types of visual evidence:

**1. Final grid comparison.** Five rendered city grids side by side (one per preset). Colour-coded by building type. This is the hero image of the paper — undeniable visual proof that configuration produces different outputs.

**2. Temporal animation.** Per-tick grid snapshots rendered as animation. Shows HOW each team built their city. Competitive teams: agents claiming quadrants, building in parallel, fragmented infrastructure. Collaborative teams: roads first, then coordinated zone filling. Hierarchical: one agent's master plan being executed by others. We already capture per-tick snapshots — this is a rendering pass over existing data.

**3. Agent contribution heatmap.** Each cell colour-coded by which agent placed it. Instantly visualises work distribution. Competitive: 4 distinct regions. Collaborative: interleaved contributions. Hierarchical: planner designs, executors fill. This gives Gini coefficient as a visual, not just a number.

### 4.5 What We Expect to See

| Preset | Expected city character | Expected score profile |
|--------|------------------------|----------------------|
| **Collaborative** | Coherent plan, connected roads, logical zones, even contribution | High accessibility, high connectivity, balanced |
| **Hierarchical** | Planned and orderly but potentially conservative | High connectivity (one plan), moderate diversity |
| **Competitive** | Fragmented — agents claim territory, duplicate infrastructure | High coverage (everyone builds), low connectivity (no coordination) |
| **Meritocratic** | High quality but potentially slow/incomplete (review overhead) | Highest zoning logic (reviewed), may have low coverage (less built) |
| **Auto** | Adaptive — structure emerges to match the task | Potentially highest overall (self-optimised for this specific task) |

## 5. EXPERIMENTAL DESIGN

### 5.1 Independent Variable: Organisational Structure (5 presets)

| Preset | Authority | Communication | Decisions | Roles | Why include |
|--------|-----------|--------------|-----------|-------|-------------|
| **collaborative** | flat | mesh | consensus | emergent | The baseline — how most frameworks work |
| **hierarchical** | hierarchy | hub-spoke | top-down | assigned | Classic management structure |
| **competitive** | anarchic | whisper | autonomous | fixed | No collaboration — agents race independently |
| **meritocratic** | distributed | mesh | meritocratic | emergent | Quality-gated — mandatory peer review |
| **auto** | (agents choose) | (agents choose) | (agents choose) | (agents choose) | Crown jewel — agents design their own structure |

These five span the key dimensions:
- Flat vs hierarchical authority
- Open vs restricted communication
- Collaborative vs competitive incentives
- Quality-focused (meritocratic) vs speed-focused (competitive)
- Human-designed vs self-designed (auto)

### 5.2 Dependent Variables: What We Measure

**Tier 1 — Outcome metrics (what did the team produce?):**
- Aggregate city score (harmonic mean of 5 dimensions)
- Individual dimension scores (coverage, accessibility, zoning, diversity, connectivity)
- Grid completeness (did they produce a valid grid?)
- Ticks to completion
- Total tokens consumed (compute cost)

**Tier 2 — Process metrics (HOW did the team work?):**
- Communication volume (messages, broadcasts)
- Communication graph density (how connected is the team?)
- Hub-spoke ratio (is one agent a bottleneck?)
- Gini coefficient (how evenly is work distributed?)
- Merge conflicts (coordination failures)
- Parallel utilisation (are agents working simultaneously?)
- Agent contribution heatmap (who built what?)

**Tier 3 — Emergence metrics (what unexpected behaviours appear?):**
- Role emergence (did unprescribed specialisation develop? e.g., "road builder" vs "zone planner")
- Restructure log (auto mode only — what structure did agents design?)
- Phase transitions (when did the team "find its rhythm"?)
- Communication efficiency (quality score / communication volume)
- Relationship trust dynamics (how did trust evolve across ticks?)

All metrics already implemented and auto-captured. Every run saves comprehensive JSON.

### 5.3 Controls

- **Agent count:** 4 per team (consistent across all presets)
- **Model:** Claude Sonnet 4 for all runs (constant)
- **Max ticks:** 15 (enough for a complete city, consistent across presets)
- **Runs per combo:** 3 (for variance estimation and statistical power)
- **Single-agent baseline:** Same task with agents=1 (is a team even helpful?)
- **Random seed variation:** Different seeds per run for stochastic variation

### 5.4 Run Matrix

| What | Presets | Runs each | Total runs |
|------|---------|-----------|------------|
| City Grid — team runs | 5 | 3 | 15 |
| City Grid — single-agent baseline | 1 | 3 | 3 |
| Civ Config Design — team runs | 5 | 2 | 10 |
| **Total** | | | **28** |

Each run produces:
- Full JSON with all 3 tiers of metrics
- Grid state at every tick (for animation) [City Grid only]
- Per-agent contribution map [City Grid only]
- Designed civ config + emergence score [Civ Config only]
- Full message content and agent reasoning
- Relationship trust snapshots per tick

### 5.5 Second Experiment: Teams as Civilisation Designers

Different Engine teams are given the task: "Design a civilisation configuration for the AgentCiv Simulation that will produce the richest emergent behaviour." Each team produces a JSON config (org structure, environment settings, drive weights, agent count). The resulting configs are scored by running them in the Simulation and measuring emergence metrics (innovation rate, governance complexity, cooperation depth).

**Why this satisfies all 4 properties:**
1. **Multiple valid outputs** — the space of valid civ configs is enormous
2. **Composition** — the team must agree on a coherent, internally consistent config
3. **Continuous scoring** — emergence metrics provide a quality spectrum
4. **Visible process** — competitive teams produce incoherent configs (each agent adds contradictory settings), collaborative teams negotiate a unified vision

**Why include this:** It shows the Engine works on meta-level tasks, not just coding. It's a use case of the Engine where the output directly connects to another AgentCiv tool (the Simulation). Different team structures produce genuinely different civilisation designs — proving configuration variance extends to abstract design tasks, not just spatial/visual ones.

**Scoring:** Run each designed config in the Simulation for N ticks. Measure: innovation count, governance formation, cooperation events, total wellbeing, structural complexity. Normalise to a 0-100 emergence score.

### 5.6 Secondary Validation: Internal Tasks

The smoke test data we already have (fizzbuzz + calculator, collaborative vs competitive) serves as secondary validation: "process-level patterns hold even on simpler, binary-outcome tasks." This data is included in the appendix.

| Task | Presets | Runs | Status |
|------|---------|------|--------|
| fizzbuzz | collaborative, competitive | 1 each | DONE |
| calculator | collaborative, competitive | 1 each | DONE |

### 5.7 Cost Estimate

- 18 City Grid runs × ~$2-3 per run = **~$36-54**
- 10 Civ Config runs × ~$2 per run = **~$20**
- Buffer / retries = ~$15
- **Total: ~$70-90**

Within $100 budget.

## 6. PAPER STRUCTURE

### Abstract (~200 words)
The problem (org structure ignored in multi-agent AI) → the task selection problem (why most benchmarks can't reveal configuration effects) → what we did (purpose-built city design task, 5 organisational structures, 4-property task framework) → what we found (visually and quantitatively different outputs, different processes, different emergence) → why it matters (opens a research programme).

### 1. Introduction (~1.5 pages)
- Multi-agent AI is booming: CrewAI, AutoGen, LangGraph, Agents SDK
- But all frameworks hardcode coordination strategy
- Management science knows structure matters (60 years of org theory)
- **We introduce the first controlled experiment treating org structure as an independent variable**
- **We introduce the 4-property framework for benchmark task design**
- Preview of findings: five visually distinct cities, quantitatively different on every dimension

### 2. Related Work (~1 page)
- **Multi-agent AI frameworks** — CrewAI, AutoGen, LangGraph, Agents SDK, Camel. Fixed architectures. No systematic comparison.
- **Organisational theory** — Burns & Stalker (mechanistic vs organic), Mintzberg (structural configurations), Galbraith (information processing), contingency theory. 60 years of evidence that structure shapes performance in human orgs.
- **AI benchmarks** — SWE-bench, HumanEval. All binary pass/fail. None measure team structure effects. None designed to reveal configuration variance.
- **Multi-agent coordination** — Existing work on agent communication, planning, tool use. Structure is always hardcoded, never the experimental variable.
- **Gap:** Nobody has systematically measured whether org structure matters for AI teams. Nobody has designed benchmark tasks specifically to reveal configuration effects. We fill both gaps.

### 3. The Task Selection Problem (~1.5 pages)
- **Why most tasks fail:** Binary outcomes (fizzbuzz, SWE-bench) converge regardless of structure. The 4-property framework: multiple valid outputs, composition from parts, continuous scoring, visible process difference.
- **Table of rejected tasks** with per-property analysis
- **The city grid:** uniquely satisfies all four properties AND produces visual output
- **Contribution:** The 4-property framework itself is a methodological contribution. Future researchers can use it to design configuration-variance-revealing tasks in other domains.

### 4. The AgentCiv Engine (~1.5 pages)
- 9 organisational dimensions (authority, communication, roles, decisions, incentives, information, conflict, groups, adaptation)
- 13 presets spanning the organisational space (5 used in this experiment)
- Enforcement mechanisms (not suggestions — hard constraints on communication, authority, information flow)
- Agent architecture: observe → reason → decide → act → reflect
- Tools: read, write, run, communicate, claim, broadcast, done
- Chronicle system: structured data capture every tick (messages, files, relationships, conflicts)

### 5. Experimental Design (~1.5 pages)
- The city grid task: grid spec, building types, placement rules, scoring dimensions
- IV: 5 presets (Section 5.1)
- DV: 3 tiers of metrics (Section 5.2)
- Controls: fixed agent count, model, max ticks
- Pre-registration: methodology committed and Bitcoin-timestamped before any runs
- Reproducibility: all code, configs, and data published

### 6. Results (~4 pages)

#### 6.1 Visual Evidence: The Five Cities
- Hero image: five rendered grids side by side, one per preset
- Temporal animation frames showing build progression
- Agent contribution heatmaps
- **This section alone proves the thesis visually**

#### 6.2 Outcome Quality (Tier 1)
- Table: preset × dimension score matrix
- Radar charts: per-preset quality profiles across 5 dimensions
- Aggregate harmonic mean comparison
- Statistical significance tests (Kruskal-Wallis across presets, Mann-Whitney pairwise)
- Effect sizes (Cohen's d)
- Key findings: [which preset wins on which dimensions?]

#### 6.3 Process Differences (Tier 2)
- Communication network graphs per preset (visualise topology)
- Hub-spoke ratios (hierarchical = high, collaborative = low)
- Gini coefficients (work distribution) with heatmap visualisation
- Communication efficiency (quality score / message volume)
- Merge conflict rates
- Key findings: [communication structure matches prescribed structure — enforcement works]

#### 6.4 Emergent Behaviour (Tier 3)
- Role emergence analysis (did agents specialise? e.g., "road builder" vs "zone planner")
- Temporal trust evolution (relationship snapshots over ticks)
- Phase transitions and convergence patterns
- Auto mode: what structure did agents choose? Did it vary across runs?
- Key findings: [auto mode converges to what structure? unexpected role patterns?]

#### 6.5 Extension: Teams as Civilisation Designers (~1 page)
- Different Engine teams given the meta-task: "design a civilisation configuration for maximal emergence"
- Each team produces a JSON config → scored by running it in the Simulation
- Shows configuration variance extends to abstract design tasks, not just spatial ones
- Shows the Engine as a tool whose output connects directly to another AgentCiv tool (the Simulation)
- Different team structures produce genuinely different civilisation designs
- Scored by emergence metrics: innovation rate, governance complexity, cooperation depth

#### 6.6 Single-Agent Baseline
- Comparison: best team score vs single-agent score
- When is a team helpful? When does coordination overhead hurt?
- Superadditivity ratio per preset

#### 6.7 Secondary Validation: Internal Tasks
- Smoke test data (fizzbuzz, calculator) showing process-level patterns hold on binary tasks
- Brief: even on pass/fail tasks, communication volume and work distribution differ by preset

### 7. Discussion (~2 pages)

#### 7.1 Core Finding
Organisational structure is a significant variable. Not marginally — qualitatively different outputs, quantitatively different quality, fundamentally different processes. Five cities built from the same task, by the same model, with the same resources, look and score nothing alike.

#### 7.2 Configuration Recommendation
- Which dimensions does each preset excel at?
- Task decomposition insight: if city-building decomposes into infrastructure (roads), planning (zoning), and filling (buildings), different phases may benefit from different configurations
- Practical guidance: "when your task requires X, use configuration Y"

#### 7.3 Implications for Multi-Agent AI
- Every framework that hardcodes one structure is leaving performance on the table
- Task-aware team design: match the org to the problem
- Auto-org: let agents figure it out (our auto mode as proof of concept)

#### 7.4 Implications for Organisational Theory
- Computational org theory: AI teams as a new testbed for org theory hypotheses
- Speed: test structures in minutes, not months
- Scale: systematic sweep of org space impossible with human teams

#### 7.5 Implications Beyond Software
- If org structure affects collaborative design, it likely affects: research teams, creative teams, decision-making teams, crisis response
- The 4-property framework applies to any domain: design a task that satisfies all four properties and you can measure configuration effects

#### 7.6 The Bigger Picture
- Multi-agent AI is headed toward AI collectives, not just single AGI
- How those collectives are organised will matter as much as the individual model capability
- This paper opens a new research programme: **Computational Organisational Intelligence**
- The question isn't "which model is smartest?" but "which TEAM is most effective?"

#### 7.7 Limitations (stated honestly)
- Single LLM provider (Anthropic Claude)
- Single task (city grid) — though designed to maximise variance
- Limited runs per condition (3)
- Single agent count (4)
- No cross-model comparison
- Scoring dimensions are designed, not standardised
- Independent researcher, not lab — budget constraints are real and stated
- "We publish all infrastructure for community reproduction at scale"

### 8. Future Work (~0.5 pages)
- **SWE-bench extension:** Apply the same methodology to real-world software engineering tasks (ecological validity)
- **More task domains:** Research briefings, API design, creative writing — each with 4-property-satisfying task design
- **Cross-model comparison:** Claude vs GPT vs Gemini
- **Scale experiments:** 2, 4, 8, 16, 32 agents
- **The recursive configuration loop (Paper 7):** Connecting CMI tools to create self-improving configuration dynamics
- **Creator Mode:** AI that searches the organisational space autonomously (Paper 5)
- **Community benchmark:** Thousands of runs across the full preset space

### 9. Conclusion (~0.5 pages)
Organisational structure matters. We proved it visually and quantitatively on a purpose-built design task. The infrastructure is open-source. The 4-property framework enables anyone to build configuration-variance benchmarks in any domain. The field is open.

---

## 7. NOVEL CONTRIBUTIONS

1. **First controlled experiment** of organisational structure as an independent variable in multi-agent AI — with continuous quality scoring, not binary pass/fail
2. **The 4-property framework** for designing benchmark tasks that reveal configuration effects (multiple valid outputs, composition, continuous scoring, visible process)
3. **9-dimensional organisational framework** with enforcement mechanisms (not suggestions)
4. **Multi-dimensional continuous scoring** that makes quality differences measurable and visual
5. **Process data, not just outcomes** — we measure HOW teams work differently, not just whether they succeed
6. **Visual evidence** — five city grids side by side is more compelling than any statistical table
7. **Auto-org mode** — agents designing their own structure, with empirical results
8. **Pre-registered methodology** with Bitcoin-timestamped provenance
9. **Fully open-source** — engine, presets, benchmark infrastructure, scoring code, all data

## 8. HYPOTHESES (pre-registered)

Based on 60 years of organisational theory applied to AI teams:

| # | Hypothesis | Rationale | Measurable via |
|---|-----------|-----------|---------------|
| H1 | Collaborative produces the most coherent city (highest connectivity + accessibility) | Mesh communication + consensus → coordinated infrastructure | Connectivity + accessibility scores |
| H2 | Competitive produces the most fragmented city (highest coverage, lowest connectivity) | No coordination → territory claiming, duplicate infrastructure | Coverage vs connectivity gap |
| H3 | Hierarchical produces the most planned city (consistent style, lower diversity) | Single vision → coherent but conservative | Low variance across dimensions, lower diversity |
| H4 | Meritocratic produces the highest quality zoning (best adjacency logic) | Mandatory review catches zoning errors | Zoning logic score |
| H5 | Auto mode matches or beats best preset on aggregate score | Self-organisation adapts to task requirements | Harmonic mean vs best fixed preset |
| H6 | Gini coefficient highest in hierarchical, lowest in collaborative | Authority concentration → work concentration | Gini from contribution heatmap |
| H7 | Communication volume highest in collaborative, lowest in competitive | Mesh network generates most messages; independent agents don't communicate | Message count from chronicle |
| H8 | Merge conflicts highest in competitive, lowest in hierarchical | No coordination → conflicts; strict coordination → few conflicts | Conflict count from chronicle |
| H9 | Different presets excel on different scoring dimensions | No single preset dominates all dimensions | Per-dimension rankings |
| H10 | Team output quality exceeds single-agent baseline (superadditivity) | Coordination benefits outweigh overhead for complex tasks | Aggregate score comparison |

**If even 4-5 of these hold, the paper is strong. Surprises are even MORE interesting.**

## 9. WHAT WE ALREADY HAVE

| Component | Status | Location |
|-----------|--------|----------|
| Engine with 13 presets | DONE | `agentciv/` |
| 9 org dimensions with enforcement | DONE | `agentciv/org/` |
| Benchmark runner (matrix orchestration) | DONE | `agentciv/benchmark/runner.py` |
| Per-agent token tracking | DONE | `agentciv/llm/client.py` + `chronicle/observer.py` |
| Per-tick metric snapshots | DONE | `agentciv/chronicle/observer.py` |
| Full message content capture | DONE | `agentciv/core/engine.py` (fixed 5 April) |
| Agent reasoning capture | DONE | `agentciv/chronicle/observer.py` (fixed 5 April) |
| Relationship trust snapshots | DONE | `agentciv/chronicle/observer.py` (fixed 5 April) |
| Conflict resolution timing | DONE | `agentciv/chronicle/observer.py` |
| Network metrics (8 metrics) | DONE | `agentciv/benchmark/analysis.py` |
| Temporal analysis | DONE | `agentciv/benchmark/analysis.py` |
| Comparative analysis + stats | DONE | `agentciv/benchmark/analysis.py` |
| Kruskal-Wallis + Mann-Whitney U | DONE | `agentciv/benchmark/analysis.py` |
| CSV/JSON/LaTeX export | DONE | `agentciv/benchmark/analysis.py` |
| Auto-save per run (crash resilient) | DONE | `agentciv/benchmark/runner.py` |
| Pre-registered methodology | DONE | `benchmark_results/methodology.md` |
| Smoke test data (internal tasks) | DONE | `benchmark_results/smoke_test/runs/` |
| Pipeline validated with real agents | DONE | 4 successful runs (5 April) |

## 10. WHAT NEEDS BUILDING

| Component | Effort | Detail |
|-----------|--------|--------|
| City grid data model | ~1 hr | Grid class, building types enum, placement validation |
| Scoring engine | ~2 hrs | 5 dimension scorers (coverage, accessibility, zoning, diversity, connectivity) + harmonic mean |
| Grid renderer | ~1 hr | ASCII for terminal + colour PNG for paper |
| Agent contribution tracker | ~30 min | Track which agent placed which cell (already have per-agent file ops) |
| Temporal grid snapshots | ~30 min | Save grid state per tick (extend existing tick snapshots) |
| City grid task definition | ~30 min | BenchmarkTask entry with grid spec, building types, rules, verification |
| City grid verification script | ~1 hr | Parse output, run all 5 scorers, return scores |
| Radar chart generator | ~1 hr | 5-dimension radar chart per preset |
| Contribution heatmap renderer | ~30 min | Colour-code grid by agent |
| Paper figures automation | ~2 hrs | Generate all charts from result JSON |
| **Total new work** | **~10 hrs** | Plus run time (~$50-70) |

## 11. EXECUTION PLAN

### Phase A: Build City Grid Infrastructure (~5 hours)
1. Create `agentciv/benchmark/city_grid.py` — grid model, building types, placement rules
2. Create `agentciv/benchmark/city_scorer.py` — 5 scoring functions + harmonic mean
3. Create `agentciv/benchmark/city_renderer.py` — ASCII + PNG output
4. Create city grid BenchmarkTask in `tasks.py` — task prompt, expected output, verification
5. Validation: run single preset, verify grid produced, scoring works, data saves

### Phase B: Run Experiment (~2-3 hours wall clock, automated)
```bash
export ANTHROPIC_API_KEY="sk-ant-..."

# Team runs: 1 task × 5 presets × 3 runs = 15 runs
agentciv test-tasks \
  --tasks city-grid \
  --presets collaborative,competitive,meritocratic,auto,hierarchical \
  --runs 3 \
  --agents 4 \
  --max-ticks 15 \
  --output benchmark_results/city_grid

# Single-agent baseline: 1 task × 1 preset × 3 runs = 3 runs
agentciv test-tasks \
  --tasks city-grid \
  --presets collaborative \
  --runs 3 \
  --agents 1 \
  --max-ticks 15 \
  --output benchmark_results/city_grid
```

### Phase C: Analysis + Figures (~2 hours)
1. Run scoring engine on all 18 city outputs
2. Generate comparison tables (preset × dimension)
3. Run statistical tests (Kruskal-Wallis, Mann-Whitney, Cohen's d)
4. Render visual outputs: 5 grids, temporal animations, contribution heatmaps, radar charts
5. Export LaTeX tables
6. Review findings against hypotheses

### Phase D: Write Paper (~4-6 hours across sessions)
1. Fill in results sections with actual data
2. Write analysis/discussion based on findings
3. Insert figures
4. Polish abstract and intro
5. Bitcoin-timestamp final paper

## 12. THE HONEST FRAMING

This paper does NOT claim:
- That one task proves everything
- That our results generalise to all domains
- That we've found the "optimal" structure
- That 3 runs = definitive statistical proof

This paper DOES claim:
- That organisational structure is a measurable variable in multi-agent AI
- That we found visually and statistically significant differences across 5 configurations
- That output quality varies continuously, not just binary pass/fail
- That process data reveals qualitatively different team behaviours
- That the 4-property framework enables anyone to build configuration-variance benchmarks
- That the infrastructure exists for anyone to reproduce at scale
- That this opens a research programme worth pursuing

The honest limitation is the strength: "One researcher with a $70 budget produced the first controlled evidence — including visual proof you can see with your eyes. Imagine what a lab could do."

## 13. WHY THE IMPLICATIONS ARE HUGE

**For AI engineering:**
- Every multi-agent deployment should consider team structure as a tunable parameter
- "Which org structure for this task?" becomes a real engineering question
- Auto-org mode suggests AI can answer this question itself
- The 4-property framework helps practitioners design tasks that reveal which config works best

**For organisational theory:**
- AI teams as computational petri dishes for org theory
- Test 60 years of theory at unprecedented speed and scale
- New phenomena: org structures that only AI can implement (true anonymity, perfect information control, instant restructuring)

**For the future of work:**
- If AI collectives need org design, then collective intelligence engineering becomes a discipline
- The question shifts from "which AI model?" to "which AI TEAM?"
- Human-AI team design implications

**For AI safety:**
- If structure shapes behaviour, then understanding and controlling structure = controlling collective AI behaviour
- Governance of AI collectives is an org design problem
- Self-organising AI teams (auto mode) raise questions about emergent collective goals

**For science:**
- Reproducible sociology: run the same society 1000 times, change one variable
- Impossible in human teams, trivial in AI teams
- Opens computational social science at a new scale

---

## Document metadata

- **Created:** 5 April 2026
- **Updated:** 5 April 2026 — unified from "Same Bug, Different Team" + City Grid Benchmark
- **Phase:** 22 of Master Roadmap
- **Depends on:** City Grid infrastructure build, benchmark runs, analysis
- **Blocks:** Paper draft
- **Pre-registration:** `benchmark_results/methodology.md` (Bitcoin-timestamped)
- **Paper series:** Paper 6 in the AgentCiv series
- **Predecessor papers:** Papers 1-5 (theoretical/conceptual). This is the first empirical paper.
