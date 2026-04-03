# Provenance — Bitcoin Blockchain Timestamps

This directory contains OpenTimestamps proof files (`.ots`) that anchor
the content of this repository to the Bitcoin blockchain.

## What This Proves

Each `.ots` file is a cryptographic proof that the corresponding document
existed at or before the Bitcoin block timestamp. This proof is:

- **Irrefutable** — anchored to Bitcoin's proof-of-work chain
- **Independently verifiable** — anyone can check without trusting us
- **Permanent** — survives regardless of GitHub, servers, or companies

## Timestamped Documents

| Proof File | Proves |
|---|---|
| `commit_e452bad.ots` | Entire repo state at commit `e452bad` (2026-04-03) — full engine codebase |
| `commit_b1d9cac.ots` | Repo state at commit `b1d9cac` — whitepaper commit specifically |
| `agentciv_paper4_organisational_arrangement.md.ots` | Paper 4: "Collective Machine Intelligence" — Mark E. Mala |

Papers 1-3 are timestamped in the [AgentCiv simulation](https://github.com/agentciv/agentciv) repo.

## How to Verify

```bash
# Install the client
pip install opentimestamps-client

# Verify the whitepaper
ots verify provenance/agentciv_paper4_organisational_arrangement.md.ots \
  -f docs/agentciv_paper4_organisational_arrangement.md

# Verify the full repo state
echo -n "e452bad4c88f0cc47a6ca92fc0e380216f57414c" > /tmp/hash.txt
ots verify provenance/commit_e452bad.ots -f /tmp/hash.txt
```

## What's Covered

The repo-level timestamp (`commit_e452bad.ots`) cryptographically covers
every file in the repository at that point — including:

- The complete AgentCiv Engine codebase
- All 13 organisational presets
- The 9-dimensional configuration framework
- MCP server integration
- Paper 4: "Collective Machine Intelligence: A New Field for the Age of AI Collectives"

A git commit hash is a Merkle tree of the entire repo contents. Proving
the commit hash proves every file.

## Why This Matters

These proofs establish that the AgentCiv Engine, the concepts of
Collective Machine Intelligence (CMI) and Computational Organisational
Theory (COT), and all associated intellectual property were authored by
Mark E. Mala and existed at the timestamps proven by the Bitcoin blockchain.
