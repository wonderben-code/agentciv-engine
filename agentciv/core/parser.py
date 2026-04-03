# Legacy text-parsing fallback — kept for non-tool-use model support.
"""Action parser — converts LLM natural language responses into concrete Actions.

The agent's LLM response is free-form text containing reasoning and a chosen
action. This parser extracts the action, file paths, targets, and content.
Designed to be forgiving — agents express themselves differently.
"""

from __future__ import annotations

import re
from ..core.types import Action, ActionType


# Maps keywords/patterns to action types
ACTION_PATTERNS: list[tuple[re.Pattern[str], ActionType]] = [
    (re.compile(r"(?:^|\n)\s*(?:ACTION:\s*)?READ_FILE\s+(.+)", re.IGNORECASE), ActionType.READ_FILE),
    (re.compile(r"(?:^|\n)\s*(?:ACTION:\s*)?WRITE_FILE\s+(.+)", re.IGNORECASE), ActionType.WRITE_FILE),
    (re.compile(r"(?:^|\n)\s*(?:ACTION:\s*)?CREATE_FILE\s+(.+)", re.IGNORECASE), ActionType.CREATE_FILE),
    (re.compile(r"(?:^|\n)\s*(?:ACTION:\s*)?DELETE_FILE\s+(.+)", re.IGNORECASE), ActionType.DELETE_FILE),
    (re.compile(r"(?:^|\n)\s*(?:ACTION:\s*)?RUN_COMMAND\s+(.+)", re.IGNORECASE), ActionType.RUN_COMMAND),
    (re.compile(r"(?:^|\n)\s*(?:ACTION:\s*)?COMMUNICATE\s+(.+)", re.IGNORECASE), ActionType.COMMUNICATE),
    (re.compile(r"(?:^|\n)\s*(?:ACTION:\s*)?BROADCAST\s+(.+)", re.IGNORECASE), ActionType.BROADCAST),
    (re.compile(r"(?:^|\n)\s*(?:ACTION:\s*)?CLAIM_TASK\s+(.+)", re.IGNORECASE), ActionType.CLAIM_TASK),
    (re.compile(r"(?:^|\n)\s*(?:ACTION:\s*)?RELEASE_TASK", re.IGNORECASE), ActionType.RELEASE_TASK),
    (re.compile(r"(?:^|\n)\s*(?:ACTION:\s*)?REQUEST_REVIEW", re.IGNORECASE), ActionType.REQUEST_REVIEW),
    (re.compile(r"(?:^|\n)\s*(?:ACTION:\s*)?PROPOSE_RESTRUCTURE\s+(.+)", re.IGNORECASE), ActionType.PROPOSE_RESTRUCTURE),
    (re.compile(r"(?:^|\n)\s*(?:ACTION:\s*)?VOTE\s+(.+)", re.IGNORECASE), ActionType.VOTE),
    (re.compile(r"(?:^|\n)\s*(?:ACTION:\s*)?IDLE", re.IGNORECASE), ActionType.IDLE),
]

# Fallback patterns — less structured agent responses
FALLBACK_PATTERNS: list[tuple[re.Pattern[str], ActionType]] = [
    (re.compile(r"(?:I(?:'ll| will|'m going to)\s+)?read\s+(?:the\s+)?(?:file\s+)?[`\"']?([^\s`\"']+)", re.IGNORECASE), ActionType.READ_FILE),
    (re.compile(r"(?:I(?:'ll| will|'m going to)\s+)?(?:write|edit|modify|update)\s+(?:the\s+)?(?:file\s+)?[`\"']?([^\s`\"']+)", re.IGNORECASE), ActionType.WRITE_FILE),
    (re.compile(r"(?:I(?:'ll| will|'m going to)\s+)?create\s+(?:a\s+)?(?:new\s+)?(?:file\s+)?[`\"']?([^\s`\"']+)", re.IGNORECASE), ActionType.CREATE_FILE),
    (re.compile(r"(?:I(?:'ll| will|'m going to)\s+)?run\s+(?:the\s+)?(?:command\s+)?[`\"']?(.+?)[`\"']?\s*$", re.IGNORECASE | re.MULTILINE), ActionType.RUN_COMMAND),
    (re.compile(r"(?:I(?:'ll| will|'m going to)\s+)?(?:message|tell|ask|say to)\s+(\w+)", re.IGNORECASE), ActionType.COMMUNICATE),
    (re.compile(r"(?:I(?:'ll| will|'m going to)\s+)?(?:broadcast|announce|tell everyone)", re.IGNORECASE), ActionType.BROADCAST),
    (re.compile(r"(?:I(?:'ll| will|'m going to)\s+)?(?:claim|take on|work on|tackle)", re.IGNORECASE), ActionType.CLAIM_TASK),
    (re.compile(r"(?:I(?:'ll| will|'m going to)\s+)?(?:wait|observe|hold|idle|pause|skip)", re.IGNORECASE), ActionType.IDLE),
]


