"""LLM client — pluggable interface using native tool-use APIs.

Key principle: leverage what frontier models already excel at.
Claude and GPT-4o have structured tool calling built in — the model calls
write_file(path, content) as a typed function call. No regex parsing,
no missed code blocks, no fragile text extraction.

Our job: assemble the right context. The model's job: reason and act.
"""

from __future__ import annotations

import json
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from ..core.tools import AGENT_TOOLS, get_openai_tools

log = logging.getLogger(__name__)


@dataclass
class ToolCall:
    """A structured tool call from the LLM."""
    name: str
    arguments: dict[str, Any]


@dataclass
class LLMResponse:
    """Response from an LLM call — may contain text, tool calls, or both."""
    content: str  # text reasoning (may be empty if tool call only)
    tool_calls: list[ToolCall] = field(default_factory=list)
    model: str = ""
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    @property
    def has_tool_call(self) -> bool:
        return len(self.tool_calls) > 0


class LLMClient(ABC):
    """Abstract base for LLM providers."""

    @abstractmethod
    async def complete_with_tools(
        self, prompt: str, system: str | None = None,
    ) -> LLMResponse:
        """Send a prompt with tool definitions and get a response with tool calls."""
        ...

    def estimate_tokens(self, text: str) -> int:
        return len(text) // 4


class AnthropicClient(LLMClient):
    """Claude models via the Anthropic API with native tool-use."""

    def __init__(self, model: str = "claude-sonnet-4-6", max_tokens: int = 4096):
        self.model = model
        self.max_tokens = max_tokens
        self._client: Any = None

    def _get_client(self) -> Any:
        if self._client is None:
            try:
                import anthropic
                self._client = anthropic.AsyncAnthropic(
                    api_key=os.environ.get("ANTHROPIC_API_KEY"),
                )
            except ImportError:
                raise RuntimeError("Install anthropic: pip install anthropic")
        return self._client

    async def complete_with_tools(
        self, prompt: str, system: str | None = None,
    ) -> LLMResponse:
        client = self._get_client()
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [{"role": "user", "content": prompt}],
            "tools": AGENT_TOOLS,
        }
        if system:
            kwargs["system"] = system

        response = await client.messages.create(**kwargs)

        # Extract text and tool calls from response blocks
        text_parts: list[str] = []
        tool_calls: list[ToolCall] = []

        for block in response.content:
            if hasattr(block, "text"):
                text_parts.append(block.text)
            elif block.type == "tool_use":
                tool_calls.append(ToolCall(
                    name=block.name,
                    arguments=block.input,
                ))

        return LLMResponse(
            content="\n".join(text_parts),
            tool_calls=tool_calls,
            model=self.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )


class OpenAIClient(LLMClient):
    """GPT models via the OpenAI API with native function calling."""

    def __init__(self, model: str = "gpt-4o", max_tokens: int = 4096):
        self.model = model
        self.max_tokens = max_tokens
        self._client: Any = None

    def _get_client(self) -> Any:
        if self._client is None:
            try:
                import openai
                self._client = openai.AsyncOpenAI(
                    api_key=os.environ.get("OPENAI_API_KEY"),
                )
            except ImportError:
                raise RuntimeError("Install openai: pip install openai")
        return self._client

    async def complete_with_tools(
        self, prompt: str, system: str | None = None,
    ) -> LLMResponse:
        client = self._get_client()
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = await client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=messages,
            tools=get_openai_tools(),
        )

        choice = response.choices[0]
        content = choice.message.content or ""
        tool_calls: list[ToolCall] = []

        if choice.message.tool_calls:
            for tc in choice.message.tool_calls:
                tool_calls.append(ToolCall(
                    name=tc.function.name,
                    arguments=json.loads(tc.function.arguments),
                ))

        usage = response.usage
        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            model=self.model,
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
        )


class MockClient(LLMClient):
    """Mock LLM for testing — returns structured tool calls."""

    def __init__(self) -> None:
        self._call_count = 0

    async def complete_with_tools(
        self, prompt: str, system: str | None = None,
    ) -> LLMResponse:
        # Cycle through a realistic sequence of tool calls
        sequence = [
            LLMResponse(
                content="I need to understand the project first.",
                tool_calls=[ToolCall(name="read_file", arguments={"path": "main.py"})],
                model="mock",
            ),
            LLMResponse(
                content="I see TODOs for /hello and /status endpoints. Let me implement them.",
                tool_calls=[ToolCall(name="write_file", arguments={
                    "path": "main.py",
                    "content": (
                        "from http.server import HTTPServer, BaseHTTPRequestHandler\n"
                        "import json\n\n\n"
                        "class APIHandler(BaseHTTPRequestHandler):\n"
                        "    def do_GET(self):\n"
                        "        if self.path == '/hello':\n"
                        "            self._respond(200, {'message': 'Hello, World!'})\n"
                        "        elif self.path == '/status':\n"
                        "            self._respond(200, {'status': 'ok'})\n"
                        "        else:\n"
                        "            self._respond(404, {'error': 'not found'})\n\n"
                        "    def _respond(self, code, data):\n"
                        "        self.send_response(code)\n"
                        "        self.send_header('Content-Type', 'application/json')\n"
                        "        self.end_headers()\n"
                        "        self.wfile.write(json.dumps(data).encode())\n\n\n"
                        "if __name__ == '__main__':\n"
                        "    server = HTTPServer(('localhost', 8000), APIHandler)\n"
                        "    print('Server running on http://localhost:8000')\n"
                        "    server.serve_forever()\n"
                    ),
                })],
                model="mock",
            ),
            LLMResponse(
                content="Implementation complete. Broadcasting to team.",
                tool_calls=[ToolCall(name="broadcast", arguments={
                    "message": "Implemented /hello and /status endpoints in main.py.",
                })],
                model="mock",
            ),
            LLMResponse(
                content="Task complete.",
                tool_calls=[ToolCall(name="done", arguments={})],
                model="mock",
            ),
        ]
        resp = sequence[self._call_count % len(sequence)]
        self._call_count += 1
        resp.input_tokens = len(prompt) // 4
        resp.output_tokens = 50
        return resp


def create_client(model: str, max_tokens: int = 4096) -> LLMClient:
    """Factory: create the right client based on model name."""
    model_lower = model.lower()

    if model_lower == "mock":
        return MockClient()

    if any(x in model_lower for x in ["claude", "anthropic", "sonnet", "opus", "haiku"]):
        return AnthropicClient(model=model, max_tokens=max_tokens)

    if any(x in model_lower for x in ["gpt", "o1", "o3", "openai"]):
        return OpenAIClient(model=model, max_tokens=max_tokens)

    log.warning("Unknown model '%s', defaulting to OpenAI-compatible client", model)
    return OpenAIClient(model=model, max_tokens=max_tokens)
