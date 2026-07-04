"""Data models for technical analysis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class TechnicalScore:
    """Comprehensive technical score for a stock."""

    symbol: str
    rsi: float | None = None
    macd: float | None = None
    macd_signal: float | None = None
    macd_histogram: float | None = None
    ema_20: float | None = None
    sma_50: float | None = None
    sma_200: float | None = None
    adx: float | None = None
    atr: float | None = None
    supertrend: float | None = None
    supertrend_signal: str | None = None
    bollinger_upper: float | None = None
    bollinger_middle: float | None = None
    bollinger_lower: float | None = None
    vwap: float | None = None
    volume_breakout: bool | None = None
    delivery_percentage: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "rsi": self.rsi,
            "macd": self.macd,
            "macd_signal": self.macd_signal,
            "macd_histogram": self.macd_histogram,
            "ema_20": self.ema_20,
            "sma_50": self.sma_50,
            "sma_200": self.sma_200,
            "adx": self.adx,
            "atr": self.atr,
            "supertrend": self.supertrend,
            "supertrend_signal": self.supertrend_signal,
            "bollinger_upper": self.bollinger_upper,
            "bollinger_middle": self.bollinger_middle,
            "bollinger_lower": self.bollinger_lower,
            "vwap": self.vwap,
            "volume_breakout": self.volume_breakout,
            "delivery_percentage": self.delivery_percentage,
        }
