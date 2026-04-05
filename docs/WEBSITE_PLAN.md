# AgentCiv Website — Master Plan

**Created:** 4 April 2026
**Author:** Ekram Alam & Claude
**Quality bar:** Apple × DeepMind × Stripe. Top 0.00000001%.
**Style reference:** `APPLE_STYLE_GUIDE.md` (same directory)
**Aesthetic:** Bright, expansive, hopeful. Warm cream palette. NOT dark cinematic — Apple is light.
**Wing 1 name:** "Collective Intelligence" (not "The Science" — too generic for a new field)

---

## The Vision

One domain. Four wings. Four extraordinary things.

AgentCiv isn't a tool, a paper, or a simulation. It's a body of work — the kind of thing Anthropic, DeepMind, and OpenAI produce. The website communicates that scale.

**The principle:** Each wing is its own Apple product page. Each one is independently mind-blowing. Nobody clicks "The Simulation" because it supports the Engine — they click it because *12 AI agents building a civilisation from scratch* is one of the most extraordinary things anyone has done with AI.

---

## Architecture: Four Wings

```
                           agentciv.ai
                               |
           +----------+--------+--------+----------+
           |          |        |        |          |
     The Science  The Sim   The Engine  Creator Mode
     (New Field) (AI Civs) (Dev Tool)  (AI Explores)
```

### The Four Products

Think iPhone, Mac, iPad, and Vision Pro on apple.com. Each is exciting in its own right. Each makes you want to click. Each represents a step toward greater AI autonomy:

| Wing | Tagline | The Excitement |
|------|---------|---------------|
| **The Science** | "A new field of AI." | 5 papers. 9 dimensions nobody mapped before. Computational Organisational Theory — we named it. |
| **The Simulation** | "They built a civilisation." | 12 agents. No instructions. Emergent governance, innovation, culture. Watch it happen. |
| **The Engine** | "Your agents. Your rules." | The first dev tool where organisational structure is a design parameter. 13 structures. pip install and go. |
| **Creator Mode** | "AI that spawns civilisations." | An AI that designs, runs, and evolves its own AI civilisations. The field explores itself. |

### The Narrative Arc

Each wing represents a step in the same story — each independently extraordinary:

| Step | Wing | Human–AI Relationship |
|------|------|-----------------------|
| 1 | The Science | Human defines the field |
| 2 | The Simulation | Human configures, AI acts |
| 3 | The Engine | Human directs, AI builds |
| 4 | Creator Mode | AI explores autonomously |

### Why Four Wings

| Structure | Problem |
|-----------|---------|
| Three wings (no Creator Mode) | Misses the frontier. Stops at "humans use AI" when the logical conclusion is "AI explores AI." |
| **Science + Simulation + Engine + Creator Mode** | **Four independently extraordinary things. Together, a body of work that goes from defining a field to letting the field explore itself. Nobody else in AI has this arc.** |

### Navigation

Peer-level. Equal weight. Every name makes you want to click.

```
[AgentCiv]    Collective Intelligence    The Simulation    The Engine    Creator Mode    [★ GitHub]
```

No nesting. No dropdowns. Four peers, always visible. GitHub star count in the nav as social proof.

---

## Homepage

### Design Philosophy

The homepage is the umbrella. It doesn't belong to any wing — it's the moment where visitors see the full scope and pick what excites them most.

Dark mode. Cinematic. Generous whitespace. One typeface, three weights. Scroll-triggered reveals. Every viewport has exactly one idea.

---

### Section 1: Hero

*Full viewport. Dark. Centred.*

**Headline:**
> What happens when AI agents form civilisations?

**Subline:**
> A new field of AI. A simulation that shocked us. A tool that changes everything. An AI that explores the field itself.

**Four cards** (evenly spaced, each a mini-hero):

| The Science | The Simulation | The Engine | Creator Mode |
|-------------|---------------|------------|-------------|
| *An entirely new field of AI research. 5 papers. 9 dimensions nobody mapped before.* | *12 AI agents. No instructions. They built a civilisation with governance, innovation, and culture.* | *The first dev tool where AI agents design their own team. 13 structures. pip install and go.* | *An AI that designs, spawns, and evolves its own AI civilisations. The field explores itself.* |
| Explore the science > | Watch it happen > | Get started > | See the frontier > |

Each card has a striking visual — a paper figure, a simulation frame, a terminal screenshot, an architecture diagram. Hover brightens the card. The energy: "all four are incredible, pick one."

**Background:** Subtle, slow animation — abstract nodes forming connections, clustering, reorganising. Not literal agents — abstract, elegant, suggestive of emergence.

---

### Section 2: The Field Map — Interactive Ecosystem Visual

*Scroll-triggered build animation. Interactive. The conceptual map of the entire field.*

**Purpose:** After the four cards show each product independently, the Field Map reveals how the entire ecosystem connects. The cards create excitement about individual products. The map creates the "oh" moment — *these aren't four separate projects, they're one coherent body of work where each piece enables the others.*

**Why it matters:** Without this, a visitor picks one wing and explores it. With it, they understand the whole picture and want to explore ALL wings. The map is a second navigation path: the cards say "pick what excites you," the map says "understand the whole picture and navigate from understanding."

**Design: The Spectrum, Not Two Boxes**

The centrepiece is a continuous gradient — warm/organic (left, emergence) to cool/structured (right, direction). NOT two boxes. A flowing continuum that makes the dual-output thesis visible: every directed civilisation produces emergence, every emergent civilisation can be loosely directed. The Simulation and Engine are points on this spectrum, not endpoints. The line extends past both — faded space at the edges says "there's more."

