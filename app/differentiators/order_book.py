"""Order book quality scoring."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.differentiators.models import OrderBookQuality


class OrderBookQualityScorer:
    """Scorer for order book quality metrics."""

    def calculate_order_book_quality(
        self,
        symbol: str,
        total_order_book: float,
        book_to_bill_ratio: float,
        order_concentration_data: dict[str, float] | None = None,
        margin_profile: float = 15.0,
        historical_data: dict[str, Any] | None = None,
    ) -> OrderBookQuality:
        """Calculate order book quality score.

        Args:
            symbol: Stock symbol.
            total_order_book: Total order book value.
            book_to_bill_ratio: Book-to-bill ratio (orders booked / orders billed).
            order_concentration_data: Dict of customer/order sizes.
            margin_profile: Average margin percentage.
            historical_data: Historical order book data for trend analysis.

        Returns:
            OrderBookQuality with quality score.
        """
        # Score individual components
        book_size_score = self._score_book_size(total_order_book)
        book_to_bill_score = self._score_book_to_bill_ratio(book_to_bill_ratio)
        concentration_score = self._score_concentration(order_concentration_data)
        margin_score = self._score_margin_profile(margin_profile)
        trend_score = self._calculate_trend_score(historical_data)

        # Calculate overall quality score
        quality_score = (
            book_size_score * 0.25 +
            book_to_bill_score * 0.30 +
            concentration_score * 0.20 +
            margin_score * 0.15 +
            trend_score * 0.10
        )

        # Determine trend
        order_book_trend = self._determine_trend(historical_data)

        return OrderBookQuality(
            symbol=symbol,
            total_order_book=total_order_book,
            book_to_bill_ratio=book_to_bill_ratio,
            order_concentration=concentration_score,
            margin_profile=margin_score,
            order_book_trend=order_book_trend,
            quality_score=quality_score,
            timestamp=datetime.now(),
        )

    def _score_book_size(self, total_order_book: float) -> float:
        """Score order book size.

        Args:
            total_order_book: Total order book value.

        Returns:
            Score (0-100).
        """
        # Normalize based on typical ranges
        # This is a simplified scoring - in production, use sector-specific benchmarks
        if total_order_book >= 1000000000:  # > 1B
            return 90.0
        elif total_order_book >= 500000000:  # > 500M
            return 80.0
        elif total_order_book >= 100000000:  # > 100M
            return 70.0
        elif total_order_book >= 50000000:  # > 50M
            return 60.0
        elif total_order_book >= 10000000:  # > 10M
            return 50.0
        else:
            return 40.0

    def _score_book_to_bill_ratio(self, ratio: float) -> float:
        """Score book-to-bill ratio.

        Args:
            ratio: Book-to-bill ratio.

        Returns:
            Score (0-100).
        """
        # Ratio > 1.0 indicates growing orders
        if ratio >= 1.3:
            return 95.0
        elif ratio >= 1.2:
            return 85.0
        elif ratio >= 1.1:
            return 75.0
        elif ratio >= 1.0:
            return 65.0
        elif ratio >= 0.9:
            return 50.0
        elif ratio >= 0.8:
            return 35.0
        else:
            return 20.0

    def _score_concentration(
        self,
        concentration_data: dict[str, float] | None,
    ) -> float:
        """Score order concentration (lower concentration is better).

        Args:
            concentration_data: Dict of customer/order sizes.

        Returns:
            Score (0-100, higher = better diversification).
        """
        if not concentration_data:
            return 50.0  # Neutral score if no data

        # Calculate Herfindahl-Hirschman Index (HHI) for concentration
        total = sum(concentration_data.values())
        if total == 0:
            return 50.0

        shares = [value / total for value in concentration_data.values()]
        hhi = sum(share * 100 * share * 100 for share in shares)  # Scale to 0-10000

        # Convert HHI to score (lower HHI = better diversification)
        if hhi <= 1000:
            return 90.0
        elif hhi <= 2000:
            return 70.0
        elif hhi <= 3000:
            return 50.0
        elif hhi <= 5000:
            return 30.0
        else:
            return 10.0

    def _score_margin_profile(self, margin: float) -> float:
        """Score margin profile.

        Args:
            margin: Average margin percentage.

        Returns:
            Score (0-100).
        """
        if margin >= 25:
            return 95.0
        elif margin >= 20:
            return 85.0
        elif margin >= 15:
            return 75.0
        elif margin >= 10:
            return 60.0
        elif margin >= 5:
            return 40.0
        else:
            return 20.0

    def _calculate_trend_score(
        self,
        historical_data: dict[str, Any] | None,
    ) -> float:
        """Calculate trend score based on historical data.

        Args:
            historical_data: Historical order book data.

        Returns:
            Trend score (0-100).
        """
        if not historical_data or len(historical_data.get("values", [])) < 2:
            return 50.0  # Neutral if insufficient data

        values = historical_data["values"]
        recent = values[-4:]  # Last 4 periods
        earlier = values[-8:-4] if len(values) >= 8 else values[:-4]

        if not earlier:
            return 50.0

        recent_avg = sum(recent) / len(recent)
        earlier_avg = sum(earlier) / len(earlier)

        growth_rate = ((recent_avg - earlier_avg) / earlier_avg) * 100 if earlier_avg != 0 else 0

        # Score based on growth rate
        if growth_rate >= 20:
            return 90.0
        elif growth_rate >= 10:
            return 80.0
        elif growth_rate >= 5:
            return 70.0
        elif growth_rate >= 0:
            return 60.0
        elif growth_rate >= -5:
            return 40.0
        elif growth_rate >= -10:
            return 30.0
        else:
            return 20.0

    def _determine_trend(
        self,
        historical_data: dict[str, Any] | None,
    ) -> str:
        """Determine order book trend.

        Args:
            historical_data: Historical order book data.

        Returns:
            Trend string (increasing, stable, decreasing).
        """
        if not historical_data or len(historical_data.get("values", [])) < 2:
            return "stable"

        values = historical_data["values"]
        recent = values[-3:]
        earlier = values[-6:-3] if len(values) >= 6 else values[:-3]

        if not earlier:
            return "stable"

        recent_avg = sum(recent) / len(recent)
        earlier_avg = sum(earlier) / len(earlier)

        change = ((recent_avg - earlier_avg) / earlier_avg) * 100 if earlier_avg != 0 else 0

        if change > 5:
            return "increasing"
        elif change < -5:
            return "decreasing"
        else:
            return "stable"
