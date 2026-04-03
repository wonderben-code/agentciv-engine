"""Step session — wraps the engine for Max Plan Mode orchestration.

In Max Plan Mode, the MCP client (Claude Code) drives agent cognition.
The StepSession manages the state machine:

  start → [prepare_tick → agent_act* → complete_tick]* → cleanup

Each agent_act call handles one multi-turn step for one agent:
the client sends tool calls from its LLM, we execute them and return results.

The client loops agent_act until the agent signals 'done' or hits the
step limit, then calls complete_tick to advance.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .agent import Agent
from .context import (
    AgentContext,
    ToolCallSubmission,
)
from .engine import Engine
from .types import Action

log = logging.getLogger(__name__)


class StepPhase(str, Enum):
    """Where we are in the step-by-step flow."""
    CREATED = "created"
    INITIALIZED = "initialized"
    TICK_PREPARED = "tick_prepared"
    AGENTS_ACTING = "agents_acting"
    TICK_COMPLETE = "tick_complete"
    FINISHED = "finished"


@dataclass
class AgentStepState:
    """Tracks multi-turn progress for one agent within a tick."""
    agent_id: str
    agent_name: str
    step: int = 0
    done: bool = False
    actions: list[Action] = field(default_factory=list)
    conversation: list[dict[str, Any]] = field(default_factory=list)
    max_steps: int = 6


@dataclass
class StepSession:
    """Manages step-by-step engine orchestration for Max Plan Mode.

    Lifecycle:
      1. start() — initialises engine, returns agent list
      2. prepare_tick() — sets up next tick, returns agent contexts
      3. act(agent_id, tool_calls) — executes one step, returns results + updated context
      4. complete_tick() — post-tick processing, returns summary
      5. Repeat 2-4 until should_continue is False
      6. finish() — cleanup
    """

    engine: Engine
    phase: StepPhase = StepPhase.CREATED
    _agent_steps: dict[str, AgentStepState] = field(default_factory=dict)
    _current_contexts: dict[str, AgentContext] = field(default_factory=dict)
    _is_meta_tick: bool = False

    async def start(self) -> dict[str, Any]:
        """Initialise the engine. Returns agent list and config summary."""
        result = await self.engine.initialize()
        self.phase = StepPhase.INITIALIZED
        return result

    async def prepare_tick(self) -> list[dict[str, Any]]:
        """Prepare the next tick. Returns serialised agent contexts.

        Each context contains system_prompt, user_prompt, tools, and
        conversation history — everything needed to make an LLM call.
        """
        contexts, is_meta_tick = await self.engine.prepare_tick()
        self._is_meta_tick = is_meta_tick

        if not contexts:
            # No more ticks — engine is done
            self.phase = StepPhase.FINISHED
            return []

        # Reset per-tick agent state
        self._agent_steps.clear()
        self._current_contexts.clear()

        for ctx in contexts:
            self._agent_steps[ctx.agent_id] = AgentStepState(
                agent_id=ctx.agent_id,
                agent_name=ctx.agent_name,
            )
            self._current_contexts[ctx.agent_id] = ctx

        self.phase = StepPhase.TICK_PREPARED
        return [ctx.to_dict() for ctx in contexts]

    async def act(
        self,
        agent_id: str,
        tool_calls: list[dict[str, Any]],
        tokens_used: int = 0,
    ) -> dict[str, Any]:
        """Execute one multi-turn step for an agent.

        Args:
            agent_id: Which agent is acting
            tool_calls: Tool calls from the client's LLM response
            tokens_used: Tokens consumed by the LLM call (for budget tracking)

        Returns:
            Dict with tool_results, agent_done, and updated context (if not done)
        """
        self.phase = StepPhase.AGENTS_ACTING

        step_state = self._agent_steps.get(agent_id)
        if not step_state:
            return {"error": f"Unknown agent: {agent_id}"}
        if step_state.done:
            return {"error": f"Agent {agent_id} already done this tick"}

        # Find the agent object
        agent = self._get_agent(agent_id)
        if not agent:
            return {"error": f"Agent {agent_id} not found in engine"}

        # Track token usage
        if tokens_used > 0:
            agent.state.token_budget_remaining -= tokens_used

        # Convert raw dicts to ToolCallSubmission
        submissions = [
            ToolCallSubmission(
                tool_call_id=tc.get("tool_call_id", tc.get("id", "")),
                tool_name=tc.get("tool_name", tc.get("name", "")),
                arguments=tc.get("arguments", tc.get("input", {})),
            )
            for tc in tool_calls
        ]

        # Execute
        results, actions, agent_done = await agent.apply_tool_calls(
            submissions,
            tick=self.engine.tick,
            enforcer=self.engine.enforcer,
        )

        # Update step state
        step_state.actions.extend(actions)
        step_state.step += 1
        step_state.done = agent_done or step_state.step >= step_state.max_steps

        # Build response
        response: dict[str, Any] = {
            "agent_id": agent_id,
            "agent_name": step_state.agent_name,
            "tool_results": [
                {
                    "tool_call_id": r.tool_call_id,
                    "output": r.output,
                    "is_error": r.is_error,
                    "agent_done": r.agent_done,
                }
                for r in results
            ],
            "agent_done": step_state.done,
            "step": step_state.step,
        }

        # If not done, return an updated context for the next LLM call
        if not step_state.done:
            # The client needs to build the conversation themselves from
            # the tool results, but we provide the context for convenience
            updated_ctx = agent.prepare_context(
                workspace=self.engine.workspace,
                org=self.engine.config.org_dimensions,
                enforcer=self.engine.enforcer,
                attention=self.engine.attention,
                events=[],  # no new events mid-tick
                messages=[],
                tick=self.engine.tick,
                step=step_state.step,
                is_meta_tick=self._is_meta_tick,
                auto_org=self.engine.auto_org,
            )
            self._current_contexts[agent_id] = updated_ctx
            response["next_context"] = updated_ctx.to_dict()

        return response

    async def complete_tick(self) -> dict[str, Any]:
        """Complete the current tick. Returns tick summary.

        Call this after all agents have finished acting (agent_done=True
        or step limit reached for all agents).
        """
        # Collect all actions from all agents
        all_actions: list[Action] = []
        for step_state in self._agent_steps.values():
            all_actions.extend(step_state.actions)

        summary = await self.engine.complete_tick(all_actions)
        self.phase = StepPhase.TICK_COMPLETE

        result = summary.to_dict()
        result["agents_summary"] = {
            aid: {
                "name": ss.agent_name,
                "steps": ss.step,
                "actions": len(ss.actions),
                "done": ss.done,
            }
            for aid, ss in self._agent_steps.items()
        }
        return result

    async def finish(self) -> dict[str, Any]:
        """Clean up and return final state."""
        await self.engine.cleanup()
        self.phase = StepPhase.FINISHED

        result: dict[str, Any] = {
            "final_tick": self.engine.tick,
            "status": "finished",
        }

        # Include chronicle if available
        if self.engine.chronicle:
            report = self.engine.chronicle.generate_report()
            result["chronicle"] = report.to_dict()

        return result

    def get_status(self) -> dict[str, Any]:
        """Current status of the step session."""
        return {
            "phase": self.phase.value,
            "tick": self.engine.tick,
            "max_ticks": self.engine.config.max_ticks,
            "running": self.engine.running,
            "agents": {
                aid: {
                    "name": ss.agent_name,
                    "step": ss.step,
                    "done": ss.done,
                    "actions": len(ss.actions),
                }
                for aid, ss in self._agent_steps.items()
            },
        }

    def _get_agent(self, agent_id: str) -> Agent | None:
        """Find an agent by ID."""
        for agent in self.engine.agents:
            if agent.state.identity.id == agent_id:
                return agent
        return None
