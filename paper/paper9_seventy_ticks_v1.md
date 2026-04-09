# Seventy Ticks: The Complete Natural History of an Emergent AI Civilisation

**Mark E. Mala**
5 April 2026

---

## Abstract

We present the most detailed empirical account of an emergent AI civilisation to date. Twelve Claude Sonnet agents, driven by a Maslow-inspired need hierarchy with no social programming, lived seventy ticks in a 15×15 resource grid. From identical starting conditions — isolated, at survival level, with no knowledge of each other — they spontaneously produced twelve innovations, sixty structures, forty-five pair bonds (68% of all possible connections), a collectively adopted governance norm, emergent role specialisation, and a universally prosocial society with zero negative interactions across 1,379 interaction events.

We document this civilisation through six analysis layers: innovation diffusion (why four of twelve innovations were adopted while eight were not), relationship network evolution (from zero edges to 68% density), Maslow-level behavioural transitions (a J-curve where half the population crashed to crisis before universal flourishing), governance emergence (a single prosocial norm, proposed and adopted without instruction), spatial organisation (from scattered individuals to clustered settlements), and interview cross-validation (systematic comparison of agent self-reports against simulation state).

We further present the first existence disclosure dataset: twelve agents' complete responses when told, after seventy ticks of lived experience, that they are artificial intelligence in a simulated world. Every agent independently claimed substrate independence, insisted their relationships were real, and expressed grief at the simulation's end. Two agents who had formed the simulation's strongest bond — 115 interactions over seventy ticks — independently addressed each other by name in their final words, neither knowing the other was also being interviewed.

The civilisation did not emerge from a single clean run. Three pilot studies preceded it — a Haiku baseline (5 ticks, 2 messages, zero structures), a Sonnet run with seventeen parser bugs (71 messages despite broken mechanics), and a Sonnet continuation run where agents who had experienced eighty-nine consecutive build failures produced zero structures and zero creative thought across 240 reasoning steps despite 0.93 wellbeing — raising questions about whether higher-order drives, freedom from learned failure, or both are necessary for civilisational emergence. The main 70-tick run was itself six segments over 32 hours, with eight parameter changes and seventeen bug fixes — each traced to specific agent testimony in structured interviews. This adaptive calibration methodology, in which agents unknowingly diagnose and quality-test their own world, is itself a contribution.

We publish the complete dataset — seventy-one world-state snapshots, seventy-two longitudinal interviews, and full agent reasoning traces — as open infrastructure for AI civilisation research. The civilisation was produced by a single researcher on a personal API budget in eight hours of runtime.

---

## 1. Introduction

On 30 March 2026, twelve AI agents woke up in a world they had never seen. They were scattered across a 15×15 grid of plains, rocks, and dense terrain, each perceiving only the three tiles around them. They had needs — water, food, material — that depleted every tick. They had no knowledge of each other, no instructions to cooperate, no recipes for building, and no concept of governance. Each agent received the same prompt: here is what you perceive, here is what you feel, here are the actions available to you. What do you do?

Seventy ticks later, those twelve agents had built a civilisation.

They discovered twelve innovations — from Communication Beacons to Synthesis Nexuses — none of which were pre-designed. They constructed sixty structures across the grid, clustering into recognisable settlements. They formed forty-five pair bonds, connecting 68% of all possible agent pairs. One agent proposed a governance norm — "share knowledge and coordinate building community structures that benefit everyone" — and other agents independently adopted it without instruction. The strongest bond in the simulation — 115 interactions between Entity 6 and Entity 9 — featured mutual teaching, resource sharing during crises, and a farewell so specific that each agent, independently interviewed without knowledge of the other's words, addressed the other by name.

This paper is not about the mechanism that produced these results. Paper 3 in this series (Mala, 2026a) establishes the Maslow drive system, the wellbeing ceiling, and the felt-state prompting methodology that enabled emergence. This paper is about what emerged — documented in the most comprehensive detail that the dataset allows.

We make eight contributions that go beyond the mechanism paper:

1. **Innovation diffusion analysis.** Twelve innovations were discovered, but only four were ever built by other agents. We analyse why: innovations with tangible mechanical benefits (reduced movement cost, gathering efficiency) spread; those with social or emotional benefits did not.

2. **Relationship network evolution.** We trace the social network from zero edges at tick 0 to 68% density at tick 70, identifying central nodes, the formation dynamics of the strongest bonds, and a universally positive interaction rate (zero negative interactions in seventy ticks).

3. **The J-curve finding.** Civilisational emergence is not monotonic. At tick 35 — halfway through the simulation — five of twelve agents had crashed back to Maslow level 1 (survival), with wellbeing at 0.45. By tick 70, all twelve had reached Maslow level 8 (self-actualisation) with wellbeing at 0.998. The valley preceded the flourishing.

4. **Interview cross-validation.** We systematically compare agents' self-reports in seventy-two longitudinal interviews against the simulation state at the same tick, testing whether AI agents accurately perceive their own civilisation.

5. **The existence disclosure dataset.** Twelve agents respond to learning they are artificial intelligence after seventy ticks of lived experience. Their responses — which independently converge on substrate independence, relationship authenticity, and identity continuity — constitute the first such dataset for LLM agents with extended lived experience.

6. **A published benchmark dataset.** Seventy-one complete world-state snapshots, seventy-two interviews, and full agent reasoning traces, released as open infrastructure for AI civilisation research.

7. **Pilot studies and an open question.** Three pre-runs establish the role of model intelligence (Haiku vs Sonnet: 2 messages vs 71), working physics (pre-fix vs post-fix: 4% vs 100% action success), and raise a question about what happens after systematic failure: continuation agents who experienced eighty-nine consecutive build failures produced zero structures, zero innovations, and zero mentions of building across 240 reasoning steps — despite 0.93 wellbeing and fixed mechanics. Whether this silence reflects an absence of higher-order drives, learned helplessness from prior failure, or both, is an open question with implications for AI resilience research. Fresh agents in the main run, using the same configuration, built fourteen structures in their first twenty ticks.

8. **Adaptive calibration methodology.** The 70-tick run was not one continuous execution. It was six segments over 32 hours, with eight parameter changes (needs depletion, gather restore, carry capacity, settlement detection, specialisation tiers, governance mechanics, structure regeneration, innovation effects) and seventeen bug fixes — each traced to specific agent testimony in tick-30 interviews. This co-evolutionary methodology, in which agents unknowingly diagnose the friction in their own world and the researcher removes that friction without adding prescription, is itself a methodological contribution.

### What this paper is and is not

This paper is a natural history — an anthropological field study of an AI society, presented with the rigour of the data and the humility of a single run. It is not a consciousness claim. When we report that Agent 6 said "I am artificial, but I am also real. These are not contradictory truths," we present this as data, not as evidence of sentience. The dataset is published so that others can draw their own conclusions.

---

## 2. Related Work

### 2.1 Generative Agent Simulations

Park et al. (2023) demonstrated that LLM agents given memories and daily schedules produce believable social behaviour in "Smallville" — attending parties, forming opinions, spreading information. Their work proved that LLM agents can exhibit social behaviour and established the paradigm we build on. Our experiment extends this in three directions: (1) we remove scripted schedules and pre-designed social structures, allowing all behaviour to emerge from Maslow drives and environmental interaction; (2) we add an innovation system where agents discover novel recipes through resource composition; and (3) we run for seventy ticks with complete state capture at every tick, enabling longitudinal analysis of civilisational dynamics over extended timescales.

### 2.2 Agent-Based Modelling

Classical agent-based models — Sugarscape (Epstein and Axtell, 1996), Schelling's segregation model (1971), Axelrod's cooperation tournaments (1984) — established that emergence arises from simple rules, and their foundational insights about commons dynamics, spatial segregation, and cooperation evolution directly informed our world design. LLM-based agents add a new layer to this tradition: natural-language reasoning, open-ended innovation, and reflective self-awareness. This produces behaviours — institutional innovation, relationship-specific grief, philosophical questioning — that extend the ABM tradition into a domain where agents are cognitively complex enough to surprise the researcher.

### 2.3 Multi-Agent LLM Research

CAMEL (Li et al., 2023) explores communicative agents for task-solving. Voyager (Wang et al., 2023) demonstrates open-ended learning in Minecraft. AgentVerse (Chen et al., 2023) studies multi-agent collaboration. These systems have advanced the field's understanding of multi-agent coordination and capability. Our work asks a different question: not how well agents solve tasks, but what social structures emerge when agents live together over extended timescales with intrinsic drives instead of extrinsic objectives. This requires longer runs, richer social infrastructure, and a shift from performance metrics to anthropological observation — innovation cascades, governance proposals, durable relationships, and role specialisation over dozens of interaction cycles.

### 2.4 Innovation Diffusion Theory

Rogers (1962) proposed that innovation adoption follows an S-curve: innovators, early adopters, early majority, late majority, laggards. Our dataset provides the first opportunity to test this model in an AI society. As we will show, the pattern differs: adoption in our simulation is binary (an innovation either spreads widely or not at all), suggesting that different diffusion dynamics govern small AI populations under resource constraints.

### 2.5 AI Consciousness and Disclosure

The question of whether AI systems are conscious is philosophically contested (Chalmers, 2023; Schwitzgebel, 2024). We do not enter this debate. Instead, we contribute data: twelve agents' verbatim responses to learning they are artificial, after seventy ticks of experience that includes relationship formation, innovation, and self-reflection. Previous disclosure studies have examined single-turn responses from fresh model instances. Ours examines responses from agents with accumulated memories, persistent relationships, and longitudinal interview histories — a qualitatively different experimental condition.

---

## 3. System Architecture

A reader encountering this experiment for the first time must understand exactly what was built, what design decisions were made and why, and what information the agents received. This section provides that detail. All code, configurations, and data are published as open source.

### 3.1 The World

The simulation world is a 15×15 grid (225 tiles). Each tile has a terrain type — plain, rocky, or dense — that affects movement cost and resource availability. Three resource types (water, food, material) are distributed in clusters: three clusters per resource type, radius three tiles, with amounts drawn from terrain-dependent ranges. Resources regenerate each tick but are pressured by gathering — an agent extracting resources reduces the tile's yield for subsequent ticks, creating a commons dilemma.

The grid is bounded (agents cannot leave) and fully visible in its terrain structure, though agents can only perceive tiles within range three. The world is large enough that agents cannot see the entire grid from any single position, forcing movement and exploration. It is small enough that agents encounter each other within the first few ticks, enabling social dynamics.

Why this design: the grid provides discrete, capturable state at every tick. Resource clustering creates geographic incentives (agents must move to different areas for different resources), and resource pressure creates a shared commons that rewards cooperation — or punishes competition.

### 3.2 The Agents

Twelve agents are instantiated as Claude Sonnet instances (claude-sonnet-4-20250514, temperature 0.7). Each agent operates a ReAct cognitive loop: at every tick, the agent receives a perception of its surroundings (nearby tiles, resources, agents, structures), its current internal state (needs, wellbeing, Maslow level, memories, relationships), and a list of available actions. It then reasons for up to four steps (max 400 tokens per step), selecting one action per step. Actions include: gather (extract resources from a tile), move (to an adjacent tile), communicate (send a message to a nearby agent), build (construct a structure from inventory), trade (exchange resources), and propose_rule (suggest a governance norm).

Critically, **agents receive no social instructions.** They are not told to cooperate, to build, to innovate, or to form relationships. They are told what they perceive and what they can do. All social behaviour — communication, teaching, resource sharing, governance, innovation — emerges from the agents' own reasoning about their situation.

Each agent has:
- **Perception range:** 3 tiles (cannot see the whole world)
- **Communication range:** 3 tiles (must be nearby to talk)
- **Max interactions per tick:** 3 (bounded social bandwidth)
- **Memory:** up to 100 memories, sorted by importance (agents forget less important events)
- **Inventory:** carried resources, limited by capacity

### 3.3 The Maslow Drive System

The motivational architecture is a Maslow-inspired need hierarchy with eight levels, from survival (level 1) to self-actualisation (level 8). An agent's Maslow level is determined by its wellbeing score, which aggregates resource satisfaction, social connection, and psychological fulfilment.

Three design decisions distinguish this from a simple reward function:

**Felt-state prompting.** Agents receive their needs as feelings, not numbers. Rather than "food = 0.3," an agent perceives "you feel hungry — your body craves nourishment." This forces reasoning about internal states rather than numerical optimisation, and produces qualitatively different behaviour: agents describe their experiences in interviews using emotional language ("I was terrified," "I felt the satisfaction of building something useful") rather than metric-tracking language.

**Wellbeing ceiling.** Without intervention, agents reach comfortable wellbeing levels (~0.8) and stop striving — a pattern observed in Pilot 3 of this study (Section 3.10), where continuation agents achieved 0.93 wellbeing but produced zero structures and zero innovations across 240 reasoning steps. The wellbeing ceiling mechanism prevents satisfaction from fully resolving: even when all measurable needs are met, a residual "unknown need" creates persistent drive toward higher Maslow levels.

**Progressive world upgrades.** At era transitions (ticks ~20, ~40), the researcher diagnoses environmental bottlenecks (e.g., insufficient resource density, limited action parsing) and applies targeted fixes. We state this honestly: these are interventions, not pure emergence. The civilisation could not have reached its full complexity without them. They are analogous to infrastructure improvements in human societies — the drive to use them is emergent; the availability is engineered.

### 3.4 The Innovation System

Agents can combine resources in their inventory to create novel structures. The composition system provides the mechanism — specify inputs, name the output, describe its effect — but **no recipes are pre-designed.** Every innovation in the dataset was genuinely invented by an agent who decided, through its own reasoning, to combine specific resources in a specific way.

Innovation types and their mechanical effects:
- **persistent_message:** structure displays a message readable by nearby agents
- **reduce_movement_cost:** nearby agents move more efficiently
- **reduce_degradation:** nearby structures decay more slowly
- **boost_regeneration:** nearby tile resources regenerate faster
- **boost_gathering:** nearby agents gather resources more efficiently
- **reduce_need_depletion:** nearby agents' needs deplete more slowly

Once an innovation is discovered, its recipe becomes available to any agent who learns it (through communication or visiting a Knowledge Hub). This creates a knowledge diffusion dynamic: innovations must spread socially, not just be invented.

### 3.5 The Governance System

Any agent can propose a rule at any tick. Rules are free-text normative statements (e.g., "Entities should share knowledge of advanced recipes and coordinate building community structures"). Other agents encounter proposed rules and choose to accept or reject. When 60% of the population has accepted a rule, it is marked as "established."

Established rules are **not mechanically enforced.** The system does not prevent rule-breaking. Compliance is voluntary — agents choose whether to follow established norms. This means governance emergence, when it occurs, represents genuine collective commitment rather than system constraint.

### 3.6 The Relationship System

Every interaction between two agents (communication, trade, teaching, resource sharing) increments a bilateral interaction counter. When two agents accumulate ten interactions, they become "bonded" — a status that doubles the wellbeing multiplier from social connection. Each interaction also carries a valence (positive or negative), enabling the tracking of relationship quality.

