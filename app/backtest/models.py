"""Backtesting models for tracking recommendation performance."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class ExitRules:
    """Exit rules for a recommendation."""

    target_price: float | None = None
    stop_loss: float | None = None
    time_based_exit_days: int | None = None  # Exit after N days regardless
    stop_loss_percentage: float | None = None  # Stop loss as percentage
    target_percentage: float | None = None  # Target as percentage

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "target_price": self.target_price,
            "stop_loss": self.stop_loss,
            "time_based_exit_days": self.time_based_exit_days,
            "stop_loss_percentage": self.stop_loss_percentage,
            "target_percentage": self.target_percentage,
        }


@dataclass
class PerformanceMetrics:
    """Performance metrics for a recommendation."""

    return_1_month: float | None = None
    return_3_month: float | None = None
    return_6_month: float | None = None
    max_drawdown: float | None = None
    max_drawdown_date: datetime | None = None
    exit_price: float | None = None
    exit_date: datetime | None = None
    exit_reason: str | None = None  # target_hit, stop_loss, time_exit, manual
    total_return: float | None = None
    holding_period_days: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "return_1_month": self.return_1_month,
            "return_3_month": self.return_3_month,
            "return_6_month": self.return_6_month,
            "max_drawdown": self.max_drawdown,
            "max_drawdown_date": self.max_drawdown_date.isoformat() if self.max_drawdown_date else None,
            "exit_price": self.exit_price,
            "exit_date": self.exit_date.isoformat() if self.exit_date else None,
            "exit_reason": self.exit_reason,
            "total_return": self.total_return,
            "holding_period_days": self.holding_period_days,
        }


@dataclass
class RecommendationTracking:
    """Tracking record for a recommendation with backtesting data."""

    symbol: str
    alpha_score: float
    recommendation_date: datetime
    entry_price: float
    id: str | None = None
    exit_rules: ExitRules | None = None
    current_price: float | None = None
    performance: PerformanceMetrics | None = None
    action: str = "hold"  # buy, hold, sell
    confidence: float = 50.0
    reasoning: str | None = None
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "symbol": self.symbol,
            "alpha_score": self.alpha_score,
            "recommendation_date": self.recommendation_date.isoformat(),
            "entry_price": self.entry_price,
            "exit_rules": self.exit_rules.to_dict() if self.exit_rules else None,
            "current_price": self.current_price,
            "performance": self.performance.to_dict() if self.performance else None,
            "action": self.action,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
