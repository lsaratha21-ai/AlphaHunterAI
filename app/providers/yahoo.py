"""Yahoo Finance data provider implementation."""

from __future__ import annotations

import aiohttp
from datetime import date

from app.core.exceptions import ProviderError
from app.providers.base import Provider, ProviderConfig, StockData


class YahooFinanceProviderConfig(ProviderConfig):
    """Configuration for Yahoo Finance provider."""

    pass


class YahooFinanceProvider(Provider):
    """Yahoo Finance data provider.

    Fetches stock data from Yahoo Finance API.
    """

    def __init__(self, config: YahooFinanceProviderConfig | None = None) -> None:
        """Initialize the Yahoo Finance provider.

        Args:
            config: Provider configuration.
        """
        super().__init__(config or YahooFinanceProviderConfig())

    async def fetch_stock_data(self, symbol: str) -> StockData:
        """Fetch stock data from Yahoo Finance.

        Args:
            symbol: Stock ticker symbol.

        Returns:
            StockData object with fetched information.

        Raises:
            ProviderError: If data fetch fails.
        """
        try:
            # Yahoo Finance API endpoint
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}.NS"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as response:
                    if response.status != 200:
                        raise ProviderError(f"Failed to fetch data for {symbol}: HTTP {response.status}")
                    
                    data = await response.json()
                    
                    result = data.get("chart", {}).get("result", [])
                    if not result:
                        raise ProviderError(f"No data found for {symbol}")
                    
                    meta = result[0].get("meta", {})
                    regular_market_price = meta.get("regularMarketPrice", 0)
                    
                    return StockData(
                        symbol=symbol.upper(),
                        name=meta.get("longName", f"{symbol.upper()}"),
                        price=float(regular_market_price or 0),
                        market_cap=float(meta.get("marketCap", 0)),
                        pe_ratio=float(meta.get("trailingPE", 0)),
                        debt_to_equity=0.0,  # Not available in basic Yahoo Finance API
                        revenue_growth=0.0,  # Not available in basic Yahoo Finance API
                        earnings_growth=0.0,  # Not available in basic Yahoo Finance API
                        promoter_holdings=0.0,  # Not available in Yahoo Finance
                        sector=meta.get("sector", "Unknown"),
                        last_updated=date.today(),
                    )
        except aiohttp.ClientError as e:
            raise ProviderError(f"Network error fetching data for {symbol}: {e}")
        except (KeyError, ValueError, TypeError) as e:
            raise ProviderError(f"Error parsing data for {symbol}: {e}")

    async def fetch_multiple_stocks(self, symbols: list[str]) -> list[StockData]:
        """Fetch data for multiple stocks from Yahoo Finance.

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
        return "Yahoo Finance"
