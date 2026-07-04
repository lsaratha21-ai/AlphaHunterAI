"""Before the Crowd scoring for identifying stocks early."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class BeforeTheCrowdFactors:
    """Factors for Before the Crowd scoring."""

    analyst_coverage: int  # Number of analysts covering
    institutional_ownership_change: float  # Percentage change
    earnings_trend: str  # improving, stable, declining
    order_book_trend: str  # increasing, stable, decreasing
    technical_breakout_stage: str  # early, middle, late
    valuation_score: float  # 0-100

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "analyst_coverage": self.analyst_coverage,
            "institutional_ownership_change": self.institutional_ownership_change,
            "earnings_trend": self.earnings_trend,
            "order_book_trend": self.order_book_trend,
            "technical_breakout_stage": self.technical_breakout_stage,
            "valuation_score": self.valuation_score,
        }


@dataclass
class BeforeTheCrowdScore:
    """Before the Crowd score for identifying stocks before retail crowd."""

    symbol: str
    overall_score: float  # 0-100
    analyst_coverage_score: float  # 0-20
    institutional_score: float  # 0-20
    earnings_score: float  # 0-15
    order_book_score: float  # 0-15
    technical_score: float  # 0-15
    valuation_score: float  # 0-15
    before_crowd_signal: str  # early, neutral, late
    reasoning: str
    timestamp: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "overall_score": self.overall_score,
            "analyst_coverage_score": self.analyst_coverage_score,
            "institutional_score": self.institutional_score,
            "earnings_score": self.earnings_score,
            "order_book_score": self.order_book_score,
            "technical_score": self.technical_score,
            "valuation_score": self.valuation_score,
            "before_crowd_signal": self.before_crowd_signal,
            "reasoning": self.reasoning,
            "timestamp": self.timestamp,
        }
