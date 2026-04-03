"""Agent context — the data contract for Max Plan Mode.

In Max Plan Mode, the engine is a pure orchestrator. It does NOT make LLM
calls — the MCP client (Claude Code on a Max subscription) drives agent
cognition externally. This module defines the data that flows between them.

Flow:
  1. Engine prepares context for each agent (system prompt, user prompt, tools)
  2. MCP client sends context to its own LLM → gets tool calls back
  3. MCP client submits tool calls to engine → engine executes them, returns results
  4. Repeat until agent calls 'done' or hits step limit
  5. Engine does post-tick processing (merge, events, attention, etc.)

This is the same cognitive loop as API mode — the only difference is WHO
makes the LLM call. The organisational layer, tool execution, enforcement,
git isolation, chronicle, and everything else work identically.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentContext:
    """Everything an MCP client needs to drive one agent's cognition.

    Returned by the engine at the start of each agent's turn within a tick.
    The client sends this to its LLM, gets tool calls back, and submits
    them via the orchestrate_act tool.
    """

    agent_id: str
    agent_name: str
    tick: int
    step: int  # current step within the multi-turn loop (0-based)

    # Prompts — ready to send to any LLM
    system_prompt: str
    user_prompt: str

    # Tools — Anthropic tool-use format (also convertible to OpenAI)
    tools: list[dict[str, Any]]

    # Conversation history for multi-turn within this tick
    # First call: empty. Subsequent calls: includes prior assistant + tool results.
    conversation: list[dict[str, Any]] = field(default_factory=list)

    # Meta
    is_meta_tick: bool = False
    token_budget_remaining: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Serialise for MCP transport."""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "tick": self.tick,
            "step": self.step,
            "system_prompt": self.system_prompt,
            "user_prompt": self.user_prompt,
            "tools": self.tools,
            "conversation": self.conversation,
            "is_meta_tick": self.is_meta_tick,
            "token_budget_remaining": self.token_budget_remaining,
        }


@dataclass
class ToolCallSubmission:
    """A tool call from the MCP client's LLM, submitted back to the engine.

    The client extracts tool_use blocks from its LLM response and sends
    them here. The engine executes them and returns results.
    """

    tool_call_id: str
    tool_name: str
    arguments: dict[str, Any]


@dataclass
class ToolCallResult:
    """Result of executing a submitted tool call.

    Returned to the MCP client so it can feed the result back into the
    conversation for the next multi-turn step.
    """

    tool_call_id: str
    output: str
    is_error: bool = False
    agent_done: bool = False  # True if this was a 'done' tool call


@dataclass
class TickSummary:
    """Summary of a completed tick, returned after complete_tick().

    Gives the MCP client visibility into what happened: merges, conflicts,
    events, org changes, and whether the run should continue.
    """

    tick: int
    actions_count: int
    merge_results: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    org_changes: list[dict[str, Any]] = field(default_factory=list)
    should_continue: bool = True  # False when max_ticks reached or stopped

    def to_dict(self) -> dict[str, Any]:
        return {
            "tick": self.tick,
            "actions_count": self.actions_count,
            "merge_results": self.merge_results,
            "events": self.events,
            "org_changes": self.org_changes,
            "should_continue": self.should_continue,
        }
