"""Screener.in data provider implementation."""

from __future__ import annotations

import aiohttp
from datetime import date

from app.core.exceptions import ProviderError
from app.providers.base import Provider, ProviderConfig, StockData


class ScreenerProviderConfig(ProviderConfig):
    """Configuration for Screener.in provider."""

    base_url: str = "https://www.screener.in"


class ScreenerProvider(Provider):
    """Screener.in data provider.

    Fetches stock data from Screener.in API.
    """

    def __init__(self, config: ScreenerProviderConfig | None = None) -> None:
        """Initialize the Screener.in provider.

        Args:
            config: Provider configuration.
        """
        super().__init__(config or ScreenerProviderConfig())

    async def fetch_stock_data(self, symbol: str) -> StockData:
        """Fetch stock data from Screener.in.

        Args:
            symbol: Stock ticker symbol.

        Returns:
            StockData object with fetched information.

        Raises:
            ProviderError: If data fetch fails.
        """
        try:
            url = f"{self.config.base_url}/api/company/{symbol}/"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as response:
                    if response.status != 200:
                        raise ProviderError(f"Failed to fetch data for {symbol}: HTTP {response.status}")
                    
                    data = await response.json()
                    
                    return StockData(
                        symbol=symbol.upper(),
                        name=data.get("name", f"{symbol.upper()}"),
                        price=float(data.get("price", {}).get("current", 0)),
                        market_cap=float(data.get("market_cap", {}).get("value", 0)),
                        pe_ratio=float(data.get("pe_ratio", {}).get("value", 0)),
                        debt_to_equity=float(data.get("debt_to_equity", {}).get("value", 0)),
                        revenue_growth=float(data.get("revenue_growth", {}).get("value", 0)),
                        earnings_growth=float(data.get("earnings_growth", {}).get("value", 0)),
                        promoter_holdings=float(data.get("promoter_holdings", {}).get("value", 0)),
                        sector=data.get("sector", "Unknown"),
                        last_updated=date.today(),
                    )
        except aiohttp.ClientError as e:
            raise ProviderError(f"Network error fetching data for {symbol}: {e}")
        except (KeyError, ValueError, TypeError) as e:
            raise ProviderError(f"Error parsing data for {symbol}: {e}")

    async def fetch_multiple_stocks(self, symbols: list[str]) -> list[StockData]:
        """Fetch data for multiple stocks from Screener.in.

        Args:
            symbols: List of stock ticker symbols.

        Returns:
            List of StockData objects.

        Raises:
            ProviderError: If data fetch fails.
        """
        results = []
        for symbol in symbols:
            try:
                data = await self.fetch_stock_data(symbol)
                results.append(data)
            except ProviderError:
                continue
        return results

    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "Screener.in"