```
                         ┌─────────────────────────┐
                         │   CMI — The Field        │
                         │  (5 unbounded axes → ∞)  │
                         └────────────┬────────────┘
                                      │
                         ┌────────────┴────────────┐
                         │     Creator Mode         │
                         │  Spawns civilisations    │
                         │  across the full space   │
                         └──┬────────┬────────┬────┘
                            │        │        │
                            ▼        ▼        ▼
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ◀━━━━━━━━━━━━━━━━━━━━ The Spectrum ━━━━━━━━━━━━━━━━━━━━▶   ║
    ║                                                               ║
    ║   Emergence                                      Direction    ║
    ║   "What do they produce                "What do they produce  ║
    ║    on their own?"                       when pointed at a     ║
    ║        ●                                 task?"               ║
    ║     Simulation                              ●                 ║
    ║                                           Engine              ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
                                      │
                         ┌────────────┴────────────┐
                         │  COT — The Method        │
                         │  9 dimensions.            │
                         │  Configuration as science. │
                         └─────────────────────────┘
```

**Interactive behaviour:**

- **Build animation on scroll:** Four product nodes appear first (familiar from the cards). Then connections draw themselves — lines flowing between them, Creator Mode rising above, CMI wrapping everything, COT threading through. The visitor watches the ecosystem assemble. The build sequence IS the narrative.
- **Hover on any node:** Expands with a one-line description + "Enter this wing →". The connections from that node light up, showing its relationships.
- **Hover on the spectrum:** A tooltip follows the cursor: far left = "Civilisations with no task — pure exploration of what emerges." Middle = "Hybrid — a goal with room for emergence." Far right = "Civilisations optimised for a specific task."
- **Particle flow between emergence and direction:** Subtle dots flowing from the directed side back toward emergence — visualising that even directed collectives produce emergent creations. The dual-output thesis, animated.
- **Creator Mode lines:** Cascade to multiple points across the ENTIRE gradient, not just the two endpoints. It explores the whole space.
- **Five axes radiating from CMI boundary:** Scale, Intelligence, Configuration, Application, Emergence. Each arrow extends to ∞. The map is explicitly a slice of something unbounded.
- **Click any node:** Enter that wing.
- **Paper icons (1-5):** Positioned near the concepts they established. Hover shows title. Click goes to Science wing.

**Anti-pigeon-hole design:**
- Spectrum is a gradient, not two boxes
- Faded space extends past both primitives — "there's more"
- Label near spectrum: *"One phenomenon. Many ways to explore it."*
- Creator Mode reaches the whole space, not just endpoints
- Five axes going to ∞ — the map is a tiny slice of something infinite
- The notation "and beyond" appears subtly at the edges

**Implementation:** Programmatic SVG + CSS animations + JS interactivity. Scientific diagram meets Apple product page. Clean lines, generous space, subtle animation, precise typography. React component, ~300-400 lines. Dark background, subtle glow on the gradient, smooth hover states.

---

### Section 3: Highlights

*Scroll-triggered. Sequential reveal. Full-width cards.*

Independent wow moments. Not a narrative — reasons to explore further:

1. **"We mapped a design space nobody knew existed."**
   *Visual: The 9-dimension framework rendered as an elegant abstract space.*

2. **"They formed a government. Nobody told them to."**
   *Visual: A frame from the simulation showing emergent governance structures.*

3. **"Agents that debate, vote, and restructure their own team — live."**
   *Visual: Rich terminal output showing --org auto in action.*

4. **"An AI that designs civilisations, runs them, and discovers what emerges."**
   *Visual: The Creator Mode architecture — meta-agent spawning and analysing civilisations.*

---

### Section 4: Proof Strip

*Horizontal. Minimal. Confident. Numbers large, labels small.*

```
5 Papers  ·  9 Dimensions  ·  13 Team Structures  ·  1 New Field  ·  ∞ Civilisations
```

---

### Section 5: Featured Moment

One stunning visual — the single most shareable image from the project. The "screenshot moment."

Candidates:
- The --org auto restructuring vote in the rich terminal
- A fishbowl replay frame showing 12 agents self-organising
- The experiment comparison table showing radically different outcomes

Caption: a single sentence. The visual does the work.

---

### Section 6: Footer

Links to all three wings, GitHub, whitepaper PDF, how to cite, about/contact.

---

## Wing 1: The Science

**URL:** `/science`
**Tagline:** "A new field of AI."
**Energy:** Discovering a breakthrough. Like reading about CRISPR for the first time — but presented with Apple's visual craft.
**Audience:** Researchers, thought leaders, press, the intellectually curious.
**Tone:** DeepMind's gravitas meets Apple's clarity. Authoritative. Exciting. Never dry.

---

### Section 1: Hero

*Full viewport. Dark. Centred.*

**Eyebrow:** The Science

**Headline:**
> A New Field of AI.

**Subline:**
> Computational Organisational Theory — the empirical study of how AI agents organise, and why it changes everything.

**Background:** Slow-morphing abstract visualisation of the 9-dimensional configuration space. Mathematical. Beautiful. Suggesting vast unexplored territory.

---

### Section 2: The Breakthrough

*One viewport. Dark. The crown jewel — position 2.*

**Two lines, large, centred:**

> Every multi-agent AI system ever built uses one organisational structure.
> We discovered there are thousands.

**Visual:** One dot labelled "what everyone else uses" vs an enormous cloud labelled "the actual design space." This is the moment.

---

### Section 3: Nine Dimensions

*Interactive. Light background. The depth layer.*

**Eyebrow:** The Framework

**Headline:**
> 9 dimensions. Infinite arrangements.

