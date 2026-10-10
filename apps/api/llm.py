"""Provider-neutral text generation boundary.

Only LangChain core primitives are used here. Provider-specific chat models can
be connected later by passing their LangChain runnable to ``LangChainTextGenerator``.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from langchain_core.runnables import Runnable, RunnableLambda

from apps.api.config import LlmSettings


@runtime_checkable
class TextGenerator(Protocol):
    """Stable application-facing contract for text generation."""

    def generate(self, prompt: str) -> str:
        """Generate text for a prompt without exposing provider details."""


class LangChainTextGenerator:
    """Adapt a LangChain runnable to the provider-neutral application contract."""

    def __init__(self, runnable: Runnable[str, Any]) -> None:
        self._runnable = runnable

    def generate(self, prompt: str) -> str:
        if not prompt.strip():
            raise ValueError("prompt must not be empty")

        response = self._runnable.invoke(prompt)
        content = getattr(response, "content", response)
        if not isinstance(content, str):
            raise TypeError("LangChain runnable must return text content")
        return content


class DeterministicMockAdapter(LangChainTextGenerator):
    """Offline LangChain adapter with stable output for foundation tests."""

    def __init__(self, prefix: str = "mock") -> None:
        if not prefix.strip():
            raise ValueError("prefix must not be empty")

        super().__init__(
            RunnableLambda(
                lambda prompt: f"{prefix}: {prompt.strip()}"
            )
        )


class LlmConfigurationError(RuntimeError):
    """Raised when a configured provider cannot be built safely."""


def build_text_generator(settings: LlmSettings | None = None) -> TextGenerator:
    """Build the configured generator while keeping provider details behind one boundary."""

    resolved = settings or LlmSettings.from_environment()
    if resolved.provider == "mock":
        return DeterministicMockAdapter()

    if resolved.provider != "groq":
        raise LlmConfigurationError(f"Unsupported LLM provider: {resolved.provider}")
    if not resolved.groq_api_key:
        raise LlmConfigurationError(
            "GROQ_API_KEY is required when LLM_PROVIDER=groq"
        )

    try:
        from langchain_groq import ChatGroq
    except ImportError as error:  # pragma: no cover - exercised in setup failures
        raise LlmConfigurationError(
            "langchain-groq is required for the Groq provider"
        ) from error

    runnable = ChatGroq(
        model=resolved.groq_model,
        temperature=resolved.temperature,
        timeout=resolved.timeout_seconds,
        max_tokens=resolved.max_output_tokens,
        api_key=resolved.groq_api_key,
    )
    return LangChainTextGenerator(runnable)


__all__ = [
    "DeterministicMockAdapter",
    "LangChainTextGenerator",
    "LlmConfigurationError",
    "TextGenerator",
    "build_text_generator",
]