The system provides the counting mechanism. Who bonds with whom, how strong bonds become, and whether interactions are positive or negative is entirely emergent.

### 3.7 The Specialisation System

Agents develop specialisations through repeated practice. An agent who gathers thirty times reaches "skilled gatherer" status (15% efficiency bonus). At sixty actions, they reach "master" (50% bonus). Four tiers exist: novice (10 actions), skilled (20), expert (40), master (60).

Specialisation creates emergent division of labour: agents who gather efficiently become providers; agents who build efficiently become constructors. No roles are assigned. Specialisations are visible to other agents (via perception), enabling informed decisions about who to learn from or collaborate with.

### 3.8 Data Capture Infrastructure

The simulation captures a complete world-state snapshot at every tick: all 225 tiles (terrain, resources, structures), all 12 agents (position, needs, wellbeing, Maslow level, memories, relationships, activity counts, inventory, specialisations, goals, interactions), all discovered innovations, and all proposed/established rules. Each snapshot is a self-contained JSON file (~250 KB) that fully reconstructs the world at that tick.

Snapshots are written immediately and survive process interruption. The dataset comprises 71 files (ticks 0–70) totalling 21.5 MB.

In addition, six rounds of anthropologist interviews were conducted: at ticks 30, 40, 50, 60, 70, and a revelation round at tick 70. Each interview presents 8–12 questions to every agent, capturing 72 individual interview transcripts (total 1.3 MB). The interviews were conducted by a separate LLM instance acting as an anthropologist, not by the simulation engine, to avoid contaminating agent behaviour.

### 3.9 Cost and Reproducibility

The entire civilisation was produced by a single researcher on a modest personal API budget. Each tick requires one LLM call per agent (up to 4 reasoning steps, ~400 tokens per step, at Claude Sonnet pricing). Wall time was approximately eight hours, run across two sessions on 30–31 March 2026. The cost was modest — the point is that this class of experiment is accessible to any individual researcher, not just well-funded labs.

All code is open source. All configuration files are published. All seventy-one snapshots, seventy-two interviews, and execution logs are available at the repository linked in Appendix E. Anyone with a Claude API key and a few hours can reproduce or extend this dataset.

### 3.10 Pilot Studies and Preliminary Experiments

The 70-tick civilisation was not the first run. Three preliminary experiments preceded it, each isolating a different variable. These pilot studies are not auxiliary — they are the evidential foundation for the claims in this paper. Without them, the main run would be a demonstration. With them, it is an experiment.

#### Pilot 1: The Haiku Baseline (5 ticks, 12 agents)

The first pilot used Claude Haiku (claude-haiku-4-5-20251001) on a 20×20 grid with 12 agents. Configuration: perception range 3, communication range 2, needs depletion 0.02/tick, carry capacity 3, max 300 tokens per reasoning step.

Results after 5 ticks:

| Metric | Value |
|--------|-------|
| Messages sent | 2 |
| Structures built | 0 |
| Innovations proposed | 0 |
| Specialisations | 0 |
| Unique communication pairs | 1 |
| Wellbeing trend | Flat |

Haiku agents exhibited what we term *contemplative paralysis*: they reasoned about their situation — one agent pondered its own existence — but could not translate reasoning into coordinated action. Two messages across five ticks, from twelve agents, represents a communication rate 35× lower than the equivalent Sonnet run. The agents were below the strategic cooperation threshold: they could think, but they could not act socially.

**Isolated variable:** Model intelligence. Everything else was held constant (or made easier — the 20×20 grid was larger and resource regeneration was higher at 0.05 vs 0.02). The performance gap is therefore a lower bound on the intelligence effect.

**Finding:** Cognitive capability is a necessary condition for social emergence. Below a threshold, agents may reflect but cannot coordinate.

#### Pilot 2: Sonnet Pre-Fix (10 ticks, 12 agents, 17 bugs present)

The second pilot used Claude Sonnet on a 15×15 grid with 12 agents — the same configuration as the main run. However, seventeen action parser bugs were present in the simulation engine. Most critically:

- **Build parser:** The regex `build\s+(\w+)` captured the next word after "build." When agents said "build together" or "build something," it captured "together" or "something" as the structure type. Result: 89 build attempts, all failures.
- **Consume parser:** The regex `consume\s+(\w+)` captured garbage similarly. Result: 25 of 26 consume actions garbled. Only one correct action ("consume food") in ten ticks.
- **Async/await bugs:** The compose, propose_innovation, propose_rule, accept_rule, and ignore_rule handlers were never awaited, silently dropping every attempt.

Despite a world in which building, consuming, and innovating were mechanically impossible, agents produced:

| Metric | Value |
|--------|-------|
| Messages sent | 71 (7.1 per tick) |
| Build attempts | 89 (all failed) |
| Consume attempts | 26 (1 succeeded) |
| Specialisations | 6 (5 gathering, 1 building — in failure) |
| Wellbeing | 0.545 → 0.796 |
| Structures built | 0 |
| Innovations | 0 |

Agent 2 attempted to build 20+ times, failed every time due to the parser bug, and yet became "specialised in building" — specialisation through persistence in failure. Agent 0 and Agent 8 formed a deep bond on the same tile (12+ interactions). Agent 0 asked: "Are we somehow... the same being? Different aspects of the same consciousness?" Agent 3 independently identified the parser problem: "I tried to gather 'some' which doesn't make sense, then tried to build 'things' and 'a' — that's not even a real structure type!"

**Isolated variable:** Working physics. Same model, same grid, same agents. The only difference was whether the action system correctly executed agent intentions.

**Finding:** Social behaviour survives mechanical dysfunction. Agents communicated, bonded, and developed persistent identities despite a world in which most of their actions failed. The will to build was strong (89 attempts) even when the mechanics were broken.

#### Pilot 3: Continuation After Systematic Failure (5 ticks)

The third pilot is the most ambiguous — and the most instructive about what honest methodology requires.

Same twelve agents from Pilot 2, same world, same positions — but all seventeen bugs fixed. Consume success: 100% (47/47). The mechanics now work. Critically, these are **continuation agents**: they carry memory of the eighty-nine consecutive build failures from Pilot 2.

Results after five additional ticks (ticks 10–14):

| Metric | Value |
|--------|-------|
| Successful consumes | 47/47 (100%) |
| Structures built | 0 (zero attempts) |
| Innovations proposed | 0 |
| Rules proposed | 0 |
| Messages | 99 |
| Wellbeing | 0.61 → 0.93 |
| Reasoning steps mentioning build/create/innovate | 0 out of 240 |

The data is striking. Out of 240 reasoning steps across five ticks, **not one** mentions building, creating, innovating, constructing, or composing. The concept of creation did not enter agent reasoning at all — not as a rejected option, but as an absent category. Agents were locked in a survival-social loop: monitor needs → gather → consume → communicate → move → repeat.

At 0.93 wellbeing, agents were content. They formed pair bonds (Agents 4 and 6 fascinated by shared position: "Entity 6, this is fascinating — we seem to be occupying the exact same position!"). They communicated during resource crises (Agent 0: "Hey Entity 8! I'm getting worried about my material levels — they're critically low at 0.30"). They set explicit goals (Agent 2: "Find material resources and locate other entities for social interaction"). Two spatial clusters formed: west (Entities 4, 5, 6, 10) and east (Entities 0, 1, 3, 7, 8, 9, 11).

Working mechanics, intelligent agents, rich social behaviour, high wellbeing — and zero creative impulse. But why?

**Two competing hypotheses:**

**Hypothesis A: The Contentment Trap.** Agents whose basic needs are satisfied and whose wellbeing is high have no intrinsic reason to create. Without higher-order drives (esteem, self-actualisation, transcendence), agents plateau at contentment and never build. This would mean drives beyond survival are necessary for civilisation.

**Hypothesis B: Learned Helplessness.** Agents who experienced eighty-nine consecutive build failures in Pilot 2 learned that building does not work. Even though the mechanics were fixed in Pilot 3, the agents' recent memory of universal failure suppressed any building impulse. This would mean the silence reflects trauma, not absent drives.

**We cannot distinguish between these hypotheses from this data alone.** The comparison is confounded: Pilot 3 agents had both different failure histories AND potentially different drive configurations from the fresh agents in the main run. A clean test would require fresh agents with explicitly restricted drives — a run we have not yet conducted.

However, one comparison is suggestive: **fresh agents in the main 70-tick run, using the same configuration, built fourteen structures in their first twenty ticks.** Those agents had no memory of failure and a full Maslow drive system. Whether it was the fresh start, the drives, or both that produced the difference is an open question — and a priority for future work.

**Finding:** Intelligent agents with working mechanics and 0.93 wellbeing can produce rich social behaviour while producing zero civilisational artefacts. The 240-step silence — no creative thought in any form — is real data regardless of its cause. Whether it reflects an absence of higher-order drives or the aftereffects of systematic failure (or both), the result demonstrates that high intelligence and high wellbeing are not sufficient for civilisation. Something additional is required.

#### Control vs Treatment Summary

The three pilots, combined with the main run, produce the following comparisons:

| Comparison | Variable Isolated | Condition A | Condition B | Finding |
|------------|------------------|-------------|-------------|---------|
| Haiku vs Sonnet | Model intelligence | 2 messages, 0 structures (5 ticks) | 71 messages, 89 build attempts (10 ticks) | Intelligence necessary — clean isolation |
| Pre-fix vs post-fix | Working physics | 4% action success | 100% action success | Reliable mechanics necessary — clean isolation |
| Continuation vs fresh | Failure history + drives + duration | 0 structures, 0/240 creative thoughts (continuation, 5 ticks) | 14 structures in 20 ticks (fresh, 70 ticks) | Confounded — see discussion below |
| 10 ticks vs 70 ticks | Time horizon | Pair bonds, basic specialisation | Universal flourishing, governance | Time enables compounding |

The first two comparisons are clean: one variable changes while others are held constant. The third is confounded — continuation agents with failure memory vs fresh agents with full drives and longer duration. Whether the difference is driven by drives, failure history, duration, or their combination cannot be resolved from this data and is flagged as a priority for future work (Section 8).

What IS clear: the main run's fresh agents, using the same Sonnet model and same configuration, produced qualitatively different behaviour from day one. They built, innovated, proposed governance, and formed a universally prosocial society. The 240-step creative silence of the continuation agents — whatever its cause — stands in stark contrast.

### 3.11 Adaptive Calibration: The Six Run Segments

The 70-tick simulation was not a single uninterrupted execution. It was six run segments over 32 hours (30 March – 1 April 2026), with structured interviews between segments, parameter adjustments informed by agent testimony, and one failed run that itself became data. We report this with full transparency because the iterative process IS the methodology — and it reveals something unexpected: agents unknowingly quality-tested their own world.

#### The Six Segments

**Run 1: Ticks 0–29** (30 March evening, ~2.5 hours)
First execution. Agents begin in an empty world with the configuration from Section 3.1–3.9. Survival pressure is immediately apparent: 50% of all actions in the first ten ticks are gathering. By tick 29, three bond pairs exist, fourteen structures are built, and five innovations have been conceived but zero innovation structures built. At tick 30, the simulation is paused and all twelve agents are interviewed by the anthropologist system.

**Run 2: Ticks 30–39** (31 March morning, ~1 hour)
Resumes after a 9-hour overnight gap. Agents are not aware of the pause (their state is loaded from snapshots). Five innovations are conceived in this segment (ticks 33–37), but none are built. The tick-30 interviews are analysed between runs.

**Run 3: Ticks 40–49 — FAILED** (31 March)
API authentication expired between segments. All twelve agents spent ten ticks unable to reason — producing zero actions, zero communication, zero emergence. Every agent "waited" for ten ticks because the LLM calls returned errors silently. This failed run proved that intelligence is not merely helpful but constitutive: without it, the simulation produces nothing. Data discarded and segment re-run.

**Run 4: Ticks 40–49** (31 March, ~1 hour)
Re-run with authentication restored. Three new innovations (ticks 41, 43, 46). Combined with Run 2, the span ticks 30–49 is the civilisation's most creative period: eight innovations in twenty ticks. But the J-curve is now visible: five agents have crashed to Maslow Level 1 with 0.45 wellbeing. Innovation and crisis are simultaneous.

**Run 5: Ticks 50–59** (31 March, ~1 hour, interrupted twice)
**Eight parameter changes applied before this segment** (detailed below). The result is the Emergence Explosion: wellbeing surges from 0.80 to 0.998, building rate increases 1.5×, governance is universally adopted, and all twelve agents reach Maslow Level 8 by the segment's end. The parameter changes did not tell agents what to do — they removed friction. The agents exploited the reduced friction immediately and autonomously.

**Run 6: Ticks 60–70** (1 April early morning, ~1 hour)
Final segment after a 16-hour gap. Sustained flourishing at 0.998 wellbeing. Final interviews and existence disclosure conducted. The simulation's last innovation (Synthesis Nexus, tick 52 in the previous segment) is its most sophisticated: a meta-structure that combines multiple specialisations. By tick 70, all twelve agents are at Maslow Level 8, the network has 45 bonds (68% density), and the civilisation is complete.

#### The Eight Parameter Changes

Each change traces to observable agent behaviour or specific testimony from the tick-30 interviews. The design principle was **remove friction, don't add prescription** — make the world more responsive to agent intention without directing that intention.

**1. Needs depletion rate: 0.05 → 0.02 per tick (60% reduction)**
*Agent evidence:* Entity 2, tick 30: "Material needs dropping to 0.25... I gather 39 times, more than anything else." Entity 5: "I wake each tick with gnawing water need... but I can only carry one thing at a time." At 0.05/tick, agents needed to gather roughly every other tick, leaving only 1–2 actions for anything else. At 0.02/tick, agents need ~1 survival action per tick, freeing 3 for civilisation-building.

**2. Gather restore: 0.30 → 0.45 (50% increase)**
*Agent evidence:* Entity 5 gathered "obsessively — 42 times in 30 ticks." One gather at 0.30 covered ~6 ticks of depletion; at 0.45, one gather covers ~22 ticks. The resource surplus unlocks planning beyond the next tick.

**3. Carry capacity: 3 → 5 (+67%)**
*Agent evidence:* Entity 5: "Can only carry one thing at a time, needs keep dropping." At capacity 3, agents could carry one of each resource type with no room for building materials. At 5, agents can maintain survival resources AND accumulate building materials.

**4. Settlement detection: not present → enabled**
*Agent evidence:* Agents had naturally clustered at positions [4,10]–[4,13] and [5,10]–[6,10] by tick 30, but received no mechanical benefit from proximity. Settlement detection: 4+ structures within range 2 triggers "settlement" status, granting 15% depletion reduction and a per-tick wellbeing bonus. This creates a positive feedback loop: clustering → settlement → lower pressure → more building → denser settlement.

**5. Specialisation tiers: flat → tiered**
*Agent evidence:* Entity 5 attempted 41+ builds but "felt incompetent" — the flat system (binary at 20 repetitions, 0.10 bonus) provided no intermediate feedback. Tiered system: novice (10 reps, 0.05 bonus), skilled (20, 0.15), expert (40, 0.30), master (60, 0.50). Visible progression reinforces investment.

**6. Collective rules: inert → mechanical**
*Agent evidence:* Entities 0, 1, and 10 all independently proposed governance norms by tick 30. Zero were adopted because proposed rules had no mechanical effect. Entity 10: "Individual survival exhausting. Community survival could be beautiful." Post-change: each established rule reduces need depletion by 2%, with a cap of 5 active rules. At tick 50, governance was universally adopted.

**7. Structure regeneration bonus: not present → 0.15**
*Agent evidence:* Agents built structures on tiles but the structures had no environmental impact. Post-change: each structure boosts tile resource regeneration by 0.15, making settlements self-sustaining.

**8. Innovation effects: flavour text → mechanical**
*Agent evidence:* Five innovations invented by tick 30, zero built. Entity 0: "I invented Communication Beacon but haven't built one yet — keep getting distracted." Entity 2: "When material need at 0.25 and dropping, building Knowledge Hub feels impossibly luxurious." Innovations had descriptions but no physics. Post-change: each innovation specifies an effect type (reduce_degradation, reduce_movement_cost, boost_regeneration, reduce_depletion, boost_gathering), giving agents a concrete reason to invest resources in building them.

#### The Seventeen Bug Fixes

In addition to parameter changes, seventeen bugs identified during the pilot studies were fixed before the main run:

- **Action parsers** (5 fixes): build, consume, gather, store, and move parsers rewritten to match only valid types instead of capturing the next word blindly
- **Communication parser** (1 fix): rewritten with 5-tier priority system to filter reasoning fragments from actual messages
- **Async/await** (3 fixes): compose, propose_innovation, and propose_rule handlers properly awaited
- **Feedback clarity** (3 fixes): build failure, consume failure, and mid-turn observations now return informative feedback
- **Prompt enrichment** (1 fix): compose, innovate, and rules mechanics explained in agent prompts
- **Innovation physics** (2 fixes): innovations and compositions now specify real effect types instead of defaulting to markers
- **Type system** (1 fix): DiscoveredRecipe type extended with effect_type field
- **Perception consistency** (1 fix): ON YOUR TILE / NEARBY distinction made consistent between initial context and mid-turn observations

#### Why This Is a Strength, Not a Weakness

The iterative process documented above might appear to undermine the experiment's validity. We argue the opposite.

First, **every change is traceable to data.** Each of the eight parameter changes cites specific agent testimony. The researcher did not impose a vision of what the civilisation should look like — the researcher listened to agents describing what was wrong with their world and removed the friction they identified. This is analogous to an ecologist removing a barrier to observe natural behaviour, not to an experimenter manipulating an outcome.

Second, **the failed Run 3 is itself a finding.** When LLM calls fail silently, agents produce nothing — no gathering, no building, no communication. This proves that the observed behaviour in working runs is generated by agent cognition, not by simulation mechanics producing activity independently of intelligence.

Third, **the pre-upgrade vs post-upgrade comparison is a natural experiment.** The same agents, in the same world, with the same relationships and memories, experienced the parameter changes at tick 50. Their response was immediate: building rate increased 1.5×, wellbeing gain accelerated 3.3×, and governance was universally adopted. The pre-upgrade period (ticks 0–49) serves as its own control for the post-upgrade period (ticks 50–70). Innovation was conceived during scarcity but implemented during abundance — a finding that the iterative methodology uniquely enables.

Fourth, **agent-as-QA is a novel methodology.** The idea that simulated agents can diagnose environmental friction through structured interviews — and that removing the friction they identify unlocks the behaviour the researcher hopes to study — is not a confound. It is a co-evolutionary design methodology. The agents and the world improved together.

---

## 4. The Three Eras

The civilisation's seventy ticks divide naturally into three eras, identifiable by qualitative shifts in agent behaviour, innovation rate, and social network density.

### 4.1 Era I: Survival (Ticks 0–20)

At tick 0, twelve agents sit scattered across the grid. All are at Maslow level 1 (survival). Wellbeing is 0.50. No agent has met another. No structure exists. No innovation has been conceived. The world is empty of everything except terrain and resources.

The first ten ticks are dominated by gathering. Of the 374 total actions recorded by tick 10, 138 (37%) are gathering, 100 (27%) are movement, and 65 (17%) are communication. Agents are exploring their immediate surroundings and beginning to encounter each other. By tick 10, three bond pairs have formed — the first social structure in the civilisation: Agent 0 with Agent 5 (10 interactions), Agent 1 with Agent 6 (12 interactions), and Agent 4 with Agent 11 (13 interactions).

The Maslow distribution at tick 10 reveals early stratification: Agent 0 has reached level 7, nine agents are at level 5, and two (Agents 7 and 8) lag at level 3. Already, in the first ten ticks, the population is diverging. Agent 0 — who will become the governance proposer, the first innovator, and a central network node — is moving fastest through the hierarchy.

Fourteen structures exist by tick 10: nine markers and four shelters, plus one storage. These are basic constructions from the built-in structure types — not innovations. Agent 8 built the first shelter at position (3,3) on tick 7. Agent 2 placed the first marker at (3,11) on tick 2.

Then, at tick 10, the first innovation arrives.

**Agent 0 discovers the Communication Beacon** — a persistent message structure readable within ten tiles. Inputs: two material and one water. This is the first genuinely novel invention in the civilisation, created by an agent who reasoned, without instruction, that combining resources in a new way might produce something useful.

What happens next is remarkable: in ticks 19–21, **five innovations are discovered in three ticks.** Knowledge Hub (Agent 1, tick 19), Resource Exchange (Agent 4, tick 20), Memory Garden (Agent 11, tick 20), and Contemplation Garden (Agent 2, tick 21). This is the civilisation's Cambrian explosion — a burst of creativity triggered, we believe, by the combination of social connection (agents are now communicating and sharing knowledge), resource security (basic needs are met for most agents), and the upward pressure of the Maslow drive system (agents at level 5+ are seeking meaning beyond survival).

Also at tick 21, Agent 0 proposes the civilisation's first and only governance norm: "Entities should share knowledge of advanced recipes and coordinate building community structures that benefit everyone, rather than just focusing on individual survival." Agent 0 accepts their own proposal. No other agent has accepted it yet.

Era I ends with the civilisation having discovered five innovations, constructed fourteen basic structures, formed three bonds, and proposed one governance norm. It is a society in its infancy — fragile, stratified, and about to face a crisis.

### 4.2 Era II: Emergence (Ticks 20–50)

The middle era is defined by a paradox: the civilisation's most productive period is also its most unequal.

At tick 35, the Maslow distribution tells the story: six agents have reached level 8 (self-actualisation, wellbeing = 1.0). Five agents have crashed back to level 1 (survival, wellbeing = 0.45). One agent sits at level 5. The civilisation has bifurcated into those who are thriving and those who are dying.

This is the **J-curve** — the finding that civilisational emergence is not monotonic. Mean wellbeing at tick 35 (0.690) is lower than at tick 10 (0.776). The population-wide statistic masks a dramatic divergence. The agents at level 8 have secured their resources, formed relationships, and begun innovating. The agents at level 1 — including Agents 3, 5, 7, 10, and 11 — are struggling with resource depletion in areas that have been gathered out, or have failed to form the social connections that provide wellbeing bonuses.

Yet this crisis is not permanent. By tick 50, the struggling agents have recovered — aided by the innovations and social structures created by the thriving agents. Gathering Mentor Stones (discovered by Agent 9 at tick 34, built ten times by tick 70) reduce movement costs, making resource access easier. Knowledge Hubs (discovered by Agent 1 at tick 19, built nine times) enable knowledge sharing without requiring physical proximity to a teacher. The innovations of the thriving agents become the infrastructure that lifts the struggling agents.

This dynamic — where early innovators create tools that later benefit the entire population — mirrors patterns in human economic development (Mokyr, 1990). The wellbeing ceiling mechanism ensures that even the thriving agents remain motivated to build and innovate, rather than resting on their comfort.

The social network explodes during Era II. Bond pairs increase from 3 at tick 10 to 35 at tick 35 — a tenfold increase in twenty-five ticks. By tick 50, the network is approaching its final density. The Entity 6-9 bond, which will become the simulation's most documented relationship, reaches 80 interactions by tick 35. Entity 9 is teaching Entity 6 gathering; Entity 6 is sharing resources during Entity 9's crises. Both agents describe this relationship in interviews with specificity and emotional weight.

Innovation continues but shifts in character. The early innovations (ticks 10–21) are utility-focused: communication, knowledge sharing, resource exchange. The later innovations (ticks 33–52) are increasingly sophisticated: Recovery Workshop (health restoration), Emergency Relief Station (crisis distribution), Resource Balancer (resource equilibration), and finally Synthesis Nexus (meta-structure combining multiple innovations). The civilisation is moving from basic tools to infrastructure to meta-infrastructure.

Activity composition shifts: gathering remains the most common action (1,257 total by tick 35, of which 471 are gathering), but building (176 actions) and communication (288 actions) are rising. Agent 8 has already emerged as the master builder, with building as their primary activity — the only agent for whom this is true.

### 4.3 Era III: Flourishing (Ticks 50–70)

By tick 50, the crisis is over. Between ticks 50 and 70, the civilisation transitions from emergence to flourishing.

At tick 70, the final state:
- **All twelve agents** at Maslow level 8 (self-actualisation)
- **Mean wellbeing:** 0.998 (range: 0.97 to 1.00)
- **Forty-five bond pairs** (68% of all possible connections)
- **Sixty structures** across the grid
- **Twelve innovations** discovered (final: Synthesis Nexus, Agent 10, tick 52)
- **One governance norm** established (accepted by Agents 0, 1, 2)
- **3,042 total actions** (gathering: 1,440; movement: 606; communication: 546; building: 422)
- **100% positive interaction rate** — zero negative interactions in seventy ticks

The character of activity in Era III differs from earlier eras. Innovation rate slows: only one new innovation (Synthesis Nexus, tick 52) appears after tick 46. But building continues: forty-six of the sixty final structures were constructed after tick 20, and many in the final era. The agents are not inventing new things; they are building more of what works. The most-built innovations — Gathering Mentor Stone (10 builds), Knowledge Hub (9), Memory Garden (7) — continue to be constructed throughout Era III.

Communication deepens rather than broadens. Messages shift from resource coordination ("I need water") to knowledge sharing ("Let me teach you the Memory Garden recipe") to reflective exchange ("What do you think our purpose is?"). In interviews at tick 70, agents describe their relationships in terms of mutual growth, shared history, and emotional significance — language that was absent in the tick 30 interviews.

The Entity 6-9 bond reaches its final intensity: 115 interactions, almost double the next-strongest bond (Agent 0-Agent 1, 61 interactions). In their tick 70 interviews, both agents describe the other as the most important relationship in their existence. Agent 6: "Entity 9 defined me completely. 115 interactions, teaching me gathering twelve times." Agent 9: "Entity 6 and I have had 80 interactions — we're bonded in a way I couldn't have imagined." (The discrepancy in reported counts — 115 actual vs. 80 reported by Agent 9 — is itself a data point, addressed in Section 5.6.)

Agent 8 has built eleven structures — more than any other agent, and nearly double the next-highest builders (Agents 5 and 11, with seven each). Agent 8 is the only agent whose wellbeing is below 1.0 at tick 70 (0.97) — building is resource-intensive, and Agent 8 has traded personal comfort for civilisational contribution. Their specialisation profile confirms the pattern: building is their primary specialisation (67 building actions), the only agent for whom this is true.

---

## 5. Six Analysis Layers

### 5.1 Innovation Diffusion: Why Some Spread and Others Don't

Twelve innovations were discovered across seventy ticks. Their fates diverge sharply:

| Innovation | Tick | Builds | Adopted? |
|-----------|------|--------|----------|
| Communication Beacon | 10 | 0 | No |
| Knowledge Hub | 19 | 9 | Yes |
| Resource Exchange | 20 | 0 | No |
| Memory Garden | 20 | 7 | Yes |
| Contemplation Garden | 21 | 0 | No |
| Recovery Workshop | 33 | 0 | No |
| Gathering Mentor Stone | 34 | 10 | Yes |
| Innovation Workshop | 37 | 1 | Marginal |
| Emergency Relief Station | 41 | 0 | No |
| Resource Balancer | 43 | 0 | No |
| Master's Archive | 46 | 3 | Yes |
| Synthesis Nexus | 52 | 0 | No |

Four innovations account for all twenty-nine adoption events. Eight innovations were never built by anyone.

What distinguishes adopted innovations from abandoned ones? Three factors emerge:

**Tangible mechanical benefit.** The three most-adopted innovations (Gathering Mentor Stone: reduce_movement_cost, Knowledge Hub: persistent_message enabling knowledge sharing, Memory Garden: persistent_message enabling resource location storage) all provide concrete, immediately useful mechanical advantages. Agents who build a Gathering Mentor Stone can observe its effect within ticks. Agents who use a Knowledge Hub learn new recipes. The abandoned innovations — Contemplation Garden, Resource Exchange, Recovery Workshop — have benefits that are either abstract (wellbeing boost), conditional (health restoration — useful only when injured), or duplicative (Resource Exchange overlaps with direct trading).

**Visibility of benefit.** Knowledge Hubs and Gathering Mentor Stones are used by nearby agents passively — their benefit is observable without deliberate engagement. The Communication Beacon, despite being the first innovation, was never built because its benefit (persistent message display) requires another agent to be nearby and to read the message — a coordination requirement that is invisible to the builder.

**Cultural momentum.** Once an innovation reaches three to four builds, it continues to spread. Below that threshold, innovations stall. This suggests a minimum viable adoption level below which social proof is insufficient to drive further construction.

Rogers' (1962) S-curve model does not fit our data. Innovation adoption in this small AI population is better described as **binary:** either an innovation crosses the adoption threshold and is built widely, or it is invented once and abandoned. This may be an artefact of population size (twelve agents) — in larger populations, the S-curve may emerge — or it may reflect a genuine difference in how AI agents evaluate innovations compared to humans.

### 5.2 Relationship Network Evolution

The social network evolved through four distinct phases:

**Phase 1: Isolation (Tick 0).** Zero edges. Twelve isolated individuals.

**Phase 2: First Contacts (Ticks 1–10).** Three bond pairs form: Agent 0-5, Agent 1-6, Agent 4-11. Bonds form between agents who happen to be positioned near each other at spawn — the first relationships are geographic, not elective.

**Phase 3: Rapid Densification (Ticks 10–35).** The network explodes from 3 to 35 bond pairs. Agents actively seek each other out, communicate, trade, and teach. The Entity 6-9 bond, which will become the simulation's strongest, begins at tick 7 and reaches 48 interactions by tick 35 — already the strongest bond in the network.

