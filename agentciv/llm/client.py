"""LLM client — pluggable interface using native tool-use APIs.

Key principle: leverage what frontier models already excel at.
Claude and GPT-4o have structured tool calling built in — the model calls
write_file(path, content) as a typed function call. No regex parsing,
no missed code blocks, no fragile text extraction.

Multi-turn tool use: the model calls a tool, we execute it and feed the
result back, the model reasons about the result and decides what to do
next. This is the native conversation loop — observe, act, observe result,
act again — handled entirely by the model's own reasoning.

Our job: assemble the right context. The model's job: reason and act.
"""

from __future__ import annotations

import asyncio
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
    id: str  # tool_use_id — needed for multi-turn result pairing
    name: str
    arguments: dict[str, Any]


@dataclass
class ToolResult:
    """Result of executing a tool call — fed back to the LLM."""
    tool_call_id: str
    output: str
    is_error: bool = False


@dataclass
class LLMResponse:
    """Response from an LLM call — may contain text, tool calls, or both."""
    content: str  # text reasoning (may be empty if tool call only)
    tool_calls: list[ToolCall] = field(default_factory=list)
    model: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    # Raw response content for conversation continuation (provider-specific)
    _raw_content: Any = field(default=None, repr=False)

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
        self, messages: list[dict[str, Any]], system: str | None = None,
        tools: list[dict[str, Any]] | None = None,
    ) -> LLMResponse:
        """Send messages with tool definitions and get a response with tool calls."""
        ...

    @abstractmethod
    def format_assistant_message(self, response: LLMResponse) -> dict[str, Any]:
        """Format the assistant's response as a message for conversation history."""
        ...

    @abstractmethod
    def format_tool_results(self, results: list[ToolResult]) -> dict[str, Any] | list[dict[str, Any]]:
        """Format tool execution results as a message for the conversation."""
        ...

    def estimate_tokens(self, text: str) -> int:
        return len(text) // 4


class AnthropicClient(LLMClient):
    """Claude models via the Anthropic API with native tool-use.

    Multi-turn format:
      user → assistant [text + tool_use blocks] → user [tool_result blocks] → assistant
    """

    def __init__(self, model: str = "claude-sonnet-4-6", max_tokens: int = 4096):
        self.model = model
        self.max_tokens = max_tokens
        self._client: Any = None

    def _get_client(self) -> Any:
        if self._client is None:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise RuntimeError(
                    "ANTHROPIC_API_KEY is not set.\n\n"
                    "To fix this:\n"
                    "  1. Get your API key from console.anthropic.com\n"
                    "  2. Set it: export ANTHROPIC_API_KEY=\"your-key-here\"\n"
                    "  3. Or add it to your shell profile (~/.zshrc or ~/.bashrc)\n\n"
                    "If you don't want to use API mode, try Max Plan mode instead — it's free.\n"
                    "Run: agentciv setup"
                )
            try:
                import anthropic
                self._client = anthropic.AsyncAnthropic(api_key=api_key)
            except ImportError:
                raise RuntimeError("Install anthropic: pip install anthropic")
        return self._client

    async def complete_with_tools(
        self, messages: list[dict[str, Any]], system: str | None = None,
        tools: list[dict[str, Any]] | None = None,
    ) -> LLMResponse:
        client = self._get_client()
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": messages,
            "tools": tools or AGENT_TOOLS,
        }
        if system:
            kwargs["system"] = system

        import anthropic as _anthropic
        _retryable = (
            _anthropic.RateLimitError,
            _anthropic.APITimeoutError,
            _anthropic.APIConnectionError,
            _anthropic.InternalServerError,
        )
        _max_retries = 3
        for _attempt in range(_max_retries + 1):
            try:
                response = await client.messages.create(**kwargs)
                break
            except _retryable as e:
                if _attempt >= _max_retries:
                    raise _enhance_api_error(e, provider="Anthropic", model=self.model)
                _delay = 2 ** _attempt  # 1s, 2s, 4s
                log.warning(
                    "Anthropic API transient error (attempt %d/%d): %s — retrying in %ds",
                    _attempt + 1, _max_retries, type(e).__name__, _delay,
                )
                await asyncio.sleep(_delay)
            except Exception as e:
                raise _enhance_api_error(e, provider="Anthropic", model=self.model)

        # Extract text and tool calls from response blocks
        text_parts: list[str] = []
        tool_calls: list[ToolCall] = []

        for block in response.content:
            if hasattr(block, "text"):
                text_parts.append(block.text)
            elif block.type == "tool_use":
                tool_calls.append(ToolCall(
                    id=block.id,
                    name=block.name,
                    arguments=block.input,
                ))

        return LLMResponse(
            content="\n".join(text_parts),
            tool_calls=tool_calls,
            model=self.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            _raw_content=response.content,
        )

    def format_assistant_message(self, response: LLMResponse) -> dict[str, Any]:
        """Anthropic: assistant content is the raw content blocks list."""
        # Use raw content blocks (preserves tool_use block structure exactly)
        if response._raw_content is not None:
            # Convert SDK objects to dicts for serialisation
            content = []
            for block in response._raw_content:
                if hasattr(block, "text"):
                    content.append({"type": "text", "text": block.text})
                elif block.type == "tool_use":
                    content.append({
                        "type": "tool_use",
                        "id": block.id,
                        "name": block.name,
                        "input": block.input,
                    })
            return {"role": "assistant", "content": content}
        # Fallback: reconstruct from parsed data
        content = []
        if response.content:
            content.append({"type": "text", "text": response.content})
        for tc in response.tool_calls:
            content.append({
                "type": "tool_use",
                "id": tc.id,
                "name": tc.name,
                "input": tc.arguments,
            })
        return {"role": "assistant", "content": content}

    def format_tool_results(self, results: list[ToolResult]) -> dict[str, Any]:
        """Anthropic: tool results are user messages with tool_result content blocks."""
        content = []
        for r in results:
            block: dict[str, Any] = {
                "type": "tool_result",
                "tool_use_id": r.tool_call_id,
                "content": r.output,
            }
            if r.is_error:
                block["is_error"] = True
            content.append(block)
        return {"role": "user", "content": content}


