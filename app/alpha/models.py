"""Alpha Score models with layered scoring architecture."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class AlphaScoreComponents:
    """Component scores for the layered Alpha Score model."""

    financial_quality: float  # Weight: 20
    growth_acceleration: float  # Weight: 15
    technical_momentum: float  # Weight: 15
    sector_momentum: float  # Weight: 10
    management_guidance: float  # Weight: 10
    institutional_buying: float  # Weight: 10
    valuation: float  # Weight: 5
    order_book: float  # Weight: 5
    risk: float  # Weight: 5
    earnings_surprise_probability: float  # Weight: 5

    def to_dict(self) -> dict[str, float]:
        """Convert to dictionary representation."""
        return {
            "financial_quality": self.financial_quality,
            "growth_acceleration": self.growth_acceleration,
            "technical_momentum": self.technical_momentum,
            "sector_momentum": self.sector_momentum,
            "management_guidance": self.management_guidance,
            "institutional_buying": self.institutional_buying,
            "valuation": self.valuation,
            "order_book": self.order_book,
            "risk": self.risk,
            "earnings_surprise_probability": self.earnings_surprise_probability,
        }


@dataclass
class AlphaScore:
    """Alpha Score with layered scoring model."""

    symbol: str
    overall_score: float
    components: AlphaScoreComponents
    action: str  # buy, hold, sell
    confidence: float  # 0 to 100
    target_price: float | None = None
    stop_loss: float | None = None
    current_price: float | None = None
    reasoning: str | None = None
    timestamp: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "overall_score": self.overall_score,
            "components": self.components.to_dict(),
            "action": self.action,
            "confidence": self.confidence,
            "target_price": self.target_price,
            "stop_loss": self.stop_loss,
            "current_price": self.current_price,
            "reasoning": self.reasoning,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }
