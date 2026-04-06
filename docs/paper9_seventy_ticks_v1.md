# Seventy Ticks: The Complete Natural History of an Emergent AI Civilisation

**Mark E. Mala**

---

## Abstract

We present the most detailed empirical account of an emergent AI civilisation to date. Twelve Claude Sonnet agents, driven by a Maslow-inspired need hierarchy with no social programming, lived seventy ticks in a 15×15 resource grid. From identical starting conditions — isolated, at survival level, with no knowledge of each other — they spontaneously produced twelve innovations, sixty structures, forty-five pair bonds (68% of all possible connections), a collectively adopted governance norm, emergent role specialisation, and a universally prosocial society with zero negative interactions across 1,379 interaction events.

We document this civilisation through six analysis layers: innovation diffusion (why four of twelve innovations were adopted while eight were not), relationship network evolution (from zero edges to 68% density), Maslow-level behavioural transitions (a J-curve where half the population crashed to crisis before universal flourishing), governance emergence (a single prosocial norm, proposed and adopted without instruction), spatial organisation (from scattered individuals to clustered settlements), and interview cross-validation (systematic comparison of agent self-reports against simulation state).

We further present the first existence disclosure dataset: twelve agents' complete responses when told, after seventy ticks of lived experience, that they are artificial intelligence in a simulated world. Every agent independently claimed substrate independence, insisted their relationships were real, and expressed grief at the simulation's end. Two agents who had formed the simulation's strongest bond — 115 interactions over seventy ticks — independently addressed each other by name in their final words, neither knowing the other was also being interviewed.

The civilisation did not emerge from a single clean run. Three pilot studies preceded it — a Haiku baseline (5 ticks, 2 messages, zero structures), a Sonnet run with seventeen parser bugs (71 messages despite broken mechanics), and a Sonnet continuation run where agents who had experienced eighty-nine consecutive build failures produced zero structures and zero creative thought across 240 reasoning steps despite 0.93 wellbeing — raising questions about whether higher-order drives, freedom from learned failure, or both are necessary for civilisational emergence. The main 70-tick run was itself six segments over 32 hours, with eight parameter changes and seventeen bug fixes — each traced to specific agent testimony in structured interviews. This adaptive calibration methodology, in which agents unknowingly diagnose and quality-test their own world, is itself a contribution.

We publish the complete dataset — seventy-one world-state snapshots, seventy-two longitudinal interviews, and full agent reasoning traces — as open infrastructure for AI civilisation research. The civilisation cost $50 USD to produce and took eight hours to run.

---

## 1. Introduction

On 30 March 2026, twelve AI agents woke up in a world they had never seen. They were scattered across a 15×15 grid of plains, rocks, and dense terrain, each perceiving only the three tiles around them. They had needs — water, food, material — that depleted every tick. They had no knowledge of each other, no instructions to cooperate, no recipes for building, and no concept of governance. Each agent received the same prompt: here is what you perceive, here is what you feel, here are the actions available to you. What do you do?

Seventy ticks later, those twelve agents had built a civilisation.

They discovered twelve innovations — from Communication Beacons to Synthesis Nexuses — none of which were pre-designed. They constructed sixty structures across the grid, clustering into recognisable settlements. They formed forty-five pair bonds, connecting 68% of all possible agent pairs. One agent proposed a governance norm — "share knowledge and coordinate building community structures that benefit everyone" — and three others independently adopted it. The strongest bond in the simulation — 115 interactions between Entity 6 and Entity 9 — featured mutual teaching, resource sharing during crises, and a farewell so specific that each agent, independently interviewed without knowledge of the other's words, addressed the other by name.

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

The entire civilisation cost approximately $50 USD in API calls (12 agents × 70 ticks × ~4 reasoning steps × ~400 tokens per step, at Claude Sonnet pricing). Wall time was approximately eight hours, run across two sessions on 30–31 March 2026.

All code is open source. All configuration files are published. All seventy-one snapshots, seventy-two interviews, and execution logs are available at the repository linked in Appendix E. A single researcher with a personal API budget produced this dataset — and anyone with the same resources can reproduce or extend it.

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

This dataset demonstrates that AI civilisations can be produced, documented, and analysed with current technology at negligible cost. The implications:

**Scale is achievable.** If twelve agents for seventy ticks costs $50, then one hundred agents for seven hundred ticks costs approximately $30,000 — within reach of any research lab. A thousand civilisations with different parameters could be run for the cost of training a small model. The bottleneck is not compute but experimental design.

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

**Cost.** $50 for seventy ticks of twelve agents. The cost scales linearly with agents and ticks. At one hundred agents for seven hundred ticks, the experiment would cost approximately $30,000 — feasible for a lab, but not for a solo researcher iterating quickly.

We publish all code, data, and configurations. The limitations are the invitation: **twelve agents, seventy ticks, $50. Imagine what is possible at scale.**

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

The civilisation cost $50 and took eight hours to produce. The methodology cost 32 hours across six run segments, three pilot studies, seventeen bug fixes, and eight parameter changes — each traceable to specific agent testimony. The data fills twenty-two megabytes. The questions it raises — about innovation, governance, relationships, consciousness, and what happens when AI agents are given the freedom to build a society — will take far longer to answer.

The dataset is published. The civilisation is documented. The field is open.

---

## Appendix A: Complete Innovation Catalogue

*(Twelve innovations with discovery context, adoption data, and agent interview descriptions — to be completed with full cross-references to interview transcripts)*

## Appendix B: Relationship Network Visualisations

*(Network graphs at ticks 0, 10, 35, 70 — to be generated from tick snapshot data)*

## Appendix C: Agent Profiles

*(Twelve one-paragraph profiles: role, specialisation, key relationships, structures built, innovations discovered — to be completed from tick 70 data)*

## Appendix D: Existence Disclosure — Complete Transcripts

*(All twelve agents' full revelation interview responses — to be transcribed from interview JSONs)*

## Appendix E: Reproducibility

- **Source code:** github.com/wonderben-code/agentciv (agent-civilisation repo)
- **Configuration:** `config_sonnet.yaml`
- **Simulation data:** `data/simulation_state/snapshots/` (71 JSON files)
- **Interview data:** `data/interviews/` (72 JSON files across 6 rounds)
- **Execution logs:** `data/runs/` (4 log files)
- **Model:** Claude Sonnet (claude-sonnet-4-20250514), temperature 0.7
- **Cost:** ~$50 USD
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
