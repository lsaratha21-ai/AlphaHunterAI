"""Unit tests for the core exceptions."""

from __future__ import annotations

import pytest

from app.core import AlphaHunterError, ConfigurationError, DatabaseError, ProviderError, ValidationError


class TestAlphaHunterError:
    """Tests for the base AlphaHunterError exception."""

    def test_alpha_hunter_error_with_message(self) -> None:
        """Ensure AlphaHunterError stores message correctly."""
        error = AlphaHunterError("Test error message")
        assert error.message == "Test error message"
        assert str(error) == "Test error message"

    def test_alpha_hunter_error_with_details(self) -> None:
        """Ensure AlphaHunterError stores details correctly."""
        details = {"key": "value"}
        error = AlphaHunterError("Test error", details=details)
        assert error.details == details


class TestConfigurationError:
    """Tests for ConfigurationError."""

    def test_configuration_error_inherits_from_base(self) -> None:
        """Ensure ConfigurationError inherits from AlphaHunterError."""
        error = ConfigurationError("Config error")
        assert isinstance(error, AlphaHunterError)


class TestDatabaseError:
    """Tests for DatabaseError."""

    def test_database_error_inherits_from_base(self) -> None:
        """Ensure DatabaseError inherits from AlphaHunterError."""
        error = DatabaseError("DB error")
        assert isinstance(error, AlphaHunterError)


class TestProviderError:
    """Tests for ProviderError."""

    def test_provider_error_inherits_from_base(self) -> None:
        """Ensure ProviderError inherits from AlphaHunterError."""
        error = ProviderError("Provider error")
        assert isinstance(error, AlphaHunterError)


class TestValidationError:
    """Tests for ValidationError."""

    def test_validation_error_inherits_from_base(self) -> None:
        """Ensure ValidationError inherits from AlphaHunterError."""
        error = ValidationError("Validation error")
        assert isinstance(error, AlphaHunterError)
