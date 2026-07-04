"""Sector rotation engine for tracking sector movements."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.sectors.models import (
    CommodityPrice,
    GovernmentAnnouncement,
    InstitutionalActivity,
    NewsItem,
    OrderBookData,
    SectorScore,
)


class SectorRotationEngine:
    """Engine for tracking sector rotation signals."""

    def __init__(self) -> None:
        """Initialize the Sector Rotation Engine."""
        self.government_announcements: list[GovernmentAnnouncement] = []
        self.order_book_data: list[OrderBookData] = []
        self.commodity_prices: list[CommodityPrice] = []
        self.news_items: list[NewsItem] = []
        self.institutional_activities: list[InstitutionalActivity] = []

    def add_government_announcement(
        self,
        sector: str,
        announcement: str,
        impact: str,
        source: str,
        timestamp: datetime | None = None,
    ) -> None:
        """Add a government announcement.

        Args:
            sector: Affected sector.
            announcement: Announcement text.
            impact: Impact level (positive, negative, neutral).
            source: Source of announcement.
            timestamp: Timestamp of announcement.
        """
        if timestamp is None:
            timestamp = datetime.now()
        self.government_announcements.append(
            GovernmentAnnouncement(
                sector=sector,
                announcement=announcement,
                impact=impact,
                timestamp=timestamp,
                source=source,
            )
        )

    def add_order_book_data(
        self,
        sector: str,
        order_book_value: float,
        growth_rate: float,
        timestamp: datetime | None = None,
    ) -> None:
        """Add order book data.

        Args:
            sector: Sector name.
            order_book_value: Total order book value.
            growth_rate: Growth rate of order book.
            timestamp: Timestamp of data.
        """
        if timestamp is None:
            timestamp = datetime.now()
        self.order_book_data.append(
            OrderBookData(
                sector=sector,
                order_book_value=order_book_value,
                growth_rate=growth_rate,
                timestamp=timestamp,
            )
        )

    def add_commodity_price(
        self,
        commodity: str,
        price: float,
        change_percent: float,
        affected_sectors: list[str],
        timestamp: datetime | None = None,
    ) -> None:
        """Add commodity price data.

        Args:
            commodity: Commodity name.
            price: Current price.
            change_percent: Price change percentage.
            affected_sectors: List of affected sectors.
            timestamp: Timestamp of data.
        """
        if timestamp is None:
            timestamp = datetime.now()
        self.commodity_prices.append(
            CommodityPrice(
                commodity=commodity,
                price=price,
                change_percent=change_percent,
                affected_sectors=affected_sectors,
                timestamp=timestamp,
            )
        )

    def add_news_item(
        self,
        sector: str,
        headline: str,
        sentiment: str,
        relevance_score: float,
        source: str,
        timestamp: datetime | None = None,
    ) -> None:
        """Add a news item.

        Args:
            sector: Affected sector.
            headline: News headline.
            sentiment: Sentiment (positive, negative, neutral).
            relevance_score: Relevance score (0-1).
            source: News source.
            timestamp: Timestamp of news.
        """
        if timestamp is None:
            timestamp = datetime.now()
        self.news_items.append(
            NewsItem(
                sector=sector,
                headline=headline,
                sentiment=sentiment,
                relevance_score=relevance_score,
                timestamp=timestamp,
                source=source,
            )
        )

    def add_institutional_activity(
        self,
        sector: str,
        institution: str,
        action: str,
        amount: float,
        timestamp: datetime | None = None,
    ) -> None:
        """Add institutional activity.

        Args:
            sector: Sector name.
            institution: Institution name.
            action: Action type (buy, sell, hold).
            amount: Transaction amount.
            timestamp: Timestamp of activity.
        """
        if timestamp is None:
            timestamp = datetime.now()
        self.institutional_activities.append(
            InstitutionalActivity(
                sector=sector,
                institution=institution,
                action=action,
                amount=amount,
                timestamp=timestamp,
            )
        )

    def calculate_government_score(self, sector: str, days: int = 30) -> float:
        """Calculate government announcement score for a sector.

        Args:
            sector: Sector name.
            days: Number of days to look back.

        Returns:
            Government score (-100 to 100).
        """
        cutoff = datetime.now().timestamp() - (days * 86400)
        relevant = [
            a for a in self.government_announcements
            if a.sector == sector and a.timestamp.timestamp() > cutoff
        ]

        if not relevant:
            return 0.0

        score = 0.0
        for announcement in relevant:
            if announcement.impact == "positive":
                score += 20
            elif announcement.impact == "negative":
                score -= 20

        return max(-100, min(100, score))

    def calculate_order_book_score(self, sector: str, days: int = 30) -> float:
        """Calculate order book score for a sector.

        Args:
            sector: Sector name.
            days: Number of days to look back.

        Returns:
            Order book score (-100 to 100).
        """
        cutoff = datetime.now().timestamp() - (days * 86400)
        relevant = [
            d for d in self.order_book_data
            if d.sector == sector and d.timestamp.timestamp() > cutoff
        ]

        if not relevant:
            return 0.0

        # Average growth rate normalized to -100 to 100
        avg_growth = sum(d.growth_rate for d in relevant) / len(relevant)
        return max(-100, min(100, avg_growth))

    def calculate_commodity_score(self, sector: str, days: int = 30) -> float:
        """Calculate commodity price score for a sector.

        Args:
            sector: Sector name.
            days: Number of days to look back.

        Returns:
            Commodity score (-100 to 100).
        """
        cutoff = datetime.now().timestamp() - (days * 86400)
        relevant = [
            c for c in self.commodity_prices
            if sector in c.affected_sectors and c.timestamp.timestamp() > cutoff
        ]

        if not relevant:
            return 0.0

        # Average change percentage
        avg_change = sum(c.change_percent for c in relevant) / len(relevant)
        return max(-100, min(100, avg_change))

    def calculate_news_score(self, sector: str, days: int = 30) -> float:
        """Calculate news sentiment score for a sector.

        Args:
            sector: Sector name.
            days: Number of days to look back.

        Returns:
            News score (-100 to 100).
        """
        cutoff = datetime.now().timestamp() - (days * 86400)
        relevant = [
            n for n in self.news_items
            if n.sector == sector and n.timestamp.timestamp() > cutoff
        ]

        if not relevant:
            return 0.0

        score = 0.0
        for news in relevant:
            weight = news.relevance_score
            if news.sentiment == "positive":
                score += 30 * weight
            elif news.sentiment == "negative":
                score -= 30 * weight

        return max(-100, min(100, score))

    def calculate_institutional_score(self, sector: str, days: int = 30) -> float:
        """Calculate institutional activity score for a sector.

        Args:
            sector: Sector name.
            days: Number of days to look back.

        Returns:
            Institutional score (-100 to 100).
        """
        cutoff = datetime.now().timestamp() - (days * 86400)
        relevant = [
            i for i in self.institutional_activities
            if i.sector == sector and i.timestamp.timestamp() > cutoff
        ]

        if not relevant:
            return 0.0

        total_amount = sum(i.amount for i in relevant)
        buy_amount = sum(i.amount for i in relevant if i.action == "buy")
        sell_amount = sum(i.amount for i in relevant if i.action == "sell")

        if total_amount == 0:
            return 0.0

        net_flow = (buy_amount - sell_amount) / total_amount
        return max(-100, min(100, net_flow * 100))

    def calculate_sector_score(
        self,
        sector: str,
        days: int = 30,
    ) -> SectorScore:
        """Calculate comprehensive sector rotation score.

        Args:
            sector: Sector name.
            days: Number of days to look back for data.

        Returns:
            SectorScore with all component scores and overall score.
        """
        government_score = self.calculate_government_score(sector, days)
        order_book_score = self.calculate_order_book_score(sector, days)
        commodity_score = self.calculate_commodity_score(sector, days)
        news_score = self.calculate_news_score(sector, days)
        institutional_score = self.calculate_institutional_score(sector, days)

        # Calculate overall score as weighted average
        weights = {
            "government": 0.2,
            "order_book": 0.25,
            "commodity": 0.15,
            "news": 0.2,
            "institutional": 0.2,
        }

        overall_score = (
            government_score * weights["government"]
            + order_book_score * weights["order_book"]
            + commodity_score * weights["commodity"]
            + news_score * weights["news"]
            + institutional_score * weights["institutional"]
        )

        # Determine rotation signal
        if overall_score > 20:
            rotation_signal = "inflow"
        elif overall_score < -20:
            rotation_signal = "outflow"
        else:
            rotation_signal = "neutral"

        return SectorScore(
            sector=sector,
            government_score=government_score,
            order_book_score=order_book_score,
            commodity_score=commodity_score,
            news_score=news_score,
            institutional_score=institutional_score,
            overall_score=overall_score,
            rotation_signal=rotation_signal,
            last_updated=datetime.now(),
        )
