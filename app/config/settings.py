"""Application configuration manager using Pydantic Settings.

Loads configuration from environment variables and .env files with type validation.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="AlphaHunterAI", description="Application name")
    app_env: Literal["development", "staging", "production"] = Field(
        default="development", description="Application environment"
    )
    app_debug: bool = Field(default=False, description="Debug mode flag")
    app_version: str = Field(default="0.1.0", description="Application version")

    database_url: str = Field(
        default="duckdb:///data/alphahunter.db", description="Database connection string"
    )
    database_echo: bool = Field(default=False, description="Echo SQL statements")

    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_reload: bool = Field(default=False, description="Enable auto-reload")

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )
    log_format: Literal["text", "json"] = Field(default="text", description="Logging format")
    log_file: str = Field(default="logs/alphahunter.log", description="Log file path")

    cache_ttl: int = Field(default=3600, description="Cache TTL in seconds")
    cache_max_size: int = Field(default=1000, description="Maximum cache size")

    secret_key: str = Field(default="change-me-in-production", description="Secret key")

    @validator("log_file", "database_url", pre=True)
    @classmethod
    def _ensure_absolute_paths(cls, value: str) -> str:
        """Convert relative paths to absolute paths based on project root."""
        if value.startswith("duckdb:///"):
            db_path = value.replace("duckdb:///", "")
            if not Path(db_path).is_absolute():
                return f"duckdb:///{Path.cwd() / db_path}"
            return value
        if not Path(value).is_absolute() and not value.startswith("http"):
            return str(Path.cwd() / value)
        return value

    @property
    def project_root(self) -> Path:
        """Return the project root directory."""
        return Path(__file__).parent.parent.parent

    @property
    def is_development(self) -> bool:
        """Return True if the application is running in development mode."""
        return self.app_env == "development"

    @property
    def is_production(self) -> bool:
        """Return True if the application is running in production mode."""
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    """Return a cached instance of application settings.

    Returns:
        Settings instance loaded from environment.
    """
    return Settings()
