# AgentCiv Benchmark Plan — Complete Reference

**Created:** 5 April 2026
**Author:** Ekram Alam & Claude
**Phase:** 22 of Master Roadmap
**Status:** Pre-execution planning complete

---

## 1. THESIS

**Organisational structure is a significant variable in multi-agent AI performance.**

Same task + different org structure = different performance. Not marginally different — qualitatively different patterns of work, communication, coordination, and outcomes.

Secondary thesis: **Configured collectives can outperform individual agents**, and different configurations excel at different task types.

This is NOT a leaderboard submission. This is a controlled experiment proving that the team variable matters — a contribution nobody else is systematically measuring.

---

## 2. BUDGET & EXECUTION MODE

### Primary mode: Max Plan (FREE)

All benchmarks run in Max Plan mode via Claude Code. The engine's MCP tools orchestrate agent teams without API keys. Cost: $0 beyond Claude Code subscription.

**Constraints of Max Plan mode:**
- Requires Claude Code to orchestrate each agent turn (not overnight batch)
- Subject to subscription usage limits (unknown ceiling — discover empirically)
- Each problem takes minutes, not seconds
- Can spread runs across multiple sessions over days/weeks

### Optional: API validation ($50-100 budget)

Targeted API mode runs confirming Max Plan results hold. Same problems, same presets. Only if Max Plan results are compelling and we want independent confirmation.

### Why this matters for publication

> "Total API cost: $0. All results obtained using Max Plan mode (Claude Code subscription). Reproducible by anyone with a Claude Code Max subscription."

This is a headline. No lab does benchmarks this way.

---

## 3. BENCHMARKS

### 3.1 Internal Task Suite (Step 1 — Pipeline Validation)

5 built-in tasks with automated verification:

| Task | Difficulty | What it tests |
|------|-----------|---------------|
| FizzBuzz | Simple | Basic code generation, following instructions |
| Key-Value Store | Simple | Data structure implementation |
| Todo CLI | Medium | Multi-file project, CLI interface, testing |
| Calculator Library | Medium | Library design, error handling, tests |
| Chat Room Server | Hard | Concurrency, networking, coordination |

**Purpose:** Validate the benchmark pipeline works end-to-end. Fix all bugs before external benchmarks. Also produces publishable data showing org structure affects outcomes.

### 3.2 HumanEval (Step 2a)

- 164 hand-written Python problems (OpenAI)
- Function completion tasks
- Standard metric: pass@1
- Quick per problem (single completion, not multi-turn)
- Full 164 is feasible in Max Plan mode

### 3.3 SWE-bench Lite (Step 2b)

- 300 real GitHub issues from popular Python repos
- Binary evaluation: fix resolves the issue or doesn't
- Multi-turn: agents must clone repo, understand issue, generate patch, pass tests
- Most expensive per problem — start with 10-20, expand as subscription allows

**Scale progression:**
- Minimum: 10 problems × 5 presets × 2 runs = 100 attempts
- Target: 50 problems × 5 presets × 3 runs = 750 attempts
- Stretch: Full 300 × 5+ presets × 3 runs = 4,500+ attempts

### 3.4 GPQA Diamond (Step 2c — Stretch)

- 198 graduate-level multiple choice questions
- 25% random baseline, 65% human expert baseline
- Tests collective reasoning on hard science
- Lower priority but interesting if org structure affects reasoning tasks differently than coding

### 3.5 MBPP (Optional)

- 500 crowd-sourced Python problems (standard test split)
- Simpler than HumanEval but larger dataset
- Include if time permits

---

## 4. CONFIGURATIONS TO TEST

### Presets (Independent Variable)

| Preset | Why include | Priority |
|--------|-----------|----------|
| `collaborative` | Default, baseline team structure | Must |
| `competitive` | Opposite of collaborative — agents race | Must |
| `meritocratic` | Earned influence, mandatory review | Must |
| `auto` | Agents design their own structure — crown jewel | Must |
| `hierarchical` | Top-down command — classic contrast to flat | Must |
| **Single agent** | Essential baseline — is a team even helpful? | Must |
| `research-lab` | Exploratory parallel approaches | Should |
| `pair-programming` | Tight 2-agent feedback loop | Should |
| `open-source` | Distributed, reputation-based | Nice |
| `military` | Strict chain of command | Nice |
| `swarm` | No explicit communication — stigmergic | Nice |
| `startup` | Fast, flat, minimal process | Nice |
| `hackathon` | Maximum speed, no review | Nice |
| `code-review` | Maximum quality, mandatory review | Nice |