class OpenAIClient(LLMClient):
    """GPT models via the OpenAI API with native function calling.

    Multi-turn format:
      user → assistant [tool_calls] → tool [result] messages → assistant
    """

    def __init__(self, model: str = "gpt-4o", max_tokens: int = 4096):
        self.model = model
        self.max_tokens = max_tokens
        self._client: Any = None

    def _get_client(self) -> Any:
        if self._client is None:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise RuntimeError(
                    "OPENAI_API_KEY is not set.\n\n"
                    "To fix this:\n"
                    "  1. Get your API key from platform.openai.com\n"
                    "  2. Set it: export OPENAI_API_KEY=\"your-key-here\"\n"
                    "  3. Or add it to your shell profile (~/.zshrc or ~/.bashrc)\n\n"
                    "If you don't want to use API mode, try Max Plan mode instead — it's free.\n"
                    "Run: agentciv setup"
                )
            try:
                import openai
                self._client = openai.AsyncOpenAI(api_key=api_key)
            except ImportError:
                raise RuntimeError("Install openai: pip install openai")
        return self._client

    async def complete_with_tools(
        self, messages: list[dict[str, Any]], system: str | None = None,
        tools: list[dict[str, Any]] | None = None,
    ) -> LLMResponse:
        client = self._get_client()
        api_messages: list[dict[str, Any]] = []
        if system:
            api_messages.append({"role": "system", "content": system})
        api_messages.extend(messages)

        # Convert custom tools to OpenAI format if provided
        if tools is not None:
            openai_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": t["name"],
                        "description": t["description"],
                        "parameters": t["input_schema"],
                    },
                }
                for t in tools
            ]
        else:
            openai_tools = get_openai_tools()

        try:
            response = await client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=api_messages,
                tools=openai_tools,
            )
        except Exception as e:
            raise _enhance_api_error(e, provider="OpenAI", model=self.model)

        choice = response.choices[0]
        content = choice.message.content or ""
        tool_calls: list[ToolCall] = []

        raw_tool_calls = choice.message.tool_calls
        if raw_tool_calls:
            for tc in raw_tool_calls:
                tool_calls.append(ToolCall(
                    id=tc.id,
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
            _raw_content=raw_tool_calls,
        )

    def format_assistant_message(self, response: LLMResponse) -> dict[str, Any]:
        """OpenAI: assistant message with tool_calls array."""
        msg: dict[str, Any] = {"role": "assistant"}
        if response.content:
            msg["content"] = response.content
        else:
            msg["content"] = None
        if response.tool_calls:
            msg["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.name,
                        "arguments": json.dumps(tc.arguments),
                    },
                }
                for tc in response.tool_calls
            ]
        return msg

    def format_tool_results(self, results: list[ToolResult]) -> dict[str, Any]:
        """OpenAI: each tool result is a separate 'tool' role message.

        Returns a list disguised as a dict — caller should extend, not append.
        We return a list here because OpenAI requires separate messages per tool result.
        """
        # Return as a list — the agent loop handles this
        return [
            {
                "role": "tool",
                "tool_call_id": r.tool_call_id,
                "content": r.output,
            }
            for r in results
        ]


