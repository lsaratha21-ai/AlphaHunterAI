"""Unit tests for Dependency Injection container."""

from __future__ import annotations

import pytest

from app.core import ConfigurationError, Container, get_container, reset_container
from app.providers import YahooFinanceProviderConfig


class TestContainer:
    """Tests for Container class."""

    def test_register_and_get_singleton(self) -> None:
        """Test registering and retrieving singleton instances."""
        container = Container()
        instance = {"key": "value"}
        container.register_singleton("test", instance)
        retrieved = container.get("test")
        assert retrieved is instance

    def test_register_factory(self) -> None:
        """Test registering and using factory functions."""
        container = Container()
        call_count = 0

        def factory() -> dict:
            nonlocal call_count
            call_count += 1
            return {"count": call_count}

        container.register_factory("test", factory)
        instance1 = container.get("test")
        instance2 = container.get("test")
        assert instance1["count"] == 1
        assert instance2["count"] == 1
        assert instance1 is instance2

    def test_register_config(self) -> None:
        """Test registering and retrieving configuration."""
        container = Container()
        config = {"setting": "value"}
        container.register_config("test_config", config)
        retrieved = container.get("test_config")
        assert retrieved == config

    def test_get_not_found(self) -> None:
        """Test retrieving unregistered instance."""
        container = Container()
        with pytest.raises(ConfigurationError, match="No instance registered"):
            container.get("nonexistent")

    def test_register_provider(self) -> None:
        """Test registering a provider via container."""
        container = Container()
        config = YahooFinanceProviderConfig(timeout=60)
        container.register_config("yahoo_config", config)
        container.register_provider("yahoo", "yahoo_config")
        provider = container.get_provider("yahoo")
        assert provider.config.timeout == 60

    def test_get_provider_not_registered(self) -> None:
        """Test getting unregistered provider."""
        container = Container()
        with pytest.raises(ConfigurationError, match="No instance registered"):
            container.get_provider("yahoo")


class TestGlobalContainer:
    """Tests for global container functions."""

    def test_get_container_returns_singleton(self) -> None:
        """Test that get_container returns the same instance."""
        reset_container()
        container1 = get_container()
        container2 = get_container()
        assert container1 is container2

    def test_reset_container(self) -> None:
        """Test resetting the global container."""
        reset_container()
        container1 = get_container()
        reset_container()
        container2 = get_container()
        assert container1 is not container2

    def test_container_persistence(self) -> None:
        """Test that container persists across calls."""
        reset_container()
        container = get_container()
        container.register_singleton("test", {"value": 42})
        retrieved = get_container().get("test")
        assert retrieved["value"] == 42