Not a product feature — an intellectual discovery. A new periodic table.

| Dimension | Spectrum | Expandable |
|-----------|----------|------------|
| Authority | hierarchy → flat → distributed → rotating → consensus → anarchic | What this means, why it matters, real examples |
| Communication | hub-spoke → mesh → clustered → broadcast → whisper | ... |
| Roles | assigned → emergent → rotating → fixed → fluid | ... |
| Decisions | top-down → consensus → majority → meritocratic → autonomous | ... |
| Incentives | collaborative → competitive → reputation → market | ... |
| Information | transparent → need-to-know → curated → filtered | ... |
| Conflict | authority → negotiated → voted → adjudicated | ... |
| Groups | imposed → self-selected → task-based → persistent → temporary | ... |
| Adaptation | static → evolving → cyclical → real-time | ... |

**Below the explorer:**
> 9 dimensions. Each with 4-6 values. Thousands of unique organisational arrangements — most of which have never existed in human history. Humans can't restructure organisations in real time. AI agents can.

---

### Section 4: The Papers

*Dark. Apple chapter pattern. Each paper is a product launch, not an academic citation.*

**Eyebrow:** Publications

**Headline:**
> Four papers. One new field.

Each paper:

```
────────────────────────────────────────────────────
PAPER [N]

[Title — large, bold]
Mark E. Mala

[One-paragraph plain-English summary — what was discovered, why it matters]

[Visual: key figure or diagram from the paper]

Bitcoin blockchain proof: block #943474
Independently verifiable. Irrefutable. Permanent.

Read the full paper >    Cite this >
────────────────────────────────────────────────────
```

Papers in order (check actual titles):
1. Paper 1: The original simulation paper
2. Paper 2: [TBD]
3. Paper 3: [TBD]
4. **Paper 4: "Collective Machine Intelligence"** — extra prominence. Key claims pulled as large-text quotes. The crown jewel of the Science wing.

---

### Section 5: Collective Machine Intelligence

*Full chapter. Dark. The Big Idea — standing on its own, not nested under a paper.*

**Eyebrow:** The Big Idea

**Headline:**
> AI civilisations as a new mode of production.

**Three statements, spaced vertically, large:**

> The entire AI industry builds better individual models.
> We asked a different question: what happens when you organise them into societies?
> Something fundamentally new emerges. We named it Collective Machine Intelligence.

**Visual:** Directed intelligence (one model, one output) vs collective intelligence (many models, emergence, the whole greater than the sum). The dual output thesis.

**Expandable:** How CMI differs from ensemble methods, swarm intelligence, and multi-agent RL. Why it's a genuinely new concept.

---

### Section 6: Open Research Directions

*Light background. Future-facing.*

**Eyebrow:** What's Next

**Headline:**
> The field is open. These questions are waiting.

Every direction is a future paper. Presented as exciting opportunities:

- **Inter-civilisation interaction** — "What happens when two differently-organised AI societies meet?"
- **Human-AI mixed teams** — "Put humans inside the configurable structure. What changes?"
- **Organisational transfer learning** — "Does the optimal structure for one task inform another?"
- **Adversarial testing** — "Which structures resist manipulation? Which are fragile?"
- **Domain-specific presets** — "The optimal structure for scientific research. Creative writing. Security auditing."
- **Cost-optimal organisation** — "For a fixed compute budget, which structure maximises output?"
- **Cultural emergence** — "Do long-running AI societies develop persistent culture?"
- **Cross-framework standards** — "Organisational structure as a universal protocol."
- **Institutional memory** — "Agents that remember across projects. Knowledge that persists."

Each expands to 2-3 sentences.

---

### Section 7: Provenance

*Dark. Trust.*

**Eyebrow:** Provenance

**Headline:**
> Timestamped. Permanent. Verify it yourself.

One paragraph: what Bitcoin blockchain timestamps mean, why they matter, how anyone can verify independently.

Key timestamps:
- Paper 4: Block 943474
- Engine codebase: Block 943474
- Simulation data: [block number]

> You don't have to trust us. You can verify everything yourself.

Verification instructions >

---

### Section 8: How to Cite

**Eyebrow:** Citation

**Headline:**
> Using this work? Here's how to cite it.

BibTeX and plain text. One-click copy.

```bibtex
@article{mala2026collective,
  title={Collective Machine Intelligence: A New Field for the Age of AI Collectives},
  author={Mala, Mark E.},
  year={2026},
  note={Bitcoin blockchain timestamp: block 943474}
}
```

```bibtex
@software{mala2026agentciv,
  title={AgentCiv Engine: Organisational Arrangement as a Design Parameter},
  author={Mala, Mark E.},
  year={2026},
  url={https://github.com/wonderben-code/agentciv-engine}
}
```

---

### Section 9: Final CTA

*Full viewport. Dark. Three paths.*

**Headline:**
> A new field of AI is here.

Three links:
- Explore the simulation >
- Try the engine >
- Read the papers >

---

## Wing 2: The Simulation

**URL:** `/simulation`
**Tagline:** "They built a civilisation."
**Energy:** Watching a nature documentary about something nobody has ever seen. Like the first footage from the deep ocean. Awe. Curiosity. "I need to see more."
**Audience:** Everyone. The most universally exciting wing.
**Tone:** Nature documentary meets Apple keynote. Wonder, not analysis.

---

### This Is the Existing Site (Elevated)

The current agentciv.ai (17 pages, React + Vite + Tailwind) IS this wing. The content is already extraordinary — Fishbowl, Journey, Highlights, Agent Interviews. What changes: the framing, the entry point, and every headline and description gets the Apple treatment.

---

