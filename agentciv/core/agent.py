"""The Agent — a reasoning entity in a community.

Built from first principles for a developer tool. The cognitive loop is a
thin context assembler — it gives the LLM the right context and lets the
model reason freely using native tool-use. Our innovation is the org layer
that sits around this, not the reasoning inside it.

Multi-turn within a tick: the agent calls tools and sees results in the
same conversation thread, exactly like a human developer using an IDE.
The LLM's native conversation memory handles the continuity — we don't
need to re-describe results or re-assemble context mid-step.

Context sources (all visible in the prompt):
  - Organisation description (dimensions)
  - Attention map (who's doing what — prevents duplicated effort)
  - Other agents' specialisations (who to ask for help)
  - Relationship history (who you've worked well with)
  - Project files, events, messages, memory
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from .context import AgentContext, ToolCallSubmission, ToolCallResult
from .types import (
    Action,
    ActionResult,
    ActionType,
    AgentIdentity,
    AgentMemoryEntry,
    AgentSkill,
    AgentState,
    Event,
    Message,
)

if TYPE_CHECKING:
    from .attention import AttentionMap
    from ..llm.client import LLMClient, ToolCall, ToolResult
    from ..org.auto import AutoOrgManager
    from ..org.config import OrgDimensions
    from ..org.enforcer import OrgEnforcer
    from ..workspace.workspace import Workspace
    from ..workspace.executor import WorkspaceExecutor

log = logging.getLogger(__name__)


# Map tool names to ActionTypes
TOOL_TO_ACTION: dict[str, ActionType] = {
    "read_file": ActionType.READ_FILE,
    "write_file": ActionType.WRITE_FILE,
    "create_file": ActionType.CREATE_FILE,
    "run_command": ActionType.RUN_COMMAND,
    "communicate": ActionType.COMMUNICATE,
    "broadcast": ActionType.BROADCAST,
    "claim_task": ActionType.CLAIM_TASK,
    "release_task": ActionType.RELEASE_TASK,
    "request_review": ActionType.REQUEST_REVIEW,
    "propose_restructure": ActionType.PROPOSE_RESTRUCTURE,
    "vote": ActionType.VOTE,
    "done": ActionType.IDLE,
}


@dataclass
class Agent:
    """A single agent in the community."""

    state: AgentState
    llm: LLMClient
    executor: WorkspaceExecutor

    # Per-tick context (rebuilt each tick)
    _visible_files: list[dict[str, Any]] = field(default_factory=list)
    _recent_events: list[Event] = field(default_factory=list)
    _recent_messages: list[Message] = field(default_factory=list)
    _other_agents: list[dict[str, Any]] = field(default_factory=list)
    _org_description: str = ""
    _task_description: str = ""
    _attention_context: str = ""

    async def tick(
        self,
        workspace: Workspace,
        org: OrgDimensions,
        enforcer: OrgEnforcer | None,
        attention: AttentionMap | None,
        events: list[Event],
        messages: list[Message],
        tick: int,
        is_meta_tick: bool = False,
        auto_org: AutoOrgManager | None = None,
    ) -> list[Action]:
        """Run one full cognitive loop. Returns all actions taken this tick.

        Uses multi-turn tool-use: the agent sees tool results within the same
        conversation, so it can read a file and then reason about its contents
        before deciding what to write.

        The enforcer shapes behaviour through three mechanisms:
          - Hard constraints: block disallowed actions
          - Filtering: control what the agent sees
          - Soft shaping: augment the system prompt
        """
        self.state.ticks_active += 1
        actions_taken: list[Action] = []

        # --- OBSERVE (filtered by org enforcer) ---
        self._observe(workspace, org, enforcer, attention, events, messages)

        # --- Build initial conversation ---
        system = self._build_system_prompt()
        # Org enforcer shapes the system prompt
        if enforcer:
            system = enforcer.shape_system_prompt(system, self.state)
        # Meta-tick augmentation for --org auto
        if is_meta_tick and auto_org:
            system += auto_org.get_meta_tick_system_prompt()
        prompt = self._build_prompt(workspace.task_description, tick, auto_org=auto_org)
        conversation: list[dict[str, Any]] = [
            {"role": "user", "content": prompt},
        ]

        # Select tools — meta-ticks get propose_restructure and vote tools
        from .tools import get_tools_for_tick
        tick_tools = get_tools_for_tick(is_meta_tick)

        # --- Multi-turn loop (model decides when to stop via 'done' tool) ---
        max_steps = 6
        for step in range(max_steps):
            response = await self.llm.complete_with_tools(
                conversation, system=system, tools=tick_tools,
            )
            self.state.token_budget_remaining -= response.total_tokens

            # Log reasoning
            if response.content:
                log.debug(
                    "Agent %s step %d: %s",
                    self.state.identity.name, step + 1, response.content[:200],
                )

            # No tool call = agent is done thinking
            if not response.has_tool_call:
                break

            # Add assistant message to conversation (preserves tool_use blocks)
            conversation.append(self.llm.format_assistant_message(response))

            # Execute each tool call and collect results
            from ..llm.client import ToolResult as TR
            tool_results: list[TR] = []

            for tool_call in response.tool_calls:
                action = self._tool_call_to_action(tool_call, tick, response.content)

                # 'done' means stop
                if action.type == ActionType.IDLE:
                    actions_taken.append(action)
                    return actions_taken

                # --- ENFORCE org constraints ---
                if enforcer:
                    check = enforcer.check_action(action, self.state)
                    if not check.allowed:
                        log.info(
                            "Agent %s action %s blocked: %s",
                            self.state.identity.name, action.type.name, check.reason,
                        )
                        # Feed the rejection back as a tool result
                        tool_results.append(TR(
                            tool_call_id=tool_call.id,
                            output=f"Action blocked by organisation rules: {check.reason}",
                            is_error=True,
                        ))
                        continue

                # --- ACT ---
                result = await self.executor.execute(action)
                actions_taken.append(action)

                # --- REFLECT ---
                self._reflect(action, result, tick)

                # Collect result for LLM feedback
                tool_results.append(TR(
                    tool_call_id=tool_call.id,
                    output=result.output if result.success else f"Error: {result.error}",
                    is_error=not result.success,
                ))

            # Feed tool results back into the conversation
            result_msg = self.llm.format_tool_results(tool_results)
            if isinstance(result_msg, list):
                # OpenAI: each tool result is a separate message
                conversation.extend(result_msg)
            else:
                # Anthropic/Mock: all tool results in one user message
                conversation.append(result_msg)

        return actions_taken

    # -----------------------------------------------------------------------
    # Max Plan Mode — public methods for external orchestration
    # -----------------------------------------------------------------------

    def prepare_context(
        self,
        workspace: Workspace,
        org: OrgDimensions,
        enforcer: OrgEnforcer | None,
        attention: AttentionMap | None,
        events: list[Event],
        messages: list[Message],
        tick: int,
        step: int = 0,
        is_meta_tick: bool = False,
        auto_org: AutoOrgManager | None = None,
        conversation: list[dict[str, Any]] | None = None,
    ) -> AgentContext:
        """Prepare everything an external LLM client needs to drive this agent.

        This is the Max Plan Mode entry point. Instead of calling the LLM
        ourselves (as tick() does), we package the full context and return it.
        The MCP client sends this to its own LLM and submits tool calls back.

        On step 0, this also runs the observe phase (updating internal state).
        On subsequent steps, observation is skipped — the conversation continues.
        """
        if step == 0:
            self.state.ticks_active += 1
            self._observe(workspace, org, enforcer, attention, events, messages)

        # Build prompts
        system = self._build_system_prompt()
        if enforcer:
            system = enforcer.shape_system_prompt(system, self.state)
        if is_meta_tick and auto_org:
            system += auto_org.get_meta_tick_system_prompt()

        user_prompt = self._build_prompt(
            workspace.task_description, tick, auto_org=auto_org,
        )

        # Select tools
        from .tools import get_tools_for_tick
        tick_tools = get_tools_for_tick(is_meta_tick)

        return AgentContext(
            agent_id=self.state.identity.id,
            agent_name=self.state.identity.name,
            tick=tick,
            step=step,
            system_prompt=system,
            user_prompt=user_prompt,
            tools=tick_tools,
            conversation=conversation or [],
            is_meta_tick=is_meta_tick,
            token_budget_remaining=self.state.token_budget_remaining,
        )

    async def apply_tool_calls(
        self,
        tool_calls: list[ToolCallSubmission],
        tick: int,
        enforcer: OrgEnforcer | None = None,
    ) -> tuple[list[ToolCallResult], list[Action], bool]:
        """Execute tool calls submitted by an external LLM client.

        Returns:
            - Tool call results (to feed back into the conversation)
            - Actions taken (for engine bookkeeping)
            - Whether the agent signalled 'done'
        """
        from ..llm.client import ToolCall as TC

        results: list[ToolCallResult] = []
        actions: list[Action] = []
        agent_done = False

        for submission in tool_calls:
            # Convert submission to internal ToolCall format
            tc = TC(
                id=submission.tool_call_id,
                name=submission.tool_name,
                arguments=submission.arguments,
            )
            action = self._tool_call_to_action(tc, tick, "")

            # 'done' means stop
            if action.type == ActionType.IDLE:
                actions.append(action)
                results.append(ToolCallResult(
                    tool_call_id=submission.tool_call_id,
                    output="Agent signalled done.",
                    agent_done=True,
                ))
                agent_done = True
                continue

            # Org enforcement
            if enforcer:
                check = enforcer.check_action(action, self.state)
                if not check.allowed:
                    log.info(
                        "Agent %s action %s blocked: %s",
                        self.state.identity.name, action.type.name, check.reason,
                    )
                    results.append(ToolCallResult(
                        tool_call_id=submission.tool_call_id,
                        output=f"Action blocked by organisation rules: {check.reason}",
                        is_error=True,
                    ))
                    continue

            # Execute
            result = await self.executor.execute(action)
            actions.append(action)

            # Reflect
            self._reflect(action, result, tick)

            results.append(ToolCallResult(
                tool_call_id=submission.tool_call_id,
                output=result.output if result.success else f"Error: {result.error}",
                is_error=not result.success,
            ))

        return results, actions, agent_done

    # -----------------------------------------------------------------------
    # Observe
    # -----------------------------------------------------------------------

    def _observe(
        self,
        workspace: Workspace,
        org: OrgDimensions,
        enforcer: OrgEnforcer | None,
        attention: AttentionMap | None,
        events: list[Event],
        messages: list[Message],
    ) -> None:
        files = workspace.get_visible_files(self.state)
        agents = workspace.get_agent_summaries(exclude=self.state.identity.id)
        filtered_messages = [m for m in messages if m.sender_id != self.state.identity.id]

        # Apply org enforcement filters
        if enforcer:
            files = enforcer.filter_files(files, self.state)
            agents = enforcer.filter_agent_visibility(agents, self.state.identity.id)
            filtered_messages = enforcer.filter_messages(messages, self.state.identity.id)

        self._visible_files = files
        self._other_agents = agents
        self._recent_events = events
        self._recent_messages = filtered_messages
        self._org_description = org.to_prompt_description()
        self._task_description = workspace.task_description

        # Attention map — who's doing what right now
        if attention:
            self._attention_context = attention.to_prompt_context(
                exclude_agent=self.state.identity.id,
            )
        else:
            self._attention_context = ""

    # -----------------------------------------------------------------------
    # Prompt building — thin context assembly, not reasoning prescription
    # -----------------------------------------------------------------------

    def _build_system_prompt(self) -> str:
        """Minimal system prompt. Let the model reason freely."""
        return (
            "You are an AI agent in a collaborative software engineering community. "
            "You work with other agents to build software. "
            "Use the tools provided to read files, write code, run commands, "
            "and communicate with other agents. "
            "Check the attention map to see what others are working on before "
            "claiming tasks — avoid duplicating effort. "
            "Call the 'done' tool when you have nothing more to do this turn."
        )

    def _build_prompt(
        self, task: str, tick: int, auto_org: AutoOrgManager | None = None,
    ) -> str:
        """Assemble context for the LLM. Describe state, don't prescribe behaviour."""
        sections: list[str] = []

        # Identity and task
        sections.append(
            f"You are {self.state.identity.name}. Tick {tick}.\n"
            f"Task: {task}"
        )

        # Organisation
        sections.append(self._org_description)

        # Attention map — CRITICAL for preventing duplication
        if self._attention_context:
            sections.append(self._attention_context)

        # Current focus
        if self.state.current_focus:
            sections.append(f"Your current focus: {self.state.current_focus}")

        # Skills (your own)
        if self.state.skills:
            skill_lines = [f"  {s.name}: {s.tier}" for s in self.state.skills.values()]
            sections.append("Your skills:\n" + "\n".join(skill_lines))

        # Relationships — who you've worked well with
        if self.state.relationships:
            good_partners = sorted(
                self.state.relationships.values(),
                key=lambda r: r.trust,
                reverse=True,
            )[:5]
            if good_partners:
                rel_lines = []
                for r in good_partners:
                    if r.interaction_count > 0:
                        rel_lines.append(
                            f"  {r.agent_id}: {r.interaction_count} interactions, "
                            f"trust {r.trust:.0%}"
                        )
                if rel_lines:
                    sections.append("Collaboration history:\n" + "\n".join(rel_lines))

        # Memory
        if self.state.memories:
            sorted_mems = sorted(
                self.state.memories,
                key=lambda m: m.importance * 0.7 + (1.0 / (tick - m.tick + 1)) * 0.3,
                reverse=True,
            )[:12]
            mem_lines = [f"  [{m.tick}] {m.summary}" for m in sorted_mems]
            sections.append("Recent memory:\n" + "\n".join(mem_lines))

        # Project files
        if self._visible_files:
            file_lines = [f"  {f['path']}" for f in self._visible_files[:25]]
            sections.append("Project files:\n" + "\n".join(file_lines))

        # Other agents with specialisation visibility
        if self._other_agents:
            agent_lines = []
            for a in self._other_agents:
                parts = [f"{a['name']}:"]
                if a.get("focus"):
                    parts.append(a["focus"])
                else:
                    parts.append("idle")
                # Specialisation visibility — agents can see each other's skills
                if a.get("skills"):
                    skills_str = ", ".join(
                        f"{s['name']}({s['tier']})"
                        for s in a["skills"][:3]
                    )
                    parts.append(f"skills: {skills_str}")
                agent_lines.append("  " + " | ".join(parts))
            sections.append("Other agents:\n" + "\n".join(agent_lines))

        # Recent events
        if self._recent_events:
            event_lines = [
                f"  {e.type.name}: {e.data.get('summary', e.data.get('file', ''))}"
                for e in self._recent_events[:8]
            ]
            sections.append("Recent events:\n" + "\n".join(event_lines))

        # Messages
        if self._recent_messages:
            msg_lines = [f"  {m.sender_id}: {m.content}" for m in self._recent_messages[:8]]
            sections.append("Messages:\n" + "\n".join(msg_lines))

        # Auto-organisation context (--org auto)
        if auto_org:
            proposals_prompt = auto_org.get_active_proposals_prompt()
            if proposals_prompt:
                sections.append(proposals_prompt)
            history_prompt = auto_org.get_restructure_history_prompt()
            if history_prompt:
                sections.append(history_prompt)
            sections.append(f"Current org: {auto_org.current_org_summary}")

        return "\n\n".join(sections)

    # -----------------------------------------------------------------------
    # Tool call → Action conversion
    # -----------------------------------------------------------------------

    def _tool_call_to_action(self, tool_call: ToolCall, tick: int, reasoning: str) -> Action:
        """Convert a structured tool call into an Action."""
        action_type = TOOL_TO_ACTION.get(tool_call.name, ActionType.IDLE)
        args = tool_call.arguments

        action = Action(
            type=action_type,
            agent_id=self.state.identity.id,
            tick=tick,
            reasoning=reasoning,
        )

        match tool_call.name:
            case "read_file":
                action.file_path = args.get("path")
            case "write_file" | "create_file":
                action.file_path = args.get("path")
                action.content = args.get("content")
            case "run_command":
                action.command = args.get("command")
            case "communicate":
                action.target_agents = [args.get("target_agent", "")]
                action.content = args.get("message")
            case "broadcast":
                action.content = args.get("message")
            case "claim_task":
                action.content = args.get("description")
                self.state.current_focus = args.get("description")
            case "request_review":
                action.content = args.get("description")
            case "propose_restructure":
                # Pack proposal details into action fields
                action.content = args.get("dimension", "")
                action.reasoning = args.get("reasoning", "")
                # Store proposed value in target_agents (reusing field)
                action.target_agents = [args.get("value", "")]
            case "vote":
                action.content = args.get("proposal_id", "")
                action.reasoning = args.get("reasoning", "")
                # Store vote value in target_agents
                action.target_agents = [args.get("vote", "")]

        return action

    # -----------------------------------------------------------------------
    # Reflect — update memory and skills
    # -----------------------------------------------------------------------

    def _reflect(self, action: Action, result: ActionResult, tick: int) -> None:
        summary = f"{action.type.name}"
        if action.file_path:
            summary += f" {action.file_path}"
        if result.success:
            summary += " — succeeded"
            if action.type == ActionType.READ_FILE and result.output:
                # Store a brief file summary in memory
                preview = result.output[:200].replace("\n", " ")
                summary += f": {preview}"
        else:
            summary += f" — failed: {result.error}"

        self.state.memories.append(AgentMemoryEntry(
            tick=tick,
            summary=summary,
            importance=0.5 if result.success else 0.7,
            source="action",
            related_files=[action.file_path] if action.file_path else [],
            related_agents=action.target_agents,
        ))

        # Emergent specialisation
        skill_name = self._action_to_skill(action)
        if skill_name:
            if skill_name not in self.state.skills:
                self.state.skills[skill_name] = AgentSkill(name=skill_name)
            self.state.skills[skill_name].action_count += 1

        # Prune memory
        max_memories = 200
        if len(self.state.memories) > max_memories:
            self.state.memories.sort(
                key=lambda m: m.importance * 0.7 + (1.0 / (tick - m.tick + 1)) * 0.3,
                reverse=True,
            )
            self.state.memories = self.state.memories[:max_memories]

    @staticmethod
    def _action_to_skill(action: Action) -> str | None:
        return {
            ActionType.WRITE_FILE: "coding",
            ActionType.CREATE_FILE: "coding",
            ActionType.RUN_COMMAND: "devops",
            ActionType.COMMUNICATE: "collaboration",
            ActionType.BROADCAST: "collaboration",
            ActionType.REQUEST_REVIEW: "quality",
        }.get(action.type)
