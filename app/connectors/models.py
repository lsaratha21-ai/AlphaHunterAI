"""Data models for connectors."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class OHLCVData:
    """OHLCV (Open, High, Low, Close, Volume) data point."""

    symbol: str
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    adjusted_close: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "date": self.date.isoformat(),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "adjusted_close": self.adjusted_close,
        }


@dataclass
class CorporateAction:
    """Corporate action data."""

    symbol: str
    action_type: str  # dividend, split, bonus, etc.
    announcement_date: datetime
    effective_date: datetime | None = None
    description: str | None = None
    ratio: float | None = None
    amount: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "action_type": self.action_type,
            "announcement_date": self.announcement_date.isoformat(),
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "description": self.description,
            "ratio": self.ratio,
            "amount": self.amount,
        }
