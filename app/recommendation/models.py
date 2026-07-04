"""Data models for AI recommendations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Recommendation:
    """AI-generated stock recommendation."""

    symbol: str
    overall_score: float
    action: str  # buy, hold, sell
    confidence: float  # 0 to 100
    target_price: float | None = None
    stop_loss: float | None = None
    current_price: float | None = None
    reasoning: str | None = None
    timestamp: datetime | None = None

    # Component scores
    financial_score: float | None = None
    technical_score: float | None = None
    sector_score: float | None = None
    guidance_score: float | None = None
    valuation_score: float | None = None
    institutional_score: float | None = None
    news_score: float | None = None
    risk_score: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "overall_score": self.overall_score,
            "action": self.action,
            "confidence": self.confidence,
            "target_price": self.target_price,
            "stop_loss": self.stop_loss,
            "current_price": self.current_price,
            "reasoning": self.reasoning,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "financial_score": self.financial_score,
            "technical_score": self.technical_score,
            "sector_score": self.sector_score,
            "guidance_score": self.guidance_score,
            "valuation_score": self.valuation_score,
            "institutional_score": self.institutional_score,
            "news_score": self.news_score,
            "risk_score": self.risk_score,
        }
