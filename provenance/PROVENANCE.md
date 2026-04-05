# Provenance — Bitcoin Blockchain Timestamps

This directory contains OpenTimestamps proof files (`.ots`) that anchor
the content of this repository to the Bitcoin blockchain.

## What This Proves

Each `.ots` file is a cryptographic proof that the corresponding document
existed at or before the Bitcoin block timestamp. This proof is:

- **Irrefutable** — anchored to Bitcoin's proof-of-work chain
- **Independently verifiable** — anyone can check without trusting us
- **Permanent** — survives regardless of GitHub, servers, or companies

## Timestamped Commits

### Confirmed — Anchored in Bitcoin Blocks

| Commit | Bitcoin Block | Description |
|--------|--------------|-------------|
| `b1d9cac` | 943474 | Paper 4: Collective Machine Intelligence — field-defining whitepaper |
| `e452bad` | 943474 | Bitcoin timestamp proofs for whitepaper provenance |
| `f4729e1` | 943476 | Enable automatic Bitcoin timestamping on every commit |
| `e3ad8dd` | 943480 | Test auto-stamping hook |
| `5e3ed8d` | 943503 | Benchmark suite: 5 standardised tasks, 13 presets, statistical analysis |
| `e2cb2cb` | 943522 | Max Plan Mode: engine as pure orchestrator, zero API keys needed |
| `8d8d6c2` | 943522 | Auto-org demo: 3 self-organising agents build a todo app (57/57 tests pass) |
| `ff4cbbf` | 943522 | Fix auto-org mode: max_tokens, executor fallback, git init |
| `9ec8dc7` | 943522 | Upgrade 5 proofs to full Bitcoin block attestations |
| `243608f` | 943533 | Auto Mode Learning: every run makes --org auto smarter |
| `7971240` | 943533 | Feature discovery UX: context-aware tips and MCP hints |
| `06e8048` | 943535 | Fix package discovery and add MCP config for Claude Code |
| `805f543` | 943535 | Setup command and smart MCP mode detection |

### Pending — Submitted, Awaiting Bitcoin Block

| Commit | Description |
|--------|-------------|
| `1e33868` | Knowledge-not-scripts: factual MCP instructions, CLAUDE.md |
| `846368e` | Make setup flow exciting — welcome message, congratulations |
| `9b68eb1` | Fix celebration message: celebrate the install, not the team |
| `f6fa341` | Interactive setup with explicit mode choice and MCP safety |
| `fdb5c24` | Full celebration: scope, crown jewel, and call to action |
| `2935174` | Add "awaits you" framing to celebration box |
| `ee68bf6` | QA/QC Audit: fix 6 critical and 8 high severity issues |
| `355817e` | Excellence Phase: rich terminal display, human language, teaching errors |

These have been accepted by OpenTimestamps calendar servers and will be
confirmed in a Bitcoin block within hours. Run `ots upgrade provenance/commit_<hash>.ots`
to check.

### Standalone File Timestamps

| Proof File | Bitcoin Block | What it proves |
|---|---|---|
| `agentciv_paper4_organisational_arrangement.md.ots` | 943474 | Paper 4: "Collective Machine Intelligence" — Mark E. Mala |

## How to Verify

```bash
# Install the client
pip install opentimestamps-client

# Verify a commit timestamp
COMMIT_HASH=$(git rev-parse b1d9cac)
echo -n "$COMMIT_HASH" > /tmp/h.txt
ots verify provenance/commit_b1d9cac.ots -f /tmp/h.txt

# Verify the whitepaper file
ots verify provenance/agentciv_paper4_organisational_arrangement.md.ots \
  -f docs/agentciv_paper4_organisational_arrangement.md

# Upgrade pending proofs (after ~1-2 hours)
ots upgrade provenance/commit_355817e.ots
```

Note: Full verification requires a Bitcoin node or a block explorer.
The `ots upgrade` command confirms that the proof has been included
in a Bitcoin block by contacting the calendar servers.

## What's Covered

A git commit hash is a Merkle tree of the entire repo contents. Proving
the commit hash proves every file in the repository at that point. The
confirmed timestamps cover:

- The complete AgentCiv Engine codebase (~11,500 lines, 40 Python files)
- All 13 organisational presets
- The 9-dimensional configuration framework
- MCP server integration
- Max Plan Mode (zero API keys)
- Auto Mode Learning system
- Rich terminal display (Excellence Phase)
- QA/QC audit fixes
- Paper 4: "Collective Machine Intelligence: A New Field for the Age of AI Collectives"

## Why This Matters

These proofs establish that the AgentCiv Engine, the concepts of
Collective Machine Intelligence (CMI) and Computational Organisational
Theory (COT), and all associated intellectual property were authored by
Mark E. Mala and existed at the timestamps proven by the Bitcoin blockchain.

## Auto-Stamping

A post-commit hook automatically submits every commit to OpenTimestamps.
Proofs are saved to this directory as `commit_<short-hash>.ots`.
Run `ots upgrade provenance/commit_*.ots` periodically to upgrade
pending proofs to full Bitcoin block attestations.
