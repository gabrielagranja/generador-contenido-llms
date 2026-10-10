from __future__ import annotations

import socket
import sys
from types import ModuleType
import unittest
from unittest.mock import patch

from apps.api.config import (
    DEFAULT_LLM_MAX_OUTPUT_TOKENS,
    LlmSettings,
)
from apps.api.llm import (
    DeterministicMockAdapter,
    LangChainTextGenerator,
    TextGenerator,
    build_text_generator,
)


class LlmBoundaryTests(unittest.TestCase):
    def test_mock_is_deterministic_and_matches_neutral_contract(self) -> None:
        generator = DeterministicMockAdapter()

        self.assertIsInstance(generator, TextGenerator)
        self.assertEqual(generator.generate("  hello  "), "mock: hello")
        self.assertEqual(generator.generate("  hello  "), "mock: hello")

    def test_boundary_adapts_a_langchain_runnable(self) -> None:
        from langchain_core.runnables import RunnableLambda

        generator = LangChainTextGenerator(
            RunnableLambda(lambda prompt: f"adapted: {prompt}")
        )

        self.assertEqual(generator.generate("brief"), "adapted: brief")

    def test_mock_does_not_use_the_network(self) -> None:
        generator = DeterministicMockAdapter()

        with patch.object(socket, "socket", side_effect=AssertionError("network access")):
            self.assertEqual(generator.generate("offline"), "mock: offline")

    def test_empty_prompts_are_rejected_before_invocation(self) -> None:
        generator = DeterministicMockAdapter()

        with self.assertRaises(ValueError):
            generator.generate("  ")

    def test_default_output_budget_is_applied(self) -> None:
        settings = LlmSettings()

        self.assertEqual(settings.max_output_tokens, DEFAULT_LLM_MAX_OUTPUT_TOKENS)
        settings.validate()

    def test_configured_output_budget_is_accepted(self) -> None:
        settings = LlmSettings(max_output_tokens=600)

        settings.validate()
        self.assertEqual(settings.max_output_tokens, 600)

    def test_invalid_output_budget_is_rejected(self) -> None:
        for value in (0, -1, 601):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    LlmSettings(max_output_tokens=value).validate()

    def test_non_numeric_environment_budget_is_rejected(self) -> None:
        with patch.dict(
            "os.environ", {"LLM_MAX_OUTPUT_TOKENS": "not-an-integer"}, clear=False
        ):
            with self.assertRaisesRegex(ValueError, "LLM_MAX_OUTPUT_TOKENS"):
                LlmSettings.from_environment()

    def test_groq_adapter_receives_output_budget_without_network_call(self) -> None:
        from langchain_core.runnables import RunnableLambda

        fake_module = ModuleType("langchain_groq")

        class FakeChatGroq:
            calls: list[dict[str, object]] = []

            def __new__(cls, **kwargs: object) -> RunnableLambda:
                cls.calls.append(kwargs)
                return RunnableLambda(lambda prompt: f"fake: {prompt}")

        fake_module.ChatGroq = FakeChatGroq  # type: ignore[attr-defined]
        settings = LlmSettings(
            provider="groq",
            groq_api_key="test-key",
            max_output_tokens=275,
        )

        with patch.dict(sys.modules, {"langchain_groq": fake_module}):
            generator = build_text_generator(settings)

        self.assertIsInstance(generator, LangChainTextGenerator)
        self.assertEqual(FakeChatGroq.calls[0]["max_tokens"], 275)
        self.assertEqual(FakeChatGroq.calls[0]["temperature"], 0.2)


if __name__ == "__main__":
    unittest.main()

class OllamaAdapterTests(unittest.TestCase):
    def _settings(self) -> LlmSettings:
        return LlmSettings(
            provider="ollama",
            ollama_model="llama3.2:3b",
            ollama_base_url="http://127.0.0.1:11434",
            temperature=0.4,
            timeout_seconds=12,
            max_output_tokens=275,
        )

    def test_ollama_sends_bounded_nonstreaming_request(self) -> None:
        class FakeResponse:
            def raise_for_status(self) -> None:
                return None

            def json(self) -> dict[str, object]:
                return {"message": {"content": "respuesta local"}}

        with patch("apps.api.llm.httpx.post", return_value=FakeResponse()) as post:
            generator = build_text_generator(self._settings())
            self.assertEqual(generator.generate("brief"), "respuesta local")

        self.assertEqual(post.call_args.args[0], "http://127.0.0.1:11434/api/chat")
        self.assertEqual(post.call_args.kwargs["timeout"], 12)
        payload = post.call_args.kwargs["json"]
        self.assertFalse(payload["stream"])
        self.assertEqual(payload["options"], {"temperature": 0.4, "num_predict": 275})

    def test_ollama_failure_is_controlled(self) -> None:
        import httpx

        with patch("apps.api.llm.httpx.post", side_effect=httpx.ConnectError("offline")):
            generator = build_text_generator(self._settings())
            with self.assertRaisesRegex(Exception, "Ollama is unavailable"):
                generator.generate("brief")

    def test_ollama_requires_an_explicit_model(self) -> None:
        with self.assertRaisesRegex(ValueError, "OLLAMA_MODEL"):
            LlmSettings(provider="ollama").validate()
