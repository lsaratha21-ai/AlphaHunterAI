"""Manual CSV data provider implementation."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from app.core.exceptions import ProviderError, ValidationError
from app.providers.base import Provider, ProviderConfig, StockData


class ManualCSVProviderConfig(ProviderConfig):
    """Configuration for Manual CSV provider."""

    file_path: str | None = None


class ManualCSVProvider(Provider):
    """Manual CSV data provider.

    Reads stock data from a manually provided CSV file.
    """

    def __init__(self, config: ManualCSVProviderConfig | None = None) -> None:
        """Initialize the Manual CSV provider.

        Args:
            config: Provider configuration.
        """
        super().__init__(config or ManualCSVProviderConfig())
        self._data_cache: dict[str, StockData] | None = None

    def _load_csv(self) -> dict[str, StockData]:
        """Load CSV file and parse stock data.

        Returns:
            Dictionary mapping symbols to StockData.

        Raises:
            ValidationError: If CSV file is invalid or missing.
            ProviderError: If file read fails.
        """
        if self._data_cache is not None:
            return self._data_cache

        config = self.config
        if not isinstance(config, ManualCSVProviderConfig):
            raise ValidationError("Invalid config type for ManualCSVProvider")

        if config.file_path is None:
            raise ValidationError("file_path is required for ManualCSVProvider")

        csv_path = Path(config.file_path)
        if not csv_path.exists():
            raise ProviderError(f"CSV file not found: {csv_path}")

        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            raise ProviderError(f"Failed to read CSV file: {e}")

        required_columns = {"symbol", "name", "price"}
        if not required_columns.issubset(df.columns):
            raise ValidationError(
                f"CSV must contain columns: {required_columns}. "
                f"Found: {df.columns.tolist()}"
            )

        data_dict: dict[str, StockData] = {}
        for _, row in df.iterrows():
            stock_data = StockData(
                symbol=str(row["symbol"]).upper(),
                name=str(row["name"]),
                price=float(row["price"]),
                market_cap=float(row["market_cap"]) if "market_cap" in row and pd.notna(row["market_cap"]) else None,
                pe_ratio=float(row["pe_ratio"]) if "pe_ratio" in row and pd.notna(row["pe_ratio"]) else None,
                debt_to_equity=float(row["debt_to_equity"]) if "debt_to_equity" in row and pd.notna(row["debt_to_equity"]) else None,
                revenue_growth=float(row["revenue_growth"]) if "revenue_growth" in row and pd.notna(row["revenue_growth"]) else None,
                earnings_growth=float(row["earnings_growth"]) if "earnings_growth" in row and pd.notna(row["earnings_growth"]) else None,
                promoter_holdings=float(row["promoter_holdings"]) if "promoter_holdings" in row and pd.notna(row["promoter_holdings"]) else None,
                sector=str(row["sector"]) if "sector" in row and pd.notna(row["sector"]) else None,
                last_updated=date.today(),
            )
            data_dict[stock_data.symbol] = stock_data

        self._data_cache = data_dict
        return data_dict

    async def fetch_stock_data(self, symbol: str) -> StockData:
        """Fetch stock data from CSV file.

        Args:
            symbol: Stock ticker symbol.

        Returns:
            StockData object with fetched information.

        Raises:
            ProviderError: If data fetch fails.
            ValidationError: If symbol not found in CSV.
        """
        data = self._load_csv()
        symbol_upper = symbol.upper()

        if symbol_upper not in data:
            raise ValidationError(f"Symbol {symbol} not found in CSV file")

        return data[symbol_upper]

    async def fetch_multiple_stocks(self, symbols: list[str]) -> list[StockData]:
        """Fetch data for multiple stocks from CSV file.

        Args:
            symbols: List of stock ticker symbols.

        Returns:
            List of StockData objects.

        Raises:
            ProviderError: If data fetch fails.
        """
        data = self._load_csv()
        results = []
        for symbol in symbols:
            symbol_upper = symbol.upper()
            if symbol_upper in data:
                results.append(data[symbol_upper])
        return results

    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "Manual CSV"
