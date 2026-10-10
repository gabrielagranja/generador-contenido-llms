"""Environment-backed configuration for the local application foundation."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv

load_dotenv()


DEFAULT_APP_ENV = "development"
DEFAULT_API_HOST = "127.0.0.1"
DEFAULT_API_PORT = 8000
DEFAULT_API_BASE_URL = "http://127.0.0.1:8000"
DEFAULT_RAG_EMBEDDING_MODEL = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
DEFAULT_RAG_EMBEDDING_REVISION = "main"
DEFAULT_RAG_CHROMA_COLLECTION = "business-context"
DEFAULT_RAG_CHROMA_PERSIST_DIRECTORY = Path(".local") / "chroma"
DEFAULT_RAG_API_BASE_URL = "https://jsonplaceholder.typicode.com"
DEFAULT_LLM_PROVIDER = "mock"
DEFAULT_GROQ_MODEL = "openai/gpt-oss-20b"
DEFAULT_LLM_TEMPERATURE = 0.2
DEFAULT_LLM_TIMEOUT_SECONDS = 30.0


@dataclass(frozen=True)
class RagLocalSettings:
    """Explicit, provider-free configuration for the local RAG boundary."""

    embedding_model: str = DEFAULT_RAG_EMBEDDING_MODEL
    embedding_revision: str = DEFAULT_RAG_EMBEDDING_REVISION
    chroma_collection: str = DEFAULT_RAG_CHROMA_COLLECTION
    chroma_persist_directory: Path = DEFAULT_RAG_CHROMA_PERSIST_DIRECTORY
    api_base_url: str = DEFAULT_RAG_API_BASE_URL

    @classmethod
    def from_environment(cls) -> "RagLocalSettings":
        settings = cls(
            embedding_model=os.getenv(
                "RAG_EMBEDDING_MODEL", DEFAULT_RAG_EMBEDDING_MODEL
            ),
            embedding_revision=os.getenv(
                "RAG_EMBEDDING_REVISION", DEFAULT_RAG_EMBEDDING_REVISION
            ),
            chroma_collection=os.getenv(
                "RAG_CHROMA_COLLECTION", DEFAULT_RAG_CHROMA_COLLECTION
            ),
            chroma_persist_directory=Path(
                os.getenv(
                    "RAG_CHROMA_PERSIST_DIRECTORY",
                    str(DEFAULT_RAG_CHROMA_PERSIST_DIRECTORY),
                )
            ),
            api_base_url=os.getenv("RAG_API_BASE_URL", DEFAULT_RAG_API_BASE_URL),
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        if not self.embedding_model.strip():
            raise ValueError("RAG_EMBEDDING_MODEL must not be empty")
        if not self.embedding_revision.strip():
            raise ValueError("RAG_EMBEDDING_REVISION must not be empty")
        if not self.chroma_collection.strip():
            raise ValueError("RAG_CHROMA_COLLECTION must not be empty")
        if self.chroma_persist_directory == Path("."):
            raise ValueError("RAG_CHROMA_PERSIST_DIRECTORY must not be the current directory")
        parsed_url = urlsplit(self.api_base_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.hostname:
            raise ValueError("RAG_API_BASE_URL must be an HTTP(S) URL")
        if parsed_url.username or parsed_url.password:
            raise ValueError("RAG_API_BASE_URL must not contain credentials")


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


@dataclass(frozen=True)
class LlmSettings:
    """Provider configuration kept on the API side of the application."""

    provider: str = DEFAULT_LLM_PROVIDER
    groq_api_key: str | None = None
    groq_model: str = DEFAULT_GROQ_MODEL
    temperature: float = DEFAULT_LLM_TEMPERATURE
    timeout_seconds: float = DEFAULT_LLM_TIMEOUT_SECONDS

    @classmethod
    def from_environment(cls) -> "LlmSettings":
        # A local key opts into Groq for the developer workflow; CI remains on
        # the deterministic mock unless LLM_PROVIDER is explicitly configured.
        provider = os.getenv("LLM_PROVIDER") or (
            "groq" if os.getenv("GROQ_API_KEY") else DEFAULT_LLM_PROVIDER
        )
        settings = cls(
            provider=provider.strip().lower(),
            groq_api_key=os.getenv("GROQ_API_KEY") or None,
            groq_model=os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL).strip(),
            temperature=_read_float("LLM_TEMPERATURE", DEFAULT_LLM_TEMPERATURE),
            timeout_seconds=_read_float(
                "LLM_TIMEOUT_SECONDS", DEFAULT_LLM_TIMEOUT_SECONDS
            ),
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        if self.provider not in {"mock", "groq"}:
            raise ValueError("LLM_PROVIDER must be 'mock' or 'groq'")
        if not self.groq_model.strip():
            raise ValueError("GROQ_MODEL must not be empty")
        if not 0 <= self.temperature <= 2:
            raise ValueError("LLM_TEMPERATURE must be between 0 and 2")
        if self.timeout_seconds <= 0:
            raise ValueError("LLM_TIMEOUT_SECONDS must be positive")


def _read_port() -> int:
    raw_port = os.getenv("API_PORT", str(DEFAULT_API_PORT))
    try:
        return int(raw_port)
    except ValueError as error:
        raise ValueError("API_PORT must be an integer") from error


def _read_float(name: str, default: float) -> float:
    raw_value = os.getenv(name, str(default))
    try:
        return float(raw_value)
    except ValueError as error:
        raise ValueError(f"{name} must be a number") from error


settings = EnvironmentSettings.from_environment()


__all__ = ["EnvironmentSettings", "LlmSettings", "RagLocalSettings", "settings"]