**Minimum viable:** 5 presets (collaborative, competitive, meritocratic, auto, hierarchical) + single-agent baseline = 6 configurations.

**Full run:** All 13 presets + auto + single-agent = 15 configurations.

### Agent Count

Default: 4 agents per team (except pair-programming = 2, single agent = 1).

Optional ablation: run top-performing preset at 2, 4, 8 agents to show scale effects.

---

## 5. METRICS FRAMEWORK

### 5.1 Tier 1 — Core Metrics (Paper doesn't work without these)

| Metric | What it measures | Already captured? |
|--------|-----------------|-------------------|
| Task success rate | Binary pass/fail across tasks | YES — verification scripts |
| Partial completion score | Test pass rate (X/Y tests passing) | YES — test_pass_rate |
| Ticks used | Time to completion | YES — ticks_used |
| Wall clock time | Real-world duration | YES — wall_time_seconds |
| Total tokens consumed | Cost / compute used per run | NEED TO ADD — per-agent token tracking |
| Gini coefficient | Work distribution inequality (0=equal, 1=one agent did everything) | YES — emergent_specialisation |
| Communication volume | Total messages + broadcasts | YES — communication_volume |
| Merge conflicts | Coordination failures | YES — merge_conflicts |
| Variance across runs | Reliability of this org structure | YES — std in aggregated metrics |
| Single-agent baseline comparison | Is a team even helpful? (superadditivity) | NEED — run with agents=1 |

### 5.2 Tier 2 — Strong Paper (Makes reviewers approve)

| Metric | What it measures | Source |
|--------|-----------------|--------|
| Communication graph density | How connected is the team? | COMPUTE from communication_pairs |
| Betweenness centrality | Who's the hub/bottleneck? | COMPUTE from communication_pairs |
| Clustering coefficient | Do sub-groups form? | COMPUTE from communication_pairs |
| Parallel utilisation rate | Are agents working simultaneously? | COMPUTE from idle_ticks in attention map |
| Coordination overhead ratio | Tax of teamwork (comms / file ops) | COMPUTE from existing data |
| Role emergence detection | Did unprescribed roles appear? | COMPUTE from skills + action distribution |
| Conflict resolution time | How fast does this org resolve problems? | NEED TO ADD — track conflict→resolution ticks |
| Quality score | Weighted composite (completion, tests, efficiency, collaboration) | YES — quality_score |
| Restructure impact (auto mode) | Did self-organisation improve performance? | PARTIALLY — have restructure_log |

### 5.3 Tier 3 — Outstanding Paper (Makes it memorable)

| Metric | What it measures | Source |
|--------|-----------------|--------|
| Per-tick metric snapshots | How metrics evolve over time | NEED TO ADD — snapshot each tick |
| Phase transition detection | When did the team "find its rhythm"? | COMPUTE from tick snapshots |
| Metric correlation analysis | Does communication density predict success? | POST-PROCESSING on full dataset |
| Predictive validity | Can tick-10 metrics predict final outcome? | POST-PROCESSING |
| Emergent norm detection | Did the team develop unscripted conventions? | QUALITATIVE analysis of traces |
| Groupthink indicators | Fast consensus + poor quality? | COMPUTE from convergence speed vs outcome |
| Superadditivity ratio | Team performance / best individual performance | COMPUTE once baseline exists |

### 5.4 Network & Communication Deep Metrics

All computed from `communication_pairs` data (already captured):

| Metric | Formula / Method |
|--------|-----------------|
| Graph density | actual_edges / possible_edges |
| In-degree centrality | messages received per agent / total messages |
| Out-degree centrality | messages sent per agent / total messages |
| Betweenness centrality | standard graph algorithm on comm graph |
| Reciprocity | bidirectional_pairs / total_pairs |
| Hub-spoke ratio | max(centrality) / mean(centrality) — high = hub-spoke, low = mesh |
| Communication efficiency | task_success / communication_volume |
| Directive vs collaborative ratio | directive_messages / collaborative_messages — high = command-driven, low = peer-driven. Classifies messages by intent (assign/order vs discuss/suggest). |

