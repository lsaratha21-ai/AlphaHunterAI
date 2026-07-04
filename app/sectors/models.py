"""Data models for sector rotation analysis."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class GovernmentAnnouncement:
    """Government policy announcement affecting sectors."""

    sector: str
    announcement: str
    impact: str  # positive, negative, neutral
    timestamp: datetime
    source: str


@dataclass
class OrderBookData:
    """Order book data for sector analysis."""

    sector: str
    order_book_value: float
    growth_rate: float
    timestamp: datetime


@dataclass
class CommodityPrice:
    """Commodity price data affecting sectors."""

    commodity: str
    price: float
    change_percent: float
    affected_sectors: list[str]
    timestamp: datetime


@dataclass
class NewsItem:
    """News item affecting sectors."""

    sector: str
    headline: str
    sentiment: str  # positive, negative, neutral
    relevance_score: float
    timestamp: datetime
    source: str


@dataclass
class InstitutionalActivity:
    """Institutional buying/selling activity."""

    sector: str
    institution: str
    action: str  # buy, sell, hold
    amount: float
    timestamp: datetime


@dataclass
class SectorScore:
    """Comprehensive sector rotation score."""

    sector: str
    government_score: float | None = None
    order_book_score: float | None = None
    commodity_score: float | None = None
    news_score: float | None = None
    institutional_score: float | None = None
    overall_score: float | None = None
    rotation_signal: str | None = None  # inflow, outflow, neutral
    last_updated: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "sector": self.sector,
            "government_score": self.government_score,
            "order_book_score": self.order_book_score,
            "commodity_score": self.commodity_score,
            "news_score": self.news_score,
            "institutional_score": self.institutional_score,
            "overall_score": self.overall_score,
            "rotation_signal": self.rotation_signal,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
        }
