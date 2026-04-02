"""Core type contracts for the AgentCiv Engine.

Every abstraction in the engine builds on these types. Designed from first
principles for a developer tool — no grid-world legacy.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Agent identity & state
# ---------------------------------------------------------------------------

@dataclass
class AgentIdentity:
    """Immutable identity of an agent in the community."""
    id: str
    name: str
    model: str  # LLM model identifier (e.g. "claude-sonnet-4-6")


@dataclass
class AgentMemoryEntry:
    """A single memory entry with importance scoring."""
    tick: int
    summary: str
    importance: float  # 0.0 – 1.0
    source: str  # "observation", "action", "communication", "reflection"
    related_files: list[str] = field(default_factory=list)
    related_agents: list[str] = field(default_factory=list)
    access_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AgentSkill:
    """Emergent skill — earned through practice, not assigned."""
    name: str  # e.g. "python", "testing", "architecture", "api-design"
    action_count: int = 0  # how many times agent has done this
    quality_score: float = 0.0  # running average of outcome quality

    @property
    def tier(self) -> str:
        if self.action_count >= 40:
            return "expert"
        if self.action_count >= 20:
            return "skilled"
        if self.action_count >= 10:
            return "familiar"
        return "novice"


@dataclass
class Relationship:
    """Tracks collaboration history between two agents."""
    agent_id: str
    interaction_count: int = 0
    positive_count: int = 0
    negative_count: int = 0
    last_tick: int = 0

    @property
    def trust(self) -> float:
        if self.interaction_count == 0:
            return 0.5  # neutral
        return self.positive_count / self.interaction_count


@dataclass
class AgentState:
    """Full mutable state of an agent. Updated each tick."""
    identity: AgentIdentity
    memories: list[AgentMemoryEntry] = field(default_factory=list)
    skills: dict[str, AgentSkill] = field(default_factory=dict)
    relationships: dict[str, Relationship] = field(default_factory=dict)
    current_focus: str | None = None  # what the agent is currently working on
    current_plan: list[str] = field(default_factory=list)
    working_files: list[str] = field(default_factory=list)  # files agent is actively editing
    token_budget_remaining: int = 0
    ticks_active: int = 0


# ---------------------------------------------------------------------------
# Actions — what agents can do
# ---------------------------------------------------------------------------

class ActionType(Enum):
    """Every action an agent can take in the workspace."""
    READ_FILE = auto()
    WRITE_FILE = auto()
    CREATE_FILE = auto()
    DELETE_FILE = auto()
    RUN_COMMAND = auto()  # build, test, lint, etc.
    COMMUNICATE = auto()  # message to specific agent(s)
    BROADCAST = auto()  # message to all agents
    CLAIM_TASK = auto()  # signal intent to work on something
    RELEASE_TASK = auto()  # stop working on something
    REQUEST_REVIEW = auto()
    PROPOSE_RESTRUCTURE = auto()  # for --org auto: propose org change
    VOTE = auto()  # for --org auto: vote on proposal
    IDLE = auto()  # explicitly choose to wait/observe


@dataclass
class Action:
    """A concrete action taken by an agent."""
    type: ActionType
    agent_id: str
    tick: int
    # Context depends on action type
    file_path: str | None = None
    content: str | None = None  # file content or message text
    target_agents: list[str] = field(default_factory=list)
    command: str | None = None  # for RUN_COMMAND
    reasoning: str | None = None  # agent's stated reason


@dataclass
class ActionResult:
    """Outcome of executing an action."""
    success: bool
    output: str | None = None  # command output, file content, etc.
    error: str | None = None
    side_effects: list[str] = field(default_factory=list)  # e.g. "test failed", "merge conflict"


# ---------------------------------------------------------------------------
# Events — what happened (for chronicle and inter-agent awareness)
# ---------------------------------------------------------------------------

class EventType(Enum):
    """Events that flow through the engine's event bus."""
    # Agent lifecycle
    AGENT_JOINED = auto()
    AGENT_IDLE = auto()
    AGENT_WOKE = auto()

    # File operations
    FILE_CREATED = auto()
    FILE_MODIFIED = auto()
    FILE_DELETED = auto()

    # Communication
    MESSAGE_SENT = auto()
    BROADCAST_SENT = auto()

    # Task flow
    TASK_CLAIMED = auto()
    TASK_RELEASED = auto()
    TASK_COMPLETED = auto()
    REVIEW_REQUESTED = auto()
    REVIEW_COMPLETED = auto()

    # Build & test
    BUILD_SUCCEEDED = auto()
    BUILD_FAILED = auto()
    TESTS_PASSED = auto()
    TESTS_FAILED = auto()

    # Organisation
    RESTRUCTURE_PROPOSED = auto()
    RESTRUCTURE_VOTED = auto()
    RESTRUCTURE_ADOPTED = auto()
    SPECIALISATION_GAINED = auto()

    # Engine
    TICK_START = auto()
    TICK_END = auto()
    ENGINE_STARTED = auto()
    ENGINE_STOPPED = auto()


@dataclass
class Event:
    """An event that occurred in the workspace."""
    type: EventType
    tick: int
    timestamp: datetime = field(default_factory=datetime.now)
    agent_id: str | None = None
    data: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Messages — agent-to-agent communication
# ---------------------------------------------------------------------------

@dataclass
class Message:
    """A message between agents."""
    sender_id: str
    receiver_ids: list[str]  # empty = broadcast
    content: str
    tick: int
    timestamp: datetime = field(default_factory=datetime.now)
    is_broadcast: bool = False


# ---------------------------------------------------------------------------
# Task signals — visible needs in the workspace
# ---------------------------------------------------------------------------

@dataclass
class TaskSignal:
    """A visible need in the workspace. Not assigned — perceived and claimed."""
    id: str
    description: str
    status: str = "open"  # open, claimed, in_progress, review, done
    claimed_by: str | None = None
    priority: float = 0.5  # 0.0 – 1.0, can be agent-assessed
    related_files: list[str] = field(default_factory=list)
    created_tick: int = 0
    completed_tick: int | None = None