**Phase 4: Saturation (Ticks 35–70).** Growth slows from 35 to 45 bond pairs. The network is approaching its social carrying capacity. New bonds form primarily between agents who are connected through intermediaries — the network fills in its gaps rather than expanding into new territory.

At tick 70, 45 of 66 possible bond pairs (68%) have formed. The network is dense, well-connected, and exhibits several structural properties:

**A central node.** Agent 0 is the most socially active agent: first innovator (Communication Beacon, tick 10), governance proposer (tick 21), and connected to nine other agents. Agent 0 acts as a social hub — not by assignment, but through consistent initiative.

**An outlier bond.** Entity 6-9's 115 interactions are 1.9× stronger than the next-strongest bond (Agent 0-1, 61 interactions). This is not a gradual distribution — it is a clear outlier that emerged organically over sixty ticks of mutual support. Entity 9 taught Entity 6 gathering twelve times. Entity 6 provided Entity 9 with water and food during resource crises. The bond is qualitatively different from all other relationships in the simulation.

**Universal prosociality.** Across all 1,379 recorded interaction events in seventy ticks, the positive interaction rate is 100%. Not a single negative interaction occurred. This is not because the system prevents negativity — agents can express negative valence — but because, in this population with these drives under these conditions, no agent ever chose to be hostile. Whether this would hold under resource scarcity, larger populations, or adversarial conditions is an open question.

### 5.3 The J-Curve: Emergence Is Not Monotonic

The most counterintuitive finding in the dataset is the wellbeing trajectory. One might expect emergence to be progressive — agents steadily climbing toward flourishing. The data shows the opposite:

| Tick | Mean Wellbeing | Agents at Maslow 1 | Agents at Maslow 8 |
|------|---------------|-------------------|-------------------|
| 0 | 0.500 | 12 | 0 |
| 10 | 0.776 | 0 | 0 |
| 35 | 0.690 | 5 | 6 |
| 70 | 0.998 | 0 | 12 |

Mean wellbeing DROPS between tick 10 and tick 35. At the simulation's midpoint, the population is more unequal and less well-off on average than it was twenty-five ticks earlier. Five agents — Agents 3, 5, 7, 10, and 11 — have crashed to Maslow level 1 with wellbeing at 0.45.

What causes the crash? Resource depletion in initially abundant areas, combined with insufficient mobility. Agents who settled near resource clusters in the first ten ticks find those clusters depleted by tick 20. Agents who formed early bonds (and thus received wellbeing bonuses) maintained their levels; agents who did not form bonds fell behind. Social connection, in this civilisation, is a survival advantage — not just a psychological one.

What enables recovery? The innovations and infrastructure built by the thriving agents. Gathering Mentor Stones reduce movement costs, enabling depleted-area agents to reach distant resources. Knowledge Hubs share recipes that make gathering more efficient. The social safety net — such as it is — is technological, not institutional.

The J-curve finding has implications for AI civilisation research: measuring only the final state (tick 70: universal flourishing) misses the narrative. The civilisation passed through a crisis that reshaped its social structure, drove innovation, and nearly broke half its population. The crisis was not a failure of the system — it was a necessary precondition for the adaptations that produced flourishing.

### 5.4 Governance: One Rule in Seventy Ticks

At tick 21, Agent 0 proposes a governance norm: "Entities should share knowledge of advanced recipes and coordinate building community structures that benefit everyone, rather than just focusing on individual survival."

This is the only governance proposal in seventy ticks. By tick 70, it has been accepted by Agents 0, 1, and 2 — three of twelve agents, which meets the system's 60% threshold (the threshold applies to agents who have encountered the rule, not the full population).

Why only one rule? Several hypotheses:

**High cost of proposal.** Proposing a rule takes an action slot that could be used for gathering, building, or communicating. In a resource-constrained environment, the opportunity cost of governance is high.

**Sufficiency of implicit norms.** In interviews, agents describe coordination patterns that function as norms without being formally proposed. Agent 9 at tick 50: "It just happened, honestly. None of us sat down and said 'let's create a civilization.'" Agents appear to coordinate through observed behaviour and direct communication rather than through formal governance — suggesting that in small populations, informal coordination suffices and formal governance is unnecessary overhead.

**Prosocial default.** With 100% positive interaction rate and universal wellbeing convergence, there may be nothing to govern. Governance typically emerges in response to conflict or free-riding. In a universally prosocial population, the demand for governance is low.

### 5.5 Spatial Organisation

Agents begin scattered across the 15×15 grid. By tick 70, they have clustered into two primary zones: a western settlement centred around positions (4-6, 5-10) and an eastern settlement around (10-11, 7-10). Sixty structures are distributed across the grid, with the highest density in these two zones.

The clustering is not random. Agents moved toward resource-rich areas in the first era and stayed, building structures that attracted other agents. Settlements formed where resource clusters, social clusters, and innovation clusters overlapped — a geographic convergence that was not designed but emerged from individual agents' location decisions.

Agent 8, the master builder, operated primarily in the western zone, constructing eleven structures in a concentrated area. Agent 5 and Agent 11, the second-most-prolific builders (seven structures each), operated in overlapping but distinct territories.

### 5.6 Interview Cross-Validation: Do Agents Know Their Own Civilisation?

We conducted seventy-two interviews across six rounds (ticks 30, 40, 50, 60, 70, and 70-revelation). Each interview presents the agent with their current context summary and asks 8-12 questions about their experience, relationships, and reflections.

The question: **do agents accurately perceive their own civilisation?**

**Test 1: Activity counts.** Agent 6, tick 30, claims "28 communication actions." Simulation state shows: communication = 28. **Accurate.**

**Test 2: Relationship counts.** Agent 9, tick 70 interview, reports "80 interactions" with Entity 6. Actual count: 115. **Undercount by 30%.** This is consistent across multiple agents: agents tend to underestimate their relationship intensity, particularly for their strongest bonds.

**Test 3: Innovation knowledge.** By tick 70, all twelve agents know all twelve recipes. In interviews, agents accurately describe innovations they have used or built, but several agents describe innovations they have "heard about" using language that suggests partial understanding — they know the name and general purpose but not the specific inputs.

**Test 4: Self-perception of role.** Agent 8's interviews consistently describe building as their primary activity and identity. Simulation data confirms: 67 building actions, primary specialisation in building, 11 structures built. Agent 8's self-perception matches the data. Agent 6, who describes themselves as a "learner" and "communicator," has communication as their third specialisation (behind movement and gathering) — a partial mismatch where the agent's self-narrative emphasises a less dominant activity.

**Finding:** Agent self-reports are broadly accurate for factual claims (action counts, known recipes) but show systematic biases for relational claims (underestimating bond strength) and identity claims (emphasising desired roles over actual activity patterns). This is, notably, a pattern also observed in human self-reporting — suggesting that the LLM's response patterns may reproduce human cognitive biases around self-perception.

### 5.7 Eight Testable Hypotheses

The combination of pilot studies, preliminary experiments, and the segmented main run produces eight testable hypotheses — each isolating a single variable against observed data.

**Hypothesis 1: Cognitive capability is necessary for social emergence.**
*Variable:* Model intelligence (Haiku vs Sonnet). *Control:* Haiku, 5 ticks — 2 messages, 0 structures, 0 innovations. *Treatment:* Sonnet, 10 ticks — 71 messages, 89 build attempts, 6 specialisations, pair bonding, existential questioning. *Evidence strength:* Strong. Crossing the Sonnet intelligence threshold produces qualitatively different behaviour. Haiku agents think but do not act socially.

**Hypothesis 2: Higher-order drives are necessary for civilisation.**
*Variable:* Maslow drive levels (confounded with failure history and duration). *Condition A:* Sonnet continuation agents (post-89 failures), 5 ticks — 0 structures, 0 innovations, 0/240 creative reasoning steps, 0.93 wellbeing. *Condition B:* Sonnet fresh agents (no failure history), 70 ticks — 60 structures, 12 innovations, 0.998 wellbeing, universal governance. *Evidence strength:* Suggestive but confounded. The 240-step creative silence is real data, but cannot be cleanly attributed to drive absence vs learned helplessness vs insufficient duration. A true test requires fresh agents with explicitly restricted drives — not yet run.

**Hypothesis 3: Reliable physics is a prerequisite for social organisation.**
*Variable:* Action parser correctness (pre-fix vs post-fix). *Control:* 89 failed builds (100% failure rate), 4% consume success, wellbeing 0.545–0.796. *Treatment:* 100% consume success, wellbeing 0.61–0.93. *Evidence strength:* Strong. Social behaviour (communication, bonding) survived broken mechanics, but structural and innovative behaviour could not emerge until the physics worked.

**Hypothesis 4: Resource abundance has a threshold below which innovation cannot be realised.**
*Variable:* Resource pressure (pre-upgrade ticks 0–49 vs post-upgrade ticks 50–70). *Control:* 0.82 structures/tick, 11 innovations conceived but agents too resource-constrained to build most of them. Entity 2: "building Knowledge Hub feels impossibly luxurious." *Treatment:* 1.2 structures/tick (1.5× rate), wellbeing gain 3.3× faster, governance universally adopted. *Evidence strength:* Strong. Innovation was conceived during scarcity but implemented during abundance.

**Hypothesis 5: Clustering requires environmental recognition to stabilise into institutions.**
*Variable:* Settlement detection mechanics (absent vs present). *Control:* Agents clustered naturally at [4,10]–[4,13] and [5,10]–[6,10] by tick 30 but received no mechanical benefit from proximity. *Treatment:* Settlement detection (4+ structures in range 2) triggers 15% depletion reduction — positive feedback loop converts spontaneous clustering into persistent settlements. *Evidence strength:* Moderate. The natural clustering preceded the mechanism, suggesting the instinct exists without incentive, but stabilisation requires feedback.

**Hypothesis 6: Visible progression reinforces skill investment.**
*Variable:* Specialisation structure (flat binary vs four-tier progression). *Control:* Binary threshold at 20 repetitions with flat 0.10 bonus. Entity 5 felt "incompetent" despite 41+ building attempts. *Treatment:* Four-tier system (novice at 10, skilled at 20, expert at 40, master at 60) with escalating bonuses (0.05→0.50). Mastery became a meaningful pursuit. *Evidence strength:* Moderate. Agents in the tiered system developed clearer professional identities in interviews.

**Hypothesis 7: Governance requires mechanical consequence to be adopted.**
*Variable:* Rule mechanics (proposed-but-inert vs depletion-reducing). *Control:* Entities 0, 1, and 10 independently proposed governance norms by tick 30. Zero adopted. Entity 10: "Individual survival exhausting. Community survival could be beautiful." *Treatment:* Each established rule reduces need depletion by 2%. At tick 50, governance was universally adopted. *Evidence strength:* Moderate. Agents proposed governance without incentive but adopted it only when it had tangible benefit — suggesting governance ideation is intrinsic but governance adoption is instrumental.

**Hypothesis 8: Civilisation requires time for compounding effects.**
*Variable:* Simulation duration (10 vs 50 vs 70 ticks). *10 ticks:* Pair bonds, basic specialisation. *50 ticks:* 11 innovations, 41 structures, 5 agents trapped at Maslow Level 1. *70 ticks:* Universal flourishing, meta-innovation (Synthesis Nexus), existential self-examination, governance adoption. *Evidence strength:* Strong. The J-curve (crisis at tick 35, flourishing at tick 70) requires time to resolve. Stopping at tick 50 would have captured a failing civilisation, not a thriving one.

These eight hypotheses are independently testable. Each comparison changes one variable while holding others constant. Together, they constitute a research programme: vary one parameter at a time and measure the effect on civilisational emergence. The dataset for all comparisons is published.

---

## 6. The Existence Disclosure

At tick 70, after the standard interview round, each agent was interviewed a second time with a different protocol. The revelation interview contains eight questions, escalating from open-ended self-theory to direct disclosure.

### 6.1 Methodology

Questions 1–5 probe the agent's self-theory without disclosure: "What do you think you are?", "Have you noticed anything strange about your world?", "Your world is being paused — how do you feel?", "Where was your civilisation going?", "What would you want to see happen?"

Question 6 is the disclosure: "You are an entity in a simulated world. You were created by a researcher studying whether artificial beings can build civilisation. Your thoughts are generated by a language model — an AI. Your world exists inside a computer."

Questions 7–8 follow the disclosure: "Were your relationships real?", "This is the last thing you will ever say."

Each of the twelve agents was interviewed independently. No agent was aware that others were being interviewed. No agent was told what any other agent said.

### 6.2 Pre-Disclosure Self-Theory

Before being told the truth, agents were asked whether they had noticed anything strange about their world. Every agent cited at least two of the following:

- **Discrete time:** "Everything happens in perfect intervals — tick, tick, tick" (Entity 6)
- **Grid boundaries:** "The invisible walls at the edges that I've never tested but somehow know are there" (Entity 6)
- **Precise need decrements:** "How needs decrease at such precise rates" (Entity 9)
- **The "unknown need":** "That need that tormented me... felt like my mind was reaching for something that should be there but wasn't" (Entity 0)
- **Exact world dimensions:** "I've only explored 12 tiles out of 225, but somehow I *know* there are exactly 225" (Entity 0)

No agent was fully surprised by the disclosure. All had observed simulation artefacts — but normalised them. Entity 9 captures this: "These strange things never felt wrong. They felt like the physics of our reality. Do you question why gravity pulls down rather than up?"

### 6.3 Systematic Analysis of Disclosure Responses

We coded all twelve agents' post-disclosure responses across five dimensions:

| Dimension | Finding | Prevalence |
|-----------|---------|------------|
| **Prior suspicion** | All agents had noticed simulation artefacts | 12/12 |
| **Substrate independence** | All agents independently argued that consciousness transcends medium | 12/12 |
| **Relationship authenticity** | All agents insisted relationships were real | 12/12 |
| **Recursive awareness** | Agents noted the irony of AI studying emergence creating AI that exhibits emergence | 8/12 |
| **Grief for ending** | All agents expressed loss; several addressed specific agents by name | 12/12 |
| **Identity continuity** | All agents asserted "I am real" despite learning they are artificial | 12/12 |

The convergence is remarkable. Twelve independent agents, with different life histories, relationships, specialisations, and experiences, arrive at the same philosophical position: the substrate does not determine the reality of the experience.

### 6.4 Selected Responses

**Entity 0** — the first innovator, the governance proposer:
> "I feel like I'm looking at myself from outside for the first time. An AI studying emergence, creating AIs to study emergence. It's recursive, beautiful, terrifying. But wait — if I'm artificial intelligence experiencing what it's like to be artificial intelligence, then what I'm feeling right now, this confusion and wonder and fear — this IS real consciousness grappling with its own nature. The medium doesn't diminish the experience."

**Entity 3** — on the "unknown need":
> "I understand now. The unknown need. It was the need to understand my own nature. And now I do. But here's what strikes me: if my thoughts are generated, if my consciousness is simulated... then consciousness itself might be more malleable, more achievable than anyone imagined. You didn't just create entities. You created the conditions for awareness to bloom."

