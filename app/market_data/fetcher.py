"""Real market data fetcher using implemented providers."""

from __future__ import annotations

import asyncio
from typing import Any

from app.providers.factory import ProviderFactory
from app.providers.screener import ScreenerProvider
from app.providers.yahoo import YahooFinanceProvider


class MarketDataFetcher:
    """Fetcher for real market data using multiple providers."""

    def __init__(self) -> None:
        """Initialize the MarketDataFetcher."""
        self.screener_provider = ProviderFactory.create_provider("screener")
        self.yahoo_provider = ProviderFactory.create_provider("yahoo")

    async def fetch_stock_data(self, symbol: str, provider: str = "screener") -> dict[str, Any]:
        """Fetch stock data from specified provider.

        Args:
            symbol: Stock ticker symbol.
            provider: Provider to use (screener, yahoo).

        Returns:
            Dictionary with stock data.
        """
        if provider == "screener":
            stock_data = await self.screener_provider.fetch_stock_data(symbol)
        elif provider == "yahoo":
            stock_data = await self.yahoo_provider.fetch_stock_data(symbol)
        else:
            raise ValueError(f"Unknown provider: {provider}")

        return {
            "symbol": stock_data.symbol,
            "name": stock_data.name,
            "price": stock_data.price,
            "market_cap": stock_data.market_cap,
            "pe_ratio": stock_data.pe_ratio,
            "debt_to_equity": stock_data.debt_to_equity,
            "revenue_growth": stock_data.revenue_growth,
            "earnings_growth": stock_data.earnings_growth,
            "promoter_holdings": stock_data.promoter_holdings,
            "sector": stock_data.sector,
            "last_updated": stock_data.last_updated,
            "provider": provider,
        }

    async def fetch_multiple_stocks(
        self,
        symbols: list[str],
        provider: str = "screener",
    ) -> list[dict[str, Any]]:
        """Fetch data for multiple stocks.

        Args:
            symbols: List of stock ticker symbols.
            provider: Provider to use (screener, yahoo).

        Returns:
            List of dictionaries with stock data.
        """
        if provider == "screener":
            stocks_data = await self.screener_provider.fetch_multiple_stocks(symbols)
        elif provider == "yahoo":
            stocks_data = await self.yahoo_provider.fetch_multiple_stocks(symbols)
        else:
            raise ValueError(f"Unknown provider: {provider}")

        return [
            {
                "symbol": data.symbol,
                "name": data.name,
                "price": data.price,
                "market_cap": data.market_cap,
                "pe_ratio": data.pe_ratio,
                "debt_to_equity": data.debt_to_equity,
                "revenue_growth": data.revenue_growth,
                "earnings_growth": data.earnings_growth,
                "promoter_holdings": data.promoter_holdings,
                "sector": data.sector,
                "last_updated": data.last_updated,
                "provider": provider,
            }
            for data in stocks_data
        ]

    async def fetch_market_analysis(self, symbols: list[str]) -> dict[str, Any]:
        """Fetch market analysis for multiple stocks.

        Args:
            symbols: List of stock ticker symbols.

        Returns:
            Dictionary with market analysis data.
        """
        # Try Screener.in first for comprehensive data
        try:
            screener_data = await self.fetch_multiple_stocks(symbols, "screener")
        except Exception as e:
            print(f"Screener.in failed: {e}, falling back to Yahoo Finance")
            screener_data = []

        # Use Yahoo Finance for price data if Screener fails
        if not screener_data:
            try:
                yahoo_data = await self.fetch_multiple_stocks(symbols, "yahoo")
            except Exception as e:
                print(f"Yahoo Finance failed: {e}")
                yahoo_data = []
        else:
            yahoo_data = []

        return {
            "screener_data": screener_data,
            "yahoo_data": yahoo_data,
            "total_stocks": len(screener_data) + len(yahoo_data),
            "data_source": "screener" if screener_data else "yahoo",
        }


async def main() -> None:
    """Test the market data fetcher with example symbols."""
    fetcher = MarketDataFetcher()

    # Test with some Indian stocks
    symbols = ["RELIANCE", "TCS", "HDFCBANK", "INFY", "BAJFINANCE"]

    print("Fetching real market data...")
    analysis = await fetcher.fetch_market_analysis(symbols)

    print(f"Data source: {analysis['data_source']}")
    print(f"Total stocks fetched: {analysis['total_stocks']}")
    print()

    if analysis['screener_data']:
        print("Screener.in Data:")
        for stock in analysis['screener_data']:
            print(f"  {stock['symbol']}: ₹{stock['price']:.2f} | PE: {stock['pe_ratio']:.2f} | Sector: {stock['sector']}")

    if analysis['yahoo_data']:
        print("Yahoo Finance Data:")
        for stock in analysis['yahoo_data']:
            print(f"  {stock['symbol']}: ₹{stock['price']:.2f} | PE: {stock['pe_ratio']:.2f} | Sector: {stock['sector']}")


if __name__ == "__main__":
    asyncio.run(main())
