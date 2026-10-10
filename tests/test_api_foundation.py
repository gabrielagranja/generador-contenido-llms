from __future__ import annotations

import os
import socket
import asyncio
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

from apps.api.main import ReadinessResponse, app


ROOT = Path(__file__).resolve().parents[1]
CLIENT_WORKSPACE = ROOT / "apps" / "web" / "components" / "Workspace.tsx"
CLIENT_SHELL = ROOT / "apps" / "web" / "components" / "shell" / "AppShell.tsx"
PROVIDER_ENVIRONMENT_KEYS = (
    "GROQ_API_KEY",
    "GOOGLE_API_KEY",
    "GEMINI_API_KEY",
    "META_ACCESS_TOKEN",
)


class ApiFoundationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_readiness_response_has_safe_deterministic_defaults(self) -> None:
        response = ReadinessResponse()

        self.assertEqual(response.model_dump(), {"status": "ready", "service": "api"})

    def test_readiness_endpoint_returns_expected_contract(self) -> None:
        response = self.client.get("/readiness")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ready", "service": "api"})

    def test_openapi_documentation_endpoints_are_available(self) -> None:
        for path in ("/docs", "/redoc", "/openapi.json"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)

        openapi = self.client.get("/openapi.json").json()
        self.assertIn("/readiness", openapi["paths"])

    def test_readiness_is_available_without_provider_credentials(self) -> None:
        with patch.dict(os.environ, {}, clear=False):
            for key in PROVIDER_ENVIRONMENT_KEYS:
                os.environ.pop(key, None)
            response = self.client.get("/readiness")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ready")

    def test_client_only_contains_the_public_api_base_configuration(self) -> None:
        client = CLIENT_WORKSPACE.read_text(encoding="utf-8") + CLIENT_SHELL.read_text(encoding="utf-8")

        self.assertIn("NEXT_PUBLIC_API_BASE_URL", client)
        self.assertNotIn("API local:", client)
        self.assertNotIn("API no disponible", client)
        self.assertNotRegex(client, r"(?i)(GROQ_API_KEY|gsk_[a-z0-9])")

    def test_foundation_readiness_does_not_open_network_connections(self) -> None:
        async def request_readiness() -> httpx.Response:
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(
                transport=transport,
                base_url="http://testserver",
            ) as client:
                return await client.get("/readiness")

        loop = asyncio.new_event_loop()
        try:
            with patch.object(
                socket,
                "create_connection",
                side_effect=AssertionError("network access"),
            ):
                response = loop.run_until_complete(request_readiness())
        finally:
            loop.close()

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
