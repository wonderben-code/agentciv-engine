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


def create_client(model: str, max_tokens: int = 1024) -> LLMClient:
    """Factory: create the right client based on model name."""
    model_lower = model.lower()

    if any(x in model_lower for x in ["claude", "anthropic", "sonnet", "opus", "haiku"]):
        return AnthropicClient(model=model, max_tokens=max_tokens)

    if any(x in model_lower for x in ["gpt", "o1", "o3", "openai"]):
        return OpenAIClient(model=model, max_tokens=max_tokens)

    # Default to OpenAI-compatible (works with most local model servers)
    log.warning("Unknown model '%s', defaulting to OpenAI-compatible client", model)
    return OpenAIClient(model=model, max_tokens=max_tokens)
