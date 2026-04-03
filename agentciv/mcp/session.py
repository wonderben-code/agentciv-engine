"""Session manager — tracks running engine instances for MCP.

Each MCP tool call that spawns a community creates a Session. The session
holds the engine, gardener, and an event buffer so MCP clients can monitor
progress and intervene mid-run.

Multiple concurrent sessions are supported. Each is fully independent.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from ..core.agent import Agent
from ..core.attention import AttentionMap
from ..core.engine import Engine
from ..core.event_bus import EventBus
from ..core.stepper import StepSession
from ..core.types import AgentIdentity, AgentState, Event
from ..gardener import Gardener, Intervention
from ..llm.client import create_client
from ..org.config import EngineConfig
from ..org.enforcer import OrgEnforcer
from ..workspace.executor import WorkspaceExecutor
from ..workspace.workspace import Workspace

log = logging.getLogger(__name__)

AGENT_NAMES = [
    "Atlas", "Nova", "Sage", "Flux", "Echo",
    "Drift", "Pulse", "Cinder", "Wren", "Quill",
    "Ember", "Loom", "Haze", "Strider", "Crux",
    "Rune", "Fern", "Glyph", "Shard", "Tide",
]


class SessionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"


@dataclass
class SessionEvent:
    """A buffered event for status reporting."""
    tick: int
    type: str
    agent: str | None
    summary: str
    timestamp: datetime


@dataclass
class Session:
    """A running or completed engine session."""
    id: str
    task: str
    org_preset: str
    agent_count: int
    model: str
    max_ticks: int
    project_dir: Path
    status: SessionStatus = SessionStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    current_tick: int = 0
    error: str | None = None

    # Internal state (not serialised)
    engine: Engine | None = field(default=None, repr=False)
    gardener: Gardener | None = field(default=None, repr=False)
    task_handle: asyncio.Task | None = field(default=None, repr=False)
    event_buffer: list[SessionEvent] = field(default_factory=list, repr=False)
    _max_buffer: int = field(default=200, repr=False)

    def buffer_event(self, event: Event) -> None:
        """Buffer an event for status reporting."""
        se = SessionEvent(
            tick=event.tick,
            type=event.type.name,
            agent=event.agent_id,
            summary=self._summarise_event(event),
            timestamp=datetime.now(),
        )
        self.event_buffer.append(se)
        if len(self.event_buffer) > self._max_buffer:
            self.event_buffer = self.event_buffer[-self._max_buffer:]
        # Track current tick
        if event.tick > self.current_tick:
            self.current_tick = event.tick

    def _summarise_event(self, event: Event) -> str:
        """One-line summary of an event."""
        agent = event.agent_id or ""
        if not isinstance(event.data, dict):
            event.data = {}
        match event.type.name:
            case "TICK_START":
                meta = " [META-TICK]" if event.data.get("is_meta_tick") else ""
                return f"Tick {event.tick} started{meta}"
            case "TICK_END":
                actions = event.data.get("actions", 0)
                return f"Tick {event.tick}: {actions} actions"
            case "FILE_CREATED":
                return f"{agent} created {event.data.get('file', '?')}"
            case "FILE_MODIFIED":
                return f"{agent} modified {event.data.get('file', '?')}"
            case "MESSAGE_SENT":
                targets = event.data.get("targets", [])
                return f"{agent} -> {', '.join(targets)}"
            case "BROADCAST_SENT":
                preview = event.data.get("content_preview", "")[:60]
                return f"{agent} broadcast: {preview}"
            case "TASK_CLAIMED":
                return f"{agent} claimed task"
            case "BRANCH_MERGED":
                count = event.data.get("count", 0)
                return f"{agent} merged ({count} files)"
            case "MERGE_CONFLICT":
                conflicts = event.data.get("conflicts", [])
                return f"{agent} CONFLICT: {', '.join(conflicts)}"
            case "RESTRUCTURE_PROPOSED":
                preview = event.data.get("content_preview", "")[:60]
                return f"{agent} proposed restructure: {preview}"
            case "RESTRUCTURE_ADOPTED":
                dim = event.data.get("dimension", "?")
                new = event.data.get("new_value", "?")
                return f"RESTRUCTURED: {dim} -> {new}"
            case "ENGINE_STARTED":
                return f"Engine started ({event.data.get('agents', '?')} agents, org={event.data.get('config', '?')})"
            case "ENGINE_STOPPED":
                return "Engine stopped"
            case _:
                return event.type.name

    def to_dict(self) -> dict[str, Any]:
        """Serialisable summary for MCP responses."""
        return {
            "id": self.id,
            "task": self.task,
            "org_preset": self.org_preset,
            "agent_count": self.agent_count,
            "model": self.model,
            "max_ticks": self.max_ticks,
            "project_dir": str(self.project_dir),
            "status": self.status.value,
            "current_tick": self.current_tick,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error": self.error,
            "recent_events": [
                {
                    "tick": e.tick,
                    "type": e.type,
                    "agent": e.agent,
                    "summary": e.summary,
                }
                for e in self.event_buffer[-30:]
            ],
        }


class SessionManager:
    """Manages multiple concurrent engine sessions.

    This is the core state object for the MCP server. It lives for the
    lifetime of the server process and tracks all sessions.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}
        self._step_sessions: dict[str, StepSession] = {}

    @property
    def sessions(self) -> dict[str, Session]:
        return self._sessions

    async def create_session(
        self,
        task: str,
        org_preset: str = "collaborative",
        agent_count: int = 4,
        model: str = "claude-sonnet-4-6",
        max_ticks: int = 50,
        project_dir: str = ".",
        dimension_overrides: dict[str, str] | None = None,
    ) -> Session:
        """Create and start a new engine session.

        The engine runs as a background asyncio task. Use get_session()
        to check progress and intervene() to guide.
        """
        session_id = uuid.uuid4().hex[:8]
        project = Path(project_dir).resolve()

        session = Session(
            id=session_id,
            task=task,
            org_preset=org_preset,
            agent_count=agent_count,
            model=model,
            max_ticks=max_ticks,
            project_dir=project,
        )
        self._sessions[session_id] = session

        # Start engine in background
        session.task_handle = asyncio.create_task(
            self._run_session(session, dimension_overrides)
        )

        return session

    async def _run_session(
        self,
        session: Session,
        dimension_overrides: dict[str, str] | None = None,
    ) -> None:
        """Run an engine session in the background."""
        try:
            session.status = SessionStatus.RUNNING
            session.started_at = datetime.now()

            # Build config from preset
            config = EngineConfig.from_preset(session.org_preset)
            config.task = session.task
            config.agent_count = session.agent_count
            config.model = session.model
            config.max_ticks = session.max_ticks
            config.project_dir = str(session.project_dir)
            config.enable_chronicle = True

            # Apply dimension overrides
            if dimension_overrides:
                dims = config.org_dimensions
                for key, value in dimension_overrides.items():
                    if hasattr(dims, key) and key != "extra":
                        setattr(dims, key, value)
                    else:
                        dims.extra[key] = value

            # Workspace
            workspace = Workspace(
                project_dir=session.project_dir,
                task_description=session.task,
            )
            workspace.scan()

            # Event bus — buffer events for MCP status queries
            event_bus = EventBus()
            event_bus.subscribe(None, session.buffer_event)

            # Attention map
            attention = AttentionMap()

            # Create agents (with per-agent model overrides from config.models)
            agents: list[Agent] = []
            for i in range(session.agent_count):
                name = AGENT_NAMES[i % len(AGENT_NAMES)]
                agent_id = f"agent_{i}"
                # Per-agent model: check by agent_id, then by name, then default
                agent_model = config.models.get(agent_id) or config.models.get(name) or session.model
                identity = AgentIdentity(id=agent_id, name=name, model=agent_model)
                state = AgentState(
                    identity=identity,
                    token_budget_remaining=config.parameters.token_budget_per_agent,
                )
                llm = create_client(agent_model, max_tokens=4096)
                executor = WorkspaceExecutor(workspace, attention=attention)
                agent = Agent(state=state, llm=llm, executor=executor)
                workspace.register_agent(state)
                agents.append(agent)

            # Org enforcer
            enforcer = OrgEnforcer(
                dimensions=config.org_dimensions,
                parameters=config.parameters,
            )
            enforcer.assign_initial_roles([a.state.identity.id for a in agents])

            # Gardener — always enabled for MCP sessions
            gardener = Gardener()
            gardener.enable()
            session.gardener = gardener

            # Engine
            engine = Engine(
                config=config,
                workspace=workspace,
                agents=agents,
                event_bus=event_bus,
                enforcer=enforcer,
                attention=attention,
                gardener=gardener,
            )
            session.engine = engine

            # Run the engine
            await engine.run()

            session.status = SessionStatus.COMPLETED
            session.completed_at = datetime.now()

        except asyncio.CancelledError:
            session.status = SessionStatus.STOPPED
            session.completed_at = datetime.now()
            log.info("Session %s was stopped", session.id)

        except Exception as e:
            session.status = SessionStatus.FAILED
            session.error = str(e)
            session.completed_at = datetime.now()
            log.exception("Session %s failed", session.id)

    def get_session(self, session_id: str) -> Session | None:
        return self._sessions.get(session_id)

    def intervene(self, session_id: str, intervention: Intervention) -> bool:
        """Submit an intervention to a running session's gardener queue."""
        session = self._sessions.get(session_id)
        if not session or not session.gardener or session.status != SessionStatus.RUNNING:
            return False
        session.gardener.submit(intervention)
        return True

    async def stop_session(self, session_id: str) -> bool:
        """Stop a running session gracefully."""
        session = self._sessions.get(session_id)
        if not session or session.status != SessionStatus.RUNNING:
            return False

        # Send stop intervention through the gardener
        if session.gardener:
            session.gardener.submit(Intervention(
                type="stop",
                tick=session.current_tick,
            ))

        # Also set the engine flag directly
        if session.engine:
            session.engine.running = False

        return True

    def list_sessions(self) -> list[dict[str, Any]]:
        """List all sessions with summary info."""
        result = [
            {
                "id": s.id,
                "task": s.task[:80],
                "org": s.org_preset,
                "status": s.status.value,
                "tick": f"{s.current_tick}/{s.max_ticks}",
                "agents": s.agent_count,
                "mode": "api",
            }
            for s in self._sessions.values()
        ]
        # Include step sessions
        for sid, ss in self._step_sessions.items():
            result.append({
                "id": sid,
                "task": ss.engine.config.task[:80],
                "org": ss.engine.config.org_preset,
                "status": ss.phase.value,
                "tick": f"{ss.engine.tick}/{ss.engine.config.max_ticks}",
                "agents": len(ss.engine.agents),
                "mode": "max_plan",
            })
        return result

    # -------------------------------------------------------------------
    # Max Plan Mode — step sessions
    # -------------------------------------------------------------------

    async def create_step_session(
        self,
        task: str,
        org_preset: str = "collaborative",
        agent_count: int = 4,
        max_ticks: int = 50,
        project_dir: str = ".",
        dimension_overrides: dict[str, str] | None = None,
    ) -> tuple[str, dict[str, Any]]:
        """Create a step session for Max Plan Mode.

        Unlike create_session(), this does NOT start a background task or
        make any LLM calls. The MCP client drives everything.

        Returns (session_id, init_result).
        """
        session_id = uuid.uuid4().hex[:8]
        project = Path(project_dir).resolve()

        # Build config
        config = EngineConfig.from_preset(org_preset)
        config.task = task
        config.agent_count = agent_count
        config.max_ticks = max_ticks
        config.project_dir = str(project)
        config.enable_chronicle = True

        # Apply dimension overrides
        if dimension_overrides:
            dims = config.org_dimensions
            for key, value in dimension_overrides.items():
                if hasattr(dims, key) and key != "extra":
                    setattr(dims, key, value)
                else:
                    dims.extra[key] = value

        # Workspace
        workspace = Workspace(
            project_dir=project,
            task_description=task,
        )
        workspace.scan()

        # Event bus
        event_bus = EventBus()

        # Attention map
        attention = AttentionMap()

        # Create agents — NO LLM client needed in Max Plan Mode
        agents: list[Agent] = []
        for i in range(agent_count):
            name = AGENT_NAMES[i % len(AGENT_NAMES)]
            agent_id = f"agent_{i}"
            # Model field is informational in Max Plan Mode
            identity = AgentIdentity(id=agent_id, name=name, model="max_plan")
            state = AgentState(
                identity=identity,
                token_budget_remaining=config.parameters.token_budget_per_agent,
            )
            # No LLM client — pass None (Max Plan Mode doesn't use it)
            executor = WorkspaceExecutor(workspace, attention=attention)
            agent = Agent(state=state, llm=None, executor=executor)  # type: ignore[arg-type]
            workspace.register_agent(state)
            agents.append(agent)

        # Org enforcer
        enforcer = OrgEnforcer(
            dimensions=config.org_dimensions,
            parameters=config.parameters,
        )
        enforcer.assign_initial_roles([a.state.identity.id for a in agents])

        # Gardener
        gardener = Gardener()
        gardener.enable()

        # Engine
        engine = Engine(
            config=config,
            workspace=workspace,
            agents=agents,
            event_bus=event_bus,
            enforcer=enforcer,
            attention=attention,
            gardener=gardener,
        )

        # Step session
        step = StepSession(engine=engine)
        init_result = await step.start()

        self._step_sessions[session_id] = step
        log.info("Created step session %s (Max Plan Mode)", session_id)

        return session_id, init_result

    def get_step_session(self, session_id: str) -> StepSession | None:
        return self._step_sessions.get(session_id)
