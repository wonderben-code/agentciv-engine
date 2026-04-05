# Pre-Registered Benchmark Methodology

**Committed:** 5 April 2026
**Author:** Mark E. Mala
**Engine:** AgentCiv Engine v0.1.0
**Status:** LOCKED — this document was committed and Bitcoin-timestamped BEFORE any benchmark runs

---

## Thesis

Organisational structure is a significant variable in multi-agent AI performance.
Same task + different org structure = different performance.

Secondary: Configured collectives can outperform individual agents, and different
configurations excel at different task types.

## Design

Controlled experiment. NOT a leaderboard submission. The independent variable is
organisational preset; the dependent variables are task success, efficiency, and
communication patterns.

## Benchmarks

1. **Internal tasks** — 5 built-in tasks (fizzbuzz, kv_store, todo_api, calculator, data_pipeline) with automated verification scripts
2. **HumanEval** — 164 Python function-generation problems, pass@1
3. **SWE-bench Lite** — up to 300 real GitHub issues, binary pass/fail
4. **GPQA Diamond** — 198 graduate-level science questions (stretch)

## Configurations

Priority presets (tested first):
1. collaborative — flat, mesh, shared reward
2. competitive — independent racing
3. meritocratic — earned influence, peer review
4. auto — agents design their own org
5. hierarchical — top-down, lead assigns

Baseline: single agent (agents=1)

Default: 4 agents, 50 max ticks per task.

## Execution Mode

Primary: Max Plan mode (Claude Code MCP tools, $0 API cost).
Optional: API mode validation ($50-100 budget).

## Metrics

### Tier 1 (core)
- Success rate (completion_rate)
- Token consumption (total, per-agent)
- Ticks used
- Gini coefficient (work distribution)
- Communication volume (messages + broadcasts)
- Merge conflicts
- Run-to-run variance (std across replications)
- Baseline comparison (vs single agent)

### Tier 2 (process)
- Network density, centrality, clustering
- Parallel utilisation rate
- Coordination overhead ratio
- Role emergence detection
- Conflict resolution time
- Hub-spoke ratio
- Communication efficiency
- Directive vs collaborative ratio

### Tier 3 (temporal)
- Per-tick metric snapshots
- Phase transition detection
- Convergence speed
- Predictive validity (tick-10 → final outcome)
- Superadditivity ratio (team / best individual)

## Statistical Approach

- **Primary test:** Kruskal-Wallis H-test across presets (non-parametric)
- **Pairwise:** Mann-Whitney U for significant pairs
- **Effect sizes:** Cohen's d between preset pairs
- **Minimum runs:** 2 per (task, preset) combo for internal; scaling for established
- **Pre-registered:** This methodology committed before seeing any results

## Data Capture

Every run saves a JSON file with: meta (benchmark, preset, model, git commit, timestamps), outcome (success, tests, ticks), efficiency (tokens per agent), communication (pairs, volumes), analysis (network metrics, temporal metrics), verification results, and full chronicle report.

All data published in `benchmark_results/` for full reproducibility.

## Scaling Strategy

Start at pilot scale, expand as results warrant. Each tier is independently publishable:
- Pilot: 3-10 problems × 3 presets (validate integration)
- Small: 10 problems × 6 configs × 2 runs (minimum publishable)
- Medium: 50 problems × 6 configs × 2 runs (strong paper)
- Full: 300 problems × 5+ presets × 3 runs (comprehensive)

Stop at any tier and publish — no obligation to complete full scale.

## Honest Limitations (pre-declared)

- Max Plan mode may behave differently from API mode
- Subscription limits may cap total runs
- 4 agents is a small team; results may not scale to 20+
- Internal tasks are simpler than real-world software
- Single model family (Claude); may not generalise to other LLMs