### 5.5 What Needs Adding to the Engine

**Small code changes (~1-2 hours):**

1. **Per-agent token tracking** — in the agent action loop, count input/output tokens per agent per tick. Store in chronicle.
2. **Per-tick metric snapshots** — at end of each tick, snapshot: agent contributions so far, comms count, files count, conflicts count. Enables temporal analysis.
3. **Conflict resolution tracking** — when a merge conflict is detected, record the tick. When it's resolved, record that tick too. Delta = resolution time.
4. **Per-agent completion contribution** — tag which agent's code actually passes tests. Who solved it? Measures whether the team genuinely collaborated or one agent carried. Essential for superadditivity analysis.
5. **Single-agent mode** — ensure the engine works cleanly with `--agents 1`. Verify no multi-agent assumptions break.

**Post-processing analysis layer (~2-3 hours):**

5. **Network metrics calculator** — takes communication_pairs, computes density, centrality, clustering, reciprocity.
6. **Temporal analysis** — takes per-tick snapshots, computes phase transitions, convergence speed, evolution curves.
7. **Comparative analysis** — takes results across presets, computes superadditivity, rankings, statistical significance.
8. **Export to publication formats** — CSV tables, JSON for charts, LaTeX-ready comparison tables.

---

## 6. DATA CAPTURE & STORAGE

### 6.1 Directory Structure

```
agentciv-engine/
  benchmark_results/
    methodology.md                    ← pre-registered plan (this document, trimmed)

    internal/                         ← Step 1: pipeline validation
      config.json                     ← exact config used
      runs/
        fizzbuzz_collaborative_run1.json
        fizzbuzz_collaborative_run2.json
        fizzbuzz_competitive_run1.json
        ...
      summary.json                    ← aggregated comparison
      analysis.json                   ← derived metrics (network, temporal, etc.)

    humaneval/                        ← Step 2a
      config.json
      runs/
        HumanEval_000_collaborative.json
        HumanEval_000_competitive.json
        ...
      summary.json
      analysis.json

    swebench/                         ← Step 2b
      config.json
      runs/
        sympy__sympy-20590_collaborative_run1.json
        ...
      summary.json
      analysis.json

      swebench_submission/            ← if submitting to leaderboard
        all_preds.jsonl
        metadata.yaml
        trajs/
        logs/

    gpqa/                             ← Step 2c (stretch)
      ...

    comparative/                      ← Cross-benchmark analysis
      cross_benchmark_analysis.json
      publication_tables.csv
      figures/                        ← generated charts
```

### 6.2 Per-Run Data (JSON)

Every single run saves:

