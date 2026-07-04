"""Data models for management guidance extraction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class GuidanceScore:
    """Comprehensive management guidance score for a company."""

    symbol: str
    document_type: str
    revenue_outlook: str | None = None
    margin_outlook: str | None = None
    demand: str | None = None
    order_book: str | None = None
    capex: str | None = None
    expansion: str | None = None
    risks: list[str] | None = None
    management_confidence: str | None = None
    overall_sentiment: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "document_type": self.document_type,
            "revenue_outlook": self.revenue_outlook,
            "margin_outlook": self.margin_outlook,
            "demand": self.demand,
            "order_book": self.order_book,
            "capex": self.capex,
            "expansion": self.expansion,
            "risks": self.risks,
            "management_confidence": self.management_confidence,
            "overall_sentiment": self.overall_sentiment,
        }
