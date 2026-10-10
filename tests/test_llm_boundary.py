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
