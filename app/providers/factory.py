"""Factory for creating provider instances using the Factory Pattern."""

from __future__ import annotations

from typing import Type

from app.core.exceptions import ProviderError
from app.providers.base import Provider, ProviderConfig
from app.providers.manual import ManualCSVProvider, ManualCSVProviderConfig
from app.providers.nse import NSEProvider, NSEProviderConfig
from app.providers.screener import ScreenerProvider, ScreenerProviderConfig
from app.providers.yahoo import YahooFinanceProvider, YahooFinanceProviderConfig


class ProviderFactory:
    """Factory for creating provider instances.

    Uses the Factory Pattern to instantiate providers based on configuration.
    """

    _providers: dict[str, tuple[Type[Provider], Type[ProviderConfig]]] = {
        "yahoo": (YahooFinanceProvider, YahooFinanceProviderConfig),
        "nse": (NSEProvider, NSEProviderConfig),
        "screener": (ScreenerProvider, ScreenerProviderConfig),
        "manual": (ManualCSVProvider, ManualCSVProviderConfig),
    }

    @classmethod
    def create_provider(cls, provider_type: str, config: ProviderConfig | None = None) -> Provider:
        """Create a provider instance.

        Args:
            provider_type: Type of provider to create (yahoo, nse, screener, manual).
            config: Optional provider-specific configuration.

        Returns:
            Provider instance.

        Raises:
            ProviderError: If provider type is not supported.
        """
        provider_type_lower = provider_type.lower()

        if provider_type_lower not in cls._providers:
            supported = ", ".join(cls._providers.keys())
            raise ProviderError(
                f"Unknown provider type: {provider_type}. "
                f"Supported providers: {supported}"
            )

        provider_class, config_class = cls._providers[provider_type_lower]

        if config is None:
            config = config_class()
        elif not isinstance(config, config_class):
            raise ProviderError(
                f"Invalid config type for {provider_type}. "
                f"Expected {config_class.__name__}, got {type(config).__name__}"
            )

        return provider_class(config)

    @classmethod
    def register_provider(
        cls,
        provider_type: str,
        provider_class: Type[Provider],
        config_class: Type[ProviderConfig],
    ) -> None:
        """Register a new provider type.

        Args:
            provider_type: Unique identifier for the provider.
            provider_class: Provider class to register.
            config_class: Configuration class for the provider.
        """
        cls._providers[provider_type.lower()] = (provider_class, config_class)

    @classmethod
    def list_providers(cls) -> list[str]:
        """Return list of registered provider types.

        Returns:
            List of provider type identifiers.
        """
        return list(cls._providers.keys())
