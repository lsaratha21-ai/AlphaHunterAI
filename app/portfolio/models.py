"""Portfolio construction models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Position:
    """Individual position in portfolio."""

    symbol: str
    company_name: str
    entry_price_low: float
    entry_price_high: float
    stop_loss: float
    target_price: float
    position_size: float  # Amount in INR
    shares: int
    weight: float  # Portfolio weight percentage
    alpha_score: float
    action: str  # buy, hold, sell
    reasoning: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "company_name": self.company_name,
            "entry_price_low": self.entry_price_low,
            "entry_price_high": self.entry_price_high,
            "stop_loss": self.stop_loss,
            "target_price": self.target_price,
            "position_size": self.position_size,
            "shares": self.shares,
            "weight": self.weight,
            "alpha_score": self.alpha_score,
            "action": self.action,
            "reasoning": self.reasoning,
        }


@dataclass
class RiskProfile:
    """Risk profile for portfolio construction."""

    risk_tolerance: str  # conservative, moderate, aggressive
    max_position_size: float  # Maximum percentage in single position
    max_sector_exposure: float  # Maximum percentage in single sector
    stop_loss_percentage: float  # Default stop loss percentage
    target_percentage: float  # Default target percentage
    max_positions: int  # Maximum number of positions
    min_positions: int  # Minimum number of positions

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "risk_tolerance": self.risk_tolerance,
            "max_position_size": self.max_position_size,
            "max_sector_exposure": self.max_sector_exposure,
            "stop_loss_percentage": self.stop_loss_percentage,
            "target_percentage": self.target_percentage,
            "max_positions": self.max_positions,
            "min_positions": self.min_positions,
        }


@dataclass
class Portfolio:
    """Complete portfolio with multiple positions."""

    id: str | None = None
    name: str
    total_capital: float
    risk_profile: RiskProfile
    positions: list[Position] = None
    cash: float = 0.0
    created_at: datetime | None = None
    horizon_months: int = 3

    def __post_init__(self) -> None:
        """Initialize default values."""
        if self.positions is None:
            self.positions = []

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "total_capital": self.total_capital,
            "risk_profile": self.risk_profile.to_dict(),
            "positions": [p.to_dict() for p in self.positions],
            "cash": self.cash,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "horizon_months": self.horizon_months,
        }

    def get_summary(self) -> dict[str, Any]:
        """Get portfolio summary statistics."""
        invested_amount = sum(p.position_size for p in self.positions)
        avg_alpha_score = sum(p.alpha_score for p in self.positions) / len(self.positions) if self.positions else 0

        return {
            "total_capital": self.total_capital,
            "invested_amount": invested_amount,
            "cash": self.cash,
            "cash_percentage": (self.cash / self.total_capital) * 100,
            "number_of_positions": len(self.positions),
            "average_alpha_score": avg_alpha_score,
            "average_weight": sum(p.weight for p in self.positions) / len(self.positions) if self.positions else 0,
        }
