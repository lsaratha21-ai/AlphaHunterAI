"""Data downloader for scheduled tasks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from app.core.exceptions import ProviderError


class DataDownloader:
    """Downloader for fetching latest market data."""

    def __init__(self, data_dir: str = "data") -> None:
        """Initialize the DataDownloader.

        Args:
            data_dir: Directory to store downloaded data.
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def download_stock_data(self, symbols: list[str]) -> dict[str, Any]:
        """Download stock data for given symbols.

        Args:
            symbols: List of stock symbols to download.

        Returns:
            Dictionary with downloaded data.

        Raises:
            ProviderError: If download fails.
        """
        # Mock implementation - in production, integrate with providers
        data = {}
        for symbol in symbols:
            # Generate mock data
            dates = pd.date_range(end=pd.Timestamp.now(), periods=90)
            prices = [100 + i * 0.5 for i in range(90)]
            volumes = [1000000 + i * 10000 for i in range(90)]

            df = pd.DataFrame({
                "date": dates,
                "close": prices,
                "volume": volumes,
                "high": [p * 1.02 for p in prices],
                "low": [p * 0.98 for p in prices],
            })

            data[symbol] = df

        return data

    def save_data(self, data: dict[str, Any], filename: str) -> str:
        """Save downloaded data to file.

        Args:
            data: Data to save.
            filename: Name of the file.

        Returns:
            Path to saved file.
        """
        file_path = self.data_dir / filename
        # Save as pickle for now - can be changed to CSV/JSON
        data["symbols"] = list(data.keys())
        file_path.write_text(str(data))  # Simplified
        return str(file_path)
