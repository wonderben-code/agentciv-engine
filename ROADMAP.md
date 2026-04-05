# AgentCiv Engine — Master Roadmap

**Last updated:** 4 April 2026
**Author:** Ekram Alam & Claude

---

## Status Overview

**22 phases completed. 17 remaining across four eras.**

The engine is built, tested, polished, and open-sourced. All 5 papers written and Bitcoin-stamped. Website deployed at agentciv.ai with all four wings. Three public repos. What remains: benchmarks, PyPI, platform features, Creator Mode, then a final website refresh and launch.

```
ERA 1: LAUNCH (Phases 19–23)
  Battle-test → Paper 5 → Website → Benchmarks → Go Public (PyPI)

ERA 2: THE SIMULATION EXPERIENCE (Phases 26–31)
  Package & Install → YAML Customisation → Rich Terminal → Live Chronicler → Gardener → Community

ERA 3: CREATOR MODE (Phases 32–36)
  Build It → Task Search → Emergence Explorer → Full Website Wing → Empirical Paper

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
| 23a | Repos Public | All 3 repos public (agentciv/agentciv, wonderben-code/agentciv-engine, wonderben-code/agentciv-creator). Internal docs removed pre-publish. | DONE |

**Current state:** ~11,500 lines across 40 Python files + website code. 13 presets. All features working and tested. Three public repos + one private (website). Website deployed at agentciv.ai. All external links verified working. All repos Bitcoin-stamped.

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

### Phase 22: Established Benchmarks — The Capstone

**Goal:** Publishable evidence that organisational structure is a significant variable in multi-agent AI performance. Same task + different org = different performance. Controlled experiment, not leaderboard submission.

**Thesis:** Configured collectives outperform individual AI on complex tasks, and different organisational structures outperform others for specific task types. This is the first controlled study of organisational arrangement as a design parameter.

**Full reference:** `docs/BENCHMARK_PLAN.md` — 13 sections, every detail, metric formulas, data schemas, statistical approach, publication plan.

**Cost:** $0 primary (Max Plan mode). Optional $50-100 API validation.

**Pre-registration:** Methodology committed and Bitcoin-timestamped BEFORE any runs. This is non-negotiable.

#### Step 0: Engine Preparation (~1-2 sessions)

Infrastructure changes required before any benchmark can run.

| Sub-step | What | Detail | Est. |
|----------|------|--------|------|
| 22-0a | Per-agent token tracking | In agent action loop, count input/output tokens per agent per tick. Store in chronicle. | 30 min |
| 22-0b | Per-tick metric snapshots | End of each tick: snapshot agent contributions, comms count, files count, conflicts count. Enables temporal analysis (Tier 3 metrics). | 1 hr |
| 22-0c | Conflict resolution timing | When merge conflict detected → record tick. When resolved → record tick. Delta = resolution time. | 30 min |
| 22-0d | Per-agent completion contribution | Tag which agent's code actually passes tests. Who solved it? Essential for superadditivity analysis. | 1 hr |
| 22-0e | Verify single-agent mode | Ensure engine works cleanly with `--agents 1`. No multi-agent assumptions break. This IS the baseline. | 30 min |
| 22-0f | Max Plan benchmark orchestration | Wire MCP tools (`agentciv_orchestrate_start/act/tick/status`) to run benchmarks end-to-end in Max Plan mode. Auto-save results. | 2 hr |
| 22-0g | Analysis layer | Network metrics calculator (density, centrality, clustering, reciprocity, hub-spoke ratio, directive vs collaborative ratio). Temporal analysis (phase transitions, convergence). Comparative analysis (cross-preset rankings, statistical significance). Export to CSV/JSON/LaTeX. | 3 hr |
| 22-0h | Results directory structure | Create `benchmark_results/` with subdirectories: `internal/`, `humaneval/`, `swebench/`, `gpqa/`, `comparative/`. Per-run JSON schema. Summary aggregation. See `docs/BENCHMARK_PLAN.md` Section 6. | 30 min |
| 22-0i | Pre-registration commit | Commit methodology (trimmed BENCHMARK_PLAN.md) to `benchmark_results/methodology.md`. Bitcoin timestamp. This locks our approach BEFORE seeing results. | 15 min |
| 22-0j | Regression test | Run existing test suite + manual smoke test of `agentciv solve` and `agentciv experiment` to confirm all benchmark instrumentation is additive-only and the dev tool UX is unchanged. No benchmark code should affect normal user experience. | 30 min |

#### Step 0.5: MCP Display Parity — Max Plan UX (~1 session)

**BLOCKER for all benchmark runs.** The CLI (`agentciv solve`) has 43 Rich display functions with coloured agent names, panels, tables, status indicators, chronicle reports. MCP mode returns raw JSON — no visual UX at all. Claude Code renders markdown, so we format MCP responses as beautiful unicode/markdown text with data attached.

| Sub-step | What | Detail | Est. |
|----------|------|--------|------|
| 22-0.5a | Create `mcp/display.py` | Display formatting module for MCP responses. Converts every tool's JSON data into beautifully formatted text using unicode box-drawing, markdown tables, status indicators (✓/✗), agent names. Parallel to `display.py` (Rich) but outputs plain text/markdown for Claude Code. | 2 hr |
| 22-0.5b | Wire into all MCP tools | Every tool in `server.py` calls the formatter. Returns formatted display text as the primary response, with JSON data embedded at the end for programmatic use. 12 tools total. | 1 hr |
| 22-0.5c | Verify MCP connection | Fix `.mcp.json` → ensure `agentciv mcp` starts cleanly, tools appear in Claude Code, no import errors. Test from a fresh terminal. | 30 min |
| 22-0.5d | Side-by-side comparison | Run the same operation via CLI and MCP. Screenshot both. Verify the MCP version conveys the same information with equal clarity. | 30 min |
| 22-0.5e | Benchmark tool display | Ensure `agentciv_benchmark_start` and `agentciv_benchmark_verify` have excellent formatted output — these are what the user will see most during benchmark runs. | 30 min |

**Design principle:** Same data, same clarity, different medium. CLI uses Rich panels; MCP uses unicode + markdown tables. Both are beautiful. Neither is a data dump.

#### Step 1: Internal Benchmark Suite — Pipeline Validation (FREE, ~1 session)

5 built-in tasks × (5 priority presets + single-agent baseline) × 2 runs = **60 runs**.

| Sub-step | What | Detail |
|----------|------|--------|
| 22-1a | Run internal tasks | fizzbuzz, todo_api, calculator, data_pipeline, web_scraper. All via Max Plan mode. |
| 22-1b | Presets tested | `collaborative`, `competitive`, `meritocratic`, `auto`, `hierarchical` + single-agent baseline. |
| 22-1c | Validate pipeline | Confirm: data saves correctly, metrics compute, analysis layer works, results directory populates. |
| 22-1d | First results | Generate first comparison tables. Do we already see org structure effects? This is the sanity check. |
| 22-1e | Fix any issues | If pipeline breaks, fix before moving to established benchmarks. Cheaper to find bugs here. |

**Success criteria:** Pipeline runs end-to-end, all metrics compute, results are reproducible across 2 runs of the same config.

#### Step 2a: HumanEval — Established Coding Benchmark (FREE, ~1-2 sessions)

164 Python function-generation problems. Pass@1 evaluation. Industry-standard, widely cited.

| Sub-step | What | Runs | Detail |
|----------|------|------|--------|
| 22-2a-i | Pilot | 30 | 10 problems × 3 presets. Validate HumanEval integration. |
| 22-2a-ii | Core run | 1,968 | 164 problems × (5 presets + baseline) × 2 runs. Full dataset. |
| 22-2a-iii | Extended (optional) | 4,920+ | Add remaining presets (13 total + auto + baseline). Only if time allows. |

**Expected output:** Pass@1 rate per preset. Token efficiency per preset. Communication pattern differences. First publishable result.

#### Step 2b: SWE-bench Lite — Real-World Software Engineering (FREE, ~2-4 sessions)

300 real GitHub issues from popular repos. Binary pass/fail (tests pass or don't). The gold standard.

| Sub-step | What | Runs | Detail |
|----------|------|------|--------|
| 22-2b-i | Pilot | 9 | 3 problems × 3 presets. Validate SWE-bench integration (repo cloning, env setup, test harness). |
| 22-2b-ii | Small scale | 120 | 10 problems × (5 presets + baseline) × 2 runs. Minimum publishable SWE-bench data. |
| 22-2b-iii | Medium scale | 600 | 50 problems × (5 presets + baseline) × 2 runs. Strong paper. |
| 22-2b-iv | Full scale | 4,500+ | 300 problems × 5+ presets × 3 runs. Spread over weeks if subscription allows. |
| 22-2b-v | Everything | 15,000+ | All benchmarks × all 13 presets + auto + baseline × 3 runs. Ultimate stretch — months of Max Plan runtime. |

**Scaling strategy:** Start at pilot, expand as results warrant. Stop at any tier and publish — each tier is independently publishable.

#### Step 2c: GPQA Diamond — Collective Reasoning (Stretch, FREE)

198 graduate-level science questions. Tests whether org structure affects reasoning, not just coding.

| Sub-step | What | Runs | Detail |
|----------|------|------|--------|
| 22-2c-i | Pilot | 30 | 10 problems × 3 presets. Does org structure matter for reasoning tasks? |
| 22-2c-ii | Full | 990 | 198 problems × 5 presets. If coding results are strong and we have capacity. |

#### Step 3: API Validation (Optional, $50-100 max)

| Sub-step | What | Detail |
|----------|------|--------|
| 22-3a | Select subset | Pick 10-20 tasks where Max Plan showed clearest org effects. |
| 22-3b | API runs | Re-run subset with `ANTHROPIC_API_KEY` mode. Same presets, same tasks. |
| 22-3c | Compare | Do API results match Max Plan results? If yes → validates free methodology. If no → document differences. |

**Purpose:** Proves Max Plan mode produces equivalent results to API mode. Makes "$0 cost" claim airtight.

#### Step 4: Analysis & Publication (~1 session)

| Sub-step | What | Detail |
|----------|------|--------|
| 22-4a | Cross-benchmark analysis | Which presets win on which benchmarks? Does the winner change by task type? |
| 22-4b | Statistical significance | Kruskal-Wallis H-test across presets. Mann-Whitney U for pairwise. Cohen's d effect sizes. All pre-registered. |
| 22-4c | Publication tables | Preset × Benchmark matrix. Token efficiency comparison. Communication pattern analysis. LaTeX-ready. |
| 22-4d | Figures | Performance by preset (box plots), communication networks (graph viz), temporal evolution (line charts), Gini coefficients (bar charts). |
| 22-4e | Write-up | Update Paper 3 ("From Emergence to Evidence") with benchmark results. Or standalone paper if results warrant it. |
| 22-4f | Data release | All raw data, configs, analysis code published in `benchmark_results/`. Full reproducibility. |
| 22-4g | Clean up internal docs | Remove internal planning docs from public repo: `docs/BENCHMARK_PLAN.md`, collapse Phase 22 detail in `ROADMAP.md` back to a summary. Keep `benchmark_results/methodology.md` (pre-registered, Bitcoin-stamped) and all raw data. Planning docs served their purpose — the published artifact is the data and the paper. |

#### Priority Presets (tested first, in order)

1. `collaborative` — the default, mesh communication, shared reward
2. `competitive` — agents race independently, best solution wins
3. `meritocratic` — earned influence, mandatory peer review
4. `auto` — agents design their own org structure
5. `hierarchical` — top-down, lead agent assigns tasks

Then expand to remaining 8 presets + `single-agent baseline` as capacity allows.

#### Metrics Framework (3 tiers — see `docs/BENCHMARK_PLAN.md` Section 5 for formulas)

- **Tier 1 (minimum publishable):** Success rate, tokens used, ticks used, Gini coefficient, communication volume, merge conflicts, run-to-run variance, baseline comparison.
- **Tier 2 (strong paper):** Network density/centrality, parallel utilisation, coordination overhead, role emergence, conflict resolution time, directive vs collaborative ratio, quality score.
- **Tier 3 (outstanding paper):** Per-tick temporal evolution, phase transition detection, metric correlation analysis, predictive validity (can tick-10 predict outcome?), emergent norm detection, superadditivity ratio.

#### Auto Mode Learning Flywheel

Every benchmark run feeds the learning system. Run → data → insights → better auto-mode starts → better runs. By the end of benchmarking, the `auto` preset will have accumulated enough history to make genuinely informed self-organisation decisions. This is a research output in itself.

---

### Phase 23: Go Public

**Goal:** Everything goes live. First public impression = best version.

| Step | What | Detail |
|------|------|--------|
| 23a | Make GitHub repo public | No secrets, no embarrassing TODOs, clean history. |
| 23b | PyPI publish | `pip install agentciv-engine` works for anyone. |
| 23c | Website live | agentciv.ai with all four wings. |
| 23d | Contributing guide | Add presets (YAML), dimensions, mechanisms. |
| 23e | Examples directory | Polished examples with READMEs showing different org structures. |

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
Phase 19 ✓  Phase 20 ✓  Phase 21 ✓  Phase 22     Phase 23
Battle-     Paper 5     Website     Benchmarks   Go Public
Test        (concept)   4 Wings     (NEXT)       (PyPI)
                        ├ Science
                        ├ Simulation
                        ├ Engine
                        └ Creator Mode

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

ERA 3: CREATOR MODE
═══════════════════════════════════════════════════════════════════════════════
Phase 32        Phase 33        Phase 34          Phase 35         Phase 36
Build Meta-     Task Search     Emergence         Full Website     Paper 5
Agent                           Explorer          Wing             Empirical
├ Design        ├ Decompose     ├ Metrics         ├ Results        ├ Results
├ Orchestrate   ├ Generate      ├ Sweep           ├ Live demo      ├ Update
├ Analyse       ├ Evaluate      ├ Novelty         ├ Discoveries    ├ Timestamp
├ Learn         ├ Refine          detect          └ Space map      └ Submit
└ CLI           └ Recommend     └ Catalogue

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
