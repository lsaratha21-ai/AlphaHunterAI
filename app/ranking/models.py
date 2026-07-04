"""Opportunity ranking models with risk-adjusted metrics."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Catalyst:
    """Catalyst for stock price movement."""

    type: str  # earnings, sector_rotation, management, institutional, technical, regulatory
    description: str
    expected_impact: str  # high, medium, low
    timeline: str  # short-term, medium-term, long-term
    probability: float  # 0-100

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "type": self.type,
            "description": self.description,
            "expected_impact": self.expected_impact,
            "timeline": self.timeline,
            "probability": self.probability,
        }


@dataclass
class Evidence:
    """Supporting evidence for recommendation."""

    type: str  # financial, technical, sector, management, institutional
    description: str
    strength: str  # strong, moderate, weak
    data_point: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "type": self.type,
            "description": self.description,
            "strength": self.strength,
            "data_point": self.data_point,
        }


@dataclass
class RiskAdjustedMetrics:
    """Risk-adjusted performance metrics."""

    expected_return_min: float  # Minimum expected return %
    expected_return_max: float  # Maximum expected return %
    expected_return_avg: float  # Average expected return %
    downside_risk: float  # Estimated downside risk %
    probability_of_success: float  # Probability of achieving target %
    risk_reward_ratio: float  # Risk/reward ratio
    sharpe_ratio: float  # Risk-adjusted return ratio
    max_drawdown_risk: float  # Maximum drawdown risk %
    volatility_risk: float  # Volatility risk %

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "expected_return_min": self.expected_return_min,
            "expected_return_max": self.expected_return_max,
            "expected_return_avg": self.expected_return_avg,
            "downside_risk": self.downside_risk,
            "probability_of_success": self.probability_of_success,
            "risk_reward_ratio": self.risk_reward_ratio,
            "sharpe_ratio": self.sharpe_ratio,
            "max_drawdown_risk": self.max_drawdown_risk,
            "volatility_risk": self.volatility_risk,
        }


@dataclass
class OpportunityRanking:
    """Ranked opportunity with comprehensive metrics."""

    symbol: str
    company_name: str
    alpha_score: float
    confidence_score: float
    risk_adjusted_metrics: RiskAdjustedMetrics
    catalysts: list[Catalyst]
    evidence: list[Evidence]
    position_size: float  # Recommended position size %
    ranking: int  # Overall ranking
    current_price: float
    entry_range_low: float
    entry_range_high: float
    target_price: float
    stop_loss: float
    time_horizon_months: int = 3
    reasoning: str | None = None
    created_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "company_name": self.company_name,
            "alpha_score": self.alpha_score,
            "confidence_score": self.confidence_score,
            "risk_adjusted_metrics": self.risk_adjusted_metrics.to_dict(),
            "catalysts": [c.to_dict() for c in self.catalysts],
            "evidence": [e.to_dict() for e in self.evidence],
            "position_size": self.position_size,
            "ranking": self.ranking,
            "current_price": self.current_price,
            "entry_range_low": self.entry_range_low,
            "entry_range_high": self.entry_range_high,
            "target_price": self.target_price,
            "stop_loss": self.stop_loss,
            "time_horizon_months": self.time_horizon_months,
            "reasoning": self.reasoning,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
