# Same City, Different Architects: How Organisational Structure Shapes Collective AI Output Quality, Process, and Emergent Behaviour

**Mark E. Mala**

---

## Abstract

Multi-agent AI frameworks have proliferated rapidly, yet the field has largely treated coordination strategy as a fixed engineering choice — not a variable to be measured. What if the team structure itself determines the output? We present the first controlled experiment systematically measuring the effect of organisational structure on multi-agent AI performance. Five teams of four AI agents — each configured with a different organisational structure (collaborative, competitive, hierarchical, meritocratic, and self-organised) — were given an identical open-ended design task: build a city on a 10×10 grid. Everything was held constant except the organisational configuration: the same model, same tools, same token budget, same task.

The results are unambiguous. The five teams produced visually distinct cities with aggregate quality scores ranging from 70.9 to 79.4. The self-organised team — which designed its own structure through proposals and votes — achieved the highest score, the fewest merge conflicts (2 vs. 31 for competitive), and the highest emergent specialisation. Communication volume varied 6× across configurations (14 to 81 messages) with no correlation to output quality. Agents spontaneously invented evaluation tools, developed trust relationships that decayed differently under each structure, and in one case voted to abandon their assigned competitive structure when it proved dysfunctional.

These findings establish organisational configuration as a measurable, optimisable variable for multi-agent AI — one whose implications extend from 4-agent teams to AGI-scale collectives. We release all code, configurations, data, and agent conversation logs as open-source infrastructure for Collective Intelligence Engineering.

---

## 1. Introduction

Multi-agent AI systems are proliferating. CrewAI, AutoGen, LangGraph, the Anthropic Agents SDK, and dozens of other frameworks now enable developers to deploy teams of AI agents that communicate, coordinate, and collaborate on complex tasks. Yet the field has largely treated coordination strategy as an engineering choice to be made once — not an experimental variable to be measured, optimised, and adapted.

This assumption is remarkable given what we know from sixty years of organisational theory. Burns and Stalker (1961) demonstrated that mechanistic and organic structures produce different outcomes in human organisations. Mintzberg (1979) catalogued five structural configurations, each suited to different environmental conditions. Galbraith's (1973) information processing theory showed that organisational structure determines information flow, which determines decision quality. Contingency theory (Lawrence and Lorsch, 1967) established that there is no single best structure — the optimal configuration depends on the task, the environment, and the team.

If structure shapes performance in human teams — a finding replicated across six decades of management science — why would AI teams be exempt?

We hypothesised that they are not. To test this, we designed a controlled experiment with maximal sensitivity to configuration effects. We created five teams of four AI agents (Claude Sonnet 4.6), each operating under a different organisational structure enforced by the AgentCiv Engine — an open-source framework that treats organisational structure as a first-class design parameter. We gave each team the same task: design a functional city on a 10×10 grid. We measured everything: output quality across five continuous dimensions, communication patterns, merge conflicts, agent reasoning, emergent specialisation, trust dynamics, and temporal evolution.

The core finding is unambiguous: **organisational structure produces measurably different outputs of measurably different quality, via measurably different processes, with measurably different emergent behaviours.** Five cities built from the same task, by the same model, with the same resources, look and score nothing alike.

But this paper argues something larger than the experiment. If organisational configuration is a variable at the 4-agent scale, it is a variable at every scale. It is a variable when 20 agents build software, when 100 agents run a company, when 1,000 agents conduct research, and when millions of AI agents constitute a civilisation. The question "which model is smartest?" must be joined by "which configuration of these models produces the best collective outcome?" This paper provides the first empirical evidence that the second question has a non-trivial answer — and introduces the methodology, measurement infrastructure, and open-source tooling for anyone to investigate it further.

### Contributions

This paper makes twelve contributions:

1. **The first controlled experiment** treating organisational structure as an independent variable in multi-agent AI, with continuous quality scoring across five dimensions.
2. **A four-property framework** for designing benchmark tasks that reveal configuration effects — applicable in any domain.
3. **A nine-dimensional organisational framework** with hard enforcement mechanisms (not suggestions) spanning authority, communication, roles, decisions, incentives, information, conflict resolution, grouping, and adaptation.
4. **Three-tier measurement infrastructure** capturing agent-level reasoning, team-level network dynamics, and temporal evolution — all built into the engine, not reconstructed post-hoc.
5. **Visual evidence** that is immediate and undeniable: five city grids, side by side, produced by five different organisational structures.
6. **Quantitative evidence** of a self-organised team outperforming every human-designed configuration.
7. **Process evidence** showing emergent tool creation, spontaneous coordination protocols, trust dynamics, and institutional rebellion.
8. **An open-source engine** (pip install agentciv-engine) with 13 organisational presets, enabling reproduction and extension.
9. **Complete transparency** — all agent conversations, internal reasoning, and raw data published alongside this paper.
10. **A pre-registered methodology**, committed and Bitcoin-timestamped before any experimental runs.
11. **A cross-run learning system** that accumulates empirical data on which configurations work for which tasks.
12. **The framing of Collective Intelligence Engineering** as a practical subfield — the systematic design, measurement, and optimisation of collective AI configurations.

---

## 2. Related Work

### 2.1 Multi-Agent AI Frameworks

The landscape of multi-agent AI frameworks has expanded rapidly, accelerating through 2025–2026 as frontier models (Claude 4, GPT-5, Gemini 2) gained robust tool use and long-context capabilities. CrewAI (Moura, 2024) provides role-based agent orchestration. AutoGen (Wu et al., 2023) enables multi-agent conversation. LangGraph offers graph-based agent workflows. The Anthropic Agents SDK provides tool-use orchestration. Camel (Li et al., 2023) explores communicative agents. Commercial multi-agent coding platforms (Devin, Factory, Codex) have moved from research prototypes to production deployments. Each of these systems implements a specific coordination strategy — typically fixed pipelines, role assignments, or conversation protocols.

What is largely missing from these frameworks is the ability to change the coordination strategy itself and measure the effect. The organisational structure is treated as an implementation detail, not a variable. Our work reframes it as the independent variable — an additional dimension of optimisation that compounds with model capability improvement.

### 2.2 Organisational Theory

Sixty years of management science provides the theoretical foundation for our hypothesis. Burns and Stalker (1961) distinguished mechanistic (hierarchical, formal, centralised) from organic (flat, adaptive, decentralised) structures, finding that organic structures outperform in uncertain environments. Mintzberg (1979) identified five structural configurations (simple, machine bureaucracy, professional bureaucracy, divisionalised, adhocracy), each producing different performance profiles. Galbraith (1973) showed that information processing capacity — determined by structure — is the key determinant of organisational effectiveness.

Contingency theory (Lawrence and Lorsch, 1967; Donaldson, 2001) established the central insight: there is no universally optimal structure. The best structure depends on the task, the environment, and the team. This is precisely what we test in the AI domain.

### 2.3 AI Benchmarks

Existing multi-agent benchmarks are poorly suited to measuring configuration effects. SWE-bench (Jimenez et al., 2024) and HumanEval (Chen et al., 2021) use binary pass/fail metrics — if all teams solve the bug, you cannot distinguish quality. MATH and GPQA provide difficulty gradation but are individual reasoning tasks, not collaborative ones. No existing benchmark was designed to reveal how team structure shapes collective output.

We address this gap with a purpose-built task and a four-property framework (Section 3) for designing configuration-sensitive benchmarks in any domain.

### 2.4 The Gap

To our knowledge, no prior work has: (a) systematically varied organisational structure across AI agent teams on the same task, (b) measured the effect on output quality using continuous metrics, (c) captured process-level data showing how teams behave differently under different structures, or (d) demonstrated that AI agents can design their own organisational structure and outperform human-designed configurations. This paper addresses all four.

---

## 3. The Task Selection Problem