### Section 1: Hero

*Full viewport. Dark. Cinematic.*

**Eyebrow:** The Simulation

**Headline:**
> Twelve agents. Zero instructions. They built a civilisation.

**Subline:**
> Emergent governance. Spontaneous innovation. Culture that nobody programmed. Watch it happen.

**Visual:** The most stunning frame from the Fishbowl — agents clustered in emergent groups, visible social structures. Full-bleed. Cinematic.

**CTAs:**
Watch the simulation >    Explore the highlights >

---

### Section 2: What Emerged

*Three cards. The crown jewel — position 2. Light background.*

**Eyebrow:** What Emerged

**Headline:**
> Nobody told them to cooperate.

Three cards, each with a visual and a bold statement:

| They formed a government. | Innovation accelerated. | They developed relationships. |
|---------------------------|------------------------|------------------------------|
| Without any instruction, agents created rules, voting systems, and collective decision-making. From nothing. | Each breakthrough enabled the next. Accelerating returns — emergent, not programmed. | Agents formed bonds and preferentially worked with partners they'd succeeded with before. Trust, from scratch. |
| See the governance > | See the acceleration > | See the bonds > |

---

### Section 3: Explore

*Light background. Navigation grid.*

**Eyebrow:** Go Deeper

**Headline:**
> Every angle. Every detail. All real.

A grid of cards linking to existing pages:

| Page | Card Description |
|------|-----------------|
| **Fishbowl** | "Watch it live. Full replay of the entire simulation, tick by tick." |
| **Highlights** | "30 extraordinary moments. Curated like a nature documentary." |
| **The Journey** | "From strangers to a functioning society. The complete arc." |
| **Agent Interviews** | "We asked the agents what they were thinking. Their answers are remarkable." |
| **Data Explorer** | "Every data point. Every tick. The raw truth, for researchers." |
| **How It Works** | "Maslow drives. ReAct loops. Custom-built from scratch." |
| **The Science** | "Why this happened. What it means. The analysis." |
| **Methodology** | "How we ran it. How to reproduce it. Full transparency." |
| **Chronicler** | "The complete event log. Every action, every decision." |
| **Observations** | "Patterns that surprised us. Honest analysis." |
| **Ethics** | "What it means to build AI societies. The questions we're asking." |

---

### Section 4: Run Your Own

*Full viewport. Dark. CTA.*

**Eyebrow:** Your Turn

**Headline:**
> Don't just watch. Run your own.

**Body:**
> The AgentCiv Engine lets you spawn your own AI civilisations with any organisational structure. Same technology. Your rules.

Try the Engine >

---

### Integration Approach

1. **New global nav** replaces current — adds Science and Engine links
2. **New landing page** (`/simulation`) with hero and navigation cards
3. **Existing pages** keep routes but under `/simulation/*` prefix
4. **Redirects** from old routes (Netlify `_redirects`)
5. **Footer** updated to include all three wings
6. **Apple copy pass** on every existing page's headlines and descriptions

Not rebuilding the simulation site — giving it a new front door, connecting it to the other wings, and elevating the copy.

---

## Wing 3: The Engine

**URL:** `/engine`
**Tagline:** "Your agents. Your rules."
**Energy:** Apple product launch. Linear's confidence. Vercel's developer focus. Every section makes you want to install it immediately.
**Audience:** Developers (primary), researchers (secondary), thought leaders (tertiary).
**Tone:** Premium. Confident. Dark-mode. Every section is a chapter.

---

### Section 1: Hero

*Full viewport. Dark. Centred.*

**Eyebrow:** The Engine

**Headline:**
> Your agents. Your rules. Thirteen ways to organise.

**Subline:**
> The first open-source dev tool where organisational structure is a design parameter.

**Two CTAs (Vercel pattern):**

```
[pip install agentciv-engine] [copy]     [★ Star on GitHub]
```

**Below:** Terminal recording — a real run. The actual rich terminal output from the Excellence Phase. Agents claiming tasks, communicating, merging. 10-15 seconds, looping. Not mocked.

---

### Section 2: The Problem

*One viewport. Dark. Text IS the visual. Large type, generous spacing.*

**Eyebrow:** The Problem

**Headline:**
> Every framework chose for you.

**Body (large, centred):**

> CrewAI: hierarchical. AutoGen: conversation. LangGraph: graph.
> Every multi-agent framework hard-codes one coordination strategy.
> What if the organisational structure itself was the variable?

---

### Section 3: Thirteen Structures

*Interactive. Light background.*

**Eyebrow:** Presets

**Headline:**
> 13 ways to organise an AI team.

Interactive grid. Each structure is a card:

```
+---------------------+
|  COLLABORATIVE      |
|                     |
|  Flat. Open.        |
|  Emergent roles.    |
|  Everyone sees      |
|  everything.        |
|                     |
|  See the config >   |
+---------------------+
```

Clicking a card expands to show:
- Org dimension values for this preset
- Visual communication topology
- Plain-English description of how agents behave
- Terminal output snippet

**The 13th card — `auto` — is golden:**
```
+-----------------------------+
|  ★ AUTO                     |
|                             |
|  Agents design their own    |
|  team structure. They       |
|  propose, vote, and         |
|  restructure — live.        |
|                             |
|  See it in action >         |
+-----------------------------+
```

---

### Section 4: The Crown Jewel — Auto Mode

*Full chapter. Dark. The "oh wow" moment. Apple chapter treatment.*

**Eyebrow:** Self-Organisation

**Headline:**
> Set the goal. They design the team.

