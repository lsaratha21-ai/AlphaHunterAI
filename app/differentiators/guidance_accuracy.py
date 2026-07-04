"""Guidance accuracy tracking for historical performance."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any

from app.differentiators.models import GuidanceAccuracyHistory


class GuidanceAccuracyTracker:
    """Tracker for management guidance accuracy over time."""

    def __init__(self) -> None:
        """Initialize the guidance accuracy tracker."""
        self.guidance_history: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(
            lambda: defaultdict(list),
        )

    def record_guidance(
        self,
        symbol: str,
        guidance_type: str,
        guidance_value: float,
        actual_value: float,
        period: str,
    ) -> None:
        """Record guidance and actual values.

        Args:
            symbol: Stock symbol.
            guidance_type: Type of guidance (revenue, profit, margin, etc.).
            guidance_value: Guided value.
            actual_value: Actual achieved value.
            period: Period (e.g., "Q1 2024", "Q2 2024").
        """
        deviation = abs((actual_value - guidance_value) / guidance_value) * 100 if guidance_value != 0 else 0
        is_accurate = deviation <= 10  # Within 10% is considered accurate

        self.guidance_history[symbol][guidance_type].append({
            "period": period,
            "guidance_value": guidance_value,
            "actual_value": actual_value,
            "deviation": deviation,
            "is_accurate": is_accurate,
            "timestamp": datetime.now(),
        })

    def calculate_accuracy_score(
        self,
        symbol: str,
        guidance_type: str,
        min_periods: int = 4,
    ) -> GuidanceAccuracyHistory:
        """Calculate accuracy score for a specific guidance type.

        Args:
            symbol: Stock symbol.
            guidance_type: Type of guidance.
            min_periods: Minimum periods required for scoring.

        Returns:
            GuidanceAccuracyHistory with accuracy metrics.
        """
        records = self.guidance_history[symbol][guidance_type]

        if len(records) < min_periods:
            # Not enough data for meaningful score
            return GuidanceAccuracyHistory(
                symbol=symbol,
                guidance_type=guidance_type,
                total_guidance_periods=len(records),
                accurate_periods=0,
                accuracy_percentage=0.0,
                average_deviation_percentage=0.0,
                recent_accuracy_trend="insufficient_data",
                accuracy_score=50.0,
                last_updated=datetime.now(),
            )

        total_periods = len(records)
        accurate_periods = sum(1 for r in records if r["is_accurate"])
        accuracy_percentage = (accurate_periods / total_periods) * 100

        avg_deviation = sum(r["deviation"] for r in records) / total_periods

        # Calculate recent trend
        recent_records = sorted(records, key=lambda x: x["timestamp"])[-4:]
        recent_accuracy = sum(1 for r in recent_records if r["is_accurate"]) / len(recent_records)

        if recent_accuracy > accuracy_percentage / 100:
            trend = "improving"
        elif recent_accuracy < accuracy_percentage / 100:
            trend = "declining"
        else:
            trend = "stable"

        # Calculate overall accuracy score
        accuracy_score = (
            accuracy_percentage * 0.6 +
            (100 - avg_deviation) * 0.4
        )

        return GuidanceAccuracyHistory(
            symbol=symbol,
            guidance_type=guidance_type,
            total_guidance_periods=total_periods,
            accurate_periods=accurate_periods,
            accuracy_percentage=accuracy_percentage,
            average_deviation_percentage=avg_deviation,
            recent_accuracy_trend=trend,
            accuracy_score=accuracy_score,
            last_updated=datetime.now(),
        )

    def get_overall_guidance_accuracy(
        self,
        symbol: str,
        guidance_types: list[str] | None = None,
    ) -> float:
        """Get overall guidance accuracy across all types.

        Args:
            symbol: Stock symbol.
            guidance_types: List of guidance types to include. If None, uses all.

        Returns:
            Overall accuracy score (0-100).
        """
        if guidance_types is None:
            guidance_types = ["revenue", "profit", "margin", "eps"]

        scores = []
        for guidance_type in guidance_types:
            history = self.calculate_accuracy_score(symbol, guidance_type)
            if history.total_guidance_periods >= 2:
                scores.append(history.accuracy_score)

        if not scores:
            return 50.0  # Neutral score if insufficient data

        return sum(scores) / len(scores)
