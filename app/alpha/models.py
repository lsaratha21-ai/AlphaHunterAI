"""Alpha Score models with layered scoring architecture."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class ComponentScore:
    """Individual component score with max value for research profile."""

    name: str
    score: float
    max_score: float
    weight: float
    details: str | None = None

    @property
    def percentage(self) -> float:
        """Calculate percentage score."""
        return (self.score / self.max_score) * 100 if self.max_score > 0 else 0

    def __str__(self) -> str:
        """String representation for research profile."""
        return f"{self.score}/{self.max_score}"


@dataclass
class AlphaScoreComponents:
    """Component scores for the layered Alpha Score model with research profile."""

    financial_quality: ComponentScore  # Max: 20, Weight: 20
    growth_acceleration: ComponentScore  # Max: 15, Weight: 15
    technical_momentum: ComponentScore  # Max: 15, Weight: 15
    sector_momentum: ComponentScore  # Max: 10, Weight: 10
    management_guidance: ComponentScore  # Max: 10, Weight: 10
    institutional_buying: ComponentScore  # Max: 10, Weight: 10
    valuation: ComponentScore  # Max: 5, Weight: 5
    order_book: ComponentScore  # Max: 5, Weight: 5
    risk: ComponentScore  # Max: 5, Weight: 5
    earnings_surprise_probability: ComponentScore  # Max: 5, Weight: 5

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation for research profile."""
        return {
            "financial_quality": {
                "score": self.financial_quality.score,
                "max_score": self.financial_quality.max_score,
                "weight": self.financial_quality.weight,
                "percentage": self.financial_quality.percentage,
                "display": str(self.financial_quality),
                "details": self.financial_quality.details,
            },
            "growth_acceleration": {
                "score": self.growth_acceleration.score,
                "max_score": self.growth_acceleration.max_score,
                "weight": self.growth_acceleration.weight,
                "percentage": self.growth_acceleration.percentage,
                "display": str(self.growth_acceleration),
                "details": self.growth_acceleration.details,
            },
            "technical_momentum": {
                "score": self.technical_momentum.score,
                "max_score": self.technical_momentum.max_score,
                "weight": self.technical_momentum.weight,
                "percentage": self.technical_momentum.percentage,
                "display": str(self.technical_momentum),
                "details": self.technical_momentum.details,
            },
            "sector_momentum": {
                "score": self.sector_momentum.score,
                "max_score": self.sector_momentum.max_score,
                "weight": self.sector_momentum.weight,
                "percentage": self.sector_momentum.percentage,
                "display": str(self.sector_momentum),
                "details": self.sector_momentum.details,
            },
            "management_guidance": {
                "score": self.management_guidance.score,
                "max_score": self.management_guidance.max_score,
                "weight": self.management_guidance.weight,
                "percentage": self.management_guidance.percentage,
                "display": str(self.management_guidance),
                "details": self.management_guidance.details,
            },
            "institutional_buying": {
                "score": self.institutional_buying.score,
                "max_score": self.institutional_buying.max_score,
                "weight": self.institutional_buying.weight,
                "percentage": self.institutional_buying.percentage,
                "display": str(self.institutional_buying),
                "details": self.institutional_buying.details,
            },
            "valuation": {
                "score": self.valuation.score,
                "max_score": self.valuation.max_score,
                "weight": self.valuation.weight,
                "percentage": self.valuation.percentage,
                "display": str(self.valuation),
                "details": self.valuation.details,
            },
            "order_book": {
                "score": self.order_book.score,
                "max_score": self.order_book.max_score,
                "weight": self.order_book.weight,
                "percentage": self.order_book.percentage,
                "display": str(self.order_book),
                "details": self.order_book.details,
            },
            "risk": {
                "score": self.risk.score,
                "max_score": self.risk.max_score,
                "weight": self.risk.weight,
                "percentage": self.risk.percentage,
                "display": str(self.risk),
                "details": self.risk.details,
            },
            "earnings_surprise_probability": {
                "score": self.earnings_surprise_probability.score,
                "max_score": self.earnings_surprise_probability.max_score,
                "weight": self.earnings_surprise_probability.weight,
                "percentage": self.earnings_surprise_probability.percentage,
                "display": str(self.earnings_surprise_probability),
                "details": self.earnings_surprise_probability.details,
            },
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