class MockClient(LLMClient):
    """Mock LLM for testing — returns structured tool calls with IDs."""

    def __init__(self) -> None:
        self._call_count = 0

    async def complete_with_tools(
        self, messages: list[dict[str, Any]], system: str | None = None,
        tools: list[dict[str, Any]] | None = None,
    ) -> LLMResponse:
        # Cycle through a realistic sequence of tool calls
        sequence = [
            LLMResponse(
                content="I need to understand the project first.",
                tool_calls=[ToolCall(id="tc_01", name="read_file", arguments={"path": "main.py"})],
                model="mock",
            ),
            LLMResponse(
                content="I see the structure. Let me implement the endpoints.",
                tool_calls=[ToolCall(id="tc_02", name="write_file", arguments={
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
                tool_calls=[ToolCall(id="tc_03", name="broadcast", arguments={
                    "message": "Implemented /hello and /status endpoints in main.py.",
                })],
                model="mock",
            ),
            LLMResponse(
                content="Task complete.",
                tool_calls=[ToolCall(id="tc_04", name="done", arguments={})],
                model="mock",
            ),
        ]
        resp = sequence[self._call_count % len(sequence)]
        self._call_count += 1
        # Estimate tokens from the latest user message
        prompt_text = ""
        for msg in messages:
            if isinstance(msg.get("content"), str):
                prompt_text += msg["content"]
        resp.input_tokens = len(prompt_text) // 4
        resp.output_tokens = 50
        return resp

    def format_assistant_message(self, response: LLMResponse) -> dict[str, Any]:
        content = []
        if response.content:
            content.append({"type": "text", "text": response.content})
        for tc in response.tool_calls:
            content.append({
                "type": "tool_use",
                "id": tc.id,
                "name": tc.name,
                "input": tc.arguments,
            })
        return {"role": "assistant", "content": content}

    def format_tool_results(self, results: list[ToolResult]) -> dict[str, Any]:
        content = []
        for r in results:
            block: dict[str, Any] = {
                "type": "tool_result",
                "tool_use_id": r.tool_call_id,
                "content": r.output,
            }
            if r.is_error:
                block["is_error"] = True
            content.append(block)
        return {"role": "user", "content": content}


def _enhance_api_error(error: Exception, provider: str, model: str) -> Exception:
    """Transform API errors into teaching moments.

    Every error should answer: what happened, why, and what to try.
    """
    msg = str(error).lower()

    # Authentication errors
    if "auth" in msg or "api key" in msg or "401" in msg or "invalid x-api-key" in msg:
        env_var = "ANTHROPIC_API_KEY" if provider == "Anthropic" else "OPENAI_API_KEY"
        return RuntimeError(
            f"{provider} API authentication failed.\n\n"
            f"Your {env_var} is missing or invalid.\n\n"
            f"To fix this:\n"
            f"  1. Get your API key from {'console.anthropic.com' if provider == 'Anthropic' else 'platform.openai.com'}\n"
            f"  2. Set it: export {env_var}=\"your-key-here\"\n"
            f"  3. Or add it to your shell profile (~/.zshrc or ~/.bashrc)\n\n"
            f"If you don't want to use API mode, try Max Plan mode instead — it's free.\n"
            f"Run: agentciv setup"
        )

    # Rate limiting
    if "rate" in msg or "429" in msg or "too many" in msg:
        return RuntimeError(
            f"{provider} rate limit hit.\n\n"
            f"You're making too many API calls too quickly.\n\n"
            f"To fix this:\n"
            f"  - Wait a minute and try again\n"
            f"  - Use fewer agents (--agents 2)\n"
            f"  - Use --model mock to test without API calls\n"
            f"  - Check your {provider} usage dashboard for current limits"
        )

    # Model not found
    if "model" in msg and ("not found" in msg or "does not exist" in msg or "404" in msg):
        return RuntimeError(
            f"Model '{model}' was not found by {provider}.\n\n"
            f"This usually means:\n"
            f"  - The model name is misspelled\n"
            f"  - Your API key doesn't have access to this model\n"
            f"  - The model has been deprecated\n\n"
            f"Try one of these instead:\n"
            f"  {'Anthropic: claude-sonnet-4-6, claude-haiku-4-5-20251001, claude-opus-4-6' if provider == 'Anthropic' else 'OpenAI: gpt-4o, gpt-4o-mini, o1, o3'}\n\n"
            f"Or use --model mock to test without API calls."
        )

    # Quota/billing
    if "quota" in msg or "billing" in msg or "insufficient" in msg:
        return RuntimeError(
            f"{provider} billing issue — your account may need credits.\n\n"
            f"Check your account at {'console.anthropic.com' if provider == 'Anthropic' else 'platform.openai.com'}\n\n"
            f"To test without API costs, use --model mock."
        )

    # Connection errors
    if "connect" in msg or "timeout" in msg or "network" in msg:
        return RuntimeError(
            f"Could not connect to {provider} API.\n\n"
            f"Check your internet connection and try again.\n"
            f"If the issue persists, check {provider}'s status page."
        )

    # Default: pass through with context
    return RuntimeError(
        f"{provider} API error with model '{model}': {error}\n\n"
        f"If this keeps happening, try:\n"
        f"  - A different model (--model claude-sonnet-4-6 or --model gpt-4o)\n"
        f"  - Mock mode for testing (--model mock)\n"
        f"  - Check {provider}'s status page for outages"
    )


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
