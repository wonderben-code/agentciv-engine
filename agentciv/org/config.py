"""Organisational configuration — the core innovation.

Three-layer system:
  Layer 1: Named presets (most users) — `--org collaborative`
  Layer 2: Organisational dimensions (power users) — readable YAML
  Layer 3: Raw parameters (researchers) — full control

Every layer is extensible. New dimensions, values, presets, and mechanisms
can be added by the community without modifying the core engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# The 9 organisational dimensions (expandable by community)
# ---------------------------------------------------------------------------

# Each dimension is a named axis with a spectrum of values.
# The engine reads these as strings and maps them to behavioural parameters.
# Unknown dimensions are preserved (not rejected) — extensibility by design.

KNOWN_DIMENSIONS = {
    "authority": [
        "hierarchy", "flat", "distributed", "rotating", "consensus", "anarchic",
    ],
    "communication": [
        "hub-spoke", "mesh", "clustered", "broadcast", "whisper",
    ],
    "roles": [
        "assigned", "emergent", "rotating", "fixed", "fluid",
    ],
    "decisions": [
        "top-down", "consensus", "majority", "meritocratic", "autonomous",
    ],
    "incentives": [
        "collaborative", "competitive", "reputation", "market",
    ],
    "information": [
        "transparent", "need-to-know", "curated", "filtered",
    ],
    "conflict": [
        "authority", "negotiated", "voted", "adjudicated",
    ],
    "groups": [
        "imposed", "self-selected", "task-based", "persistent", "temporary",
    ],
    "adaptation": [
        "static", "evolving", "cyclical", "real-time",
    ],
}


@dataclass
class OrgDimensions:
    """Layer 2: The organisational dimensions as readable config.

    Community can add new dimensions — they're stored in `extra` and passed
    through to agent prompts and behavioural logic without core changes.
    """
    authority: str = "flat"
    communication: str = "mesh"
    roles: str = "emergent"
    decisions: str = "consensus"
    incentives: str = "collaborative"
    information: str = "transparent"
    conflict: str = "negotiated"
    groups: str = "self-selected"
    adaptation: str = "evolving"
    extra: dict[str, str] = field(default_factory=dict)  # community-added dimensions

    def to_prompt_description(self) -> str:
        """Human-readable description for agent prompts."""
        lines = []
        for dim in [
            "authority", "communication", "roles", "decisions", "incentives",
            "information", "conflict", "groups", "adaptation",
        ]:
            lines.append(f"  {dim}: {getattr(self, dim)}")
        for dim, val in self.extra.items():
            lines.append(f"  {dim}: {val}")
        return "Organisation:\n" + "\n".join(lines)

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> OrgDimensions:
        known_fields = {
            "authority", "communication", "roles", "decisions", "incentives",
            "information", "conflict", "groups", "adaptation",
        }
        known = {k: v for k, v in data.items() if k in known_fields}
        extra = {k: v for k, v in data.items() if k not in known_fields}
        return cls(**known, extra=extra)


# ---------------------------------------------------------------------------
# Layer 3: Raw parameters (researchers)
# ---------------------------------------------------------------------------

@dataclass
class RawParameters:
    """Fine-grained control for researchers running controlled experiments."""
    # Communication
    max_messages_per_tick: int = 5
    communication_range: str = "all"  # "all", "team", "adjacent" (in task graph)
    message_visibility: str = "org-mediated"  # "all", "org-mediated", "direct-only"

    # Task allocation
    task_claim_mode: str = "voluntary"  # "voluntary", "assigned", "bid", "lottery"
    max_concurrent_tasks: int = 2
    allow_task_stealing: bool = False

    # Quality & review
    require_review: bool = False
    review_mode: str = "peer"  # "peer", "lead", "vote", "none"
    min_reviewers: int = 1

    # Agent lifecycle
    sleep_after_idle_ticks: int = 3
    wake_on_events: list[str] = field(default_factory=lambda: ["task_available", "message_received", "build_failed"])
    max_steps_per_tick: int = 4

    # Cost
    token_budget_per_agent: int = 100_000
    token_budget_total: int = 1_000_000

    # Specialisation
    enable_specialisation: bool = True
    specialisation_threshold: int = 10  # actions before "familiar"
    specialisation_visible: bool = True  # other agents can see your specialisations

    # Relationships
    enable_relationships: bool = True  # agents track collaboration history
    relationship_decay: float = 0.95  # per-tick decay (1.0 = no decay)
    prefer_known_collaborators: bool = True  # agents prefer working with past partners

    # Attention map
    enable_attention_map: bool = True  # shared view of who's working on what

    # Git integration
    enable_git_branches: bool = True  # branch-per-agent with auto-merge
    contention_strategy: str = "branch-per-agent"  # "branch-per-agent", "lock", "optimistic"

    # Human-in-the-loop
    enable_gardener_mode: bool = True  # allow mid-run intervention
    pause_on_conflict: bool = False  # pause and ask human when agents conflict

    # Auto-org (for --org auto mode)
    meta_tick_interval: int = 10  # ticks between org restructure votes
    restructure_threshold: float = 0.6  # vote proportion needed to adopt

    # Extra — community can add parameters
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RawParameters:
        known = {}
        extra = {}
        known_fields = {f.name for f in cls.__dataclass_fields__.values()} - {"extra"}
        for k, v in data.items():
            if k in known_fields:
                known[k] = v
            else:
                extra[k] = v
        return cls(**known, extra=extra)


# ---------------------------------------------------------------------------
# Full engine configuration
# ---------------------------------------------------------------------------

@dataclass
class EngineConfig:
    """Complete configuration for an AgentCiv Engine run."""
    # Project
    task: str = ""  # what the community should build/solve
    project_dir: str = "."
    output_dir: str = ".agentciv"

    # Agents
    agent_count: int = 4
    model: str = "claude-sonnet-4-6"  # default LLM
    models: dict[str, str] = field(default_factory=dict)  # per-agent model overrides

    # Organisation (Layer 1 + 2)
    org_preset: str = "collaborative"  # Layer 1
    org_dimensions: OrgDimensions = field(default_factory=OrgDimensions)  # Layer 2

    # Raw parameters (Layer 3)
    parameters: RawParameters = field(default_factory=RawParameters)

    # Engine
    max_ticks: int = 100
    tick_timeout_seconds: int = 120

    # Chronicle
    enable_chronicle: bool = True
    chronicle_model: str | None = None  # separate model for observer

    @classmethod
    def from_yaml(cls, path: str | Path) -> EngineConfig:
        """Load config from YAML file. Unknown keys are preserved, not rejected."""
        path = Path(path)
        if not path.exists():
            return cls()

        with open(path) as f:
            raw = yaml.safe_load(f) or {}

        config = cls()

        # Simple top-level fields
        for key in ["task", "project_dir", "output_dir", "agent_count", "model",
                     "models", "org_preset", "max_ticks", "tick_timeout_seconds",
                     "enable_chronicle", "chronicle_model"]:
            if key in raw:
                setattr(config, key, raw[key])

        # Layer 2: org dimensions
        if "organization" in raw:
            config.org_dimensions = OrgDimensions.from_dict(raw["organization"])
        elif "organisation" in raw:  # accept both spellings
            config.org_dimensions = OrgDimensions.from_dict(raw["organisation"])

        # Layer 3: raw parameters
        if "parameters" in raw:
            config.parameters = RawParameters.from_dict(raw["parameters"])

        return config

    @classmethod
    def from_preset(cls, preset_name: str, **overrides: Any) -> EngineConfig:
        """Load a named preset from the presets directory."""
        preset_path = Path(__file__).parent.parent / "presets" / f"{preset_name}.yaml"
        if preset_path.exists():
            config = cls.from_yaml(preset_path)
        else:
            config = cls()
        config.org_preset = preset_name

        for key, val in overrides.items():
            if hasattr(config, key):
                setattr(config, key, val)

        return config
