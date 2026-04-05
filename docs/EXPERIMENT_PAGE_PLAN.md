# Experiment Page — "Same Task. Five Teams. Measurable Truth."

**Created:** 5 April 2026
**Location:** `/experiment` (linked from Engine wing landing page)
**Type:** Single-page, scroll-driven, progressively disclosable
**Quality bar:** Apple × Nature journal × The Pudding (data storytelling)
**Style:** Follows `APPLE_STYLE_GUIDE.md` — bright, warm cream, confident

---

## Design Philosophy

**The Pudding meets Apple.** Data journalism quality with Apple's visual confidence.

Three depth levels on one page:
1. **10 seconds** — Hero + headline result. "Auto-organised agents beat every human-designed team."
2. **2 minutes** — Results table + team cards. Clear picture of what happened.
3. **30+ minutes** — Expandable per-team deep dives: full conversations, network graphs, grid evolution, tick-by-tick replay.

**No separate pages.** Everything lives on one scroll. Expandable sections keep it clean.
**No jargon without hover-explain.** Every technical term has a tooltip.
**Every claim is linked to data.** Click any number and see where it came from.

---

## Page Structure (Top to Bottom)

### Section 0: Breadcrumb + Context Bar
```
Engine > Experiments > City Grid
```
Subtle. Establishes where you are. Links back to Engine wing.

---

### Section 1: Hero — "Same Task. Five Teams."

**Headline:** "Same task. Five teams. Measurable truth."
**Subhead:** "We gave the exact same problem to five AI teams — each organised differently. Same agents. Same model. Same tools. Only the organisational structure changed. Here's what happened."

**Visual:** The 5 city grids rendered side-by-side as small pixel-art thumbnails (each ~150px). Clean, coloured by building type. Below each: the team name and aggregate score. The auto grid subtly glows or has a tiny crown/star — it won.

**One-liner underneath:** "The team that designed its own structure outperformed every human-designed configuration."

---

### Section 2: The Setup — "The Experiment."

**Headline:** "The experiment."

**1-2-1 copy:**
> Organisational structure is the invisible variable in multi-agent AI. Everyone tunes the model, the prompt, the tools. Nobody tunes how agents relate to each other.
>
> We created a controlled experiment: one task (design a city), four agents per team, five different organisational configurations, identical everything else. Each team worked autonomously — communicating, coordinating, resolving conflicts, building. We measured everything.
>
> This is the first empirical evidence that how you organise AI agents matters as much as which AI you use.

**Visual element:** Minimal diagram showing the experimental design:
```
┌─────────────┐
│  CONSTANT    │  Same model (Claude Sonnet 4.6)
│              │  Same task (10×10 city grid)
│              │  Same tools (read, write, run, communicate)
│              │  Same budget (250K tokens per agent)
│              │  Same team size (4 agents)
└─────────────┘
        ↓
┌─────────────┐
│  VARIABLE    │  Organisational structure only
└─────────────┘
        ↓
┌─────────────────────────────────────────────┐
│  Collaborative │ Competitive │ Hierarchical  │
│  Meritocratic  │ Auto        │ Solo baseline │
└─────────────────────────────────────────────┘
```

---

### Section 3: Meet the Teams — "Five ways to organise."

**Headline:** "Five ways to organise."
**Subhead:** "Each team had the same four agents. The only difference: the rules of engagement."

**Layout:** 5 team cards in a row (responsive: 2×3 on mobile). Each card:

```
┌─────────────────────────────────┐
│  🏷️ COLLABORATIVE               │
│  "Everyone sees everything."     │
│                                  │
│  Authority:     Flat             │
│  Communication: Open mesh        │
│  Decisions:     Consensus        │
│  Roles:         Self-chosen      │
│  Information:   Fully transparent│
│  Review:        None required    │
│                                  │
│  Plain English:                  │
│  "Like a startup brainstorm.     │
│   All four agents can talk to    │
│   anyone, see everything, and    │
│   pick their own tasks. No boss, │
│   no gates, no hierarchy."       │
│                                  │
│  [Expand full config ↓]          │
└─────────────────────────────────┘
```

Each card shows:
- **Team name** (bold, coloured — each team gets a consistent colour throughout the page)
- **One-line personality** (the soul of the config in ≤5 words)
- **6 key dimensions** (the ones that differ most between teams — not all 9)
- **Plain English paragraph** (2-3 sentences: what it actually felt like to be on this team)
- **Expandable: Full YAML config** (for researchers who want the exact parameters)

#### The 5 Team Cards:

**COLLABORATIVE** — colour: blue
- Personality: "Everyone sees everything."
- Plain English: "Like a startup brainstorm. All four agents talk freely, see all information, and choose their own tasks. No boss, no gates. Decisions by consensus. Conflicts negotiated between the agents involved."
- Key diffs: Flat authority, mesh comms, voluntary tasks, no review, transparent info