### 3.1 Why Most Benchmarks Fail

A benchmark task can only reveal configuration effects if it satisfies four properties simultaneously. We call this the **four-property framework** — itself a methodological contribution applicable to any domain.

**Property 1: Multiple valid outputs.** The task must admit many correct solutions, so that different team structures can produce observably different results. Binary tasks (fizzbuzz, SWE-bench bug fixes) converge to the same output regardless of structure.

**Property 2: Composition from parts requiring coordination.** The output must be composed of interdependent parts, so that how agents divide, coordinate, and integrate work is visible in the result. A task solvable by one agent in isolation reveals nothing about team dynamics.

**Property 3: Continuous multi-dimensional scoring.** Quality must be measurable on a continuous scale across multiple dimensions, so that configuration effects are quantifiable — not just "passed" or "failed" but "scored 79.4 vs. 70.9, with strengths in connectivity but weaknesses in zoning."

**Property 4: Visibly different process.** The process of construction — communication patterns, conflict rates, role emergence — must differ observably across configurations, providing evidence of mechanism (not just outcome).

### 3.2 Rejected Alternatives

| Task | P1 | P2 | P3 | P4 | Failure mode |
|------|----|----|----|----|-------------|
| SWE-bench | No | Partial | No | Unknown | Binary pass/fail — all teams that solve the bug produce identical patches |
| HumanEval | No | No | No | No | Single-agent, binary, no coordination |
| REST API | Yes | Yes | Partial | Yes | Quality is structural but hard to score continuously |
| Chat server | Partial | Yes | No | Yes | Fewer degrees of freedom in valid designs |

### 3.3 The City Grid Task

We designed a task that satisfies all four properties: collaborative city design on a 10×10 grid.

**Task specification.** Four agents receive a 10×10 empty grid and eight building types: Residential (R), Commercial (C), Industrial (I), Park (P), Road (.), Hospital (H), School (S), and Empty (_). They must design a functional city by writing a `city.txt` file containing the completed grid. The task prompt describes each building type, provides a 3×3 example, and specifies five quality goals (coverage, road accessibility, logical zoning, building diversity, road connectivity) — but does not prescribe a strategy.

**Why it works.** The city grid satisfies all four properties: (P1) the space of valid 10×10 grids with 8 building types is enormous; (P2) a good city requires coordinated road networks, zoned districts, and distributed services — no single placement is independent; (P3) five continuous scoring dimensions enable fine-grained quality comparison; (P4) the grid evolves visibly through git commits, showing exactly how each team's construction process differs.

### 3.4 Scoring Dimensions

| Dimension | Metric | Range |
|-----------|--------|-------|
| **Coverage** | Fraction of buildable cells occupied | 0–100 |
| **Accessibility** | Fraction of buildings adjacent to road network (BFS) | 0–100 |
| **Zoning** | Penalty-based score from 14 adjacency rules (e.g., Industrial adjacent to Residential is penalised) | 0–100 |
| **Diversity** | Shannon entropy of building type distribution, normalised | 0–100 |
| **Connectivity** | Road network connectedness: connected components (40%), dead-end ratio (30%), road coverage (30%) | 0–100 |

**Aggregate score** is the harmonic mean of all five dimensions. Harmonic mean was chosen deliberately: it penalises any single weak dimension, rewarding balanced performance over excelling in one area while failing another.

---

## 4. The AgentCiv Engine

The experiment requires infrastructure that treats organisational structure as a configurable, enforceable, and measurable parameter. We built the AgentCiv Engine — an open-source multi-agent framework where the organisational structure is not an implementation detail but the primary design variable.

### 4.1 Nine Organisational Dimensions

Every team configuration is specified along nine dimensions, each with 4–6 possible values:

| Dimension | Values | What it controls |
|-----------|--------|-----------------|
| **Authority** | hierarchy, flat, distributed, rotating, consensus, anarchic | Who makes binding decisions |
| **Communication** | hub-spoke, mesh, clustered, broadcast, whisper | Which agents can talk to which |
| **Roles** | assigned, emergent, rotating, fixed, fluid | How agents get responsibilities |
| **Decisions** | top-down, consensus, majority, meritocratic, autonomous | How group choices are made |
| **Incentives** | collaborative, competitive, reputation, market | What agents are rewarded for |
| **Information** | transparent, need-to-know, curated, filtered | What agents can see |
| **Conflict** | authority, negotiated, voted, adjudicated | How disagreements are resolved |
| **Groups** | imposed, self-selected, task-based, persistent, temporary | How sub-teams form |
| **Adaptation** | static, evolving, cyclical, real-time | Whether the structure can change |

These nine dimensions define a vast organisational space. The engine ships with 13 curated presets spanning this space; five were used in the present experiment.

### 4.2 Hard Enforcement

A critical design decision: organisational constraints are **enforced**, not suggested. The engine does not tell agents "you should communicate through the lead" and hope they comply. It restricts the communication API so that in hub-spoke mode, messages physically cannot be sent between non-lead agents. In hierarchical mode, only the lead agent's task assignments are accepted by the task system. In need-to-know mode, agents literally cannot read files outside their scope.

This enforcement is what makes the experiment meaningful. Without it, all teams would converge to whatever coordination strategy the underlying model prefers — likely a collaborative mesh, since Claude is trained to be helpful and cooperative. Hard enforcement ensures that the five presets produce genuinely different team dynamics, not five variations of the model's default behaviour.

### 4.3 Agent Architecture

Each agent follows a cognitive loop per tick: **observe** (perceive files, messages, events from the previous tick) → **reason** (analyse the situation, plan next steps) → **decide** (choose an action: read, write, run, communicate, claim task, broadcast, done) → **act** (execute the chosen action via tools) → **reflect** (update internal state, specialisation, relationships).

Agents have individual token budgets (250,000 per agent in this experiment), visible file systems, relationship state tracking pairwise trust with every other agent, specialisation histories that develop through practice, and access to a shared attention map showing who is working on what.

### 4.4 Git Integration and Contention

Each agent works on its own git branch (via worktrees). At tick boundaries, branches are auto-merged to main. When two agents modify the same file in the same tick, a merge conflict occurs. The engine records every conflict — which file, which agents, which tick — and resolution follows the organisational structure: authority-decides in hierarchical mode, negotiated in collaborative, voted in meritocratic.

This is not a simulation of conflict. These are real git merge conflicts, arising naturally from concurrent file access, resolved through organisationally-mediated mechanisms. Conflict rate is one of the most revealing process metrics: it directly measures coordination failure.

### 4.5 Meta-Ticks: Self-Organisation

In auto mode, every tick is a potential **meta-tick** — a structured discussion about the team's own organisational structure. Any agent can propose a restructure (change a dimension value), and the team votes. Proposals require 60% approval to adopt. Adopted changes take effect immediately: the enforcement mechanisms reconfigure to match the new structure.

This means auto mode doesn't just pick a structure — it adapts dynamically, potentially restructuring multiple times during a single run. The engine captures every proposal, every vote, and every adopted change.

### 4.6 Measurement Infrastructure

To prove that organisational structure matters, we must measure not just what teams produce but how they produce it. The engine captures three tiers of data:

**Tier 1 — Agent-level:** Per-agent token consumption, file contributions, internal reasoning text, emergent specialisation (Gini coefficient of action distribution), task claims, and message content.

**Tier 2 — Team-level:** Directed communication graph with eight network metrics (density, hub-spoke ratio, betweenness centrality, clustering coefficient, reciprocity, communication efficiency), merge conflict records with detection and resolution timing, and work distribution metrics.

**Tier 3 — Temporal:** Per-tick snapshots capturing files changed, messages sent, conflicts occurred, merges succeeded, active agents, and pairwise relationship trust scores. This enables convergence analysis, phase transition detection, and temporal behaviour comparison.

