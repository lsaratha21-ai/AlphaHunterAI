"""Unit tests for the configuration manager."""

from __future__ import annotations

import pytest

from app.config import Settings, get_settings


class TestSettings:
    """Tests for the Settings class."""

    def test_default_settings(self) -> None:
        """Ensure default settings load correctly."""
        settings = Settings()

        assert settings.app_name == "AlphaHunterAI"
        assert settings.app_env == "development"
        assert settings.app_version == "0.1.0"
        assert settings.log_level == "INFO"
        assert settings.api_port == 8000

    def test_is_development(self) -> None:
        """Test environment detection for development."""
        settings = Settings(app_env="development")
        assert settings.is_development is True
        assert settings.is_production is False

    def test_is_production(self) -> None:
        """Test environment detection for production."""
        settings = Settings(app_env="production")
        assert settings.is_production is True
        assert settings.is_development is False


class TestGetSettings:
    """Tests for the cached settings factory."""

    def test_get_settings_returns_instance(self) -> None:
        """Ensure get_settings returns a Settings instance."""
        settings = get_settings()
        assert isinstance(settings, Settings)

    def test_get_settings_cached(self) -> None:
        """Ensure get_settings returns the same cached instance."""
        first = get_settings()
        second = get_settings()
        assert first is second