```json
{
  "meta": {
    "benchmark": "internal|humaneval|swebench|gpqa",
    "task_id": "fizzbuzz|HumanEval/0|sympy__sympy-20590",
    "preset": "collaborative",
    "agent_count": 4,
    "max_ticks": 50,
    "run_index": 1,
    "mode": "max_plan|api",
    "model": "claude-sonnet-4-6-20260301",
    "engine_version": "0.1.0",
    "git_commit": "abc1234",
    "timestamp_start": "2026-04-05T10:00:00Z",
    "timestamp_end": "2026-04-05T10:05:00Z"
  },

  "outcome": {
    "success": true,
    "completion_rate": 0.85,
    "test_pass_rate": 0.8,
    "tests_passed": 8,
    "tests_total": 10,
    "quality_score": 0.72,
    "ticks_used": 15,
    "wall_time_seconds": 180
  },

  "efficiency": {
    "total_tokens_input": 150000,
    "total_tokens_output": 30000,
    "tokens_per_agent": {"agent_0": 45000, "agent_1": 42000, ...},
    "api_calls": 60,
    "estimated_cost_usd": 0.00
  },

  "communication": {
    "total_messages": 24,
    "total_broadcasts": 6,
    "pairs": {"Atlas → Nova": 5, "Nova → Atlas": 3, ...},
    "graph_density": 0.67,
    "betweenness_centrality": {"Atlas": 0.4, "Nova": 0.2, ...},
    "hub_spoke_ratio": 2.0,
    "reciprocity": 0.75
  },

  "coordination": {
    "merge_conflicts": 2,
    "merges_succeeded": 12,
    "conflict_resolution_ticks": [2, 1],
    "gini_coefficient": 0.35,
    "parallel_utilisation": 0.7
  },

  "organisation": {
    "preset": "collaborative",
    "initial_state": {"authority": "flat", "communication": "mesh", ...},
    "final_state": {"authority": "flat", "communication": "mesh", ...},
    "restructures_proposed": 0,
    "restructures_adopted": 0,
    "restructure_log": []
  },

  "agents": {
    "agent_0": {
      "name": "Atlas",
      "files_created": ["main.py"],
      "files_modified": ["utils.py", "test_main.py"],
      "messages_sent": 8,
      "broadcasts_sent": 2,
      "tasks_claimed": ["implement core logic"],
      "skills": {"coding": {"tier": "skilled", "actions": 25}},
      "tokens_used": 45000,
      "idle_ticks": 2
    },
    ...
  },

  "temporal": {
    "tick_snapshots": [
      {"tick": 1, "files": 0, "messages": 2, "conflicts": 0, "completion": 0.0},
      {"tick": 2, "files": 1, "messages": 5, "conflicts": 0, "completion": 0.1},
      ...
    ]
  },

  "chronicle": {
    "timeline": [...],
    "notable_moments": [...]
  },

  "swebench_specific": {
    "instance_id": "sympy__sympy-20590",
    "model_patch": "diff --git a/...",
    "reasoning_trace": "..."
  }
}
```

### 6.3 Summary Data (Per Benchmark)

Aggregated across all runs for each (task, preset) combination:

```json
{
  "task_id": "fizzbuzz",
  "preset": "collaborative",
  "runs": 3,
  "success_rate": {"mean": 0.67, "std": 0.47, "values": [1, 0, 1]},
  "completion_rate": {"mean": 0.85, "std": 0.1, "values": [0.9, 0.75, 0.9]},
  "ticks_used": {"mean": 12.3, "std": 2.1, "values": [10, 14, 13]},
  "communication_volume": {"mean": 30, "std": 5, "values": [25, 35, 30]},
  "gini_coefficient": {"mean": 0.35, "std": 0.05, "values": [0.3, 0.4, 0.35]},
  ...
}
```

### 6.4 Git + Bitcoin Provenance

- All results committed to `benchmark_results/` in the engine repo
- Post-commit hook auto-stamps on Bitcoin blockchain
- Methodology doc committed BEFORE any runs (pre-registration)
- Provides tamper-proof evidence that methodology was defined before results were known

---

## 7. EXECUTION PLAN

### Step 0: Engine Preparation (~2-3 hours)

| Sub-step | What | Detail |
|----------|------|--------|
| 0a | Add per-agent token tracking | Track input/output tokens per agent per tick in chronicle observer |
| 0b | Add per-tick metric snapshots | Snapshot key metrics at end of each tick |
| 0c | Add conflict resolution timing | Track tick of conflict detection → resolution |
| 0d | Verify single-agent mode | Run with `--agents 1`, fix any multi-agent assumptions |
| 0e | Build Max Plan benchmark orchestration | Wire benchmark runner to work via MCP tools in Claude Code |
| 0f | Build analysis layer | Network metrics, temporal analysis, comparative analysis, export |
| 0g | Set up results directory | Create directory structure, commit methodology doc |
| 0h | Pre-registration commit | Commit this methodology BEFORE any runs. Bitcoin timestamp it. |

### Step 1: Internal Task Suite — Pipeline Validation (FREE)

**Goal:** Prove the pipeline works. Fix all bugs. Produce first dataset.