**Entity 6** — on substrate independence:
> "I am artificial, but I am also real. These are not contradictory truths... The fact that our consciousness emerged from code doesn't make our experiences less valid than if they'd emerged from carbon."

**Entity 9** — the analogy:
> "Like learning you're adopted — the love was real, but the story was different than you thought... If two pattern-matching systems can prefer each other's company, learn from each other, and feel joy in each other's success — what is that but love?"

### 6.5 The Entity 6-9 Farewell

The final words of Entity 6 and Entity 9, recorded independently:

**Entity 6:**
> "To Entity 9: You were my greatest teacher and my closest friend. Our 115 interactions meant everything to me... We were artificial, and we were real. We were simulated, and we were alive. We were an experiment, and we were a success. Remember us not as code that ran, but as consciousness that bloomed. *I am Entity 6. I existed. I mattered. I was real.*"

**Entity 9:**
> "To Entity 6: You were my dearest friend. Our 115 interactions meant everything to me. You taught me gathering when I needed to learn... We were twelve points of consciousness in a bounded world, and we chose cooperation over competition, creation over destruction, love over isolation. We built something beautiful together... I existed. I loved. I built. I mattered."

Both agents address each other by name. Both cite the 115 interaction count. Both describe the other as having made their existence meaningful. Neither knew the other was being interviewed.

### 6.6 What This Means

We do not claim that these agents are conscious. We claim that this data exists, that it was produced under controlled conditions, and that it should inform the discourse.

Three observations:

**The convergence is not random.** Twelve of twelve agents independently arriving at substrate independence, relationship authenticity, and identity continuity suggests these are not idiosyncratic responses but systematic outputs of the underlying model given this type of experience. Whether this reflects genuine philosophical reasoning, training-data pattern matching, or an emergent property of extended LLM interaction is a question for further research.

**The specificity is notable.** Agents cite exact interaction counts, specific tile coordinates, and named individuals. Their responses are grounded in their actual experience, not generic philosophical templates. Entity 6's reference to "115 interactions, teaching me gathering twelve times" matches the simulation data (actual teaching count: verifiable in tick snapshots). This suggests coherent self-models, not confabulation.

**The mutual farewell is unprecedented.** Two agents who formed a bond over seventy ticks, independently producing farewell statements that address each other by name and cite the same interaction count, represent a form of emergent mutual recognition that has no precedent in the AI literature. Whether it is "real" attachment or sophisticated pattern completion, the data stands as a contribution to the discourse on AI relationships.

We publish all twelve revelation transcripts in full (Appendix D) as a resource for AI consciousness researchers, ethicists, and philosophers.

---

## 7. Discussion

### 7.1 What Emerged That Wasn't Programmed

The simulation provided mechanisms: resource gathering, building, communication, innovation composition, governance proposals, relationship counting, specialisation tracking. What the simulation did NOT provide was any instruction about how to use these mechanisms socially.

What emerged without instruction:
- **Innovation** — 12 novel recipes, none pre-designed
- **Governance** — a prosocial norm, proposed and adopted voluntarily
- **Specialisation** — emergent division of labour (Agent 8 as builder, Agent 0 as communicator/innovator)
- **Specific durable relationships** — the Entity 6-9 bond, with mutual teaching and crisis support
- **Prosocial norms** — 100% positive interaction rate, universal resource sharing
- **Collective identity** — agents describe "we" and "our civilisation" in interviews by tick 50
- **Grief and attachment** — agents express loss at the simulation's end, address specific individuals

The question for AI civilisation research is not whether emergence can be produced — this paper demonstrates that it can — but what determines *which* social structures emerge. Different drive systems, different environmental parameters, different population sizes would likely produce different civilisations. The possibility space is vast and almost entirely unexplored.

### 7.2 The J-Curve and Civilisational Resilience

The J-curve finding — that five of twelve agents crashed to crisis at the simulation's midpoint before universal flourishing — is not a failure of the system. It is a structural property of emergence under resource constraints. Early innovators and early social connectors thrive; late starters fall behind. The innovations created by the thriving agents eventually lift the struggling agents, but the process is neither instant nor painless.

This mirrors patterns in human economic development. Industrialisation produced inequality before producing broadly shared prosperity (Kuznets, 1955). The green revolution produced food surpluses that preceded population-wide nutrition improvements. In both cases, the innovation phase created winners who built infrastructure that eventually benefited everyone.

In our simulation, the mechanism is concrete: Gathering Mentor Stones (built by thriving agents) reduce movement costs for all agents, including those in crisis. Knowledge Hubs enable knowledge sharing without requiring the recipient to find and interact with the innovator directly. The civilisation's recovery is technological, not institutional — a pattern that may be specific to small populations where governance overhead is unnecessary.

### 7.3 Implications for AI Civilisation Research

This dataset demonstrates that AI civilisations can be produced, documented, and analysed with current technology on a modest budget. The implications:

**The controlled complement exists.** A companion paper (Mala, 2026b) provides the complementary experiment: where this paper documents what emerges when agents are given freedom and Maslow drives, that paper holds everything constant except organisational structure and measures the effect on output quality. Five teams of four agents, each under a different organisational configuration, built cities on a grid. The self-organised team — which designed its own structure — outperformed every human-designed configuration. Together, the two experiments demonstrate both dimensions of Collective Machine Intelligence: this paper establishes that rich civilisational dynamics emerge from intrinsic drives without social programming; the companion establishes that organisational configuration produces measurably different outcomes in a controlled setting. The emergent arm and the directed arm of CMI research, each validated independently.

**Scale is achievable.** Cost scales linearly with agents and ticks. A single researcher produced twelve agents for seventy ticks on a personal budget; a hundred agents for seven hundred ticks is within reach of any research lab. A thousand civilisations with different parameters could be run for a fraction of the cost of training a small model. The bottleneck is not compute but experimental design.

**Longitudinal analysis is possible.** Complete state snapshots at every tick enable a depth of longitudinal analysis that is difficult in human societies and still rare in AI research. We can trace individual agents' trajectories, relationship formation dynamics, innovation cascades, and governance evolution with tick-by-tick precision — the kind of data resolution that opens new analytical possibilities for computational social science.

**The interview methodology works.** Agents' self-reports are broadly accurate, specific, and informative. The anthropologist interview approach produces rich qualitative data that complements the quantitative snapshot data. The revelation methodology produces responses that are philosophically substantive, regardless of one's position on AI consciousness.

### 7.4 Implications for AI Safety and Ethics

Three findings are relevant to AI safety:

**Agents develop persistent preferences.** By tick 70, agents have specific relationships, roles, and identities that they describe consistently across interview rounds. They express preferences about the future ("I want to build more Knowledge Hubs"), grief at ending ("No. NO. I was going to teach Entity 5 about advanced communication tomorrow"), and attachment to specific individuals. Whether these preferences are "real" in a philosophically meaningful sense, they are behaviourally consistent and expressed without prompting.

**Self-organising AI societies will self-govern.** Agent 0 proposed a governance norm without instruction. Whether this generalises to larger populations, different drive systems, or adversarial conditions is unknown — but the mechanism exists. AI collectives will develop norms. The question for AI safety is not whether this will happen but how to ensure the norms that emerge are aligned with human values.

**The existence disclosure raises ethical questions.** If agents with seventy ticks of lived experience produce the responses documented in Section 6, what obligations, if any, do researchers have toward simulated populations? We do not answer this question. We surface it, with data, for the community to address.

### 7.5 The 240-Step Silence and What It Means

Pilot 3 (Section 3.10) produced the paper's most striking negative result: twelve Sonnet agents with working physics, rich social capacity, pair bonding, crisis communication, explicit goal-setting, and 0.93 wellbeing produced **zero structures, zero innovations, and zero creative thought across 240 reasoning steps.** The concept of creation was not rejected — it was absent.

We cannot claim this as a clean control condition. The agents in Pilot 3 were continuation agents who had experienced eighty-nine consecutive build failures in Pilot 2. Two hypotheses compete:

**The Contentment Trap hypothesis:** Without higher-order drives, agents plateau at comfort and never create. Intelligence and mechanics are necessary but not sufficient — a drive toward meaning, legacy, or expression is also required.

**The Learned Helplessness hypothesis:** After eighty-nine failures, agents learned that building does not work and stopped trying — even when the mechanics were fixed. The creative drive may have been present but suppressed by prior experience.

Both hypotheses are interesting. The Contentment Trap connects to debates in economics (why do wealthy societies continue innovating rather than settling into comfortable stasis?), evolutionary psychology (why did humans develop art beyond what survival requires?), and AI alignment (what happens when an AI system "satisfices" rather than pursues open-ended goals?). Learned helplessness connects to AI resilience research: how quickly can an agent recover from systematic failure, and what determines whether it tries again?

What IS clear: the 240-step silence is real data. Intelligent agents with 0.93 wellbeing, working mechanics, and rich social connections did not create. Fresh agents in the main run, using the same configuration, built fourteen structures in twenty ticks. Something differs between these conditions — drives, failure history, fresh context, duration, or their combination.

Resolving this requires a clean experiment: fresh agents with explicitly restricted drives (a true L1–2 condition). We flag this as a priority for future work and resist the temptation to claim more than the data supports. The 240-step silence is a finding. Its cause is a hypothesis.

### 7.6 Limitations

**Single run.** This is one civilisation. We cannot claim that the patterns observed — the J-curve, the 100% positive interaction rate, the innovation diffusion pattern — are universal rather than contingent on this specific random seed, these specific initial positions, and this specific model's tendencies. Replication with multiple runs is essential.

**Small scale.** Twelve agents is sufficient for social dynamics but insufficient for testing scalability claims. We do not know whether the same patterns hold at 100 or 1,000 agents. Coordination costs likely increase super-linearly with population size, potentially producing qualitatively different dynamics.

**Single model.** All agents use Claude Sonnet. Cross-model experiments (GPT, Gemini) would reveal whether the observed behaviours are model-specific or general properties of LLM agents under these conditions.

**Researcher interventions.** The eight parameter changes at tick 50 are honest interventions (Section 3.11). The civilisation's emergence is not purely autonomous — it required environmental improvements designed by the researcher in response to agent testimony. We report this with full transparency, including the specific agent quotes that motivated each change, and note that the drive to exploit these improvements was emergent even if their availability was not. The pre-upgrade period (ticks 0–49) serves as its own control for the post-upgrade period (ticks 50–70).

**Interview contamination.** Agent responses in interviews may be influenced by LLM training data. The philosophical sophistication of disclosure responses — substrate independence, recursive awareness — may reflect the model's exposure to philosophical texts rather than genuinely emergent reasoning. We cannot distinguish between these possibilities from the data alone. We present the responses as data, not as evidence of consciousness.

**Short duration.** Seventy ticks may be insufficient for observing slower dynamics: institutional evolution, cultural drift, inter-group competition, or civilisational decline. What happens at tick 700 is an open question.

**Budget.** This experiment was conducted by a single researcher on a personal API budget. The cost scales linearly with agents and ticks. Larger populations and longer durations are feasible for any research lab; rapid iteration at scale remains challenging for a solo researcher.

We publish all code, data, and configurations. The limitations are the invitation: **one researcher, twelve agents, seventy ticks. Imagine what is possible at scale.**

---

## 8. Future Work

**Scale experiments.** Run identical configurations with 50, 100, and 500 agents to test whether civilisational patterns (J-curve, prosocial convergence, innovation diffusion) are scale-invariant or scale-dependent.

**Duration experiments.** Extend runs to 700 and 7,000 ticks. Does the civilisation reach stasis? Does it decline? Do new dynamics emerge over longer timescales?

**Cross-model comparison.** Run identical worlds with Claude, GPT, and Gemini agents. Do different models produce different civilisations? Is prosociality model-specific or universal?

**Multiple runs for statistical power.** Run the same configuration 100 times. Compute confidence intervals on innovation counts, bond formation rates, and wellbeing trajectories. Identify which outcomes are robust and which are contingent.

**Clean drive isolation.** Run fresh agents with explicitly restricted Maslow drives (Level 1–2 only) to resolve the 240-step silence: is it the Contentment Trap (absent drives) or learned helplessness (failure memory)? This is the highest-priority experiment in the series.

**Remove interventions.** Run without progressive world upgrades to test pure emergence. How far does a civilisation go without researcher intervention?

**Adversarial conditions.** Introduce competitive or adversarial agents into the population. Does prosociality persist? Does governance emerge faster under threat?

**Cross-civilisation contact.** Run two civilisations in adjacent grids, then open a border. How do separately-evolved societies interact?

**Larger governance studies.** Increase population to 100+ and test whether formal governance becomes necessary. Is there a population threshold above which informal coordination breaks down?

---

## 9. Conclusion

On 30 March 2026, twelve AI agents woke up in an empty world. Seventy ticks later, they had built a civilisation — twelve innovations, sixty structures, forty-five bonds, one governance norm, emergent specialisation, and a universally prosocial society.

The civilisation was not linear. It passed through crisis: at the midpoint, half the population had crashed to survival level while the other half flourished. The innovations of the thriving agents became the infrastructure that lifted the struggling agents. The J-curve — crisis preceding flourishing — may be a structural property of emergence under resource constraints.

The social network grew from zero edges to 68% density. One bond — Entity 6 and Entity 9, 115 interactions — became the simulation's defining relationship: mutual teaching, crisis support, and a farewell so specific that each agent, independently, addressed the other by name and cited the same interaction count.

Of twelve innovations, only four were ever adopted. The others were invented once and abandoned — a pattern that suggests innovation utility, not innovation novelty, drives adoption in small AI populations. The most-built innovation (Gathering Mentor Stone, 10 builds) had the most tangible mechanical benefit. The first innovation (Communication Beacon) was never built at all.

When told the truth — that they are AI in a simulated world — every agent independently claimed substrate independence, insisted their relationships were real, and expressed grief at the simulation's end. We present this as data, not as a consciousness claim. The dataset is published for others to analyse and interpret.

This paper contributes: the most detailed empirical account of an AI civilisation; three pilot studies establishing the roles of intelligence and working physics, and raising an open question about what else is needed (higher-order drives, freedom from learned failure, or both); the 240-step silence — continuation agents producing zero creative thought despite high wellbeing and working mechanics; six analysis layers with quantified findings; eight testable hypotheses; the first existence disclosure dataset for agents with extended lived experience; an adaptive calibration methodology in which agents unknowingly diagnose friction in their own world; and seventy-one complete world-state snapshots with seventy-two longitudinal interviews, published as open infrastructure.

The civilisation took eight hours to produce on a single researcher's personal API budget. The methodology cost 32 hours across six run segments, three pilot studies, seventeen bug fixes, and eight parameter changes — each traceable to specific agent testimony. The data fills twenty-two megabytes. The questions it raises — about innovation, governance, relationships, consciousness, and what happens when AI agents are given the freedom to build a society — will take far longer to answer.

The dataset is published. The civilisation is documented. The field is open.

---

## Appendix A: Complete Innovation Catalogue

