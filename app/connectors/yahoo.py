"""Yahoo Finance connector for OHLCV data."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import httpx
import pandas as pd

from app.connectors.models import OHLCVData
from app.core.exceptions import ProviderError


class YahooFinanceConnector:
    """Connector for Yahoo Finance OHLCV data."""

    def __init__(self, timeout: int = 30) -> None:
        """Initialize the Yahoo Finance connector.

        Args:
            timeout: Request timeout in seconds.
        """
        self.timeout = timeout
        self.base_url = "https://query1.finance.yahoo.com"

    async def fetch_ohlcv_data(
        self,
        symbol: str,
        period: str = "1y",
        interval: str = "1d",
    ) -> list[OHLCVData]:
        """Fetch OHLCV data for a symbol.

        Args:
            symbol: Stock symbol (e.g., "RELIANCE.NS" for NSE).
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max).
            interval: Data interval (1m, 2m, 5m, 15m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo).

        Returns:
            List of OHLCVData objects.

        Raises:
            ProviderError: If data fetch fails.
        """
        try:
            # Use yfinance library if available, otherwise use direct API
            try:
                import yfinance as yf

                ticker = yf.Ticker(symbol)
                df = ticker.history(period=period, interval=interval)

                if df.empty:
                    raise ProviderError(f"No data found for symbol: {symbol}")

                data_points = []
                for date, row in df.iterrows():
                    data_point = OHLCVData(
                        symbol=symbol,
                        date=date.to_pydatetime(),
                        open=float(row["Open"]),
                        high=float(row["High"]),
                        low=float(row["Low"]),
                        close=float(row["Close"]),
                        volume=int(row["Volume"]),
                        adjusted_close=float(row["Close"]) if "Adj Close" not in df.columns else float(row["Adj Close"]),
                    )
                    data_points.append(data_point)

                return data_points

            except ImportError:
                # Fallback to direct API call if yfinance not available
                return await self._fetch_via_api(symbol, period, interval)

        except Exception as e:
            raise ProviderError(f"Failed to fetch Yahoo Finance data for {symbol}: {e}")

    async def _fetch_via_api(
        self,
        symbol: str,
        period: str,
        interval: str,
    ) -> list[OHLCVData]:
        """Fetch data via direct Yahoo Finance API.

        Args:
            symbol: Stock symbol.
            period: Time period.
            interval: Data interval.

        Returns:
            List of OHLCVData objects.

        Raises:
            ProviderError: If API call fails.
        """
        # Convert period to timestamp range
        now = datetime.now()
        if period == "1mo":
            start = now - timedelta(days=30)
        elif period == "3mo":
            start = now - timedelta(days=90)
        elif period == "6mo":
            start = now - timedelta(days=180)
        elif period == "1y":
            start = now - timedelta(days=365)
        elif period == "2y":
            start = now - timedelta(days=730)
        elif period == "5y":
            start = now - timedelta(days=1825)
        else:
            start = now - timedelta(days=365)  # Default to 1 year

        start_timestamp = int(start.timestamp())
        end_timestamp = int(now.timestamp())

        # Build URL
        url = f"{self.base_url}/v8/finance/chart/{symbol}"
        params = {
            "period1": start_timestamp,
            "period2": end_timestamp,
            "interval": interval,
            "includePrePost": "true",
            "events": "div%7Csplit",
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        result = data.get("chart", {}).get("result", [])
        if not result:
            raise ProviderError(f"No data found for symbol: {symbol}")

        timestamp_list = result[0].get("timestamp", [])
        indicators = result[0].get("indicators", {})
        quote = indicators.get("quote", [{}])[0]

        data_points = []
        for i, ts in enumerate(timestamp_list):
            try:
                data_point = OHLCVData(
                    symbol=symbol,
                    date=datetime.fromtimestamp(ts),
                    open=float(quote["open"][i]) if quote["open"][i] else 0.0,
                    high=float(quote["high"][i]) if quote["high"][i] else 0.0,
                    low=float(quote["low"][i]) if quote["low"][i] else 0.0,
                    close=float(quote["close"][i]) if quote["close"][i] else 0.0,
                    volume=int(quote["volume"][i]) if quote["volume"][i] else 0,
                    adjusted_close=None,
                )
                data_points.append(data_point)
            except (IndexError, TypeError, ValueError):
                continue

        return data_points

    async def fetch_multiple_symbols(
        self,
        symbols: list[str],
        period: str = "1y",
        interval: str = "1d",
    ) -> dict[str, list[OHLCVData]]:
        """Fetch OHLCV data for multiple symbols.

        Args:
            symbols: List of stock symbols.
            period: Time period.
            interval: Data interval.

        Returns:
            Dictionary mapping symbols to their OHLCV data.
        """
        results = {}
        for symbol in symbols:
            try:
                data = await self.fetch_ohlcv_data(symbol, period, interval)
                results[symbol] = data
            except ProviderError as e:
                # Log error but continue with other symbols
                print(f"Error fetching {symbol}: {e}")
                results[symbol] = []

        return results

    def fetch_ohlcv_data_sync(
        self,
        symbol: str,
        period: str = "1y",
        interval: str = "1d",
    ) -> list[OHLCVData]:
        """Synchronous version of fetch_ohlcv_data.

        Args:
            symbol: Stock symbol.
            period: Time period.
            interval: Data interval.

        Returns:
            List of OHLCVData objects.
        """
        import asyncio

        return asyncio.run(self.fetch_ohlcv_data(symbol, period, interval))