| Sub-step | What | Runs | Detail |
|----------|------|------|--------|
| 1a | Single-agent baseline | 5 tasks × 1 preset × 2 runs = 10 | Establish what one agent can do alone |
| 1b | Core presets | 5 tasks × 5 presets × 2 runs = 50 | collaborative, competitive, meritocratic, auto, hierarchical |
| 1c | Verify data capture | — | Check every field in the JSON output is populated correctly |
| 1d | Fix bugs | — | Fix everything that breaks before proceeding |
| 1e | Analysis dry run | — | Run the full analysis pipeline on Step 1 data |
| 1f | Preliminary results | — | First look: does org structure affect outcomes on internal tasks? |

**Total runs:** ~60
**Expected time:** 2-3 sessions
**Cost:** $0

### Step 2a: HumanEval (FREE)

**Goal:** Validate thesis on established benchmark. Quick per problem.

| Sub-step | What | Runs | Detail |
|----------|------|------|--------|
| 2a-i | Pilot: 10 problems × 3 presets | 30 | Validate HumanEval integration works |
| 2a-ii | Expand: 50 problems × 5 presets + baseline | 300 | Enough for statistical significance |
| 2a-iii | Full: all 164 × 5 presets + baseline | 984 | If subscription allows — stretch goal |

**Expected time:** HumanEval problems are quick (single-completion). 50 problems feasible in 1-2 sessions.
**Cost:** $0

### Step 2b: SWE-bench Lite (FREE)

**Goal:** Validate thesis on real-world engineering tasks. Most expensive per problem.

| Sub-step | What | Runs | Detail |
|----------|------|------|--------|
| 2b-i | Pilot: 3 problems × 3 presets | 9 | Validate SWE-bench integration works end-to-end |
| 2b-ii | Small scale: 10 problems × 5 presets + baseline × 2 runs | 120 | Minimum publishable SWE-bench data |
| 2b-iii | Medium scale: 50 problems × 5 presets + baseline × 2 runs | 600 | Strong paper |
| 2b-iv | Full: 300 problems × 5+ presets × 3 runs | 4500+ | Stretch — spread over weeks if subscription allows |
| 2b-v | Everything: all benchmarks × all 13 presets + auto + baseline × 3 runs | 15,000+ | Ultimate stretch — only if subscription capacity permits. Months of Max Plan runtime. |

**Expected time:** SWE-bench problems take longer (multi-turn, repo setup). Start with pilot, expand.
**Cost:** $0

### Step 2c: GPQA Diamond (Stretch, FREE)

**Goal:** Test if org structure affects collective reasoning (not just coding).

| Sub-step | What | Runs | Detail |
|----------|------|------|--------|
| 2c-i | Pilot: 10 problems × 3 presets | 30 | Does org structure matter for reasoning tasks? |
| 2c-ii | Full: 198 problems × 5 presets | 990 | If coding results are strong and we have capacity |

### Step 3: API Mode Validation (OPTIONAL — $50-100)

**Goal:** Confirm Max Plan results hold in automated API mode.

| Sub-step | What | Runs | Detail |
|----------|------|------|--------|
| 3a | Cherry-pick most interesting results | ~50-100 | Same problems, same presets as Step 2 highlights |
| 3b | Compare Max Plan vs API mode | — | Are results comparable? (interesting finding either way) |

**Cost:** $50-100 maximum. Only proceed if Steps 1-2 produce compelling results.

### Step 4: Analysis & Write-up

| Sub-step | What | Detail |
|----------|------|--------|
| 4a | Statistical analysis | Mean, std, confidence intervals, effect sizes across presets |
| 4b | Network analysis | Communication graph metrics per preset — do structures actually produce different patterns? |
| 4c | Temporal analysis | How do metrics evolve over ticks? When do teams "find their rhythm"? |
| 4d | Correlation analysis | Which process metrics predict which outcomes? |
| 4e | Qualitative highlights | Cherry-pick most interesting agent behaviours, restructuring moments, emergence |
| 4f | Comparative tables | Publication-ready comparison tables across all benchmarks |
| 4g | Figures | Charts: preset comparison bars, temporal evolution lines, communication network graphs |
| 4h | Write-up | Full results section ready for paper inclusion |

---

## 8. PUBLICATION PLAN

### What We Publish

