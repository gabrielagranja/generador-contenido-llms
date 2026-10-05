"""Environment-backed configuration for the local application foundation."""

from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urlsplit


DEFAULT_APP_ENV = "development"
DEFAULT_API_HOST = "127.0.0.1"
DEFAULT_API_PORT = 8000
DEFAULT_API_BASE_URL = "http://127.0.0.1:8000"


@dataclass(frozen=True)
class EnvironmentSettings:
    """Small, non-secret configuration surface used by the foundation."""

    app_env: str = DEFAULT_APP_ENV
    api_host: str = DEFAULT_API_HOST
    api_port: int = DEFAULT_API_PORT
    next_public_api_base_url: str = DEFAULT_API_BASE_URL

    @classmethod
    def from_environment(cls) -> "EnvironmentSettings":
        """Read foundation settings without requiring provider credentials."""

        settings = cls(
            app_env=os.getenv("APP_ENV", DEFAULT_APP_ENV),
            api_host=os.getenv("API_HOST", DEFAULT_API_HOST),
            api_port=_read_port(),
            next_public_api_base_url=os.getenv(
                "NEXT_PUBLIC_API_BASE_URL", DEFAULT_API_BASE_URL
            ),
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        """Reject unsafe or unusable local foundation values."""

        if not self.app_env.strip():
            raise ValueError("APP_ENV must not be empty")
        if not self.api_host.strip():
            raise ValueError("API_HOST must not be empty")
        if not 1 <= self.api_port <= 65535:
            raise ValueError("API_PORT must be between 1 and 65535")

        parsed_url = urlsplit(self.next_public_api_base_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.hostname:
            raise ValueError("NEXT_PUBLIC_API_BASE_URL must be an HTTP(S) URL")
        if parsed_url.username or parsed_url.password:
            raise ValueError("NEXT_PUBLIC_API_BASE_URL must not contain credentials")


def _read_port() -> int:
    raw_port = os.getenv("API_PORT", str(DEFAULT_API_PORT))
    try:
        return int(raw_port)
    except ValueError as error:
        raise ValueError("API_PORT must be an integer") from error


settings = EnvironmentSettings.from_environment()


__all__ = ["EnvironmentSettings", "settings"]
