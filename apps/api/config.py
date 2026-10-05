"""Environment-backed settings for the local API foundation."""

from os import environ

from pydantic import BaseModel, Field


DEFAULT_CORS_ORIGINS = (
    "http://localhost:3000",
    "http://127.0.0.1:3000",
)


class Settings(BaseModel):
    """Non-secret runtime settings required by the foundation API."""

    cors_origins: tuple[str, ...] = Field(default=DEFAULT_CORS_ORIGINS)

    @classmethod
    def from_environment(cls) -> "Settings":
        """Read supported environment variables with safe local defaults."""

        raw_origins = environ.get("API_CORS_ORIGINS")
        if raw_origins is None:
            return cls()

        origins = tuple(
            origin.strip() for origin in raw_origins.split(",") if origin.strip()
        )
        return cls(cors_origins=origins or DEFAULT_CORS_ORIGINS)