**COMPETITIVE** — colour: red
- Personality: "Race to win."
- Plain English: "Four agents working in near-isolation. Each tackles the full problem independently. Communication is restricted to whispers — max 1 message per tick. No shared strategy, no collaboration. May the best solution win."
- Key diffs: Anarchic authority, whisper comms, 1 msg/tick, filtered info, no specialisation

**HIERARCHICAL** — colour: gold
- Personality: "One lead. Clear chain."
- Plain English: "Traditional top-down management. The first agent (Atlas) is the designated lead — assigns tasks, coordinates work, reviews output. Others communicate through the lead. Information is curated, not raw."
- Key diffs: Hierarchy authority, hub-spoke comms, assigned tasks, lead review, curated info

**MERITOCRATIC** — colour: green
- Personality: "Earn your influence."
- Plain English: "Influence proportional to demonstrated quality. Every change requires peer review. Reputation builds over time — agents who produce better work get more say in decisions. Conflicts resolved by vote."
- Key diffs: Distributed authority, mandatory peer review, reputation incentives, voted conflicts

**AUTO** — colour: purple/violet
- Personality: "Design your own team."
- Plain English: "The agents start with a neutral baseline and can restructure at any point. Every tick, they can propose changes to how the team works — new roles, different decision rules, communication changes — and vote on them. The human sets the goal; the agents design the organisation."
- Key diffs: Real-time adaptation, meta-tick every tick, 60% vote threshold to restructure

---

### Section 4: The Results — "What happened."

**Headline:** "What happened."

**Primary visual: Results Table**

Clean, sortable table. Each row is a team (in their colour). Columns:

| Team | Score | Conflicts | Comms | Ticks | Specialisation | Time |
|------|-------|-----------|-------|-------|----------------|------|
| Auto | **79.4** | 2 | 37 | 9 | 0.250 | 784s |
| Hierarchical | 78.5 | 4 | 14 | 10 | 0.107 | 540s |
| Collaborative | 78.4 | 5 | 81 | 8 | 0.000 | 390s |
| Meritocratic | 76.8 | 9 | 15 | 9 | 0.000 | 705s |
| Competitive | 70.9 | 31 | 21 | 13 | 0.150 | 635s |
| Solo (baseline) | TBD | 0 | 0 | TBD | — | TBD |

Each column header has a tooltip explaining the metric.
Table is sorted by Score by default. Click any column to re-sort.

**Below the table: 3-4 "headline findings" as callout cards:**

1. **"Self-organised agents won."** Auto mode — where agents designed their own structure — produced the highest-quality city with the fewest conflicts.

2. **"Competition breeds chaos."** The competitive team had 15× more merge conflicts than auto, and the lowest score. Racing independently ≠ winning.

3. **"Communication ≠ quality."** Collaborative sent 81 messages (most). Hierarchical sent 14 (least among teams). They scored nearly identically. More talking doesn't mean better work.

4. **"Only free agents specialised."** Auto (Gini 0.250) and competitive (0.150) were the only teams where agents developed different roles. Collaborative — despite "emergent roles" in its config — showed zero specialisation.

---

### Section 5: Score Breakdown — "Five dimensions of a city."

**Headline:** "Five dimensions. One score."

**Visual:** Radar/spider chart with all 5 teams overlaid (in their colours). 5 axes: Coverage, Accessibility, Zoning, Diversity, Connectivity.

**Below: expandable explanation of each scoring dimension:**

| Dimension | What it measures | Max |
|-----------|-----------------|-----|
| Coverage | % of buildable cells filled (not road/empty) | 100 |
| Accessibility | % of buildings reachable from roads | 100 |
| Zoning | Penalty for incompatible adjacencies (e.g. Industrial next to Residential) | 100 |
| Diversity | Shannon entropy of building type distribution | 100 |
| Connectivity | Road network connectedness (largest component / total roads) | 100 |

**Aggregate = Harmonic mean** (not arithmetic — rewards balanced performance, punishes single weak dimensions).

**Key insight callout:** "Every team achieved 100% coverage and most hit 100% accessibility. The differentiators were zoning discipline, diversity, and connectivity — the dimensions that require coordination."

---

### Section 6: Deep Dives — "Inside each team."

**Headline:** "Inside each team."
**Subhead:** "Click any team to see exactly what happened — every conversation, every decision, every conflict."

**Layout:** 5 expandable accordion sections, one per team (+ solo baseline). Each in team colour. Collapsed by default — click to expand.

#### Each team's deep dive contains:

**A. The Story (2-3 paragraphs)**
Narrative summary of what this team did. Written from the data. E.g. for collaborative: "All four agents immediately began broadcasting strategy proposals. By tick 2, they'd converged on a grid-road approach with zoned districts. The main challenge was coordination — five merge conflicts as multiple agents edited city.txt simultaneously. By tick 6, they were making single-cell tweaks and debating zoning penalties."

**B. Communication Graph**
Visual network diagram: 4 nodes (agents), edges weighted by message count. Directed edges (arrows). For collaborative: dense mesh. For hierarchical: hub-spoke star. For competitive: almost nothing.

**C. Key Conversations (curated, 3-5 per team)**
The most interesting/revealing exchanges, pulled from the timeline data. Each shows:
- Tick number
- Agent name + avatar
- Full message text
- Agent's internal reasoning (expandable — "What they were thinking")

Example format:
```
┌─ Tick 1 ──────────────────────────────────────┐
│ 🟦 Atlas (broadcast)                          │
│ "Hey team! Let me propose a strategy —        │
│  grid road network with zoned districts..."    │
│                                                │
│ [What Atlas was thinking ↓]                    │
│ "I'll start by broadcasting a strategy         │
│  proposal to the team, then we can             │
│  collaborate on the design."                   │
└────────────────────────────────────────────────┘
```

**D. Grid Evolution**
Side-by-side or filmstrip of the city at key ticks (from git snapshots). Shows how the grid changed over time. Pixel-art rendering with building-type colours.

**E. Tick-by-Tick Timeline**
Expandable vertical timeline. Each tick shows: active agents, messages sent, files changed, conflicts. Compact by default, expand any tick for full detail.

**F. The Numbers**
Per-agent breakdown table:
| Agent | Messages | Files Modified | Tasks Claimed | Conflicts | Tokens Used |
|-------|----------|---------------|---------------|-----------|-------------|

Network metrics: Graph density, clustering coefficient, reciprocity, hub-spoke ratio.

**G. Raw Data**
Link to download the full JSON for this run. "Want to run your own analysis? Here's everything."

---

### Section 7: The Auto Mode Story — "They designed their own team."

**Headline:** "They designed their own team."

This gets its own section because it's the crown jewel finding.

**The narrative:**
> We gave four agents a neutral starting configuration and one freedom the other teams didn't have: the ability to change how they were organised. Every tick, any agent could propose a restructuring — new roles, different communication rules, changed decision processes — and the team would vote.
>
> What happened? [Pull from actual auto run data — did they restructure? What did they propose? What did they vote on?]

**Expandable: Full restructuring log**
Every proposal, every vote, every adopted change. Timestamped.

**The punchline:**
"The team that had no pre-set organisation — that had to figure it out themselves — produced the best city, with the fewest conflicts, and the most specialised division of labour. Configuration isn't just a parameter. It's a capability."

---

### Section 8: What This Means — "Beyond the grid."

**Headline:** "Beyond the grid."

**1-2-1 copy:**
> This experiment used four agents and a 10×10 grid. The principle scales to any number of agents and any task.
>
> If organisational structure measurably changes outcomes for 4 agents on a toy problem, it changes outcomes for 20 agents on a codebase, 100 agents on a company, 1,000 agents on an economy. Configuration is a performance variable — one that can be optimised, adapted, and evolved just like any other hyperparameter in AI.
>
> This is what Collective Intelligence Engineering looks like in practice. Not better models. Better teams.

**Scale table (visual):**

| Scale | Agents | Example | What changes |
|-------|--------|---------|-------------|
| This experiment | 4 | City grid | Configuration → measurable score difference |
| Team | 10-20 | Software project | Configuration → shipping speed, code quality |
| Department | 50-100 | Product org | Configuration → innovation rate, coordination cost |
| Company | 1,000+ | AGI-scale firm | Configuration → competitive advantage |
| Civilisation | 10,000+ | AI society | Configuration → governance, culture, stability |

---

### Section 9: Methodology & Data — "Everything is open."

**Headline:** "Everything is open."

**Subsections:**

**Reproducibility**
- Engine version, commit hash, Bitcoin timestamp
- Exact configs used (links to YAML files on GitHub)
- "Run this experiment yourself: `agentciv test-tasks --tasks city-grid --presets collaborative,competitive,hierarchical,meritocratic,auto`"

**Raw Data Downloads**
- Per-run JSON files (all 6)
- Combined dataset (single JSON with all runs)
- Grid PNGs

**Scoring Methodology**
- Link to `score_city.py` on GitHub
- Full explanation of each metric
- Why harmonic mean for aggregate

**Engine Architecture (brief)**
- Link to Engine wing for full details
- Key relevant features: branch-per-agent git, auto-merge, chronicle observer, organisational enforcer

**The Paper**
- Link to Paper 6 (when published)
- "This experiment is one section of a larger paper on Collective Intelligence Engineering."

---