**Visual:** Terminal recording of auto mode:
1. Agents start work
2. Meta-tick: an agent proposes restructuring
3. Agents debate and vote
4. Restructure adopted (the golden panel)
5. Work resumes under new structure

**Body (large):**
> In auto mode, agents propose changes to their own organisational structure, debate them, vote, and restructure in real time. Authority, communication, roles, decisions — everything evolves based on what the agents discover works.

**Expandable depth:**
- How meta-ticks work
- The voting mechanism
- How auto mode learns from past runs
- Real data from battle-test runs

---

### Section 5: Nine Dimensions

*Interactive explorer. Light background.*

**Eyebrow:** Configuration

**Headline:**
> 9 dimensions. Every combination is a different society.

Interactive widget — 9 selectors. As you change values, a live preview updates:

```
Authority:      [hierarchy] [flat] [distributed] [rotating] [consensus] [anarchic]
Communication:  [hub-spoke] [mesh] [clustered] [broadcast] [whisper]
Roles:          [assigned] [emergent] [rotating] [fixed] [fluid]
...

Your configuration:
  "A flat team where everyone communicates directly,
   roles emerge naturally, and decisions are by consensus."

agentciv solve --task "..." \
  --override authority=flat \
  --override communication=mesh \
  --override roles=emergent \
  --override decisions=consensus
```

Community-expandable: add your own dimensions, values, and presets with a YAML file.

---

### Section 6: Features

*Apple chapter pattern. Scroll through. Each follows: Eyebrow → Headline → Significance → Proof → Expandable.*

---

**Chapter: Git Isolation**

- **Eyebrow:** Parallel Work
- **Headline:** Every agent. Their own branch.
- **Significance:** Real parallel development, not turn-taking. Every agent works in isolation with automatic merging at tick end.
- **Proof:** Conflict detection, contention warnings via attention map, configurable merge strategies.
- **Plain English:** Like giving each developer their own branch. The engine handles merging.

---

**Chapter: Experiment Mode**

- **Eyebrow:** Research
- **Headline:** Same task. Different teams. Measurable truth.
- **Significance:** The first A/B testing framework for AI team structures.
- **Proof:** Run the same task under collaborative, hierarchical, and auto mode. Statistical comparison, JSON export, research-grade data.
- **Visual:** The experiment comparison table from a real run.
- **Plain English:** Same task, different structures, real outcomes. One command.

---

**Chapter: Chronicle**

- **Eyebrow:** Data
- **Headline:** Every run. A complete record.
- **Significance:** Every action, communication, decision, and restructure — captured automatically.
- **Proof:** Per-agent contributions, communication patterns, timeline of key moments, merge statistics, organisational evolution. JSON export.
- **Plain English:** Who did what. Who talked to whom. What changed. All of it.

---

**Chapter: Gardener Mode**

- **Eyebrow:** Control
- **Headline:** Shape conditions. Don't command.
- **Significance:** Intervene mid-run without breaking emergence. You're the gardener, not the boss.
- **Proof:** Message injection, task redirection, forced meta-ticks, live parameter adjustment — all while agents continue working.
- **Plain English:** Nudge. Redirect. Observe. The agents do the rest.

---

**Chapter: Learning**

- **Eyebrow:** Intelligence
- **Headline:** Every run makes it smarter.
- **Significance:** Auto mode consults history from past runs, matching similar tasks to proven structures.
- **Proof:** Similarity matching across task descriptions, accumulated outcome data, structure recommendation generation.
- **Plain English:** The more you use it, the better it gets at choosing the right structure.

---

**Chapter: Specialisation & Relationships**

- **Eyebrow:** Memory
- **Headline:** Skills develop. Partnerships form.
- **Significance:** Agents build specialisation through practice and remember who they work well with.
- **Proof:** Skill tracking, relationship scoring, preference weighting, relationship decay over time.
- **Plain English:** Like a real team. Expertise develops. Partnerships form. Trust accumulates.

---

### Section 7: Two Modes

*Side by side. Light background.*

**Eyebrow:** Modes

**Headline:**
> Two ways in. Zero friction either way.

```
+---------------------------+---------------------------+
|       MAX PLAN            |          API              |
|                           |                           |
|  Inside Claude Code       |  CLI: agentciv solve      |
|  or Cursor via MCP        |                           |
|                           |                           |
|  Free (uses your          |  Pay per token            |
|  existing subscription)   |  (your API key)           |
|                           |                           |
|  Your AI assistant        |  Engine makes its         |
|  drives agent cognition   |  own LLM calls            |
|                           |                           |
|  Best for:                |  Best for:                |
|  Everyday use             |  Research & experiments   |
|                           |                           |
|  Set up Max Plan >        |  Get started with API >   |
+---------------------------+---------------------------+
```

---

### Section 8: Code Sample

*Stripe pattern. Left: code. Right: output.*

**Eyebrow:** Try It

**Headline:**
> Three commands. Then launch.

**Left (code, syntax highlighted, copy button):**
```bash
pip install agentciv-engine
agentciv setup
agentciv solve \
  --task "Build a REST API with /hello and /status" \
  --org collaborative \
  --agents 2 \
  --max-ticks 3
```

**Right (rich terminal output, recreated in HTML/CSS):**
```
── tick 1 ──────────────────────────
  Atlas  claimed  Build REST API endpoints
  Nova   claimed  Write comprehensive tests
  Atlas  created  server.py
  Nova   created  test_server.py

── tick 2 ──────────────────────────
  Atlas → Nova  : Here's the architecture...
  Nova  → Atlas : Tests ready, merging...

── tick 3 ──────────────────────────
  ✓ All 4 tests pass
```

---

### Section 9: Real Results

*Light background. Evidence.*