def parse_action(response: str, agent_id: str, tick: int) -> Action:
    """Parse an LLM response into a concrete Action.

    Tries structured patterns first (ACTION: READ_FILE path), then falls
    back to natural language patterns. Returns IDLE if nothing matches.
    """
    # Extract reasoning (everything before the action line)
    reasoning = response.strip()

    # Try structured patterns first
    for pattern, action_type in ACTION_PATTERNS:
        match = pattern.search(response)
        if match:
            return _build_action(action_type, match, agent_id, tick, reasoning, response)

    # Try fallback natural language patterns
    for pattern, action_type in FALLBACK_PATTERNS:
        match = pattern.search(response)
        if match:
            return _build_action(action_type, match, agent_id, tick, reasoning, response)

    # Nothing matched — agent is idle or confused
    return Action(
        type=ActionType.IDLE,
        agent_id=agent_id,
        tick=tick,
        reasoning=reasoning,
    )


def _build_action(
    action_type: ActionType,
    match: re.Match[str],
    agent_id: str,
    tick: int,
    reasoning: str,
    full_response: str,
) -> Action:
    """Build an Action from a regex match."""
    groups = match.groups()
    arg = groups[0].strip() if groups else ""

    action = Action(
        type=action_type,
        agent_id=agent_id,
        tick=tick,
        reasoning=reasoning,
    )

    if action_type in (ActionType.READ_FILE, ActionType.WRITE_FILE,
                       ActionType.CREATE_FILE, ActionType.DELETE_FILE):
        # Clean file path
        action.file_path = arg.strip("`\"' ")

        # For write/create, extract content (look for code block in response)
        if action_type in (ActionType.WRITE_FILE, ActionType.CREATE_FILE):
            content = _extract_code_block(full_response)
            if not content:
                # Fallback: grab everything after the ACTION line as content
                content = _extract_content_after_action(full_response)
            action.content = content

    elif action_type == ActionType.RUN_COMMAND:
        action.command = arg.strip("`\"' ")

    elif action_type == ActionType.COMMUNICATE:
        # First word is agent name, rest is message
        parts = arg.split(None, 1)
        if parts:
            action.target_agents = [parts[0]]
            action.content = parts[1] if len(parts) > 1 else ""

    elif action_type == ActionType.BROADCAST:
        action.content = arg

    elif action_type == ActionType.CLAIM_TASK:
        action.content = arg  # task description

    elif action_type == ActionType.PROPOSE_RESTRUCTURE:
        action.content = arg  # restructure proposal

    elif action_type == ActionType.VOTE:
        action.content = arg  # vote content

    return action


def _extract_code_block(text: str) -> str | None:
    """Extract content from a markdown code block in the response."""
    # Try fenced code block first
    fenced = re.search(r"```\w*\n(.*?)```", text, re.DOTALL)
    if fenced:
        return fenced.group(1)

    # Try indented code block (4 spaces or tab)
    lines = text.split("\n")
    code_lines = []
    in_code = False
    for line in lines:
        if line.startswith("    ") or line.startswith("\t"):
            code_lines.append(line[4:] if line.startswith("    ") else line[1:])
            in_code = True
        elif in_code and line.strip() == "":
            code_lines.append("")
        elif in_code:
            break

    if code_lines:
        return "\n".join(code_lines).strip()

    return None


def _extract_content_after_action(text: str) -> str | None:
    """Fallback: extract content that appears after the ACTION line.

    Some agents write the file content directly after the action without
    using a code fence. This grabs everything after the ACTION: WRITE_FILE line.
    """
    # Find the ACTION: WRITE_FILE or ACTION: CREATE_FILE line
    match = re.search(
        r"ACTION:\s*(?:WRITE_FILE|CREATE_FILE)\s+\S+\s*\n(.*)",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if match:
        content = match.group(1).strip()
        if content:
            return content
    return None