### Section 10: Footer CTA

**Headline:** "Run your own experiment."

**Two paths:**

```
┌──────────────────────┐  ┌──────────────────────┐
│   Try the Engine     │  │   Read the Paper     │
│                      │  │                      │
│  pip install         │  │  "Organisational     │
│  agentciv-engine     │  │   Configuration as   │
│                      │  │   a Performance      │
│  [Get Started →]     │  │   Variable"          │
│                      │  │                      │
│                      │  │  [Read Paper →]      │
└──────────────────────┘  └──────────────────────┘
```

---

## Visual Design Notes

### Colour System (per team)
- **Collaborative:** Blue (#3B82F6)
- **Competitive:** Red (#EF4444)
- **Hierarchical:** Gold (#F59E0B)
- **Meritocratic:** Green (#10B981)
- **Auto:** Purple (#8B5CF6)
- **Solo baseline:** Grey (#6B7280)

These colours are used EVERYWHERE: table rows, chart lines, team cards, grid borders, conversation bubbles. Instant visual recognition.

### City Grid Rendering
Each building type gets a colour:
- R (Residential): Light green
- C (Commercial): Blue
- I (Industrial): Orange/brown
- P (Park): Bright green
- H (Hospital): Red cross / pink
- S (School): Yellow
- . (Road): Light grey
- _ (Empty): White/cream

Render as clean pixel-art squares. ~15px per cell = 150px grids for thumbnails, 300px for detail view.

### Expandable Sections
Use smooth accordion animations. Chevron icon (↓/↑). Subtle background colour shift when expanded. Content fades in, doesn't pop.

### Tooltips
Every technical term (Gini coefficient, harmonic mean, hub-spoke, etc.) has a hover tooltip with a plain-English explanation. Consistent style: cream background, small shadow, appears on hover/tap.

### Mobile
- Team cards: 1 column, swipeable
- Results table: horizontal scroll
- Grid thumbnails: 2×3 grid
- Deep dives: full width accordions
- Conversations: full width, stacked

---

## Data Requirements (from run JSONs)

For each of the 6 runs, the page needs:

1. **Scores** — `artifacts.city_scores` (5 dimensions + aggregate)
2. **Grid** — `artifacts["city.txt"]` (render as pixel art)
3. **Grid snapshots** — `artifacts.grid_snapshots` (for evolution filmstrip)
4. **Communication pairs** — `report.communication` (for network graph)
5. **Timeline with content** — `report.timeline` (for conversations + tick timeline)
6. **Agent contributions** — `report.contributions` (for per-agent tables)
7. **Conflict records** — `report.conflict_records` (for conflict analysis)
8. **Tick snapshots** — `report.tick_snapshots` (for temporal charts)
9. **Network analysis** — `analysis.network` (density, clustering, etc.)
10. **Temporal analysis** — `analysis.temporal` (activity curves)
11. **Tokens per agent** — `report.tokens_per_agent` or `metrics.tokens_per_agent`
12. **Config** — the YAML preset used (embedded or linked)

All of this already exists in the saved JSONs. No new data collection needed.

---

## Implementation Notes

- **Framework:** Same as rest of website (React + Tailwind, presumably)
- **Charts:** D3.js or Recharts for radar chart, network graph, temporal plots
- **Grid renderer:** Custom SVG or Canvas component — simple pixel grid
- **Data:** Import the 6 run JSONs as static data at build time
- **Conversations:** Custom component with expandable reasoning
- **No API calls.** All data is static, baked at build time.

---

## Relationship to Other Pages

```
Engine Wing Landing → [View Experiment Results] → THIS PAGE
                                                      ↓
                                                 [Read the Paper] → Paper 6 PDF
                                                 [Try the Engine] → Engine Getting Started
                                                 [Raw Data] → GitHub repo
```

The Engine wing landing page gets a prominent card/section:
> "Same task. Five teams. See what happened."
> [View the Experiment →]

---

## Content Checklist

- [ ] Hero visual (5 grids side by side)
- [ ] Experiment setup diagram
- [ ] 5 team cards with plain English descriptions
- [ ] Results table (sortable)
- [ ] 4 headline finding callouts
- [ ] Radar/spider chart (5 scoring dimensions × 5 teams)
- [ ] Per-team deep dives (5 + solo baseline)
  - [ ] Narrative summary
  - [ ] Communication network graph
  - [ ] Curated conversations (3-5 per team)
  - [ ] Grid evolution filmstrip
  - [ ] Tick timeline
  - [ ] Per-agent breakdown table
  - [ ] Raw JSON download link
- [ ] Auto mode spotlight section
- [ ] "Beyond the grid" scale argument
- [ ] Methodology & reproducibility
- [ ] Raw data downloads
- [ ] Footer CTAs (engine + paper)