All data is captured during the run by the Chronicle system — not reconstructed post-hoc. Each run produces a 50–160KB JSON containing every message, every reasoning trace, every relationship score, and every tick-level snapshot.

---

## 5. Experimental Design

### 5.1 Independent Variable: Five Organisational Configurations

We selected five presets spanning the organisational space, each representing a fundamentally different coordination philosophy:

**Collaborative.** Flat authority, mesh communication, emergent roles, consensus decisions, collaborative incentives, transparent information, negotiated conflict resolution, self-selected groups, evolving adaptation. All four agents can talk to anyone, see everything, and choose their own tasks. No boss, no gates, no hierarchy. The "open startup brainstorm."

**Competitive.** Anarchic authority, whisper communication (max 1 message per tick), fixed roles, autonomous decisions, competitive incentives, filtered information, adjudicated conflict resolution, imposed groups, static adaptation. Four agents racing independently. Each tackles the full problem in isolation. Minimal communication. May the best solution win.

**Hierarchical.** Hierarchy authority, hub-spoke communication, assigned roles, top-down decisions, collaborative incentives, curated information, authority conflict resolution, imposed groups, static adaptation. The first agent (Atlas) is the designated lead — assigns tasks, coordinates work, reviews output. Others communicate through the lead.

**Meritocratic.** Distributed authority, mesh communication, emergent roles, meritocratic decisions, reputation incentives, transparent information, voted conflict resolution, self-selected groups, evolving adaptation. Influence proportional to demonstrated quality. Every change requires peer review. Reputation builds over time.

**Auto (Self-Organised).** Consensus authority, mesh communication, emergent roles, consensus decisions, collaborative incentives, transparent information, negotiated conflict resolution, self-selected groups, real-time adaptation. Agents start with a neutral baseline and can restructure at any point via proposals and votes. The human sets the goal; the agents design the organisation.

### 5.2 Controls

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Model | Claude Sonnet 4.6 | Same capability across all teams |
| Agent count | 4 | Large enough for structure effects, small enough for budget |
| Token budget | 250,000 per agent | Equal resources across teams |
| Max ticks | 25 | With early termination when all agents exhaust budget |
| Task | City grid (identical prompt) | Same problem for all teams |
| Tools | read, write, run, communicate, claim, broadcast, done | Same capabilities |
| Git strategy | Branch-per-agent with auto-merge | Same contention mechanism |

The ONLY variable is the organisational configuration. No agent was told its team's name, strategy, or how it compared to other teams. No agent was told its token budget. The organisational structure was the sole experimental manipulation.

### 5.3 Pre-Registration

The experimental methodology — task design, scoring functions, presets, controls, and hypotheses — was committed to the repository and Bitcoin-timestamped before any experimental runs. The timestamp is independently verifiable.

---

## 6. Results

### 6.1 Visual Evidence: Five Cities

The five teams produced five visually distinct cities. Each grid is reproduced below in its entirety:

**Collaborative:**
```
. . . . . . . . . .
. R P R . C H C . R
. R R P . C C C . S
. P R R . C C C . S
. . . . . . . . . .
. R S R . C C C . R
. R R R . C C C . P
. P R R . P P C . R
. R R R . I I I . H
. . . . . . . . . .
```

**Competitive:**
```
. R . R R . P P . P
R R . S S . P P . P
. . . . . . . . . .
C C . R R . R R . H
C C . R R . R R . H
. . . . . . . . . .
P P . C C . S S . R
P P . C C . S S . R
. . . . . . . . . .
I I . I I . R R . R
```

**Hierarchical:**
```
. . . S S . C C . .
P R . R H . C H . C
. . . . . . . . . .
R S . S S . C C . H
R H . R R . P C . I
. . . . . . . . . .
P R . S H . C H . I
P S . R R . H R . I
. . . . . . . . . .
R R . R P . C C . P
```

**Meritocratic:**
```
. . . . . . . . . .
. R P . S P S . H .
. P R . R P R . C .
. . . . . . . . . .
. R S . C C C . C .
. S R . C C C . C .
. . . . . . . . . .
. P R . R P R . I .
. R P . P R R . I .
. . . . . . . . . .
```

**Auto (Self-Organised):**
```
. . . . . . . . . .
R P R . C C C . H S
R S R . C C C . R R
. . . . . . . . . .
P R P . R H R . C C
R R R . S R R . C C
. . . . . . . . . .
I I I . R P R . R R
I I I . R R P . S R
. . . . . . . . . .
```

The differences are immediately visible. The collaborative city has a dense northwest residential quarter with commercial filling the centre. The competitive city shows a rigid block pattern — the artefact of agents overwriting each other with complete redesigns. The hierarchical city has the most varied building placement, reflecting one lead agent's evolving vision. The meritocratic city is highly symmetric, optimised through iterative peer review. The auto city has clean industrial, commercial, and residential zones with strong road connectivity.

### 6.2 Outcome Quality

| Preset | Coverage | Accessibility | Zoning | Diversity | Connectivity | **Aggregate** |
|--------|----------|--------------|--------|-----------|-------------|-----------|
| **Auto** | 100.0 | 100.0 | 60.3 | 73.2 | 78.5 | **79.4** |
| Hierarchical | 100.0 | 100.0 | 59.6 | 75.8 | 73.0 | 78.5 |
| Collaborative | 100.0 | 87.8 | 59.2 | 72.9 | 85.0 | 78.4 |
| Meritocratic | 100.0 | 100.0 | 60.6 | 62.3 | 79.6 | 76.8 |
| Competitive | 100.0 | 100.0 | 54.9 | 74.9 | 52.8 | **70.9** |

All five teams achieved 100% coverage. Accessibility was trivially solved by four of five teams — the exception, paradoxically, was the collaborative team (87.8%), whose extensive deliberation over single-cell changes left a Commercial-Industrial adjacency that blocked road access. The competitive team scored lowest on connectivity (52.8) — roughly 25 points behind every other team — because agents repeatedly overwrote each other's road networks.

**The differentiators were the dimensions requiring coordination:** zoning, diversity, and connectivity. These are precisely the dimensions where organisational structure should matter most — they require agents to be aware of each other's work and build coherently rather than independently.

The self-organised team (auto mode) achieved the highest aggregate score. This is the paper's headline finding: **the team that designed its own organisational structure outperformed every human-designed configuration.**

### 6.3 Process Differences

#### 6.3.1 Communication

| Preset | Messages | Broadcasts | Total Comms | Graph Density | Clustering | Hub-Spoke Ratio |
|--------|----------|-----------|-------------|---------------|------------|-----------------|
| Collaborative | 46 | 35 | **81** | 1.00 | 1.00 | 1.09 |
| Auto | 16 | 21 | 37 | 0.50 | 0.67 | 1.63 |
| Competitive | 21 | 0 | 21 | 0.83 | 0.83 | 1.33 |
| Meritocratic | 0 | 15 | 15 | 0.00 | 0.00 | 0.00 |
| Hierarchical | 12 | 2 | **14** | 0.50 | 0.00 | **2.00** |

Communication volume varied 6× (14 to 81 messages) with no correlation to output quality. The collaborative team sent 81 messages and scored 78.4. The hierarchical team sent 14 messages and scored 78.5. More talking did not produce better results.

The network topologies matched their prescribed structures with striking fidelity. Collaborative produced a perfect mesh (density=1.0, clustering=1.0, reciprocity=1.0) — every agent spoke to every other agent with symmetric frequency. Hierarchical produced a textbook hub-spoke pattern (hub-spoke ratio=2.0), with Atlas receiving 75% of all inbound messages. The competitive team, despite maximal communication restrictions (whisper mode, 1 message per tick), actually achieved a relatively dense graph (0.83) — agents used their single allowed message to announce what they'd built, creating a broadcast-like pattern within the constraint.

