"""LLM client — pluggable interface for any model provider.

Model-agnostic by design. Anthropic, OpenAI, Google, local models.
Different agents in the same community can run different models.
"""

from __future__ import annotations

import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

log = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Response from an LLM call."""
    content: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


class LLMClient(ABC):
    """Abstract base for LLM providers. Implement this to add a new provider."""

    @abstractmethod
    async def complete(self, prompt: str, system: str | None = None) -> LLMResponse:
        """Send a prompt and get a response."""
        ...

    @abstractmethod
    def estimate_tokens(self, text: str) -> int:
        """Rough token count estimate for budget tracking."""
        ...


class AnthropicClient(LLMClient):
    """Claude models via the Anthropic API."""

    def __init__(self, model: str = "claude-sonnet-4-6", max_tokens: int = 1024):
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

    async def complete(self, prompt: str, system: str | None = None) -> LLMResponse:
        client = self._get_client()
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            kwargs["system"] = system

        response = await client.messages.create(**kwargs)

        content = ""
        for block in response.content:
            if hasattr(block, "text"):
                content += block.text

        return LLMResponse(
            content=content,
            model=self.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )

    def estimate_tokens(self, text: str) -> int:
        return len(text) // 4


class OpenAIClient(LLMClient):
    """GPT models via the OpenAI API."""

    def __init__(self, model: str = "gpt-4o", max_tokens: int = 1024):
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

    async def complete(self, prompt: str, system: str | None = None) -> LLMResponse:
        client = self._get_client()
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = await client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=messages,
        )

        content = response.choices[0].message.content or ""
        usage = response.usage

        return LLMResponse(
            content=content,
            model=self.model,
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
        )

    def estimate_tokens(self, text: str) -> int:
        return len(text) // 4


class MockClient(LLMClient):
    """Mock LLM for testing the full pipeline without API calls.

    Cycles through predefined responses that exercise different action types.
    """

    def __init__(self, responses: list[str] | None = None):
        self.responses = responses or [
            "I need to understand the project first. Let me look at the main file.\n\nACTION: READ_FILE main.py",
            "The main.py has TODOs for /hello and /status endpoints. Let me implement them.\n\nACTION: WRITE_FILE main.py\n\n```python\nfrom http.server import HTTPServer, BaseHTTPRequestHandler\nimport json\n\n\nclass APIHandler(BaseHTTPRequestHandler):\n    def do_GET(self):\n        if self.path == '/hello':\n            self.send_response(200)\n            self.send_header('Content-Type', 'application/json')\n            self.end_headers()\n            self.wfile.write(json.dumps({'message': 'Hello, World!'}).encode())\n        elif self.path == '/status':\n            self.send_response(200)\n            self.send_header('Content-Type', 'application/json')\n            self.end_headers()\n            self.wfile.write(json.dumps({'status': 'ok'}).encode())\n        else:\n            self.send_response(404)\n            self.send_header('Content-Type', 'application/json')\n            self.end_headers()\n            self.wfile.write(json.dumps({'error': 'not found'}).encode())\n\n\nif __name__ == '__main__':\n    server = HTTPServer(('localhost', 8000), APIHandler)\n    print('Server running on http://localhost:8000')\n    server.serve_forever()\n```",
            "I've implemented both endpoints. Let me broadcast to the team what I did.\n\nACTION: BROADCAST Implemented /hello and /status endpoints in main.py. Both return JSON responses.",
            "The task seems complete. I'll wait and observe.\n\nACTION: IDLE",
        ]
        self._call_count = 0

    async def complete(self, prompt: str, system: str | None = None) -> LLMResponse:
        response = self.responses[self._call_count % len(self.responses)]
        self._call_count += 1
        return LLMResponse(
            content=response,
            model="mock",
            input_tokens=len(prompt) // 4,
            output_tokens=len(response) // 4,
        )

    def estimate_tokens(self, text: str) -> int:
        return len(text) // 4


def create_client(model: str, max_tokens: int = 1024) -> LLMClient:
    """Factory: create the right client based on model name."""
    model_lower = model.lower()

    if model_lower == "mock":
        return MockClient()

    if any(x in model_lower for x in ["claude", "anthropic", "sonnet", "opus", "haiku"]):
        return AnthropicClient(model=model, max_tokens=max_tokens)

    if any(x in model_lower for x in ["gpt", "o1", "o3", "openai"]):
        return OpenAIClient(model=model, max_tokens=max_tokens)

    # Default to OpenAI-compatible (works with most local model servers)
    log.warning("Unknown model '%s', defaulting to OpenAI-compatible client", model)
    return OpenAIClient(model=model, max_tokens=max_tokens)
