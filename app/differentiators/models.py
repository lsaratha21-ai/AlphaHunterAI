"""Data models for differentiating features."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class ManagementGuidanceAnalysis:
    """LLM analysis of management guidance."""

    symbol: str
    document_type: str
    overall_sentiment: str  # positive, neutral, negative
    confidence_level: float  # 0-100
    key_insights: list[str]
    risk_factors: list[str]
    growth_indicators: list[str]
    management_credibility: float  # 0-100
    guidance_score: float  # 0-100
    timestamp: datetime

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "document_type": self.document_type,
            "overall_sentiment": self.overall_sentiment,
            "confidence_level": self.confidence_level,
            "key_insights": self.key_insights,
            "risk_factors": self.risk_factors,
            "growth_indicators": self.growth_indicators,
            "management_credibility": self.management_credibility,
            "guidance_score": self.guidance_score,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class GuidanceAccuracyHistory:
    """Historical guidance accuracy tracking."""

    symbol: str
    guidance_type: str  # revenue, profit, margin, etc.
    total_guidance_periods: int
    accurate_periods: int
    accuracy_percentage: float  # 0-100
    average_deviation_percentage: float
    recent_accuracy_trend: str  # improving, stable, declining
    accuracy_score: float  # 0-100
    last_updated: datetime

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "guidance_type": self.guidance_type,
            "total_guidance_periods": self.total_guidance_periods,
            "accurate_periods": self.accurate_periods,
            "accuracy_percentage": self.accuracy_percentage,
            "average_deviation_percentage": self.average_deviation_percentage,
            "recent_accuracy_trend": self.recent_accuracy_trend,
            "accuracy_score": self.accuracy_score,
            "last_updated": self.last_updated.isoformat(),
        }


@dataclass
class OrderBookQuality:
    """Order book quality metrics."""

    symbol: str
    total_order_book: float
    book_to_bill_ratio: float
    order_concentration: float  # 0-100, lower is better (less concentration)
    margin_profile: float  # 0-100, average margin percentage
    order_book_trend: str  # increasing, stable, decreasing
    quality_score: float  # 0-100
    timestamp: datetime

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "total_order_book": self.total_order_book,
            "book_to_bill_ratio": self.book_to_bill_ratio,
            "order_concentration": self.order_concentration,
            "margin_profile": self.margin_profile,
            "order_book_trend": self.order_book_trend,
            "quality_score": self.quality_score,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class SectorRotationRanking:
    """Sector rotation ranking."""

    sector: str
    rank: int
    total_sectors: int
    momentum_score: float  # 0-100
    inflow_outflow: float  # positive for inflow, negative for outflow
    relative_strength: float  # 0-100
    rotation_signal: str  # inflow, outflow, neutral
    week_ending: datetime

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "sector": self.sector,
            "rank": self.rank,
            "total_sectors": self.total_sectors,
            "momentum_score": self.momentum_score,
            "inflow_outflow": self.inflow_outflow,
            "relative_strength": self.relative_strength,
            "rotation_signal": self.rotation_signal,
            "week_ending": self.week_ending.isoformat(),
        }


@dataclass
class SmartMoneyActivity:
    """Smart money activity tracking."""

    symbol: str
    promoter_buying: float  # 0-100 score
    promoter_selling: float  # 0-100 score
    fii_dii_change: float  # percentage change
    mutual_fund_ownership_change: float  # percentage change
    block_deal_activity: float  # 0-100 score
    insider_confidence: float  # 0-100
    smart_money_score: float  # 0-100
    signal: str  # bullish, bearish, neutral
    timestamp: datetime

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "promoter_buying": self.promoter_buying,
            "promoter_selling": self.promoter_selling,
            "fii_dii_change": self.fii_dii_change,
            "mutual_fund_ownership_change": self.mutual_fund_ownership_change,
            "block_deal_activity": self.block_deal_activity,
            "insider_confidence": self.insider_confidence,
            "smart_money_score": self.smart_money_score,
            "signal": self.signal,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class CrowdSentiment:
    """Crowd sentiment and popularity metrics."""

    symbol: str
    social_media_mentions: int
    news_volume: int  # recent news articles
    retail_interest: float  # 0-100
    analyst_coverage: int
    popularity_score: float  # 0-100, higher = more popular
    crowd_score: float  # 0-100, lower = contrarian opportunity
    sentiment_signal: str  # overheated, normal, contrarian
    timestamp: datetime

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "social_media_mentions": self.social_media_mentions,
            "news_volume": self.news_volume,
            "retail_interest": self.retail_interest,
            "analyst_coverage": self.analyst_coverage,
            "popularity_score": self.popularity_score,
            "crowd_score": self.crowd_score,
            "sentiment_signal": self.sentiment_signal,
            "timestamp": self.timestamp.isoformat(),
        }
