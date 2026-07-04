"""Dependency Injection container for AlphaHunter AI.

Manages service lifecycle and dependency resolution.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any, Callable

from app.core.exceptions import ConfigurationError
from app.providers.base import Provider
from app.providers.factory import ProviderFactory


class Container:
    """Simple dependency injection container.

    Manages singleton instances and factory functions.
    """

    def __init__(self) -> None:
        """Initialize the container."""
        self._singletons: dict[str, Any] = {}
        self._factories: dict[str, Callable[[], Any]] = {}
        self._configs: dict[str, Any] = {}

    def register_singleton(self, name: str, instance: Any) -> None:
        """Register a singleton instance.

        Args:
            name: Unique identifier for the instance.
            instance: Instance to register.
        """
        self._singletons[name] = instance

    def register_factory(self, name: str, factory: Callable[[], Any]) -> None:
        """Register a factory function.

        Args:
            name: Unique identifier for the factory.
            factory: Factory function to create instances.
        """
        self._factories[name] = factory

    def register_config(self, name: str, config: Any) -> None:
        """Register a configuration object.

        Args:
            name: Unique identifier for the config.
            config: Configuration object.
        """
        self._configs[name] = config

    def get(self, name: str) -> Any:
        """Retrieve an instance by name.

        Args:
            name: Identifier of the instance to retrieve.

        Returns:
            Registered instance or newly created instance from factory.

        Raises:
            ConfigurationError: If instance not found.
        """
        if name in self._singletons:
            return self._singletons[name]

        if name in self._factories:
            instance = self._factories[name]()
            self._singletons[name] = instance
            return instance

        if name in self._configs:
            return self._configs[name]

        raise ConfigurationError(f"No instance registered for: {name}")

    def register_provider(
        self,
        provider_type: str,
        provider_config_name: str | None = None,
    ) -> None:
        """Register a provider factory.

        Args:
            provider_type: Type of provider (yahoo, nse, screener, manual).
            provider_config_name: Optional config name for the provider.
        """
        def factory() -> Provider:
            config = None
            if provider_config_name and provider_config_name in self._configs:
                config = self._configs[provider_config_name]
            return ProviderFactory.create_provider(provider_type, config)

        self.register_factory(f"provider_{provider_type}", factory)

    def get_provider(self, provider_type: str) -> Provider:
        """Get a provider instance.

        Args:
            provider_type: Type of provider to retrieve.

        Returns:
            Provider instance.

        Raises:
            ConfigurationError: If provider not registered.
        """
        return self.get(f"provider_{provider_type}")


# Global container instance
_container: Container | None = None


@lru_cache
def get_container() -> Container:
    """Get the global container instance.

    Returns:
        Global Container instance.
    """
    global _container
    if _container is None:
        _container = Container()
    return _container


def reset_container() -> None:
    """Reset the global container (useful for testing)."""
    global _container
    _container = None
    get_container.cache_clear()