**Eyebrow:** Results

**Headline:**
> Built by agents. Verified by tests.

2-3 real examples of tasks completed by agent teams:

| Task | Org | Agents | Ticks | Result |
|------|-----|--------|-------|--------|
| REST API | collaborative | 2 | 3 | 4 passing tests |
| Key-value store | auto | 3 | 5 | 53 passing tests |
| Calculator module | experiment | 3×2 | 5 | Collaborative vs hierarchical |

Each with: task, org, agents, ticks, result, key moments.

---

### Section 10: The Research Connection

*Dark. Connecting back to the other wings.*

**Eyebrow:** Foundation

**Headline:**
> Built on research. Grounded in evidence.

**Body:**
> This isn't just code. It implements the framework described in 5 papers that define a new field of AI. Every design decision is grounded in empirical evidence from the AgentCiv simulation — where 12 agents built a civilisation from nothing.

Links:
- The Science > (papers and framework)
- The Simulation > (watch the evidence)
- Read the whitepaper > (direct PDF)

---

### Section 11: Getting Started

*Light background. Ultra-simple. Zero friction.*

**Eyebrow:** Start

**Headline:**
> From zero to agents in sixty seconds.

```
1. Install
   pip install agentciv-engine

2. Set up
   agentciv setup

3. Go
   "Use agentciv to build a REST API with a meritocratic team"
```

> That's it. Three commands and you're running agent teams.

For API mode: show the `export ANTHROPIC_API_KEY` step.

---

### Section 12: Open Source + GitHub + Provenance

*Three columns. Light background.*

**Left: Open Source**
- MIT License
- "Built for the community. Every preset is a YAML file. Every dimension is expandable. Fork it, extend it, make it yours."
- Contributing guide >

**Centre: GitHub**
- Live star count
- Direct repo link
- Recent commit activity
- "Built in public. Every commit timestamped."

**Right: Provenance**
- "Every line of code — Bitcoin blockchain-timestamped."
- Key block numbers
- "Independently verifiable. Irrefutable. Permanent."
- Verification instructions >

---

### Section 13: How to Cite

**Eyebrow:** Citation

**Headline:**
> Using the engine? Here's how to cite it.

```bibtex
@software{mala2026agentciv,
  title={AgentCiv Engine: Organisational Arrangement as a Design Parameter for Multi-Agent AI Systems},
  author={Mala, Mark E.},
  year={2026},
  url={https://github.com/wonderben-code/agentciv-engine},
  note={Bitcoin blockchain provenance: block 943474}
}
```

One-click copy.

---

### Section 14: Final CTA

*Full viewport. Dark.*

**Headline:**
> The first tool where AI agents design their own team.

**Three CTAs:**
```
[pip install agentciv-engine]    [★ Star on GitHub]    [Read the whitepaper]
```

---

## Wing 4: Creator Mode

**URL:** `/creator`
**Tagline:** "AI that spawns civilisations."
**Energy:** The frontier. The moment AI stops being the tool and starts being the explorer. This is the "oh my god, what's next" wing. The one that makes people realise the implications of everything else.
**Audience:** Researchers (primary), thought leaders (secondary), developers (tertiary), press/media (this is the headline).
**Tone:** Visionary but grounded. Not sci-fi speculation — this is built, this works, here's what it found. Apple's confidence meets DeepMind's ambition.

**Concept document:** `docs/CREATOR_MODE.md` (Bitcoin timestamped 4 April 2026)

---

### Section 1: Hero

*Full viewport. Dark. The most dramatic hero on the site.*

**Eyebrow:** Creator Mode

**Headline:**
> AI that designs its own civilisations.

**Subline:**
> An autonomous system that spawns AI societies, observes what emerges, and evolves the next generation. The field explores itself.

**Visual:** The architecture diagram — a meta-agent at the top, spawning civilisation runs below, analysis flowing back up, next generation flowing down. Animated: civilisations spawn, data flows, new civilisations spawn. The loop is visible.

---

### Section 2: The Insight

*One viewport. Dark. Text IS the visual.*

**Eyebrow:** The Bottleneck

**Headline:**
> The human is the bottleneck.

**Body (large, centred):**

> A human chooses the configuration. A human picks the task. A human reads the results. A human decides what to try next.
> The possibility space is infinite. No human could explore it.
> Creator Mode removes the human from the loop.

---

### Section 3: Three Axes

*Light background. Three cards — the crown jewel position.*

**Eyebrow:** What It Does

**Headline:**
> Three modes. One autonomous explorer.

| Tasks | Emergence | The Field |
|-------|-----------|-----------|
| Given a complex project, Creator Mode finds the optimal organisational configuration by actually running teams and comparing outcomes. Automated organisational search. | Creator Mode designs civilisations to explore the conditions that produce the richest emergence. It varies environment, drives, scale, configuration — and discovers what nobody would think to try. | The research flywheel, fully automated. AI runs experiments, analyses data, designs follow-ups, discovers patterns. It does in days what human researchers take years to explore. |
| "Find the best way to build this." | "Find what produces the most interesting emergence." | "Explore the field itself." |
| Learn more > | Learn more > | Learn more > |

---

### Section 4: The Self-Referential Thesis

*Full chapter. Dark. The philosophical depth.*

**Eyebrow:** The Deeper Story

**Headline:**
> Each layer emerged from the previous.

**Four statements, spaced vertically:**

> A simulation was built. Humans configured AI agents.
> The simulation inspired an engine. Humans directed AI teams.
> The engine enabled configurable civilisations. Humans designed, AI built.
> Creator Mode. AI designs, AI builds, AI analyses, AI evolves.