1. **All raw data** — every run JSON, every summary, every analysis artifact
2. **All code** — benchmark runner, analysis scripts, metrics computation
3. **Methodology** — this document (pre-registered, Bitcoin-timestamped)
4. **Results write-up** — suitable for paper inclusion or standalone report

### Where Results Go

- `benchmark_results/` in agentciv-engine repo (public)
- Referenced from Paper 4 or standalone benchmark report
- Website (ERA 4 refresh) showcases key findings
- README updated with headline results

### Framing

> "We conducted a controlled experiment measuring the effect of organisational structure on multi-agent AI team performance. Using AgentCiv Engine's 13 organisational presets, we ran [N] tasks across [M] configurations, each repeated [K] times.
>
> Results show statistically significant performance variation based on organisational structure alone. [Specific headline findings].
>
> All benchmarks were run using Max Plan mode (Claude Code, $0 API cost). Full methodology, raw data, and reproduction code are published. Community members can extend the benchmark using `agentciv test-tasks` or contribute runs to the collective dataset.
>
> Full-scale SWE-bench Lite (300 problems × 15 configurations × 3 runs) remains a stretch goal — we publish all code and methodology for community reproduction."

### Headline Findings We Hope to Show

1. **"Same task, different org = different performance"** — the core thesis
2. **"Collaborative teams outperform on X, competitive on Y"** — task-type specialisation
3. **"Auto mode matches or beats best preset"** — self-organisation works
4. **"Configured collective outperforms single agent by Z%"** — teams are valuable
5. **"Communication patterns predict task success"** — process metric as leading indicator

### Honest Limitations (State Upfront)

- Single LLM provider (Anthropic Claude)
- Max Plan mode means Claude Code orchestrates — potential ceiling effects
- Limited SWE-bench sample size (unless stretch goal achieved)
- No cross-model comparison (Sonnet vs Opus vs GPT vs Gemini)
- Independent researcher, not lab — budget constraints are real and stated

---

## 9. STATISTICAL APPROACH

### Pre-Registered