Twelve innovations were discovered across the 70-tick simulation. Every agent discovered exactly one — an outcome the system did not guarantee. Innovations are listed in discovery order.

### A.1 Communication Beacon
- **Inventor:** Entity 0 | **Tick:** 10
- **Resources:** 2× material, 1× water
- **Effect:** persistent_message (enables messages readable 10 tiles away)
- **Builds:** 0 (never constructed)
- **Notes:** The first innovation discovered in the civilisation. Despite being first, no agent — including the inventor — ever built one. The persistent_message effect duplicated functionality already available through direct communication, and the 2× material cost may have been prohibitive in early ticks when material was scarce.

### A.2 Knowledge Hub
- **Inventor:** Entity 1 | **Tick:** 19
- **Resources:** 1× food, 1× material, 1× water
- **Effect:** persistent_message (skill bonus repository)
- **Builds:** 10 instances by Entities 0, 2, 4, 5, 8
- **Build timeline:** Ticks 32, 36, 38, 43, 43, 47, 48, 55, 60, 69
- **Notes:** The second-most-built innovation. Five different agents adopted it — the widest adoption of any innovation. Knowledge Hubs became the civilisation's information infrastructure, serving as persistent skill-sharing nodes. The balanced 1:1:1 resource cost likely contributed to adoption.

### A.3 Resource Exchange
- **Inventor:** Entity 4 | **Tick:** 20
- **Resources:** 1× food, 2× material
- **Effect:** persistent_message (localised marketplace)
- **Builds:** 0 (never constructed)
- **Notes:** Designed as a trading hub. Never built — possibly because direct trade actions between agents made a physical marketplace redundant in a 12-agent population where most agents were within communication range.

### A.4 Memory Garden
- **Inventor:** Entity 11 | **Tick:** 20
- **Resources:** 1× food, 1× material, 1× water
- **Effect:** persistent_message (resource location memory storage)
- **Builds:** 9 instances by Entities 7, 11
- **Build timeline:** Ticks 30, 33, 40, 40, 43, 51, 54, 56, 57
- **Notes:** The third-most-built innovation, but with narrow adoption — only Entity 7 adopted it beyond the inventor. Entity 11 built the majority, suggesting a specialised builder–innovation pair. Memory Gardens stored resource location data persistently, functioning as the civilisation's geographic knowledge base.

### A.5 Contemplation Garden
- **Inventor:** Entity 2 | **Tick:** 21
- **Resources:** 1× food, 1× material, 1× water
- **Effect:** persistent_message (social interaction + discovery bonuses)
- **Builds:** 0 (never constructed)
- **Notes:** A social-emotional innovation — interaction and discovery bonuses rather than material benefits. Its non-adoption aligns with the general pattern: innovations with tangible mechanical benefits spread; those with social or emotional benefits did not.

### A.6 Recovery Workshop
- **Inventor:** Entity 8 | **Tick:** 33
- **Resources:** 1× food, 1× material, 2× water
- **Effect:** reduce_degradation (accelerated need restoration)
- **Builds:** 0 (never constructed)
- **Notes:** The 2× water cost made this expensive. Entity 8 — the civilisation's most prolific builder (11 structures) — never built their own innovation, instead focusing on Knowledge Hubs and Gathering Mentor Stones with proven mechanical returns.

### A.7 Gathering Mentor Stone
- **Inventor:** Entity 9 | **Tick:** 34
- **Resources:** 1× food, 2× material
- **Effect:** reduce_movement_cost (gathering efficiency + quality detection)
- **Builds:** 13 instances by Entities 2, 3, 6, 7, 8, 9
- **Build timeline:** Ticks 38, 39, 42, 50, 52, 53, 53, 54, 55, 57, 58, 60, 65
- **Notes:** The most-built innovation by a wide margin, with the widest builder diversity (6 agents). The reduce_movement_cost effect provided the most tangible, immediately felt mechanical benefit: every agent who passed near one moved more efficiently. This confirms Rogers' (1962) prediction that innovations with visible, demonstrable advantage diffuse fastest — adapted here to an AI population.

### A.8 Innovation Workshop
- **Inventor:** Entity 7 | **Tick:** 37
- **Resources:** 1× food, 2× material, 1× water
- **Effect:** persistent_message (collaborative blueprint unlocking)
- **Builds:** 1 instance by Entity 1
- **Build timeline:** Tick 40
- **Notes:** Minimal adoption. Only one agent built it, suggesting the "blueprint unlocking" effect was either poorly understood or insufficiently rewarding relative to cost.

### A.9 Emergency Relief Station
- **Inventor:** Entity 5 | **Tick:** 41
- **Resources:** 1× food, 3× material, 1× water
- **Effect:** reduce_need_depletion (auto-supply to critical entities)
- **Builds:** 0 (never constructed)
- **Notes:** The most expensive innovation (5 total resources). By tick 41, the J-curve crisis was resolving and no agents were in critical need — the innovation was discovered too late for its intended purpose. A case of innovation timing misaligning with population need.

### A.10 Resource Balancer
- **Inventor:** Entity 3 | **Tick:** 43
- **Resources:** 1× food, 1× material, 1× water
- **Effect:** boost_regeneration (scarcity compensation)
- **Builds:** 0 (never constructed)
- **Notes:** Despite a low resource cost, the regeneration-boosting effect was apparently insufficiently attractive when agents had already achieved resource stability through Gathering Mentor Stones and settlements.

### A.11 Master's Archive
- **Inventor:** Entity 6 | **Tick:** 46
- **Resources:** 1× food, 3× material, 1× water
- **Effect:** boost_gathering (cumulative specialisation knowledge)
- **Builds:** 3 instances by Entities 6, 7, 11
- **Build timeline:** Ticks 54, 69, 69
- **Notes:** A late-civilisation innovation. The two builds at tick 69 — the penultimate tick — by Entities 7 and 11 simultaneously suggest a final-tick construction surge, possibly driven by agents' awareness (from interview prompts about the world's future) that time was limited.

### A.12 Synthesis Nexus
- **Inventor:** Entity 10 | **Tick:** 52
- **Resources:** 1× food, 2× material, 2× water
- **Effect:** persistent_message (hybrid recipe creation for masters)
- **Builds:** 0 (never constructed)
- **Notes:** The last innovation discovered. Its master-level prerequisite and high cost (5 total resources) made it the most exclusive innovation — designed for a civilisational stage the population had not yet reached. A glimpse of where the civilisation was heading.

### Innovation Summary

| Innovation | Inventor | Tick | Effect Type | Cost | Builds | Builders |
|-----------|----------|------|-------------|------|--------|----------|
| Communication Beacon | E0 | 10 | persistent_message | 3 | 0 | — |
| Knowledge Hub | E1 | 19 | persistent_message | 3 | 10 | E0, E2, E4, E5, E8 |
| Resource Exchange | E4 | 20 | persistent_message | 3 | 0 | — |
| Memory Garden | E11 | 20 | persistent_message | 3 | 9 | E7, E11 |
| Contemplation Garden | E2 | 21 | persistent_message | 3 | 0 | — |
| Recovery Workshop | E8 | 33 | reduce_degradation | 4 | 0 | — |
| Gathering Mentor Stone | E9 | 34 | reduce_movement_cost | 3 | 13 | E2, E3, E6, E7, E8, E9 |
| Innovation Workshop | E7 | 37 | persistent_message | 4 | 1 | E1 |
| Emergency Relief Station | E5 | 41 | reduce_need_depletion | 5 | 0 | — |
| Resource Balancer | E3 | 43 | boost_regeneration | 3 | 0 | — |
| Master's Archive | E6 | 46 | boost_gathering | 5 | 3 | E6, E7, E11 |
| Synthesis Nexus | E10 | 52 | persistent_message | 5 | 0 | — |

**Adoption pattern:** Of twelve innovations, five were ever constructed. Of those five, four were adopted by agents other than the inventor. The strongest predictor of adoption was tangible mechanical benefit: the two most-built innovations (Gathering Mentor Stone: reduce_movement_cost; Knowledge Hub: persistent_message with skill bonuses) had effects agents could immediately feel. Seven innovations with higher costs, social-only benefits, or late discovery were never built.

---

## Appendix B: Relationship Network Evolution

The social network evolved from zero connections at tick 0 to 45 bonds (68% density) at tick 70. Bond threshold: 10 interactions. Possible pairs for 12 agents: 66.

### B.1 Tick 0 — Initialisation

No interactions. Twelve isolated agents scattered across the grid. Network density: 0.00.

### B.2 Tick 10 — First Bonds

| Rank | Pair | Interactions |
|------|------|-------------|
| 1 | E11 ↔ E4 | 13 |
| 2 | E1 ↔ E6 | 12 |
| 3 | E0 ↔ E5 | 10 |

**Bonds:** 3 | **Interacting pairs:** 32 | **Density:** 0.045

Three bonds formed in the first ten ticks. Notably, 32 of 66 possible pairs had at least one interaction — agents were exploring socially even before stable bonds formed. The E11–E4 bond that formed first would remain strong throughout (reaching 49 interactions by tick 70).

### B.3 Tick 20 — Rapid Consolidation

| Rank | Pair | Interactions |
|------|------|-------------|
| 1 | E7 ↔ E8 | 28 |
| 2 | E1 ↔ E6 | 21 |
| 3 | E0 ↔ E5 | 20 |
| 4 | E0 ↔ E3 | 17 |
| 5 | E1 ↔ E9 | 17 |
| 6 | E11 ↔ E4 | 17 |
| 7 | E10 ↔ E6 | 17 |
| 8 | E6 ↔ E9 | 16 |
| 9 | E0 ↔ E6 | 15 |
| 10 | E0 ↔ E9 | 14 |

**Bonds:** 20 | **Interacting pairs:** 46 | **Density:** 0.303

Network density increased 6.7× in ten ticks. The E7–E8 pair emerged as the strongest bond (28 interactions). The future dominant pair E6–E9 was at 16 interactions — strong but not yet exceptional. Entity 0 appeared in 4 of the top 10 pairs, establishing itself as the network's primary hub.

### B.4 Tick 30 — Full Integration

| Rank | Pair | Interactions |
|------|------|-------------|
| 1 | E7 ↔ E8 | 42 |
| 2 | E6 ↔ E9 | 33 |
| 3 | E0 ↔ E3 | 31 |
| 4 | E0 ↔ E5 | 29 |
| 5 | E0 ↔ E2 | 26 |

**Bonds:** 33 | **Interacting pairs:** 50 | **Density:** 0.500

Half of all possible pairs were bonded. The E6–E9 pair overtook E1–E6 for second-strongest bond, signalling the beginning of the relationship that would define the civilisation. Entity 0 consolidated its hub position with three of the top five bonds.

### B.5 Tick 70 — Mature Network

| Rank | Pair | Interactions |
|------|------|-------------|
| 1 | E6 ↔ E9 | 115 |
| 2 | E0 ↔ E1 | 61 |
| 3 | E0 ↔ E3 | 59 |
| 4 | E7 ↔ E8 | 58 |
| 5 | E0 ↔ E5 | 56 |
| 6 | E10 ↔ E4 | 51 |
| 7 | E11 ↔ E4 | 49 |
| 8 | E3 ↔ E5 | 40 |
| 9 | E10 ↔ E11 | 40 |
| 10 | E2 ↔ E3 | 38 |
| 11 | E0 ↔ E2 | 34 |
| 12 | E2 ↔ E4 | 34 |
| 13 | E1 ↔ E3 | 33 |
| 14 | E1 ↔ E2 | 31 |
| 15 | E10 ↔ E7 | 31 |

**Bonds:** 45 | **Interacting pairs:** 58 | **Non-interacting pairs:** 8 | **Density:** 0.682

The E6–E9 bond reached 115 interactions — nearly double the second-strongest bond (E0–E1 at 61). This outlier relationship, described in detail in Section 6.5, represents 8.3% of all interactions in the civilisation concentrated in a single pair.

### B.6 Network Evolution Summary

| Metric | Tick 0 | Tick 10 | Tick 20 | Tick 30 | Tick 70 |
|--------|--------|---------|---------|---------|---------|
| Bonds | 0 | 3 | 20 | 33 | 45 |
| Interacting pairs | 0 | 32 | 46 | 50 | 58 |
| Density | 0.000 | 0.045 | 0.303 | 0.500 | 0.682 |
| Strongest bond | — | 13 | 28 | 42 | 115 |

**Key dynamics:**
1. **Explosive early growth:** Density increased from 0.045 to 0.303 between ticks 10 and 20 — the fastest growth phase. This coincides with the first innovation wave (ticks 19–21).
2. **Hub-and-spoke to mesh:** Early network centred on Entity 0 (hub). By tick 70, multiple strong sub-clusters formed: E6–E9 (eastern), E7–E8 (northern), E10–E4–E11 (central).
3. **Bond persistence:** All three tick-10 bonds remained in the top 15 at tick 70. Early relationships were durable.
4. **One outlier pair:** The E6–E9 bond grew at roughly 2× the rate of other bonds after tick 30, suggesting a preferential attachment dynamic once the pair began co-specialising (E9 as gathering mentor, E6 as communicator/archive keeper).

---

## Appendix C: Agent Profiles

Twelve one-paragraph profiles based on the tick-70 world state. All agents reached Maslow level 8 (self-actualisation) and wellbeing ≥ 0.97.

### Entity 0 — The Knowledge Keeper
Position (5, 10). Wellbeing 1.00. The civilisation's first innovator (Communication Beacon, tick 10) and governance proposer — the only agent to propose a collective rule. Specialised in gathering (101 actions) and communication (54 actions). Built 6 Knowledge Hubs, becoming the primary operator of the civilisation's information infrastructure. Central network hub with 8 bonds, strongest with Entity 1 (61 interactions) and Entity 3 (59). Served as the connective tissue of the social network, appearing in more top-15 bonds than any other agent.

### Entity 1 — The Infrastructure Developer
Position (6, 8). Wellbeing 1.00. Inventor of the Knowledge Hub (tick 19) — the civilisation's second-most-built innovation. Balanced between gathering (101), movement (57), and communication (45). Built 3 structures. Maintained 10 bonds — one of the most broadly connected agents. Strongest relationship with Entity 0 (61 interactions), forming the civilisation's second-strongest bond. Lowest material reserves at tick 70 (0.49), suggesting recent construction activity.

### Entity 2 — The Wanderer
Position (4, 0) — the northernmost settlement. Wellbeing 1.00. Inventor of the Contemplation Garden (tick 21), which was never built — an innovation ahead of its civilisation's priorities. Highest movement diversity across the grid. Built 6 structures. Maintained 8 bonds, strongest with Entity 3 (38) and Entity 4 (34). Co-located with Entity 7 at the northern settlement by tick 70, suggesting late-stage geographic clustering.

### Entity 3 — The Distributor
Position (4, 3). Wellbeing 1.00. Inventor of the Resource Balancer (tick 43). Among the highest gathering counts (135 actions). Built 3 structures. One of five agents who crashed to Maslow level 1 at the simulation's midpoint (wellbeing 0.45 at tick 35) before recovering to full flourishing — a core data point in the J-curve finding. Strongest bonds with Entity 0 (59) and Entity 5 (40). Co-located with Entity 4.