**Body:**
> Creator Mode is the point where the field becomes self-exploring — where AI doesn't just operate within CMI, it pioneers CMI itself. This connects to the deepest thesis of Collective Machine Intelligence: that AI civilisations represent a new mode of production. Creator Mode is the moment that mode of production becomes self-directing.

---

### Section 5: How It Works

*Light background. Technical depth.*

**Eyebrow:** Architecture

**Headline:**
> The meta-agent. The orchestration layer above everything.

**Architecture diagram (interactive):**

```
┌─────────────────────┐
│    CREATOR MODE      │
│    (Meta-Agent)      │
│                      │
│  Receives a goal     │
│  Reasons about what  │
│  to try              │
└──────────┬──────────┘
           │
    Spawns civilisations
           │
    ┌──────┼──────┐
    │      │      │
  Civ 1  Civ 2  Civ N
    │      │      │
    └──────┼──────┘
           │
    Analyses results
    Designs next generation
           │
         Loop
```

**Expandable details:**
- Goal types: explore emergence, solve a project, map the space
- Configuration generation: intelligent sampling, not brute force
- Analysis: structured comparison, pattern recognition, novelty detection
- Learning: Bayesian-style search over the 9-dimensional space
- Budget management: token/compute limits, convergence detection

---

### Section 6: Results Preview

*Dark. Evidence.*

**Eyebrow:** Discovery

**Headline:**
> What it finds.

**Body:**
> Creator Mode explored 847 configurations overnight. It identified three unexplored regions of the possibility space that produce unprecedented emergence. It found that civilisations with rotating authority and whisper communication develop governance 4x faster than any configuration a human has ever tried.

*(Placeholder — real results will replace this once Creator Mode is built and run.)*

**Expandable:** Discovery catalogue, configuration space visualisation, comparison to human-directed exploration.

---

### Section 7: The Paper

*Light background.*

**Eyebrow:** Paper 5

**Headline:**
> Self-Exploring AI Civilisations.

**Body:**
> The whitepaper documenting Creator Mode as a novel contribution to AI research. How automated organisational search compares to Neural Architecture Search, AutoML, and open-ended evolution — and why searching social structures is fundamentally different from searching computational structures.

Read the paper >    Cite this >

---

### Section 8: Final CTA

*Full viewport. Dark.*

**Headline:**
> The field explores itself.

**Three CTAs:**
```
[Read the concept paper]    [Explore the engine]    [Watch the simulation]
```

---

## Design System

### Visual Language

| Element | Specification |
|---------|--------------|
| **Mode** | Dark mode default |
| **Dark backgrounds** | `#000000` (hero/dramatic), `#1d1d1f` (elevated/cards) |
| **Light backgrounds** | `#f5f5f7` (technical/interactive sections) |
| **Text (dark bg)** | `#f5f5f7` (headings), `#86868b` (body) |
| **Text (light bg)** | `#1d1d1f` (headings), `#86868b` (body) |
| **Accent** | `#2997ff` (links, CTAs, interactive elements) |
| **Crown jewel accent** | `#ffd60a` (auto mode card, breakthrough diagram) |
| **Typography** | Inter. Weights: 400 (body), 500 (emphasis), 600 (headings). Mono: JetBrains Mono. |
| **Content width** | 87.5% viewport, max 1260px |
| **Section padding** | 144px top/bottom (desktop), 80px (mobile) |
| **Element spacing** | Minimum 24px between elements |
| **Grid** | 12-column, 20px gutter |
| **Images** | Float in negative space. No backgrounds behind product images. |
| **Code blocks** | Syntax highlighted, copy button, real output only — never mocked. |

### Type Scale

| Element | Desktop | Mobile | Weight |
|---------|---------|--------|--------|
| Hero headline | 80px | 48px | 600 |
| Section headline | 64px | 40px | 600 |
| Sub-headline | 48px | 32px | 600 |
| Feature headline | 40px | 28px | 600 |
| Card headline | 28-32px | 24px | 600 |
| Body (lead) | 24px | 21px | 400 |
| Body (standard) | 21px | 17px | 400 |
| Eyebrow | 17px | 14px | 600 |

All headings: tracking -0.015em. Eyebrows: tracking 0.04em.

### Animation

| Property | Value |
|----------|-------|
| Reveal | Fade-up: translateY(30px) → 0, opacity 0 → 1 |
| Duration | 900ms |
| Easing | cubic-bezier(0.25, 0.46, 0.45, 0.94) |
| Stagger | 150ms between sequential elements |
| Trigger | Intersection Observer, 15% visibility threshold |
| Fires | Once only. Never re-animates on scroll-back. |

### Dark/Light Transitions

- **Dark = emotional, impressive, cinematic.** Heroes, crown jewels, CTAs.
- **Light = technical, detailed, practical.** Interactive explorers, code, feature grids.
- Hard cut between sections. No gradient transitions.

### Responsive

- **Desktop:** Full experience, all interactions
- **Tablet:** Simplified grid, maintained hierarchy
- **Mobile:** Vertically stacked, swipe-friendly cards, hamburger nav

---

## Tech Stack

### Same Stack as Existing Site

| Component | Choice | Why |
|-----------|--------|-----|
| **Framework** | React 19 + TypeScript | Matches existing site |
| **Build** | Vite | Matches existing site |
| **Styling** | Tailwind CSS 4 | Matches existing site |
| **Animations** | Framer Motion | Scroll-triggered reveals, layout animations |
| **Code highlighting** | Shiki or Prism | Syntax highlighting |
| **Terminal rendering** | Custom CSS component | Recreate rich terminal output in HTML |
| **Deployment** | Netlify | Same domain |
| **Routing** | React Router v7 | Matches existing site |

