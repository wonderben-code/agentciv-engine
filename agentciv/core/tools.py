"""Tool definitions for agent actions.

Instead of parsing free text, we define tools that the LLM calls natively
using structured tool-use APIs. This leverages what frontier models already
excel at — no regex, no missed code blocks, no fragile extraction.
"""

from __future__ import annotations

# Anthropic tool-use format
AGENT_TOOLS = [
    {
        "name": "read_file",
        "description": "Read the contents of a file in the project.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "File path relative to project root",
                },
            },
            "required": ["path"],
        },
    },
    {
        "name": "write_file",
        "description": "Write content to a file. Creates parent directories if needed. Use this to implement code changes.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "File path relative to project root",
                },
                "content": {
                    "type": "string",
                    "description": "The full file content to write",
                },
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "create_file",
        "description": "Create a new file. Fails if the file already exists.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "File path relative to project root",
                },
                "content": {
                    "type": "string",
                    "description": "The file content",
                },
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "run_command",
        "description": "Run a shell command (e.g. tests, build, lint). Only whitelisted commands are allowed.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to run",
                },
            },
            "required": ["command"],
        },
    },
    {
        "name": "communicate",
        "description": "Send a message to a specific agent. Use this to coordinate, share findings, ask questions, or request help.",
        "input_schema": {
            "type": "object",
            "properties": {
                "target_agent": {
                    "type": "string",
                    "description": "Name of the agent to message",
                },
                "message": {
                    "type": "string",
                    "description": "The message content",
                },
            },
            "required": ["target_agent", "message"],
        },
    },
    {
        "name": "broadcast",
        "description": "Send a message to all agents in the community. Use for announcements, status updates, or proposals.",
        "input_schema": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message content",
                },
            },
            "required": ["message"],
        },
    },
    {
        "name": "claim_task",
        "description": "Signal that you're working on a specific task. Helps other agents avoid duplicating effort.",
        "input_schema": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "What you're working on",
                },
            },
            "required": ["description"],
        },
    },
    {
        "name": "release_task",
        "description": "Stop working on your current task, making it available for others.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "request_review",
        "description": "Ask other agents to review your recent work.",
        "input_schema": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "What you'd like reviewed",
                },
            },
            "required": ["description"],
        },
    },
    {
        "name": "done",
        "description": "Signal that you have nothing more to do this tick. Use when you've completed your actions or are waiting.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
]


# OpenAI function-calling format (converted from above)
def get_openai_tools() -> list[dict]:
    """Convert Anthropic tool format to OpenAI function-calling format."""
    return [
        {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["input_schema"],
            },
        }
        for tool in AGENT_TOOLS
    ]
