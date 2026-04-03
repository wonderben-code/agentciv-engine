"""Auto-organisation — the crown jewel.

When `--org auto` is active, agents can propose and vote on changes to
their own organisational structure. Every N ticks (configurable), a
meta-tick occurs where agents discuss how to restructure.

The four-step progression of organisational intelligence:
  1. No choice — fixed hierarchy (status quo, every other tool)
  2. Human choice — presets and configuration (Engine v1)
  3. AI choice — agents vote on their own structure via meta-ticks (THIS)
  4. Fluid real-time adaptation — structure reshapes continuously (future)

Step 3 is where AI surpasses human organisational design: agents restructure
without ego, politics, or status anxiety.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from .config import OrgDimensions, RawParameters

log = logging.getLogger(__name__)


@dataclass
class Proposal:
    """A proposed change to the organisational structure."""
    id: str
    proposer_id: str
    proposer_name: str
    dimension: str
    current_value: str
    proposed_value: str
    reasoning: str
    tick: int
    votes: dict[str, str] = field(default_factory=dict)  # agent_id → "yes"/"no"
    vote_reasons: dict[str, str] = field(default_factory=dict)  # agent_id → reasoning

    @property
    def yes_count(self) -> int:
        return sum(1 for v in self.votes.values() if v == "yes")

    @property
    def no_count(self) -> int:
        return sum(1 for v in self.votes.values() if v == "no")

    @property
    def total_votes(self) -> int:
        return len(self.votes)

    def to_prompt(self) -> str:
        """Render proposal for agent context."""
        status = f"{self.yes_count} yes / {self.no_count} no"
        return (
            f"  [{self.id}] {self.proposer_name} proposes: "
            f"{self.dimension} → {self.proposed_value} "
            f"(currently: {self.current_value}). "
            f"Reason: {self.reasoning}. Votes: {status}"
        )


@dataclass
class RestructureEvent:
    """Record of an adopted restructure."""
    tick: int
    dimension: str
    old_value: str
    new_value: str
    proposer: str
    yes_votes: int
    no_votes: int


@dataclass
class AutoOrgManager:
    """Manages the self-organisation process for --org auto mode.

    Tracks proposals, collects votes, applies adopted changes.
    When learning data is available, provides empirical recommendations.
    """

    dimensions: OrgDimensions
    parameters: RawParameters
    agent_count: int = 0

    # Learning insights (injected from engine, empty string if no data)
    learning_prompt: str = ""

    # State
    _proposals: list[Proposal] = field(default_factory=list)
    _active_proposals: dict[str, Proposal] = field(default_factory=dict)
    _history: list[RestructureEvent] = field(default_factory=list)
    _proposal_counter: int = 0
    _last_meta_tick: int = 0

    def is_meta_tick(self, tick: int) -> bool:
        """Check if this tick should be a meta-tick (restructuring discussion)."""
        interval = self.parameters.meta_tick_interval
        if interval <= 0:
            return False
        return tick > 0 and tick % interval == 0

    def start_meta_tick(self, tick: int) -> None:
        """Prepare for a meta-tick. Clear stale proposals."""
        self._last_meta_tick = tick
        # Close any active proposals from previous meta-ticks
        for p in self._active_proposals.values():
            self._proposals.append(p)
        self._active_proposals.clear()
        log.info("Meta-tick %d: restructuring discussion open", tick)

    def submit_proposal(
        self,
        agent_id: str,
        agent_name: str,
        dimension: str,
        value: str,
        reasoning: str,
        tick: int,
    ) -> Proposal:
        """Submit a restructuring proposal."""
        self._proposal_counter += 1
        proposal_id = f"P{self._proposal_counter}"

        # Get current value
        if hasattr(self.dimensions, dimension):
            current = getattr(self.dimensions, dimension)
        else:
            current = self.dimensions.extra.get(dimension, "unknown")

        proposal = Proposal(
            id=proposal_id,
            proposer_id=agent_id,
            proposer_name=agent_name,
            dimension=dimension,
            current_value=current,
            proposed_value=value,
            reasoning=reasoning,
            tick=tick,
        )
        # Auto-vote yes from proposer
        proposal.votes[agent_id] = "yes"
        proposal.vote_reasons[agent_id] = "I proposed this change."

        self._active_proposals[proposal_id] = proposal
        log.info(
            "Proposal %s by %s: %s → %s (reason: %s)",
            proposal_id, agent_name, dimension, value, reasoning[:100],
        )
        return proposal

    def submit_vote(
        self,
        agent_id: str,
        proposal_id: str,
        vote: str,
        reasoning: str = "",
    ) -> str:
        """Submit a vote on an active proposal. Returns status message."""
        proposal = self._active_proposals.get(proposal_id)
        if not proposal:
            return f"Proposal {proposal_id} not found or already closed."

        if agent_id in proposal.votes:
            return f"You already voted on {proposal_id}."

        proposal.votes[agent_id] = vote
        if reasoning:
            proposal.vote_reasons[agent_id] = reasoning

        log.info(
            "Vote on %s by %s: %s",
            proposal_id, agent_id, vote,
        )
        return f"Vote recorded: {vote} on {proposal_id}. Current tally: {proposal.yes_count} yes / {proposal.no_count} no."

    def resolve_proposals(self, tick: int) -> list[RestructureEvent]:
        """Resolve all active proposals. Called at the end of a meta-tick.

        Returns list of adopted restructures.
        """
        adopted: list[RestructureEvent] = []
        threshold = self.parameters.restructure_threshold

        for pid, proposal in list(self._active_proposals.items()):
            if proposal.total_votes == 0:
                continue

            approval_rate = proposal.yes_count / max(proposal.total_votes, 1)

            if approval_rate >= threshold:
                # ADOPT the restructure
                self._apply_restructure(proposal)
                event = RestructureEvent(
                    tick=tick,
                    dimension=proposal.dimension,
                    old_value=proposal.current_value,
                    new_value=proposal.proposed_value,
                    proposer=proposal.proposer_name,
                    yes_votes=proposal.yes_count,
                    no_votes=proposal.no_count,
                )
                adopted.append(event)
                self._history.append(event)
                log.info(
                    "RESTRUCTURE ADOPTED: %s → %s (%.0f%% approval)",
                    proposal.dimension, proposal.proposed_value, approval_rate * 100,
                )
            else:
                log.info(
                    "Proposal %s rejected: %s → %s (%.0f%% approval, needed %.0f%%)",
                    pid, proposal.dimension, proposal.proposed_value,
                    approval_rate * 100, threshold * 100,
                )

            self._proposals.append(proposal)

        self._active_proposals.clear()
        return adopted

    def _apply_restructure(self, proposal: Proposal) -> None:
        """Apply an adopted restructure to the live dimensions."""
        dim = proposal.dimension
        val = proposal.proposed_value

        if hasattr(self.dimensions, dim) and dim != "extra":
            setattr(self.dimensions, dim, val)
        else:
            self.dimensions.extra[dim] = val

    def get_active_proposals_prompt(self) -> str:
        """Render active proposals for agent context."""
        if not self._active_proposals:
            return ""
        lines = ["Active restructuring proposals (vote with the 'vote' tool):"]
        for p in self._active_proposals.values():
            lines.append(p.to_prompt())
        return "\n".join(lines)

    def get_restructure_history_prompt(self) -> str:
        """Render restructure history for agent context."""
        if not self._history:
            return ""
        lines = ["Organisational changes adopted:"]
        for h in self._history[-5:]:  # last 5
            lines.append(
                f"  tick {h.tick}: {h.dimension} changed from '{h.old_value}' "
                f"to '{h.new_value}' (proposed by {h.proposer}, "
                f"{h.yes_votes}-{h.no_votes})"
            )
        return "\n".join(lines)

    def get_meta_tick_system_prompt(self) -> str:
        """Additional system prompt during meta-ticks.

        Includes learning insights when available, giving agents
        empirical data to inform restructuring decisions.
        """
        prompt = (
            "\n\nThis is a META-TICK — a restructuring discussion. "
            "Reflect on how the team has been working. Is the current "
            "organisational structure effective? Consider proposing changes "
            "using 'propose_restructure' or voting on existing proposals. "
            "You can also do regular work during a meta-tick."
        )
        if self.learning_prompt:
            prompt += self.learning_prompt
        return prompt

    @property
    def current_org_summary(self) -> str:
        """One-line summary of current org state."""
        return (
            f"authority={self.dimensions.authority}, "
            f"communication={self.dimensions.communication}, "
            f"roles={self.dimensions.roles}, "
            f"decisions={self.dimensions.decisions}"
        )