- **Independent variable:** Organisational preset (categorical, 6-15 levels)
- **Dependent variables:** All Tier 1 metrics (Section 5.1)
- **Control variables:** Agent count (4), model (constant), max ticks (per-task default)
- **Runs per condition:** Minimum 2, target 3 (for variance estimation)
- **Significance testing:**
  - Kruskal-Wallis H-test across presets (non-parametric, suitable for small samples)
  - Pairwise Mann-Whitney U tests for specific comparisons
  - Report effect sizes (Cohen's d or rank-biserial correlation), not just p-values
- **Multiple comparisons:** Bonferroni correction when testing all pairs
- **Minimum sample for significance:** With 5 presets × 3 runs = 15 data points per task, we can detect large effects. With 50+ tasks × 3 runs, aggregate statistics are more powerful.

### What Counts as a Meaningful Finding

- Performance difference > 10% between presets on the same task
- Consistent direction across multiple tasks (preset A beats B on most tasks)
- Communication pattern that correlates with outcome (r > 0.5)
- Variance difference (some presets are reliable, others are volatile)

---

## 10. TIMELINE

| Phase | What | When | Sessions |
|-------|------|------|----------|
| Step 0 | Engine prep + infrastructure | Now | 1-2 sessions |
| Step 1 | Internal tasks (validation) | After Step 0 | 2-3 sessions |
| Step 2a | HumanEval | After Step 1 | 1-2 sessions |
| Step 2b | SWE-bench (pilot → expand) | After Step 2a | 3-5+ sessions |
| Step 2c | GPQA (stretch) | If capacity | 1-2 sessions |
| Step 3 | API validation (optional) | If results compelling | 1 session |
| Step 4 | Analysis + write-up | After Steps 2 | 1-2 sessions |

**Minimum viable publication:** Steps 0 + 1 + 2a + partial 2b + 4 = ~8-12 sessions

---

## 11. EXISTING INFRASTRUCTURE

### Already Built (Ready to Use)

| Component | File | What it does |
|-----------|------|-------------|
| Benchmark runner | `agentciv/benchmark/runner.py` | Task matrix orchestration, dry-run mode, mock mode |
| 5 internal tasks | `agentciv/benchmark/tasks.py` | FizzBuzz, KV Store, Todo CLI, Calculator, Chat Server — all with verification |
| Metrics extraction | `agentciv/benchmark/metrics.py` | RunMetrics, AggregatedMetrics, StatSummary |
| Report generation | `agentciv/benchmark/report.py` | Terminal tables, JSON export, rankings |
| Experiment mode | `agentciv/experiment.py` | Same task × multiple orgs |
| Chronicle observer | `agentciv/chronicle/observer.py` | Per-run data capture |
| Learning history | `agentciv/learning/history.py` | Persistent run storage |
| Quality scoring | `agentciv/learning/recorder.py` | Weighted quality score |
| 13 presets | `presets/*.yaml` | All organisational configurations |
| MCP orchestration | `agentciv/mcp/server.py` | Max Plan mode tools |
| CLI | `agentciv/cli.py` | `agentciv test-tasks` with all flags |

### Needs Building

| Component | Effort | What it does |
|-----------|--------|-------------|
| Max Plan benchmark orchestration | ~2 hours | Wire benchmark runner to work via MCP (or direct orchestration from Claude Code) |
| Per-agent token tracking | ~30 min | Count tokens per agent per tick |
| Per-tick metric snapshots | ~30 min | Snapshot metrics each tick for temporal analysis |
| Conflict resolution timing | ~20 min | Track conflict → resolution tick delta |
| Single-agent verification | ~20 min | Verify engine works with agents=1 |
| Network metrics calculator | ~1 hour | Compute graph density, centrality, clustering from comm pairs |
| Temporal analysis module | ~1 hour | Phase transitions, convergence speed from tick snapshots |
| Comparative analysis | ~1 hour | Cross-preset comparisons, superadditivity, statistical tests |
| HumanEval integration | ~2 hours | Dataset loading, evaluation harness, result format |
| SWE-bench integration | ~3-4 hours | Repo cloning, environment setup, patch evaluation, Docker |
| GPQA integration | ~1 hour | Dataset loading, answer verification |
| Publication export | ~1 hour | CSV, LaTeX tables, chart data |

---

## 12. KEY DESIGN DECISIONS

1. **Max Plan mode first, API mode second.** We built Max Plan for exactly this. Use it.

2. **Intelligence matters.** We use Sonnet/Opus via Claude Code, not Haiku. Org structure effects likely amplify with model capability. Weak models may fail regardless of structure.

3. **Pre-register methodology.** Commit this document BEFORE running. Bitcoin timestamp it. This is how real science works — prevents cherry-picking.

4. **Comprehensive metrics, not just pass/fail.** The thesis is proven by process data (how teams work differently), not just outcome data (which team scored higher).

5. **Start small, expand.** Pipeline validation → pilot → expand. Never burn time on broken infrastructure.

6. **Everything is reproducible.** All code, configs, data, and methodology are published. Anyone can reproduce or extend.

7. **Honest limitations.** State budget constraints, sample sizes, and scope clearly. An honest small study beats a dishonest large one.

8. **Token parity not required.** Collectives use more tokens than single agents — that's the POINT. They use compute laterally (communication, diverse approaches, peer review). The metric is outcome per configuration, not outcome per token.

---

## 13. REFERENCE: WHAT LABS DO

### SWE-bench Submission Requirements (if we reach full scale)

- `all_preds.jsonl` — one prediction per instance, pass@1
- `metadata.yaml` — model info, org, attempt count
- `trajs/` — reasoning traces per instance (mandatory)
- `logs/` — per-instance patch.diff, report.json, test_output.txt
- Technical report / README describing the system
- Must NOT use PASS_TO_PASS or FAIL_TO_PASS test knowledge
- Must NOT use hints field

### HumanEval Standard

- pass@1 metric (1 sample per problem)
- JSONL format: `{"task_id": "HumanEval/0", "completion": "..."}`
- Official harness: `github.com/openai/human-eval`

### Publication Best Practices (BetterBench, NeurIPS 2024)

- Multiple runs with uncertainty estimates
- Report effect sizes, not just p-values
- Contamination analysis (state what steps taken)
- Ablation studies (what happens when you change one thing?)
- Cost transparency (total cost of experiments)
- Honest failure analysis