### Routes

```
/                          → Homepage
/science                   → The Science
/science/papers            → All papers
/science/paper/[slug]      → Individual paper
/science/dimensions        → 9-dimension framework (interactive)
/science/cite              → How to cite
/science/provenance        → Bitcoin timestamps + verification

/simulation                → The Simulation (landing)
/simulation/highlights     → Highlights (existing)
/simulation/fishbowl       → Fishbowl (existing)
/simulation/journey        → Journey (existing)
/simulation/interviews     → Interviews (existing)
/simulation/explorer       → Data Explorer (existing)
/simulation/how-it-works   → How It Works (existing)
/simulation/methodology    → Methodology (existing)
/simulation/chronicler     → Chronicler (existing)
/simulation/observations   → Observations (existing)
/simulation/ethics         → Ethics (existing)

/engine                    → The Engine
/engine/presets            → All 13 presets
/engine/auto               → Crown jewel deep-dive
/engine/start              → Getting started
/engine/docs               → Documentation / API reference

/creator                   → Creator Mode
/creator/tasks             → Organisational search (task mode)
/creator/emergence         → Possibility space explorer
/creator/discoveries       → Discovery catalogue
/creator/paper             → Paper 5
```

### Migration Plan

1. Create new top-level routing structure
2. Move simulation pages under `/simulation/*`
3. Set up redirects from old routes (Netlify `_redirects`)
4. Build homepage
5. Build Science wing
6. Build Engine wing
7. Build Simulation landing page
8. Apple copy pass on all existing simulation pages
9. Update global nav and footer
10. Test all routes
11. Deploy

---

## Build Order

| Step | What | Effort |
|------|------|--------|
| 1 | **Global nav + routing restructure** | Small |
| 2 | **Homepage** | Medium |
| 3 | **Engine wing** | Large — 14 sections, interactive elements |
| 4 | **Science wing** | Medium |
| 5 | **Simulation landing** | Small — hero + navigation cards |
| 6 | **Creator Mode wing** | Medium — 8 sections, concept-heavy, visionary |
| 7 | **Apple copy pass on existing pages** | Medium — every headline, every description |
| 8 | **Polish pass** | Medium — animations, transitions, responsive |
| 9 | **Content creation** | Medium — terminal recordings, diagrams, screenshots |
| 10 | **Deploy** | Small — Netlify, DNS, redirects |

---

## Content Needed

| Content | For | Status |
|---------|-----|--------|
| Terminal recording: collaborative run | Engine hero | Generate from battle-tests |
| Terminal recording: auto mode restructuring | Engine crown jewel | Generate |
| Experiment comparison table | Engine experiment chapter | Have from battle-tests |
| 9-dimension interactive explorer | Engine + Science | Build |
| Paper summaries (plain English) | Science wing | Write |
| "One dot vs vast space" diagram | Science breakthrough | Design |
| Communication topology diagrams | Engine presets | Design |
| Competitive landscape data | Engine problem section | Have |
| Real run results | Engine results | Have from battle-tests |
| Fishbowl hero screenshot | Simulation hero | Capture |
| Simulation highlight card descriptions | Simulation section 3 | Apple copy pass |

---

## Quality Checklist

Before launch, every page passes these:

**Copy:**
- [ ] Every headline: 2-7 words, uses one of the 5 Apple formulas
- [ ] Every body block: 1-2-1 structure (significance → substance → expansion)
- [ ] Zero hedging language ("we believe", "arguably", "one of the best")
- [ ] Zero exclamation marks
- [ ] Contractions everywhere
- [ ] Active voice, present tense throughout
- [ ] "You" within first 2 sentences of every paragraph
- [ ] Every number has context (comparison + benefit)
- [ ] One prestige word per section maximum
- [ ] Reads aloud naturally

**Structure:**
- [ ] One idea per viewport
- [ ] Crown jewel in position 2-3 (early)
- [ ] No transitional copy between sections
- [ ] Dark = emotional, light = technical
- [ ] Eyebrow → Headline → Significance → Proof → Cards for every feature
- [ ] CTAs: 4-7 per page, quiet and confident

**Experience:**
- [ ] Every wing feels like an Apple product page — exciting, never academic
- [ ] All four wings feel like peers — none dominates
- [ ] A first-time visitor understands AgentCiv in 10 seconds
- [ ] A developer goes from landing to `pip install` in 30 seconds
- [ ] A researcher finds papers and citation in 60 seconds
- [ ] Auto mode is visible within first 3 scrolls of Engine page
- [ ] All terminal output is real, not mocked
- [ ] All code is copy-pasteable with copy button
- [ ] Mobile is a complete experience, not degraded desktop
- [ ] Page load < 2 seconds on 3G
- [ ] Scroll animations fire once, are subtle, reward the scroll

**Trust:**
- [ ] Every claim backed by evidence or linked to a paper
- [ ] Bitcoin provenance verification instructions work
- [ ] GitHub link prominent on Engine page
- [ ] Citation formats correct and copyable
- [ ] Creator Mode wing conveys both the vision AND the grounded architecture

---

## The Principle

> Every visitor — developer, researcher, thought leader, curious person — leaves the site knowing:
>
> 1. This is a new field of AI and these people created it.
> 2. They ran an extraordinary simulation and the results are real.
> 3. There's a tool you can install right now and it's remarkable.
> 4. They built an AI that explores the field itself — and it's finding things nobody expected.
>
> Each of these is independently extraordinary. Together, they're a body of work that goes from defining a field to letting the field explore itself.
> Nobody else in AI has this arc.
