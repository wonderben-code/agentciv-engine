"""Organisational enforcement — where dimensions have teeth.

The config module defines WHAT the org looks like.
This module enforces HOW it constrains agent behaviour.

Three kinds of enforcement:
  1. Hard constraints — block actions that violate org rules
     (e.g. can't broadcast in whisper mode, can't assign tasks in flat authority)
  2. Soft shaping — modify prompts to describe expected behaviour
     (e.g. in hierarchy, the lead agent's prompt says "you coordinate the team")
  3. Filtering — control what agents see
     (e.g. information: need-to-know → agents only see files they've touched)

The enforcer is stateless — it reads the OrgDimensions + RawParameters
and returns decisions. The engine calls it; it doesn't call the engine.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from .config import OrgDimensions, RawParameters
from ..core.types import Action, ActionType, AgentState, Message

log = logging.getLogger(__name__)


@dataclass
class EnforcementResult:
    """Result of checking an action against org rules."""
    allowed: bool = True
    reason: str = ""
    modified_action: Action | None = None  # if we need to transform the action


@dataclass
class OrgEnforcer:
    """Enforces organisational dimensions as mechanical constraints.

    Not a prompt engineering trick — this shapes what agents CAN do,
    not just what they're told to do.
    """

    dimensions: OrgDimensions
    parameters: RawParameters
    # Agent roles — assigned or emergent. Maps agent_id → role
    agent_roles: dict[str, str] = field(default_factory=dict)
    # Lead agent (for hierarchical modes). None if flat/anarchic/distributed
    lead_agent_id: str | None = None
    # Group assignments — maps agent_id → group_name (for clustered communication)
    agent_groups: dict[str, str] = field(default_factory=dict)
    # Communication history — maps agent_id → set of agent_ids they've communicated with
    communication_history: dict[str, set[str]] = field(default_factory=dict)

    # -----------------------------------------------------------------------
    # Hard constraints — block or modify actions
    # -----------------------------------------------------------------------

    def check_action(self, action: Action, agent_state: AgentState) -> EnforcementResult:
        """Check whether an action is allowed under current org rules."""
        checks = [
            self._check_communication(action, agent_state),
            self._check_task_claiming(action, agent_state),
            self._check_review_requirements(action, agent_state),
        ]
        for result in checks:
            if not result.allowed:
                return result
        return EnforcementResult(allowed=True)

    def _check_communication(self, action: Action, agent_state: AgentState) -> EnforcementResult:
        """Enforce communication topology."""
        if action.type == ActionType.BROADCAST:
            if self.dimensions.communication == "whisper":
                return EnforcementResult(
                    allowed=False,
                    reason="Broadcast not allowed in whisper communication mode. Use direct messages.",
                )
            if self.dimensions.communication == "hub-spoke" and agent_state.identity.id != self.lead_agent_id:
                return EnforcementResult(
                    allowed=False,
                    reason="Only the lead agent can broadcast in hub-spoke communication.",
                )

        if action.type == ActionType.COMMUNICATE:
            if self.dimensions.communication == "hub-spoke":
                # Non-lead agents can only message the lead
                if (agent_state.identity.id != self.lead_agent_id
                        and action.target_agents
                        and action.target_agents[0] != self.lead_agent_id):
                    return EnforcementResult(
                        allowed=False,
                        reason="In hub-spoke communication, messages must go through the lead agent.",
                    )

        return EnforcementResult(allowed=True)

    def _check_task_claiming(self, action: Action, agent_state: AgentState) -> EnforcementResult:
        """Enforce task allocation rules."""
        if action.type == ActionType.CLAIM_TASK:
            if self.parameters.task_claim_mode == "assigned":
                # Only lead can assign tasks
                if self.dimensions.authority == "hierarchy" and agent_state.identity.id != self.lead_agent_id:
                    return EnforcementResult(
                        allowed=False,
                        reason="In hierarchical authority with assigned tasks, only the lead assigns tasks.",
                    )
            # Check concurrent task limit
            if agent_state.current_focus and self.parameters.max_concurrent_tasks <= 1:
                return EnforcementResult(
                    allowed=False,
                    reason=f"Already working on: {agent_state.current_focus}. Release current task first.",
                )

        return EnforcementResult(allowed=True)

    def _check_review_requirements(self, action: Action, agent_state: AgentState) -> EnforcementResult:
        """Enforce review requirements before certain actions."""
        # When review is required, writing files to already-reviewed paths
        # should trigger re-review. For now, just log.
        return EnforcementResult(allowed=True)

    # -----------------------------------------------------------------------
    # Filtering — control what agents see
    # -----------------------------------------------------------------------

    def filter_messages(
        self,
        messages: list[Message],
        agent_id: str,
    ) -> list[Message]:
        """Filter messages based on communication topology and information rules."""
        if self.dimensions.communication == "mesh" and self.dimensions.information == "transparent":
            # Everyone sees everything
            return [m for m in messages if m.sender_id != agent_id]

        filtered = []
        for msg in messages:
            if msg.sender_id == agent_id:
                continue

            # Direct messages always delivered
            if not msg.is_broadcast and agent_id in (msg.receiver_ids or []):
                filtered.append(msg)
                continue

            # Broadcast delivery rules
            if msg.is_broadcast:
                if self.dimensions.communication in ("mesh", "broadcast"):
                    filtered.append(msg)
                elif self.dimensions.communication == "hub-spoke":
                    # Only delivered to/from lead
                    if msg.sender_id == self.lead_agent_id or agent_id == self.lead_agent_id:
                        filtered.append(msg)
                elif self.dimensions.communication == "whisper":
                    # Broadcasts converted to nothing in whisper mode
                    pass
                elif self.dimensions.communication == "clustered":
                    # Delivered within same group
                    if self._in_same_group(msg.sender_id, agent_id):
                        filtered.append(msg)

            # Mesh: direct messages + broadcasts all pass
            elif self.dimensions.communication == "mesh":
                filtered.append(msg)

        return filtered

    def filter_files(
        self,
        files: list[dict[str, Any]],
        agent_state: AgentState,
    ) -> list[dict[str, Any]]:
        """Filter file visibility based on information dimension."""
        if self.dimensions.information == "transparent":
            return files

        if self.dimensions.information == "need-to-know":
            # Only see files you've touched or that relate to your focus
            touched = {m.related_files[0] for m in agent_state.memories
                       if m.related_files}
            return [f for f in files if f["path"] in touched or self._file_relevant_to_focus(f, agent_state)]

        if self.dimensions.information == "curated":
            # Lead decides what's visible — for now, show all to lead, recent to others
            if agent_state.identity.id == self.lead_agent_id:
                return files
            # Others see recently modified files only
            return files[:10]

        if self.dimensions.information == "filtered":
            # Only see files in your role's domain
            role = self.agent_roles.get(agent_state.identity.id, "general")
            return [f for f in files if self._file_matches_role(f, role)]

        return files

    def filter_agent_visibility(
        self,
        agents: list[dict[str, Any]],
        agent_id: str,
    ) -> list[dict[str, Any]]:
        """Control whether agents know about each other."""
        if self.dimensions.information == "transparent":
            return [a for a in agents if a.get("id") != agent_id]

        if self.dimensions.communication == "whisper":
            # Can only see agents you've directly communicated with
            known = self.communication_history.get(agent_id, set())
            return [a for a in agents if a.get("id") in known]

        if self.dimensions.communication == "clustered":
            # Can only see agents in the same group
            my_group = self.agent_groups.get(agent_id)
            return [
                a for a in agents
                if a.get("id") != agent_id
                and self.agent_groups.get(a.get("id")) == my_group
            ]

        return [a for a in agents if a.get("id") != agent_id]

    # -----------------------------------------------------------------------
    # Soft shaping — augment system prompts based on org structure
    # -----------------------------------------------------------------------

    def shape_system_prompt(self, base_prompt: str, agent_state: AgentState) -> str:
        """Add org-specific instructions to the system prompt.

        These are behavioural nudges, not hard constraints — the model can
        still reason freely, but it understands its role in the organisation.
        """
        additions: list[str] = []

        # Authority
        if self.dimensions.authority == "hierarchy":
            if agent_state.identity.id == self.lead_agent_id:
                additions.append(
                    "You are the lead agent. Coordinate the team: assign tasks, "
                    "review work, and make final decisions. Other agents report to you."
                )
            else:
                additions.append(
                    "You report to the lead agent. Check with them before starting "
                    "major work. Follow their task assignments."
                )
        elif self.dimensions.authority == "flat":
            additions.append(
                "This is a flat organisation. No one is in charge — coordinate "
                "as equals. Claim tasks voluntarily and negotiate when priorities conflict."
            )
        elif self.dimensions.authority == "consensus":
            additions.append(
                "Decisions require consensus. Before making significant changes, "
                "propose your plan and wait for agreement from other agents."
            )
        elif self.dimensions.authority == "distributed":
            additions.append(
                "Authority is distributed by expertise. Defer to whoever has "
                "the most experience with the relevant part of the codebase."
            )

        # Communication
        if self.dimensions.communication == "whisper":
            additions.append(
                "Communication is private. Only send direct messages to specific agents. "
                "Broadcasting is not allowed."
            )
        elif self.dimensions.communication == "hub-spoke":
            if agent_state.identity.id == self.lead_agent_id:
                additions.append(
                    "All communication flows through you. Relay important information "
                    "between agents as needed."
                )
            else:
                additions.append(
                    "Send messages through the lead agent. Direct agent-to-agent "
                    "communication is limited."
                )

        # Incentives
        if self.dimensions.incentives == "competitive":
            additions.append(
                "You're evaluated individually. Focus on producing the best work "
                "you can. Your contributions are tracked separately."
            )
        elif self.dimensions.incentives == "collaborative":
            additions.append(
                "Success is shared. Help other agents when they're stuck. "
                "The team's output matters more than individual contributions."
            )
        elif self.dimensions.incentives == "reputation":
            additions.append(
                "Your reputation is built through quality work and helpful reviews. "
                "Other agents will defer to you on topics where you've proven expertise."
            )

        # Decisions
        if self.dimensions.decisions == "meritocratic":
            additions.append(
                "Decisions are merit-based. Agents with proven track records on "
                "relevant topics have more weight in architectural discussions."
            )
        elif self.dimensions.decisions == "autonomous":
            additions.append(
                "You have full autonomy over your work. Make decisions independently. "
                "No need to seek approval unless you want feedback."
            )
        elif self.dimensions.decisions == "top-down":
            if agent_state.identity.id == self.lead_agent_id:
                additions.append("You make all final decisions for the team.")
            else:
                additions.append("Major decisions are made by the lead agent.")

        # Roles
        role = self.agent_roles.get(agent_state.identity.id)
        if role:
            additions.append(f"Your assigned role: {role}.")
        elif self.dimensions.roles == "emergent":
            if agent_state.skills:
                top_skill = max(agent_state.skills.values(), key=lambda s: s.action_count)
                additions.append(
                    f"You've naturally specialised in {top_skill.name} "
                    f"({top_skill.tier} level). Lean into this expertise."
                )

        # Groups
        if self.dimensions.groups == "task-based":
            additions.append(
                "Teams form around tasks. Collaborate with whoever is working on "
                "related problems."
            )

        # Adaptation
        if self.dimensions.adaptation == "real-time":
            additions.append(
                "The organisation can restructure at any time. If the current approach "
                "isn't working, propose changes."
            )

        # Community-added dimensions — automatically included in prompt shaping.
        # Any key=value pair in the org YAML that isn't a built-in dimension
        # gets described to the agent. This is how extensibility works without
        # code changes.
        for dim_name, dim_value in self.dimensions.extra.items():
            additions.append(
                f"Organisational dimension '{dim_name}' is set to '{dim_value}'."
            )

        if not additions:
            return base_prompt

        return base_prompt + "\n\n" + " ".join(additions)

    # -----------------------------------------------------------------------
    # Role assignment
    # -----------------------------------------------------------------------

    def assign_initial_roles(self, agent_ids: list[str]) -> None:
        """Assign roles and groups based on the org dimensions."""
        if self.dimensions.roles == "assigned" and self.dimensions.authority == "hierarchy":
            # First agent is lead
            if agent_ids:
                self.lead_agent_id = agent_ids[0]
                self.agent_roles[agent_ids[0]] = "lead"
                for aid in agent_ids[1:]:
                    self.agent_roles[aid] = "contributor"

        elif self.dimensions.authority in ("hierarchy", "rotating"):
            if agent_ids:
                self.lead_agent_id = agent_ids[0]

        elif self.dimensions.authority in ("flat", "distributed", "consensus", "anarchic"):
            self.lead_agent_id = None

        # Assign initial groups
        self._assign_initial_groups(agent_ids)

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def record_communication(self, sender_id: str, receiver_ids: list[str]) -> None:
        """Record that agents communicated — used for whisper visibility."""
        if sender_id not in self.communication_history:
            self.communication_history[sender_id] = set()
        for rid in receiver_ids:
            self.communication_history[sender_id].add(rid)
            # Bidirectional — receiver also knows about sender
            if rid not in self.communication_history:
                self.communication_history[rid] = set()
            self.communication_history[rid].add(sender_id)

    def update_task_groups(self, focus_map: dict[str, str | None]) -> None:
        """Update group assignments for task-based grouping.

        Agents working on the same task (current_focus) are in the same group.
        Agents with no focus get their own singleton group.
        """
        if self.dimensions.groups != "task-based":
            return

        task_groups: dict[str, list[str]] = {}
        no_focus: list[str] = []

        for agent_id, focus in focus_map.items():
            if focus:
                task_groups.setdefault(focus, []).append(agent_id)
            else:
                no_focus.append(agent_id)

        self.agent_groups.clear()
        for i, (task, members) in enumerate(task_groups.items()):
            group_name = f"task_{i}"
            for agent_id in members:
                self.agent_groups[agent_id] = group_name

        # Unfocused agents each get their own group (isolated)
        for agent_id in no_focus:
            self.agent_groups[agent_id] = f"solo_{agent_id}"

    def _assign_initial_groups(self, agent_ids: list[str]) -> None:
        """Assign initial groups based on the groups dimension."""
        if self.dimensions.groups in ("imposed", "persistent"):
            # Split agents into groups of 2-3
            group_size = max(2, len(agent_ids) // max(1, len(agent_ids) // 3))
            for i, aid in enumerate(agent_ids):
                self.agent_groups[aid] = f"group_{i // group_size}"
        elif self.dimensions.groups == "task-based":
            # All start ungrouped — updated dynamically by update_task_groups
            for aid in agent_ids:
                self.agent_groups[aid] = "unassigned"
        else:
            # self-selected, temporary — all in one group (no restriction)
            for aid in agent_ids:
                self.agent_groups[aid] = "all"

    def _in_same_group(self, agent_a: str, agent_b: str) -> bool:
        """Check if two agents are in the same group (for clustered communication)."""
        group_a = self.agent_groups.get(agent_a)
        group_b = self.agent_groups.get(agent_b)
        if group_a is None or group_b is None:
            return True  # if no groups assigned, allow
        return group_a == group_b

    def _file_relevant_to_focus(self, file_info: dict[str, Any], agent_state: AgentState) -> bool:
        """Check if a file is relevant to an agent's current focus."""
        if not agent_state.current_focus:
            return False
        path = file_info.get("path", "").lower()
        focus_words = agent_state.current_focus.lower().split()
        return any(word in path for word in focus_words if len(word) > 3)

    def _file_matches_role(self, file_info: dict[str, Any], role: str) -> bool:
        """Check if a file matches an agent's role domain."""
        path = file_info.get("path", "").lower()
        role_patterns = {
            "testing": ["test", "spec", "fixture"],
            "frontend": ["src", "component", "page", "style", "css", "html"],
            "backend": ["api", "server", "route", "model", "db", "migration"],
            "devops": ["docker", "ci", "deploy", "config", "yaml", "toml"],
        }
        patterns = role_patterns.get(role, [])
        return not patterns or any(p in path for p in patterns)