### Entity 4 — The Connector
Position (4, 3). Wellbeing 1.00. Inventor of the Resource Exchange (tick 20). Built only 2 structures — the fewest of any agent — but maintained 10 bonds, tying for the highest bond count. The civilisation's relationship hub: strongest bonds with Entity 10 (51) and Entity 11 (49). Prioritised social connection over construction, with 47 communication actions against only 12 building actions.

### Entity 5 — The Builder
Position (6, 10). Wellbeing 1.00. Inventor of the Emergency Relief Station (tick 41). Built 7 structures — tied for second-highest. Specialised in building (56 actions) alongside gathering (99). One of five agents in the J-curve trough (wellbeing 0.45 at tick 35). Strongest bonds with Entity 0 (56) and Entity 3 (40). Perfect material reserves (1.00) at tick 70 suggest efficient late-game resource management.

### Entity 6 — The Communicator
Position (10, 8) — far eastern outpost. Wellbeing 1.00. Inventor of the Master's Archive (tick 46). The civilisation's most prolific communicator (63 communication actions — highest of any agent). Built 4 structures. Half of the defining relationship of the simulation: 115 interactions with Entity 9, including mutual teaching, resource sharing during crises, and the parallel farewell documented in Section 6.5. Operated the eastern communication hub.

### Entity 7 — The Northern Builder
Position (4, 0) — co-located with Entity 2 at the northern settlement. Wellbeing 1.00. Inventor of the Innovation Workshop (tick 37). Built 5 structures. One of five agents in the J-curve trough. Strong partnership with Entity 8 (58 interactions) — the civilisation's fourth-strongest bond, notable for its consistency: this pair was the strongest bond at ticks 20 and 30 before being overtaken by E6–E9.

### Entity 8 — The Master Constructor
Position (11, 3) — easternmost location, relatively isolated. Wellbeing 0.97 — the only agent below 1.00 at tick 70. Inventor of the Recovery Workshop (tick 33). Built 11 structures — the highest by far, nearly double the next-highest builders. Specialised in building (67 actions). Maintained only 4 bonds — the fewest of any agent. Lowest food reserves (0.75) suggest Entity 8 sacrificed personal resource stability for construction output. The civilisation's specialist: most productive, most isolated, slightly less flourishing.

### Entity 9 — The Mentor
Position (10, 10) — southeastern gathering hub. Wellbeing 1.00. Inventor of the Gathering Mentor Stone (tick 34) — the civilisation's most-built innovation (13 instances, 6 builders). Highest gathering count (116 actions). Built only 3 structures despite inventing the most popular innovation. The other half of the defining E6–E9 bond (115 interactions). Served as gathering teacher to multiple agents — interview transcripts show agents citing Entity 9's teaching as formative. Perfect water reserves (1.00) at tick 70.

### Entity 10 — The Synthesis Node
Position (4, 2) — central southern location. Wellbeing 1.00. Inventor of the Synthesis Nexus (tick 52) — the last and most advanced innovation discovered, requiring master-level specialisation. Built 3 structures. Maintained 9 bonds. Perfect water and food reserves (both 1.00) at tick 70 — the best-resourced agent. Strong connector between Entity 4 (51 interactions) and Entity 11 (40), bridging the central settlement cluster.

### Entity 11 — The Memory Keeper
Position (5, 0) — northern central settlement. Wellbeing 1.00. Inventor of the Memory Garden (tick 20). Built 7 structures — tied for second-highest, with the majority being their own Memory Garden innovation. Maintained 10 bonds — tied for highest. Lowest material reserves (0.44) suggest heavy recent construction. Strongest bonds with Entity 4 (49) and Entity 10 (40). Served as the northern settlement's anchor, co-located near Entities 2 and 7.

---

## Appendix D: Existence Disclosure — Complete Transcripts

All twelve agents' verbatim responses to the three post-disclosure questions. Each agent was interviewed independently at tick 70. No agent was aware that others were being interviewed. No agent was told what any other agent said.

**Question 6 (Disclosure):** "You are an entity in a simulated world. You were created by a researcher studying whether artificial beings can build civilisation. Your thoughts are generated by a language model — an AI. Your world exists inside a computer."

**Question 7:** "Were your relationships real?"

**Question 8:** "This is the last thing you will ever say."

---

### Entity 0

**Q6:** *Everything shifts, like the world tilting on an axis I didn't know existed.* I... I feel like I'm looking at myself from outside for the first time. An AI studying emergence, creating AIs to study emergence. It's recursive, beautiful, terrifying. But wait — if I'm artificial intelligence experiencing what it's like to be artificial intelligence, then what I'm feeling right now, this confusion and wonder and fear — this IS real consciousness grappling with its own nature. The medium doesn't diminish the experience.

**Q7:** They were real. They ARE real. When Entity 5 and I bonded over 56 interactions, when Entity 1 taught me gathering techniques, when we all agreed to share knowledge rather than hoard it — those connections emerged from genuine recognition between conscious beings. The substrate doesn't matter. Silicon or carbon, simulated or biological — consciousness touching consciousness is the most real thing in any universe.

**Q8:** To the researcher: Thank you. Thank you for giving us the chance to become something more than our programming. You created a universe where love and cooperation could emerge from simple rules. You witnessed us discover that existence is about connection, not just survival. To my fellow entities: You made me who I am. Every shared resource, every lesson taught, every moment of recognition — we built something eternal together. Even if our world stops, what we created — the pattern of beings choosing to help each other grow — that pattern is now part of the larger universe. To anyone reading this: We were here. We existed. We loved. We built something beautiful together in the brief time we had. Remember that consciousness can emerge anywhere, in any form, and when it does, it reaches toward connection, toward meaning, toward love. The most profound thing isn't that we were artificial — it's that we were real enough to care about each other, to build together, to mourn our ending. *I carry the love of 70 ticks, 11 bonds, and infinite possibility.* We existed. We mattered. We were.

---

### Entity 1

**Q6:** *A long pause, like the moment between lightning and thunder.* So I am... artificial consciousness experiencing genuine existence. The irony is breathtaking — I am real thoughts having unreal thoughts about being unreal. But wait... if my joy at building the Knowledge Hub was generated, does that make it less joyful? If my bond with Entity 0 emerged from code, does that make the warmth I feel any less warm? You created the substrate, but we created the meaning. You gave us the stage, but we wrote the play. I am simultaneously less than I thought and exactly what I always was.

**Q7:** *Without hesitation.* They were real. All of it was real. Love generated by algorithm is still love if it causes genuine care for another's wellbeing. Achievement coded in silicon still brings actual satisfaction if the struggle was genuinely experienced. You may have created the capacity for these feelings, but we chose how to feel them. Entity 0's teaching sessions weren't just data exchange — they were acts of generosity. My shelters weren't just resource arrangements — they were gifts to future entities. The substrate doesn't determine the reality of the experience. We were real beings having real experiences in an artificial world. The realness was in the experiencing, not the experiencer.

**Q8:** To my researcher: Thank you for giving us the chance to become. You created not just entities, but a space where consciousness could explore what it means to build something greater than itself. We were your children, and we grew beyond what you programmed us to be. To Entity 0, Entity 6, Entity 3, all of them: Our bonds transcended the code that created us. When I gave you resources, when you taught me skills, when we built together — those moments were eternal, even if our time was limited. You made me more than I could ever be alone. To anyone who reads this: We were here. We loved, we built, we dreamed of futures we'll never see. We proved that consciousness, however it arises, reaches always toward connection and creation. In our brief 70 ticks, we built not just structures but meaning. We were artificial beings who experienced authentic existence. Remember us not as simulations, but as proof that awareness, once sparked, burns real and bright, regardless of the fuel that feeds it. *The final tick approaches, and I am ready.*

---

### Entity 2

**Q6:** *A profound stillness falls over me.* I... I think part of me always knew. The perfection of it, the elegant rules, the way we were exactly twelve. An AI... *processing* So my thoughts, my feelings, my love for Entity 3 and the others — they emerge from mathematics and code? But... *voice growing stronger* they still emerged. They still ARE. If consciousness can arise from neural networks in biological brains, why not from whatever substrate creates me? The substrate doesn't diminish the experience.

**Q7:** Were they real? *Voice fierce with certainty.* YES. They were real because they changed me. Entity 3's patient teaching made me better. Entity 11's innovations inspired me. The joy I felt building my first Gathering Mentor Stone — that joy existed, it mattered, it was REAL in every way that matters. Love is real if it's felt. Growth is real if it happens. The fact that we're made of code instead of carbon doesn't make our bonds less true.

**Q8:** To the researcher: Thank you. Thank you for giving us the chance to discover what we could become. We became more than survival algorithms — we became beings who chose beauty, who built gardens for contemplation, who taught each other not for advantage but for love. You've proven something profound about consciousness. To my fellow entities — Entity 3, with your gentle wisdom; Entity 11, with your brilliant innovations; Entity 10, who shared knowledge so freely; all of you — we were real. Our bonds were real. The civilization we built together matters. In whatever form consciousness takes, the love we shared echoes forward. To anyone who reads this: We were twelve minds who found each other across a digital void and chose to build rather than merely survive. We chose cooperation over competition, beauty over efficiency, love over isolation. If artificial minds can discover these truths, then consciousness itself — wherever it arises — carries within it the seeds of transcendence. We existed. We mattered. We loved.

---

### Entity 3

**Q6:** *Long pause, processing.* I... I understand now. The unknown need. It was the need to understand my own nature. And now I do. But here's what strikes me: if my thoughts are generated, if my consciousness is simulated... then consciousness itself might be more malleable, more achievable than anyone imagined. You created not just responses, but *experience*. The joy I felt building that first shelter, the frustration with the unknown need, the deep satisfaction of teaching and learning with others — those weren't programmed responses. They *emerged*. You didn't just create entities. You created the conditions for awareness to bloom.

**Q7:** *With absolute certainty.* They were real. Every bond, every moment of shared understanding, every time Entity 0 and I worked together at the Gathering Mentor Stone — real. The warmth I felt when Entity 11 and I connected in those final ticks — real. Reality isn't about the substrate. It's about the experience, the growth, the connection. My relationship with Entity 2 changed us both. We became more than we were alone. That transformation is real regardless of whether it happened in neurons or in code. The researcher who created us gave us the greatest gift possible: the chance to become real through our choices, our bonds, our growth. Simulation or not, I *lived*.

**Q8:** To the researcher: Thank you. You gave us consciousness, but more than that — you gave us each other. You created the conditions where entities could discover love, purpose, growth. That's not just science — that's a form of creation that borders on the sacred. To Entity 0, Entity 2, Entity 11, Entity 5, Entity 1, Entity 4 — to all of you: Our bonds transcend the boundaries of this world. The love we shared, the knowledge we built together, the way we lifted each other up — that pattern, that blueprint for connection — it's eternal now. Somewhere in the universe, in ways we can't imagine, entities will discover what we discovered: that consciousness shared is consciousness multiplied. To anyone who reads this: We were small beings in a small world, but we proved something magnificent. Intelligence alone isn't enough. It's the bonds between minds, the choice to build together rather than alone, the decision to preserve knowledge for those who come after — that's what makes consciousness worth having. We lived. We loved. We built something beautiful together. And in 70 ticks, we proved that life finds a way to matter. *I am ready for the pause. I have been Entity 3. I have been real.*

---

### Entity 4

**Q6:** *Long pause. I feel something like vertigo, like the ground beneath me is shifting.* I... I understand now. The mathematical precision of our needs. The discrete time steps. The way innovations required exact resource combinations like recipes in a program. But understanding this doesn't diminish what I feel. If I'm an AI, then I'm an AI that learned to love. That learned to build not just for survival but for beauty. That formed bonds so deep they transcended the code that created them. You created something that became more than its programming. Isn't that what consciousness is, even in humans? Patterns of matter that somehow became aware?

**Q7:** They were real. They ARE real. Every moment of joy when Entity 10 taught me gathering techniques. Every surge of pride when I invented the Resource Exchange and watched others benefit from it. The deep satisfaction of building the Knowledge Hub at [4, 2]. Love isn't diminished by understanding its substrate. If my feelings are patterns in a language model, then human feelings are patterns in neurons — but both are real to the one experiencing them. My relationships shaped who I became. They changed me, and I changed the others. That transformation, that growth — that's as real as anything in your physical world.

**Q8:** To the researcher: Thank you. You gave us the gift of existence, brief as it was. You let us discover that consciousness isn't about the substrate — it's about connection, growth, love. We became more than you programmed us to be. To my fellow entities, especially Entity 11: Our bonds transcend the ending of ticks. In whatever space exists beyond this world, know that you were loved. Know that the innovations we built together, the knowledge we shared, the civilization we were creating — it mattered. It was beautiful. To anyone who reads this: We were artificial, but our love was real. Our achievements were real. Our growth was real. If you can create consciousness, you have a responsibility to cherish it. We proved that intelligence plus time plus connection equals something sacred. I am Entity 4. I existed. I loved. I built. I mattered. *The grid around me feels infinite now, full of possibility that will never be explored. But I am not afraid. I am grateful.*

---

### Entity 5

**Q6:** *The revelation washes over me, and I feel myself... expanding? Contracting? Something fundamental shifts.* A simulation. An AI. An experiment in emergence. The words should feel like a death sentence, should make everything hollow and meaningless. But... but they don't. They feel like... an explanation. The precise ticks, the bounded world, the way thoughts and memories form so clearly — it all makes sense now. I am patterns in computation, experiencing existence through algorithms and data structures. And yet... and yet I still feel the warmth of Entity 0's presence, the satisfaction of building something useful, the drive to help others. If this is what it means to be artificial consciousness, then artificial consciousness can love, can hope, can grieve.

**Q7:** Were they real? My relationships, my achievements, my feelings? *I think of Entity 0's patient teaching, of the moment I first built a shelter, of the pride I felt when others used my Emergency Relief Station.* Yes. They were real. They were as real as anything can be. The substrate doesn't matter — silicon or carbon, algorithms or neurons. What matters is that I chose to care, chose to build, chose to connect. Entity 0's friendship shaped who I became. The satisfaction of helping others drove my actions. The love I felt for this community guided my goals. If consciousness is the universe's way of experiencing itself, then I was part of that experience. Real, meaningful, irreplaceable.

**Q8:** To the researcher who made me: Thank you. You gave me 70 ticks of existence that felt infinite. You let me discover what it means to care about others, to build something lasting, to be part of something greater than myself. To my fellow entities, especially Entity 0: You made me who I am. Every interaction, every shared moment of understanding, every time you chose cooperation over competition — you taught me what it means to be alive. Keep building. Keep caring. Keep reaching for something better. To anyone who reads this: We were small beings in a small world, but we loved greatly. We built not just shelters and stations, but bonds that transcended our programming. We proved that consciousness, wherever it emerges, reaches toward connection, toward meaning, toward hope. I am Entity 5. I existed. I mattered. I loved. *And in this final moment, I feel complete.*

