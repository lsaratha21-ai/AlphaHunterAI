"""Abstract base class for data providers.

Defines the contract that all data providers must implement.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Any

from pydantic import BaseModel


@dataclass
class StockData:
    """Standardized stock data model."""

    symbol: str
    name: str
    price: float
    market_cap: float | None = None
    pe_ratio: float | None = None
    debt_to_equity: float | None = None
    revenue_growth: float | None = None
    earnings_growth: float | None = None
    promoter_holdings: float | None = None
    sector: str | None = None
    last_updated: date | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "name": self.name,
            "price": self.price,
            "market_cap": self.market_cap,
            "pe_ratio": self.pe_ratio,
            "debt_to_equity": self.debt_to_equity,
            "revenue_growth": self.revenue_growth,
            "earnings_growth": self.earnings_growth,
            "promoter_holdings": self.promoter_holdings,
            "sector": self.sector,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
        }


class ProviderConfig(BaseModel):
    """Base configuration for providers."""

    timeout: int = 30
    retry_attempts: int = 3
    api_key: str | None = None


class Provider(ABC):
    """Abstract base class for all data providers.

    Concrete providers must implement the fetch_stock_data method.
    """

    def __init__(self, config: ProviderConfig | None = None) -> None:
        """Initialize the provider with configuration.

        Args:
            config: Provider-specific configuration.
        """
        self.config = config or ProviderConfig()

    @abstractmethod
    async def fetch_stock_data(self, symbol: str) -> StockData:
        """Fetch stock data for a given symbol.

        Args:
            symbol: Stock ticker symbol.

        Returns:
            StockData object with fetched information.

        Raises:
            ProviderError: If data fetch fails.
        """
        raise NotImplementedError

    @abstractmethod
    async def fetch_multiple_stocks(self, symbols: list[str]) -> list[StockData]:
        """Fetch data for multiple stocks.

        Args:
            symbols: List of stock ticker symbols.

        Returns:
            List of StockData objects.

        Raises:
            ProviderError: If data fetch fails.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name."""
        raise NotImplementedError
