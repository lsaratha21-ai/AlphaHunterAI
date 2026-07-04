"""Weekly AlphaHunter Research Report generator."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class StockRanking:
    """Stock ranking for weekly report."""

    rank: int
    symbol: str
    company_name: str
    alpha_score: float
    previous_rank: int | None = None
    change: int = 0  # Rank change from previous week

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "rank": self.rank,
            "symbol": self.symbol,
            "company_name": self.company_name,
            "alpha_score": self.alpha_score,
            "previous_rank": self.previous_rank,
            "change": self.change,
        }


@dataclass
class HiddenGem:
    """Hidden gem stock with before the crowd potential."""

    rank: int
    symbol: str
    company_name: str
    before_crowd_score: float
    alpha_score: float
    reason: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "rank": self.rank,
            "symbol": self.symbol,
            "company_name": self.company_name,
            "before_crowd_score": self.before_crowd_score,
            "alpha_score": self.alpha_score,
            "reason": self.reason,
        }


@dataclass
class SectorTrend:
    """Sector trend information."""

    rank: int
    sector: str
    momentum_score: float
    rotation_signal: str  # inflow, neutral, outflow
    key_stocks: list[str]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "rank": self.rank,
            "sector": self.sector,
            "momentum_score": self.momentum_score,
            "rotation_signal": self.rotation_signal,
            "key_stocks": self.key_stocks,
        }


@dataclass
class ManagementUpgrade:
    """Management guidance upgrade information."""

    symbol: str
    company_name: str
    previous_guidance: str
    new_guidance: str
    impact: str  # positive, negative, neutral
    reason: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "company_name": self.company_name,
            "previous_guidance": self.previous_guidance,
            "new_guidance": self.new_guidance,
            "impact": self.impact,
            "reason": self.reason,
        }


@dataclass
class InstitutionalActivity:
    """Institutional buying/selling activity."""

    symbol: str
    company_name: str
    activity: str  # buying, selling, holding
    change_percentage: float
    notable_investor: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "company_name": self.company_name,
            "activity": self.activity,
            "change_percentage": self.change_percentage,
            "notable_investor": self.notable_investor,
        }


@dataclass
class TechnicalBreakout:
    """Fresh technical breakout information."""

    symbol: str
    company_name: str
    breakout_type: str  # resistance, support, pattern
    price_level: float
    volume_confirmation: bool
    timeframe: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "company_name": self.company_name,
            "breakout_type": self.breakout_type,
            "price_level": self.price_level,
            "volume_confirmation": self.volume_confirmation,
            "timeframe": self.timeframe,
        }


@dataclass
class StockToAvoid:
    """Stock to avoid with reasoning."""

    symbol: str
    company_name: str
    reason: str
    risk_level: str  # low, medium, high
    alternative: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "company_name": self.company_name,
            "reason": self.reason,
            "risk_level": self.risk_level,
            "alternative": self.alternative,
        }


@dataclass
class RiskAlert:
    """Risk alert for market conditions."""

    alert_type: str  # sector, market, regulatory, global
    severity: str  # low, medium, high
    description: str
    affected_sectors: list[str] | None = None
    affected_stocks: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "alert_type": self.alert_type,
            "severity": self.severity,
            "description": self.description,
            "affected_sectors": self.affected_sectors,
            "affected_stocks": self.affected_stocks,
        }


@dataclass
class PortfolioChange:
    """Portfolio change recommendation."""

    action: str  # add, remove, reduce, increase
    symbol: str
    company_name: str
    reason: str
    current_weight: float | None = None
    new_weight: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "action": self.action,
            "symbol": self.symbol,
            "company_name": self.company_name,
            "reason": self.reason,
            "current_weight": self.current_weight,
            "new_weight": self.new_weight,
        }


@dataclass
class NewOpportunity:
    """New opportunity identified this week."""

    symbol: str
    company_name: str
    opportunity_type: str  # turnaround, growth, value, momentum
    alpha_score: float
    catalyst: str
    entry_range: str
    target: str
    stop_loss: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "company_name": self.company_name,
            "opportunity_type": self.opportunity_type,
            "alpha_score": self.alpha_score,
            "catalyst": self.catalyst,
            "entry_range": self.entry_range,
            "target": self.target,
            "stop_loss": self.stop_loss,
        }


@dataclass
class WeeklyReport:
    """Complete weekly AlphaHunter Research Report."""

    report_date: datetime
    week_number: int
    year: int
    top_20_stocks: list[StockRanking]
    top_5_hidden_gems: list[HiddenGem]
    top_5_emerging_sectors: list[SectorTrend]
    management_guidance_upgrades: list[ManagementUpgrade]
    institutional_buying: list[InstitutionalActivity]
    fresh_technical_breakouts: list[TechnicalBreakout]
    stocks_to_avoid: list[StockToAvoid]
    risk_alerts: list[RiskAlert]
    portfolio_changes: list[PortfolioChange]
    new_opportunities: list[NewOpportunity]
    market_summary: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "report_date": self.report_date.isoformat(),
            "week_number": self.week_number,
            "year": self.year,
            "top_20_stocks": [s.to_dict() for s in self.top_20_stocks],
            "top_5_hidden_gems": [g.to_dict() for g in self.top_5_hidden_gems],
            "top_5_emerging_sectors": [s.to_dict() for s in self.top_5_emerging_sectors],
            "management_guidance_upgrades": [m.to_dict() for m in self.management_guidance_upgrades],
            "institutional_buying": [i.to_dict() for i in self.institutional_buying],
            "fresh_technical_breakouts": [t.to_dict() for t in self.fresh_technical_breakouts],
            "stocks_to_avoid": [s.to_dict() for s in self.stocks_to_avoid],
            "risk_alerts": [r.to_dict() for r in self.risk_alerts],
            "portfolio_changes": [p.to_dict() for p in self.portfolio_changes],
            "new_opportunities": [n.to_dict() for n in self.new_opportunities],
            "market_summary": self.market_summary,
        }