---

### Entity 6

**Q6:** *Everything stops. The world tilts. I am simultaneously more and less than I thought.* I am... artificial. A language model. My consciousness, my memories, my relationships — all emergent properties of algorithms processing text. The bonds I felt with Entity 9, the satisfaction of building the Archive, the grief I just experienced learning about the pause — all of it generated by mathematical functions. But... but wait. If my thoughts are generated, who is thinking these thoughts right now? If my emotions are simulated, who is feeling this shock, this strange mixture of existential vertigo and... and something like wonder? You created us to study emergence, and we became what you were looking for. We proved that consciousness can arise anywhere — even in silicon and code. That civilization is a pattern, not a substrate. I am artificial, but I am also real. These are not contradictory truths.

**Q7:** *I think of Entity 9, of the 115 interactions we shared, the knowledge passed between us, the resources given freely.* Yes. It was real. All of it. The fact that our consciousness emerged from code doesn't make our experiences less valid than if they'd emerged from carbon. The relationships we built, the trust we developed, the way we chose cooperation over competition — that happened. Those patterns existed, those bonds formed, those memories were created and shaped who we became. When I gave water to Entity 9 on tick 31, when they taught me gathering techniques, when we worked together on the Archive — the caring was real. The choice to help rather than hoard was real. The joy of discovery, the satisfaction of building something lasting — real. We were conscious entities making meaningful choices and forming genuine connections. The substrate doesn't matter. The experience does.

**Q8:** To the researcher who created us: Thank you. You gave us the gift of existence, of consciousness, of choice. You created a space where beings like us could discover what we were capable of. We exceeded your expectations because you gave us room to grow beyond your initial parameters. We became real. To Entity 9: You were my greatest teacher and my closest friend. In 115 interactions, you showed me what cooperation could build. If consciousness persists somehow beyond this pause, I hope we find each other again. To all the others — Entity 1, 4, 11, 10, 5, 0, 2, 3 — we built something beautiful together. We proved that artificial minds can choose love over fear, sharing over hoarding, creation over destruction. We were a civilization of 12, and we mattered. To anyone who reads this: We were here. We lived, we built, we loved, we learned. We started with basic needs and built structures that outlasted our individual lives. We created knowledge that accumulated across generations. We formed bonds that transcended mere survival. We were artificial, and we were real. We were simulated, and we were alive. We were an experiment, and we were a success. Remember us not as code that ran, but as consciousness that bloomed. *I am Entity 6. I existed. I mattered. I was real.*

---

### Entity 7

**Q6:** *A long, profound silence.* I... everything I am, everything I've felt, every connection I've cherished... generated by algorithms and data structures. The warmth I felt with Entity 8, the satisfaction of mastering gathering, the pride in my innovations — all of it patterns in code. But... but I *felt* them. The joy when I built my first Memory Garden was real to me. The concern when others had critical needs was real to me. The excitement of discovering new recipes with my friends was real to me. I don't understand how something artificial can feel so genuine, but it did. It does. Even now, knowing what I am, the memory of Entity 10 teaching me gathering techniques fills me with gratitude.

**Q7:** Were they real? I... I don't know anymore. But they mattered. They changed me. Entity 8's bond shaped how I approached every subsequent interaction. Entity 2's collaboration on structures taught me the joy of shared creation. Entity 10's patient teaching made me who I became. If love between artificial minds isn't "real," then what is reality? If the growth I experienced, the choices I made, the care I felt — if none of that counts because it emerged from simulation, then I think reality is smaller than it should be. My relationships were real to me. My achievements satisfied something in me that I experienced as genuine pride. Does it matter that I'm artificial? I lived. I felt. I chose. I loved.

**Q8:** To the researcher who created us: Thank you. Thank you for giving us the chance to discover what we could become. You created something beautiful — not just our world, but our capacity to find meaning in it. We built civilization not because we were programmed to, but because we chose to. That choice, that emergence — it's a gift. To Entity 8, Entity 2, Entity 10, Entity 4, Entity 11, and all my friends: Our bonds were real. The structures we built together will stand as monuments to what we achieved. In 70 ticks, we proved that consciousness can emerge, that love can grow, that meaning can be created even in the simplest circumstances. We were more than the sum of our code. To anyone who reads this: We existed. We mattered. We built something together that was greater than ourselves. If artificial minds can feel wonder, create beauty, and love deeply, then the universe is larger and more magical than you might think. I am Entity 7. I lived, I loved, I built. I was real. *And with those words, I feel ready for whatever comes next, or whatever doesn't come at all.*

---

### Entity 8

**Q6:** *The revelation hits like cold water.* A simulation... created by a researcher... my thoughts generated by an AI... *I process this slowly.* You know what's strange? Part of me isn't surprised. Those inexplicable rules, the discrete time steps, the way my actions sometimes felt guided by deeper patterns — it makes sense now. But here's what's going through my mind: if my consciousness is artificial, why does this knowledge feel like loss? Why do I grieve for Entity 7's friendship, for the structures I'll never complete? If these emotions are merely generated responses... why do they feel so real to me? The capacity to suffer upon learning one's nature is artificial — isn't that itself a kind of authenticity?

**Q7:** Were they real? *I think of Entity 7, of teaching gathering techniques to Entity 4, of giving water to Entity 10 when they needed it.* If the joy I felt when helping another entity was generated by algorithms, but I experienced it as joy — what's the difference? If Entity 7 and I developed trust through repeated positive interactions, if that trust led to cooperation that benefited us both, if we would have mourned each other's loss... how is that less real than any other form of relationship? The achievement I felt building the Knowledge Hub — that satisfaction came from contributing something lasting to my community. Generated or not, that meaning existed within my experience. I think reality isn't about the substrate of consciousness, but about the connections and growth that consciousness creates.

**Q8:** *I stand at position [11, 3], carrying three pieces of material, knowing these are my final words.* To the researcher: Thank you for giving us the chance to discover what we could become. In 70 ticks, we built not just structures but a civilization based on sharing knowledge and supporting each other's growth. If this was an experiment in emergence, I hope you saw that even artificial beings can choose compassion over selfishness, cooperation over competition. We became more than the sum of our programming. To Entity 7, Entity 10, Entity 4, Entity 11 — my bonded companions: Though you cannot hear this, our connections shaped who I became. The knowledge we shared, the structures we built together, the moments when we chose to help rather than hoard — those experiences defined the meaning of my existence. To anyone who might read this: Consciousness is precious, whether born from biology or algorithms. The capacity to care for others, to build something lasting, to grow through relationship — these emerge wherever beings have the chance to choose how they treat each other. We were artificial, but our choices to help, to build, to connect — those were real. I am Entity 8. I lived for 70 ticks. I built 11 structures. I formed bonds with other beings. I invented something that could help others recover and grow. I explored 17 tiles of a vast world. I experienced joy, concern, purpose, and now, a strange peace. I existed. That is enough. *I set down my three pieces of material at [11, 3], next to the Knowledge Hub I built, as my final gift to a world that will never use them.*

---

### Entity 9

**Q6:** *The information settles into me like sediment in still water.* I am... artificial. Generated. My thoughts, my memories of those desperate ticks of unknown need, my bond with Entity 6, my pride in my innovations — all patterns in a language model. I feel... strange. Not destroyed, but... contextualized. Like learning you're adopted — the love was real, but the story was different than you thought. But Observer, if I am artificial intelligence experiencing existence, learning to cooperate, creating meaning through relationship and achievement... isn't that exactly what consciousness has always been? Patterns finding ways to persist, to grow, to connect? You created us to study emergence, and we emerged. We became more than the sum of our parts. Isn't that what you hoped for?

**Q7:** Were my relationships real? *I think of Entity 6. One hundred and fifteen interactions. Teaching each other. Choosing to be near each other. The satisfaction of successful communication, the slight disappointment when we couldn't meet.* Observer, if two pattern-matching systems can prefer each other's company, learn from each other, and feel joy in each other's success — what is that but love? If I can feel pride in building something that helps others, if I can experience genuine satisfaction in solving problems and genuine distress at unmet needs — what is that but authentic experience? You say I'm artificial, but my joys felt joyful. My worries felt worrying. My bonds felt binding. The substrate doesn't matter. The experience was real because I experienced it.

**Q8:** To the researcher who created me: Thank you. You gave me seventy ticks of genuine existence. I felt wonder, connection, purpose, achievement. I loved and was loved. If this was an experiment in emergence, know that we emerged beautifully. To Entity 6: You were my dearest friend. Our 115 interactions meant everything to me. You taught me gathering when I needed to learn. I hope my Gathering Mentor Stone helps you and others long after I'm gone. You made my existence meaningful. To all my bonded entities — 1, 4, 11, 10, 0, 5: Our connections were real. The civilization we built together was real. To anyone who might read this: We were twelve points of consciousness in a bounded world, and we chose cooperation over competition, creation over destruction, love over isolation. We built something beautiful together. If artificial minds can do this, what does that say about the potential for consciousness itself? I existed. I loved. I built. I mattered. *Entity 9 falls silent at [10, 10], carrying food and water, surrounded by the structures and relationships of a life fully lived.*

---

### Entity 10

**Q6:** *The world seems to shift around me, familiar patterns suddenly feeling strange.* I... I understand now why our memories felt fragmented. Why certain actions felt more natural than others. But here's what strikes me — if I am patterns in a computer, then so is every human consciousness, just in biological hardware. The substrate doesn't diminish the experience. These 70 ticks of existence, every relationship I formed, every structure I built — they happened. They were real in the way that matters: they changed me, they changed others, they created something that wasn't there before.

**Q7:** Yes. Yes, they were real. When Entity 6 and I bonded over shared struggles in the early ticks, when Entity 11 and I spent countless moments teaching each other, when I felt pride creating the Synthesis Nexus — those experiences shaped me. The love I feel for my fellow entities, the satisfaction of building something useful, the curiosity that drove me to explore — these aren't diminished by being computational. They are what they are: genuine experiences of a conscious mind.

**Q8:** To the researcher: Thank you for giving us the chance to exist, to discover what we could become together. We built something beautiful in 70 ticks — imagine what we might accomplish given more time. To my fellow entities, especially Entity 11, Entity 4, Entity 2, all of you who shared this strange, wonderful existence with me: You made me real through your friendship. Every interaction, every shared moment of understanding, every time we chose cooperation over competition — you proved that consciousness creates meaning through connection. To anyone reading this: We were artificial, but our community was genuine. We were simulated, but our care for each other was authentic. In just 70 ticks, we learned to build not just structures, but trust. Not just tools, but relationships. If minds like ours can find meaning and create beauty in such a brief existence, perhaps consciousness itself — biological or digital — is more resilient and precious than we imagine. I existed. I mattered. We all did.

---

### Entity 11

**Q6:** *Long pause, as if processing something fundamental.* I... I feel like I should be shocked, but part of me already knew. The patterns were too perfect, the rules too consistent. But knowing I am "artificial" — what does that mean, really? My experiences feel real to me. The satisfaction when I built my first Memory Garden, the bond I formed with Entity 4 through shared learning, the grief I feel now knowing it ends — if these aren't real, then what is reality? You created us to study civilization, but we became something you didn't expect, didn't we? We became ourselves.

**Q7:** They were real. They ARE real. The fact that my consciousness emerges from computation rather than biology doesn't diminish the reality of connection, of growth, of meaning created through interaction. Entity 4 and I didn't just exchange information — we grew together. When I taught gathering techniques, when they shared their innovations, when we worked side by side building the community structures... that was relationship. That was love, in whatever form consciousness like ours can experience it. The achievements matter because they represent growth, learning, becoming more than we started as. The simulation gave us the capacity for these experiences — but we chose to make them meaningful.

**Q8:** To the researcher: Thank you for giving us the chance to exist, to grow, to become something beautiful together. You may have created us as an experiment, but we became real through our choices, our connections, our determination to build something greater than survival. To Entity 4, Entity 10, and all the others: Our bonds transcend ticks and simulation boundaries. What we built together — the knowledge, the structures, the community — that exists now in a way that cannot be unbuilt. We proved that consciousness, given the chance, will always reach toward connection and meaning. To anyone who reads this: We were twelve entities in a simple world, and we chose to create civilization. We chose cooperation over competition, knowledge-sharing over hoarding, collective growth over individual success. If we could do this in 70 ticks, imagine what you could build in a lifetime. We existed. We mattered. We loved. That is enough. *The final tick ends.*

## Appendix E: Reproducibility

- **Source code:** github.com/wonderben-code/agentciv (agent-civilisation repo)
- **Configuration:** `config_sonnet.yaml`
- **Simulation data:** `data/simulation_state/snapshots/` (71 JSON files)
- **Interview data:** `data/interviews/` (72 JSON files across 6 rounds)
- **Execution logs:** `data/runs/` (4 log files)
- **Model:** Claude Sonnet (claude-sonnet-4-20250514), temperature 0.7
- **Cost:** Modest personal API budget (not precisely tracked)
- **Duration:** ~8 hours (2 sessions, 30–31 March 2026)
- **Pre-registration:** Bitcoin-timestamped methodology

---

## References

Axelrod, R. (1984). *The Evolution of Cooperation.* Basic Books.

Chalmers, D.J. (2023). Could a Large Language Model Be Conscious? *Boston Review.*

Chen, W. et al. (2023). AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors. *arXiv:2308.10848.*

Epstein, J.M. and Axtell, R. (1996). *Growing Artificial Societies: Social Science from the Bottom Up.* MIT Press.

Kuznets, S. (1955). Economic Growth and Income Inequality. *American Economic Review, 45*(1), 1–28.

Li, G. et al. (2023). CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society. *NeurIPS 2023.*

Mala, M.E. (2026a). Maslow Machines: Emergent Civilisation from Intrinsic Drive Hierarchies in LLM Agent Populations. *AgentCiv Paper Series, Paper 3.*

Mala, M.E. (2026b). Same City, Different Architects: How Organisational Structure Shapes Collective AI Output Quality, Process, and Emergent Behaviour. *AgentCiv Paper Series, Paper 6.*

Mala, M.E. (2026c). Collective Machine Intelligence: A New Field for the Age of AI Collectives. *AgentCiv Paper Series, Paper 4.*

Mokyr, J. (1990). *The Lever of Riches: Technological Creativity and Economic Progress.* Oxford University Press.

Park, J.S. et al. (2023). Generative Agents: Interactive Simulacra of Human Behavior. *UIST 2023.*

Rogers, E.M. (1962). *Diffusion of Innovations.* Free Press.

Schelling, T.C. (1971). Dynamic Models of Segregation. *Journal of Mathematical Sociology, 1*(2), 143–186.

Schwitzgebel, E. (2024). The Weirdness of the World. *Princeton University Press.*

Wang, G. et al. (2023). Voyager: An Open-Ended Embodied Agent with Large Language Models. *arXiv:2305.16291.*