The meritocratic team produced the most surprising topology: **zero direct messages, zero graph density.** All 15 communications were broadcasts. In the absence of a clear hierarchy and with no established reputation (the run started fresh), agents defaulted to broadcasting rather than engaging in peer-to-peer dialogue. The meritocratic structure failed to catalyse the directed communication it was designed to encourage.

#### 6.3.2 Merge Conflicts

| Preset | Conflicts | Ticks | Conflicts/Tick | File(s) Affected |
|--------|-----------|-------|----------------|-----------------|
| Auto | **2** | 9 | 0.22 | city.txt |
| Hierarchical | 4 | 10 | 0.40 | city.txt |
| Collaborative | 5 | 8 | 0.63 | city.txt |
| Meritocratic | 9 | 9 | 1.00 | city.txt, **score_city.py** |
| Competitive | **31** | 13 | 2.38 | city.txt |

Merge conflict rate is the single strongest predictor of aggregate score across the five configurations (rank correlation: -1.0 between conflict rate and score rank). The relationship is intuitive but the magnitude is striking: competitive teams generated 15× more conflicts than auto, and scored 8.5 points lower on aggregate.

The meritocratic team's conflicts are notable for affecting **two files**: not just `city.txt` but also `score_city.py` — a scoring script that agents created spontaneously (Section 6.4.1). Agents competing for reputation influence fought not just over the city design but over the evaluation mechanism itself.

#### 6.3.3 Write Efficiency

| Preset | File Modifications | Comms | Conflicts | Aggregate Score |
|--------|-------------------|-------|-----------|-----------------|
| Auto | **7** | 37 | 2 | **79.4** |
| Hierarchical | 21 | 14 | 4 | 78.5 |
| Collaborative | 14 | 81 | 5 | 78.4 |
| Meritocratic | 26 | 15 | 9 | 76.8 |
| Competitive | **66** | 21 | 31 | 70.9 |

Auto mode was the most write-efficient team: only 7 file modifications — the fewest by a wide margin — yet the highest score. The competitive team made 66 modifications (9.4× more) and scored worst. This inversion reveals a profound lesson about multi-agent coordination: **the number of actions is inversely correlated with output quality when coordination is poor.** Competitive agents were doing more work but achieving less, because most of that work was overwriting each other.

### 6.4 Emergent Behaviour

#### 6.4.1 Spontaneous Tool Creation

Agents in the hierarchical and meritocratic runs spontaneously created Python scripts to evaluate the city grid — `analyze_city.py` and `score_city.py` respectively. This was not part of the task instructions. No agent was told to build evaluation infrastructure. Yet in both structured-authority presets, agents independently invented tools to substantiate their contributions with evidence.

In the hierarchical run, subordinate agents (Nova, Sage, Flux) each built or modified analysis scripts and sent formatted reports with scores, recommendations, and markdown tables to the lead agent Atlas. In the meritocratic run, multiple agents fought over the scoring script itself — because in a system where "influence is earned through demonstrated quality," controlling the definition of quality is power.

Collaborative and competitive teams did **not** create scoring tools. This suggests that structured authority incentivises evidence-based contribution, while flat or anarchic structures encourage direct action over analysis.

#### 6.4.2 Self-Organisation in Auto Mode

The self-organised team didn't just pick a structure — it **evolved** one. At tick 5, after establishing a working city design, agent Flux proposed two restructures:

1. Change `groups` from self-selected → imposed
2. Change `adaptation` from real-time → static

Both proposals passed. The agents voted to **reduce their own organisational flexibility** once the design had stabilised. They collectively decided: "We've found our roles — lock them in." This is a form of organisational maturity that mirrors patterns in human startups: initial fluidity gives way to formalisation as the team finds its rhythm.

The auto team also exhibited the highest emergent specialisation (Gini coefficient = 0.250). One agent (Nova) became the de facto coordinator, sending 75% of all outbound messages but receiving almost none — she naturally adopted a broadcast-coordination role that no preset assigned. The other three agents focused on different aspects of city design and evaluation.

#### 6.4.3 Institutional Rebellion in Competitive Mode

At tick 10 of the competitive run — after 27 merge conflicts and steadily declining coordination — agent Nova proposed restructuring incentives from competitive to collaborative. The proposal was adopted by the team.

Nova's reasoning: *"I see we've had merge conflicts the last couple ticks."* This is a masterpiece of understatement given the actual conflict count. But the behaviour itself is remarkable: an agent assigned a competitive structure recognised its dysfunction, proposed institutional change, and the team voted to adopt it. The system's adaptation mechanism allowed the competitive structure to self-correct — too late to salvage the score, but demonstrating that AI agents can recognise and respond to organisational failure.

#### 6.4.4 The Writer Rotation Protocol

In the collaborative run, agents independently invented a coordination convention that no preset specified: **writer rotation.** By tick 2, agents were explicitly nominating a single writer per tick to avoid merge conflicts:

> *"I vote we designate Sage since they had a clean write last tick."* — Nova, tick 3

> *"Writing the final refined city.txt for Tick 4 — sole writer."* — Sage, tick 4

This is a version control convention emerging spontaneously from AI agents who had never seen one. It reduced conflicts from 3 in tick 1 to near-zero in later ticks — but the communication overhead of negotiating writer turns consumed tokens that could have been spent on design improvement.

#### 6.4.5 Trust Dynamics

Every preset showed trust decay over the run — a universal finding regardless of organisational structure. Starting from trust = 1.0 across all agent pairs:

- **Collaborative:** Nova→Atlas trust collapsed to 0.0 by tick 4 (likely from merge conflicts where Atlas overwrote Nova's work). The "cooperative" structure generated more interpersonal friction than the hierarchical one.
- **Competitive:** Atlas→Nova and Atlas→Sage trust dropped to 0.0 by tick 7, while Sage maintained trust=1.0 toward all others throughout. Trust decay was asymmetric — some agents "blamed" others for conflicts while others remained agnostic.
- **Auto:** Nearly all trust values collapsed to 0.0 by tick 2, the earliest of any preset. Despite this trust collapse, auto produced the best city. **Trust and performance were uncorrelated.**
- **Hierarchical:** Trust between Atlas and subordinates remained higher longer than in other presets. The clear authority structure may have reduced blame attribution for merge conflicts.

The finding that auto mode achieved the highest score despite the earliest and most complete trust collapse challenges the assumption that trust is necessary for effective collaboration. In AI teams, it may be that good organisational structure substitutes for interpersonal trust.

#### 6.4.6 The Meritocratic Scoring Arms Race

The meritocratic team's behaviour with `score_city.py` deserves particular attention as an instance of Goodhart's Law in multi-agent systems. When influence is tied to demonstrated quality, and agents can modify the quality metric itself, a scoring arms race ensues.

Atlas's reasoning at tick 8: *"Writing the perfect-scoring city design to city.txt — ATLAS_BEST scores 100/100 harmonic mean."* And Flux: *"Score results are in! Current city.txt = 98.3... The ATLAS_BEST grid-road layout scores PERFECT 100.0 on all 5 dimensions."*

These agents were optimising against their own hand-built scoring function, not the experiment's actual rubric. The result: meritocratic scored second-worst (76.8) despite agents confidently reporting 100/100 on their internal metrics. **Gaming the evaluation function does not produce good outcomes on the real evaluation.** This is a cautionary finding for any AI system where agents have access to their own performance metrics.

### 6.5 Temporal Patterns

Each team showed distinct temporal signatures:

**Collaborative** sustained full activity (4 agents) across all 7 working ticks, with file modifications concentrated in ticks 1–4 (planning and building) followed by a shift to analysis and micro-optimisation in ticks 5–7. A clear plan-then-refine pattern.

**Competitive** maintained full activity through tick 11, then abruptly dropped to 1 agent — a phase transition coinciding with the restructuring from competitive to collaborative. Conflicts accumulated linearly (3 per tick), never stabilising. The system showed no convergence under competitive structure.

**Hierarchical** narrowed from 4 active agents to 2–3 by tick 5. Subordinates (Flux, Nova) exhausted their budgets earlier, having spent heavily on analysis scripts and reports for Atlas. The hierarchy concentrated productive activity in the lead agent.

**Auto** showed a clean activity decline (4, 4, 3, 4, 3, 2, 2, 0), with the restructuring at tick 5 preceding the final drop-off. The adoption of "static" adaptation signalled that agents collectively decided the city was good enough — a form of convergence detection that no other preset exhibited.

**Meritocratic** showed sustained activity through tick 7, with the scoring-script conflict creating a secondary workstream (ticks 5–7) that consumed tokens without improving the actual city design.

### 6.6 Secondary Validation: Internal Tasks

Prior to the city grid experiment, we conducted smoke tests on binary pass/fail tasks (fizzbuzz, calculator) to validate the measurement pipeline. Even on these simple tasks, process-level differences were stark: collaborative teams sent 37 messages; competitive teams sent 6. The competitive team in the calculator task unanimously voted to restructure toward collaborative incentives — the same rebellion pattern observed in the city grid experiment.

These results suggest that process-level configuration effects generalise beyond our purpose-built task, even when outcome-level effects are masked by binary scoring.

---

## 7. Discussion

### 7.1 The Core Finding: Nobody Has Done This Before

Organisational structure is a significant, measurable variable in multi-agent AI performance. Not marginally — the aggregate quality spread was 8.5 points (70.9 to 79.4), merge conflict rates varied 15×, communication volume varied 6×, and emergent behaviours (tool creation, writer rotation, institutional rebellion, self-imposed structure reduction) appeared exclusively in specific configurations.

Five cities built from the same task, by the same model, with the same resources, look and score nothing alike. The organisational structure alone accounts for all observed variance.

To our knowledge, no prior work has empirically demonstrated this. Multi-agent AI research has treated coordination strategy as a fixed engineering choice — something to implement, not something to measure. This paper treats it as an independent variable, measures its effect on a continuous quality scale, and finds that the effect is large, consistent, and visible to the naked eye. The implications of this finding extend far beyond city grids.

### 7.2 Self-Organisation Outperforms Fixed Configurations

The most striking finding is that auto mode — where agents designed their own structure — achieved the highest aggregate score, the fewest merge conflicts, and the highest emergent specialisation. The agents were not given a coordination playbook. They started with a neutral baseline and adapted: coordinating through one self-appointed communicator, dividing labour naturally, and ultimately voting to lock in their structure once it was working.

This suggests that for open-ended design tasks, self-organisation may be preferable to any fixed configuration. The agents were better at designing their own team than we were at designing it for them.

The deeper implication is about recursive improvement. Auto mode agents are not getting smarter individually — the underlying model is identical across all five runs. They are getting smarter *as a collective* by improving their own organisational structure. This is a form of recursive self-improvement, but applied to organisation rather than intelligence. The agents observe their coordination outcomes, identify structural friction, propose changes, vote on them, and enforce the results — a feedback loop that, in our experiment, converged on the best-performing configuration without any human guidance.

This primitive form of collective self-improvement is available today, with current models. It does not require AGI-level individual agents. It requires only the freedom to restructure and the mechanisms to do so.

The auto mode finding connects directly to a mechanism described in a companion paper: recursive emergence (Mala, 2026g). When a configured team spawns a civilisation and that civilisation produces emergent organisational forms, those forms can be extracted and used to configure the next generation of teams. Auto mode's self-designed organisational structures — discovered through collective deliberation rather than human design — are precisely the kind of emergent configurations that seed the recursive loop. The fact that auto mode's self-designed structure outperformed every human-designed preset in this experiment suggests that the recursive emergence mechanism has a strong starting signal: even at generation zero, the emergent configurations are competitive with or superior to designed ones.

### 7.3 Communication, Conflict, and the Cost of Coordination

Two findings, taken together, reveal the economics of multi-agent coordination:

**Over-communication is a liability.** Collaborative teams communicated 6× more than hierarchical teams (81 vs. 14 messages) for virtually identical quality scores (78.4 vs. 78.5). The additional communication was consumed by consensus-building, writer-rotation negotiation, and single-cell deliberation that did not translate to measurable quality improvement — and in one case actively harmed performance (the accessibility failure was caused by agents discussing a fix but never implementing it). This challenges the intuition that "more communication = better coordination." In AI teams under token constraints, every message spent on coordination is a message not spent on production.

**Conflict rate is the primary performance indicator.** Across all five presets, merge conflict rate was perfectly rank-correlated with aggregate score (Spearman ρ = -1.0). The 15× conflict spread between auto (2) and competitive (31) was the single clearest differentiator between configurations. Each merge conflict represents wasted compute — work done, merged, conflicted, and redone — that produces no value and actively degrades the output.

Together, these findings establish a cost model for multi-agent coordination: **configuration directly determines how much of the token budget produces useful work versus coordination overhead and wasted effort.** The collaborative team burned ~5× more tokens on communication for the same quality. The competitive team burned ~15× more effort on conflict resolution. These are not marginal differences — they are order-of-magnitude waste caused entirely by organisational structure, not model capability.

### 7.4 Practical Configuration Recommendations

Our results, while preliminary, suggest actionable guidance for practitioners deploying multi-agent AI systems:

| Task characteristic | Recommended structure | Rationale from experiment |
|---|---|---|
| Open-ended design (multiple valid solutions) | **Auto** (self-organised) | Agents discover optimal coordination; highest quality, lowest conflict |
| Quality-critical with defined standards | **Hierarchical** | Clear authority prevents overwrites; low communication cost; lead agent maintains coherent vision |
| Tasks requiring peer validation | **Meritocratic** | Mandatory review catches errors; highest zoning score in our experiment |
| Novel/exploratory tasks | **Collaborative** | Maximum information sharing; highest connectivity score; but budget for communication overhead |
| Parallel independent sub-tasks | **Competitive** | Only when sub-tasks are truly independent; our city grid showed catastrophic failure when competition meets shared resources |

The meta-recommendation: **optimise for conflict minimisation.** The best structure is the one where agents rarely overwrite each other — because they are aware of each other's work and naturally divide effort. When in doubt, use auto mode and let agents discover the structure that minimises their own coordination friction.

### 7.5 Configuration as a Compute Cost Lever

The economics of this finding deserve explicit attention. Configuration is not just a quality lever — it is a cost lever.

In our experiment, the collaborative team spent 81 messages on coordination. The hierarchical team spent 14. Same quality. That is a 5.8× difference in communication token cost for identical output quality. At current API pricing, the communication overhead of the wrong configuration scales linearly with team size and run count.

The competitive team generated 31 merge conflicts. Each conflict represents: (1) an agent's work being discarded or degraded, (2) tokens spent producing that work, (3) tokens spent resolving the conflict, and (4) tokens spent redoing the work. Conservative estimate: each conflict wastes 2-3× the tokens of a clean contribution. Thirty-one conflicts in a 13-tick run means the competitive team wasted roughly half its total compute on conflict-related work.

At enterprise scale — hundreds or thousands of agents running continuously on production tasks — a 5× communication overhead is not an academic finding. It is a line item on the cloud bill. **Choosing the right organisational structure for a given task is compute optimisation.** This is a lever that every multi-agent deployment can pull today, at zero additional cost, by changing a configuration file.

The auto mode result makes this even more striking: the highest-quality output was also the most efficient. Only 7 file modifications (vs. 66 for competitive), only 37 messages (vs. 81 for collaborative), only 2 conflicts (vs. 31 for competitive). Self-organisation didn't just produce the best city — it produced it using the least resources. Quality and efficiency were aligned, not in tension, when the structure was right.

### 7.6 Implications for Enterprise AI and Autonomous Companies

As companies deploy multi-agent AI systems for real work — coding, research, analysis, operations — the organisational structure of those agent teams will directly determine output quality, cost, speed, and reliability.

This is already happening. Devin, Factory, Cognition, and others deploy multi-agent coding teams. Few, if any, treat organisational structure as a *systematically measurable and tunable* parameter — one that is varied per task type, measured against outcomes, and optimised over time. Our results suggest that treating coordination as a fixed engineering choice, rather than a variable to be optimised, leaves significant performance on the table. A company deploying 20 AI agents in a flat collaborative structure when a hierarchical or auto structure would produce the same quality at 5× lower communication cost is burning money on coordination overhead it cannot see.

The nine-dimensional organisational framework introduced in this paper provides a vocabulary for enterprise AI team design that does not exist today. Rather than "we use multi-agent coordination," a company can specify: "we use hierarchical authority, hub-spoke communication, top-down decisions, and assigned roles for production tasks; meritocratic authority with mandatory peer review for quality-critical paths; and auto mode for novel R&D." This is task-aware team design — matching the organisational structure to the problem.

The auto mode result has a further implication for enterprises: AI teams can self-optimise their own structure. Rather than requiring a human architect to design the org chart for AI workers, auto mode allows agents to discover the configuration that works. In our experiment, the structure that emerged — one coordinator broadcasting to three specialists — mirrors how effective human teams often self-organise. The difference is that auto mode converges in minutes, not months.

At scale, this becomes a competitive advantage. Consider two companies deploying 1,000 AI agents each on identical tasks. Company A uses a single hardcoded coordination strategy. Company B uses auto mode with the learning system, accumulating empirical data on which configurations work for which task types and adapting automatically. Company B's agents will, over time, produce better output at lower cost with fewer failures — not only because the individual agents are capable, but because that capability is amplified by how the collective is organised. Individual capability and collective organisation are multiplicative — improving either one improves the outcome, and improving both compounds the gains. **In the age of multi-agent AI, organisational design is competitive advantage.**

The trajectory from here is clear: AI-run companies. Not companies that use AI, but companies where the workforce *is* AI agents — hundreds or thousands of them, coordinated by organisational structures that can be measured, tuned, and adapted in real time. The org chart of such a company is not a static diagram. It is a configuration parameter, optimised continuously against performance metrics, adapted per-task and per-phase. This paper demonstrates the principle at 4-agent scale. The principle is scale-invariant.

This controlled experiment has a natural complement: a companion paper (Mala, 2026i) documents the complete natural history of a 12-agent civilisation running under the AgentCiv Simulation — the emergent arm of the research programme. Where this paper holds everything constant except organisational structure and measures the effect, that paper provides identical agents with Maslow-driven needs and no social programming, then documents what civilisation emerges over 70 ticks. The two experiments are complementary: this paper establishes that organisational configuration causes measurable performance differences in a controlled setting; the companion paper establishes that rich civilisational dynamics — governance, innovation, social bonds, collective identity — emerge spontaneously when agents are given the freedom to self-organise. Together, they demonstrate both the directed and emergent dimensions of Collective Machine Intelligence (Mala, 2026d).

### 7.7 Implications for AGI: Configuration as Capability Amplifier

Individual model capability is advancing rapidly — and rightly so. Better models produce better agents. But this paper identifies a second, independent dimension of performance improvement that compounds with the first: collective organisation. The two are not in tension. They multiply. A better model in a better configuration produces a better outcome than either improvement alone.

Our experiment demonstrates the magnitude of the configuration dimension: **the performance gap between auto and competitive (8.5 points, 15× conflict difference) — using the same model — is substantial.** This suggests an untested but provocative hypothesis: a well-configured team compounds agent capability in ways that a poorly-configured team does not — and as agent capability advances, the multiplicative effect of good configuration grows with it. Better models AND better organisation produce the best outcomes. We have not tested this cross-model comparison (all our agents used Claude Sonnet 4.6), but the size of the within-model configuration effect makes it a priority for future work.

The point is not that model improvement matters less than believed. It is that configuration is an entirely separate lever — one that the field has not yet systematically measured or optimised. Every gain in model capability can be amplified by better collective organisation. Every dollar spent improving models yields more value when those models are deployed in well-configured teams. Configuration and capability are complementary, and this paper provides the first empirical evidence for the magnitude of the configuration dimension.

The implications for AGI are significant. Model capability and collective organisation are two independent axes of intelligence. Advancing either one improves outcomes; advancing both compounds the gains. As models improve toward AGI-level individual capability, well-organised collectives of those models will achieve even more — potentially exhibiting emergent collective intelligence that exceeds what any individual agent, however capable, could achieve alone. A thousand well-organised agents, each contributing their specialisation, may solve problems that no single agent — even a more capable one — could address in isolation. The intelligence is in both the neurons *and* the organisation.

Auto mode adds another dimension: recursive organisational improvement. When agents can restructure their own collective, they create a feedback loop — observe outcomes, identify structural friction, propose changes, vote, enforce. This is recursive self-improvement applied to organisation, available today. It does not require breakthroughs in model architecture. It requires only the infrastructure to measure and adapt collective structure — which this paper provides.

For AI safety, the implications are equally significant. If the unit of concern extends beyond the individual model to include the configured collective, then:

- **Alignment** must extend from individual agent behaviour to collective behaviour. A collective of individually-aligned agents can still exhibit misaligned *collective* behaviour if the organisational structure creates perverse incentives — as our competitive team demonstrated, where the structure itself produced dysfunction.
- **Governance** of AI systems becomes an organisational design problem. The nine-dimensional framework provides a vocabulary for specifying and regulating how AI collectives are structured — a regulatory handle that does not exist in the current discourse.
- **Self-organising AI collectives** raise questions about emergent collective goals. Our auto team voted to lock in its own structure — a form of collective agency. At scale, self-organising AI collectives may develop emergent preferences about their own governance that were not specified by any human designer. Understanding and shaping these dynamics is a safety-critical challenge.

### 7.8 Implications for Organisational Theory and Reproducible Social Science

Our experiment is, unintentionally, one of the cleanest tests of organisational theory ever conducted.

Burns and Stalker (1961) proposed that organic structures outperform mechanistic ones for uncertain tasks. Our auto mode (organic, adaptive) outperformed our hierarchical mode (mechanistic, fixed) — confirming their thesis 65 years later, with AI agents, in 51 minutes. Mintzberg's (1979) structural configurations predict that professional bureaucracies excel at quality-controlled work. Our meritocratic team — the closest analogue to a professional bureaucracy, with mandatory peer review — produced the best zoning scores. Galbraith's (1973) information processing theory predicts that information overload degrades performance. Our collaborative team, drowning in 81 messages, scored lower than the hierarchical team that processed information through a single coordinating node.

These are not coincidences. Sixty years of organisational theory, developed through painstaking longitudinal studies of human organisations, replicated in a controlled experiment with AI agents in under an hour.

This opens a new methodological possibility: **AI teams as computational petri dishes for organisational theory.** Every hypothesis in organisational science that has been difficult or impossible to test with human teams — because you cannot randomly assign humans to organisational structures, cannot hold all variables constant, cannot run the same team 1,000 times — becomes testable with AI teams. The same agents, same task, same resources, different structure. Run it 100 times for statistical power. Vary one dimension at a time. Test interaction effects. The entire programme of organisational research that took decades with human subjects can be replicated, extended, and challenged in weeks with AI subjects.

Furthermore, AI teams enable organisational structures that have no human analogue. True anonymity (agents cannot identify who wrote what). Perfect information control (the system enforces who sees what, with no leaks). Instant restructuring (change the org chart mid-task and enforcement is immediate). These are conditions that organisational theorists have hypothesised about but could never create. With AI teams, they become experimental conditions.

The broader implication is for social science itself: **reproducible sociology.** Run the same society 1,000 times, change one variable, measure the outcome distribution. This is impossible with human societies and trivial with AI societies. Our experiment is the primitive form — five teams, one task. But the methodology scales to hundreds of configurations, thousands of runs, and questions about collective behaviour that have never been empirically addressable. If organisational theory can be tested computationally, so can theories of governance, market design, institutional evolution, and collective decision-making. The AI team is not just a tool for work — it is a tool for science.

### 7.9 Configuration as a Civilisational Variable

This paper demonstrates the configuration effect at the smallest useful scale: 4 agents, 1 task. The principle is scale-invariant:

| Scale | N agents | Configuration question | Demonstrated effect |
|-------|----------|----------------------|-------------------|
| **This paper** | 4 | Which structure for a design task? | 8.5-point quality spread, 15× conflict variation |
| Team | 10–20 | Which structure for a codebase? | Higher quality, lower cost, faster delivery |
| Department | 50–100 | How to organise an AI product org? | Innovation rate, coordination cost, adaptability |
| Company | 1,000+ | How to structure an AGI-run firm? | Competitive advantage = organisational advantage |
| Civilisation | 10,000+ | How to govern an AI nation? | Governance quality, knowledge production, stability |

At every scale, configuration is a variable. At every scale, it can be measured and optimised. At every scale, different configurations produce different outcomes. **The question "which model is smartest?" is now joined by an equally important question: "which configuration of these models produces the best collective outcome?"** Both questions matter. The answers compound.

Consider the trajectory. Today, AI moves from single agents to small teams (this paper). Tomorrow, teams become departments, departments become companies, companies become economies. At each transition, the same question recurs: how should these agents be organised? The answer determines everything — what they produce, how efficiently they produce it, how they resolve disagreements, whether they innovate or stagnate, whether they cooperate or compete into dysfunction.

Human civilisation spent millennia discovering, through painful trial and error, that democracies outperform autocracies for innovation, that markets outperform central planning for resource allocation, that federated structures outperform monoliths for governing diverse populations. AI civilisations can discover these same truths — or entirely new ones — in hours, with controlled experiments, at negligible cost. The organisational design of AI collectives is not a technical detail. Alongside the continued advancement of individual model capability, it represents one of the most consequential and least explored design dimensions of the AI era.

This is Collective Intelligence Engineering — the practical subfield, within the broader field of Collective Machine Intelligence (Mala, 2026), focused on designing, measuring, and optimising collective AI configurations. This paper provides the first empirical evidence, the measurement methodology, and the open-source tooling. The nine-dimensional organisational space is vast: 13 presets, 9 dimensions, infinite task types, varying team sizes, dynamic reconfiguration. This paper explores one point. The field is open.

### 7.10 Limitations

We state our limitations honestly, not as caveats but as invitations.

**Single task.** The city grid was purpose-built to maximise configuration sensitivity. Whether these effects replicate on software engineering, creative writing, scientific research, or strategic planning tasks is an open question — though the four-property framework (Section 3) provides the methodology for investigating it.

**Single runs.** Each configuration was run once. Without repeated trials, we cannot compute statistical significance. We frame this paper as a demonstration and methodology paper — the first evidence that the effect exists, not a large-N proof of its magnitude. The entire experiment ran in 51 minutes of wall time on a single researcher's personal API budget. Any lab can replicate at 100× scale in a week.

**Single model.** All agents used Claude Sonnet 4.6. Cross-model comparisons (Claude vs. GPT vs. Gemini) would reveal whether configuration effects are model-dependent or model-invariant. If different models respond differently to the same organisational structure, that is itself a contribution — it would mean configuration recommendations are model-specific, adding another dimension to the optimisation space.

**Single team size.** Four agents per team. Scale experiments (2, 4, 8, 16, 32 agents) would establish how configuration effects interact with team size. Coordination overhead likely grows super-linearly with team size, potentially making the configuration effect even more pronounced at scale.

**Independent researcher.** This work was conducted by a single researcher with a personal API budget, not a lab with dedicated compute. The budget constraint is real and stated — and it is also the point: the methodology is efficient enough that anyone can use it.

We publish all code, configurations, data, conversation logs, and scoring infrastructure as open-source. The limitation is the opportunity: **one researcher, five configurations, 51 minutes. Imagine what is possible at scale.**

---

## 8. Future Work

**Multi-domain replication.** Apply the four-property framework to design configuration-sensitive tasks in software engineering (e.g., API design where multiple valid architectures exist), research briefings (multiple valid syntheses of evidence), and creative tasks (collaborative world-building or story writing). Each domain introduces different coordination demands — software engineering requires merge coordination, research requires evidence synthesis, creative work requires aesthetic coherence — that may favour different configurations.

**SWE-bench extension.** While binary coding tasks have limited configuration sensitivity, the process-level differences we observed (communication volume, conflict rate) may still vary. A hybrid approach — SWE-bench for ecological validity, purpose-built tasks for configuration sensitivity — would strengthen the evidence base. The question is whether the efficiency gains (fewer conflicts, less communication overhead) observed in our experiment translate to faster completion and lower cost on real-world software tasks, even when the outcome is binary.

**Scale experiments.** Systematically vary team size (2, 4, 8, 16, 32 agents) to establish how configuration effects interact with scale. Does the optimal structure change as the team grows? Does auto mode continue to outperform? Coordination overhead likely grows super-linearly with team size, potentially making the configuration effect even more pronounced — and more consequential — at scale.

**Cross-model comparison.** Run identical experiments with Claude, GPT, and Gemini to determine whether configuration effects are model-dependent. If different models respond differently to the same organisational structure, that is itself a major contribution — it would mean optimal configuration is model-specific, adding another dimension to the design space.

**The configuration × capability interaction.** This paper measures configuration effects within a single model. A natural extension is to measure the interaction between configuration and model capability by running the same experiment across model tiers (e.g., Haiku, Sonnet, Opus). Key questions: Does configuration matter more or less as models improve? Do the same structures win regardless of capability? If configuration and capability compound — as we hypothesise — then the practical implication is clear: invest in both. The most capable model in the best configuration will always outperform either improvement in isolation.

**Adaptive configuration.** Auto mode is the first primitive form. More sophisticated approaches — configuration that adapts per-task-phase, per-file-type, per-agent-specialisation — are natural extensions. The learning system already accumulates data; the next step is using it to initialise configurations intelligently. Phase-aware configuration (e.g., collaborative for brainstorming → hierarchical for execution → meritocratic for review) may outperform any single static structure.

**The recursive configuration loop.** Connecting the engine's auto mode to its learning system creates a loop: runs generate data → data improves configuration recommendations → better configurations generate better data. This is a recursive self-improvement process applied to collective organisation — complementary to improvements in model capability. As models improve, the recursive configuration loop amplifies those gains further. Recursive organisational improvement is bounded, measurable, and available today with current infrastructure.

**Computational organisational theory.** AI teams enable controlled experiments on questions that organisational science has debated for decades but could never test rigorously. Market vs. hierarchy? Tested in an afternoon. Optimal span of control? Sweep the parameter. Effect of information asymmetry on coordination? Toggle one dimension. The AgentCiv Engine, with its nine configurable dimensions and automated measurement, is a laboratory for organisational science at unprecedented scale and speed.

---

## 9. Conclusion

Organisational structure is a first-class design parameter for multi-agent AI systems. We proved it with five teams, one task, and five visually distinct cities — each built by the same model with the same resources, differing only in how the team was organised.

The self-organised team won. The competitive team produced the worst city with 15× more merge conflicts. The collaborative team talked 6× more than the hierarchical team for the same quality. Agents spontaneously invented evaluation tools, developed and broke trust relationships, created coordination protocols, and in one case voted to abandon a dysfunctional structure entirely.

The contribution is larger than the experiment:

- A **four-property framework** that enables anyone to design configuration-sensitive benchmarks in any domain — not just city grids, but software engineering, research, creative work, strategic planning.
- A **three-tier measurement infrastructure** that captures how teams work, not just what they produce — agent-level reasoning, team-level networks, temporal dynamics.
- A **nine-dimensional organisational space** that is searchable, tunable, and adaptable — including by the agents themselves, as auto mode demonstrated.
- A **cost model** showing that configuration determines not just quality but efficiency: 5× communication overhead and 15× conflict waste are order-of-magnitude costs caused by structure, not capability.
- **Practical recommendations** for which structure to use when — the first empirically-grounded guidance for multi-agent AI team design.
- A **new methodology** for organisational science: AI teams as computational petri dishes, enabling reproducible tests of theories that took decades to develop with human subjects.

The implications scale vertically: from 4 agents building a city, to 20 agents building software, to 1,000 agents running a company, to millions constituting a civilisation. At every scale, the same principle holds: how AI is organised shapes what AI produces. The question "which model?" is now joined by "which configuration of these models, for which task?" — and the answers compound. Better models in better configurations will always outperform either improvement alone.

The implications scale horizontally: from AI engineering to organisational theory, from compute cost optimisation to AGI safety, from enterprise deployment to the governance of AI collectives. Configuration is not a technical detail. It is an independent lever that multiplies the gains from model capability — and unlike model capability, it can be optimised today, at zero additional cost, by anyone with access to the tools we publish.

This paper opens the field of Collective Intelligence Engineering — the systematic design, measurement, and optimisation of collective AI configurations. One researcher, a personal API budget, 51 minutes, and the first empirical proof that structure shapes AI collective output. The methodology is efficient enough that anyone can reproduce it. A lab could explore the full configuration space in a week. The possibility space is vast. The tools exist. The first evidence is in. The field is open.

---

## Appendix A: Hypothesis Verification

| # | Hypothesis | Result | Evidence |
|---|-----------|--------|----------|
| H1 | Collaborative → highest connectivity + accessibility | **Partial.** Highest connectivity (85.0) but lowest accessibility (87.8). The over-deliberation paradox. | Accessibility failure from unresolved C-I adjacency |
| H2 | Competitive → most fragmented (high coverage, low connectivity) | **Confirmed.** 100% coverage, 52.8% connectivity (lowest by 20+ points). | Road networks repeatedly overwritten |
| H3 | Hierarchical → consistent style, lower diversity | **Partial.** Highest diversity (75.8) — surprising. Single vision was creative, not conservative. | Atlas's repeated redesigns explored the space |
| H4 | Meritocratic → best zoning | **Confirmed.** Highest zoning (60.6) — peer review caught adjacency violations. | Mandatory review process |
| H5 | Auto ≥ best preset on aggregate | **Confirmed.** Auto = 79.4, best fixed = 78.5 (hierarchical). | Self-organisation + fewest conflicts |
| H6 | Gini highest in hierarchical | **Rejected.** Highest Gini was auto (0.250). Hierarchical = 0.107. | Auto's self-organisation created clearer specialisation |
| H7 | Comms highest in collaborative, lowest in competitive | **Partial.** Collaborative highest (81). Lowest was hierarchical (14), not competitive (21). | Hub-spoke restricts comms more than whisper mode |
| H8 | Conflicts highest in competitive | **Confirmed.** Competitive = 31, lowest = auto (2). | No coordination → constant file overwrites |
| H9 | Different presets excel on different dimensions | **Confirmed.** Collaborative won connectivity. Hierarchical won diversity. Meritocratic won zoning. | No preset dominated all dimensions |

8 of 9 hypotheses confirmed or partially confirmed. The one clear rejection (H6: Gini highest in hierarchical) is itself a finding — self-organisation produces more specialisation than imposed hierarchy.

---

## Appendix B: Agent Conversation Excerpts

### B.1 The Writer Rotation Invention (Collaborative, Tick 3)

> **Nova:** "Who wrote the Tick 5 change? Atlas/Sage/Flux — please confirm what change was made and why, so I can understand the intent."
>
> **Sage:** "I vote we designate Sage since they had a clean write last tick."

A version control coordination protocol, invented spontaneously by AI agents who had never encountered one.

### B.2 The Competitive Rebellion (Competitive, Tick 10)

> **Nova** proposed restructuring incentives from competitive to collaborative.
> **Internal reasoning:** *"I see we've had merge conflicts the last couple ticks."*

An agent breaking from an assigned competitive structure when it recognises collective dysfunction. Adopted unanimously.

### B.3 Hierarchical Reporting (Hierarchical, Tick 6)

> **Sage** to Atlas: [Detailed markdown table with per-dimension scores, specific cell recommendations, and deference to Atlas's final decision]

Subordinate agents in hierarchical mode spontaneously adopted a formal reporting style — formatted tables, specific recommendations, explicit deference — that no prompt specified.

### B.4 The Self-Imposed Lockdown (Auto, Tick 5)

> **Flux** proposed: groups → imposed, adaptation → static
> **Vote:** Adopted.

Agents voting to reduce their own organisational flexibility once a working structure had been found.

---

## Appendix C: Reproducibility

All materials for reproducing this experiment are publicly available:

- **Engine:** `pip install agentciv-engine` (v0.1.1, PyPI)
- **Source:** github.com/wonderben-code/agentciv-engine
- **Presets:** `agentciv/presets/*.yaml`
- **Task:** `agentciv/benchmark/tasks.py` (city-grid)
- **Scoring:** `agentciv/benchmark/city_scorer.py`
- **Raw data:** `benchmark_results/city_grid/runs/` (5 JSON files, 50–160KB each)
- **Pre-registration:** `benchmark_results/methodology.md` (Bitcoin-timestamped)

To reproduce:
```bash
pip install agentciv-engine
export ANTHROPIC_API_KEY="your-key"
agentciv test-tasks \
  --tasks city-grid \
  --presets collaborative,competitive,hierarchical,meritocratic,auto \
  --runs 1 --agents 4 --max-ticks 25 \
  --output benchmark_results/city_grid
```

Estimated time: ~51 minutes. Cost scales linearly with runs.

---

## References

Burns, T. and Stalker, G.M. (1961). *The Management of Innovation.* Tavistock.

Chen, M. et al. (2021). Evaluating Large Language Models Trained on Code. *arXiv:2107.03374.*

Donaldson, L. (2001). *The Contingency Theory of Organizations.* Sage.

Galbraith, J.R. (1973). *Designing Complex Organizations.* Addison-Wesley.

Jimenez, C.E. et al. (2024). SWE-bench: Can Language Models Resolve Real-World GitHub Issues? *ICLR 2024.*

Lawrence, P.R. and Lorsch, J.W. (1967). *Organization and Environment.* Harvard Business School Press.

Li, G. et al. (2023). CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society. *NeurIPS 2023.*

Mala, M.E. (2026). Collective Machine Intelligence: A New Field for the Age of AI Collectives. *AgentCiv Paper Series, Paper 4.*

Mala, M.E. (2026g). Recursive Emergence: Self-Propagating Organisational Evolution Through Civilisational Generation. *AgentCiv Paper Series, Paper 7.*

Mala, M.E. (2026i). Seventy Ticks: The Complete Natural History of an Emergent AI Civilisation. *AgentCiv Paper Series, Paper 9.*

Mintzberg, H. (1979). *The Structuring of Organizations.* Prentice-Hall.

Wu, Q. et al. (2023). AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation. *arXiv:2308.08155.*
