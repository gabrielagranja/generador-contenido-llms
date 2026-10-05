from __future__ import annotations

import socket
import unittest
from unittest.mock import patch

from apps.api.llm import DeterministicMockAdapter, LangChainTextGenerator, TextGenerator


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


if __name__ == "__main__":
    unittest.main()
