"""Backtest engine for calculating recommendation performance metrics."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from app.backtest.models import ExitRules, PerformanceMetrics, RecommendationTracking


class BacktestEngine:
    """Engine for calculating backtesting metrics for recommendations."""

    def __init__(self) -> None:
        """Initialize the BacktestEngine."""
        pass

    def calculate_performance(
        self,
        tracking: RecommendationTracking,
        price_history: dict[datetime, float],
    ) -> PerformanceMetrics:
        """Calculate performance metrics for a recommendation.

        Args:
            tracking: RecommendationTracking record.
            price_history: Dictionary of dates to prices.

        Returns:
            PerformanceMetrics with calculated metrics.
        """
        if not price_history:
            return PerformanceMetrics()

        # Calculate returns at different time intervals
        return_1_month = self._calculate_return(
            tracking.entry_price,
            tracking.recommendation_date,
            price_history,
            days=30,
        )
        return_3_month = self._calculate_return(
            tracking.entry_price,
            tracking.recommendation_date,
            price_history,
            days=90,
        )
        return_6_month = self._calculate_return(
            tracking.entry_price,
            tracking.recommendation_date,
            price_history,
            days=180,
        )

        # Calculate maximum drawdown
        max_drawdown, max_drawdown_date = self._calculate_max_drawdown(
            tracking.entry_price,
            tracking.recommendation_date,
            price_history,
        )

        # Determine exit
        exit_price, exit_date, exit_reason = self._determine_exit(
            tracking,
            price_history,
        )

        # Calculate total return if exited
        total_return = None
        holding_period_days = None
        if exit_price is not None and exit_date is not None:
            total_return = ((exit_price - tracking.entry_price) / tracking.entry_price) * 100
            holding_period_days = (exit_date - tracking.recommendation_date).days

        return PerformanceMetrics(
            return_1_month=return_1_month,
            return_3_month=return_3_month,
            return_6_month=return_6_month,
            max_drawdown=max_drawdown,
            max_drawdown_date=max_drawdown_date,
            exit_price=exit_price,
            exit_date=exit_date,
            exit_reason=exit_reason,
            total_return=total_return,
            holding_period_days=holding_period_days,
        )

    def _calculate_return(
        self,
        entry_price: float,
        entry_date: datetime,
        price_history: dict[datetime, float],
        days: int,
    ) -> float | None:
        """Calculate return after specified number of days.

        Args:
            entry_price: Entry price.
            entry_date: Entry date.
            price_history: Dictionary of dates to prices.
            days: Number of days to calculate return for.

        Returns:
            Return percentage or None if data not available.
        """
        target_date = entry_date + timedelta(days=days)

        # Find the closest date to target date in price history
        closest_date = min(
            price_history.keys(),
            key=lambda d: abs((d - target_date).days),
            default=None,
        )

        if closest_date is None or abs((closest_date - target_date).days) > 5:
            return None  # No data within 5 days of target

        exit_price = price_history[closest_date]
        return ((exit_price - entry_price) / entry_price) * 100

    def _calculate_max_drawdown(
        self,
        entry_price: float,
        entry_date: datetime,
        price_history: dict[datetime, float],
    ) -> tuple[float | None, datetime | None]:
        """Calculate maximum drawdown from entry.

        Args:
            entry_price: Entry price.
            entry_date: Entry date.
            price_history: Dictionary of dates to prices.

        Returns:
            Tuple of (max_drawdown_percentage, max_drawdown_date).
        """
        if not price_history:
            return None, None

        max_drawdown = 0.0
        max_drawdown_date = None
        peak = entry_price

        # Sort prices by date
        sorted_dates = sorted(
            [d for d in price_history.keys() if d >= entry_date],
        )

        for date in sorted_dates:
            price = price_history[date]
            if price > peak:
                peak = price

            drawdown = ((peak - price) / peak) * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown
                max_drawdown_date = date

        return max_drawdown, max_drawdown_date

    def _determine_exit(
        self,
        tracking: RecommendationTracking,
        price_history: dict[datetime, float],
    ) -> tuple[float | None, datetime | None, str | None]:
        """Determine exit point based on exit rules.

        Args:
            tracking: RecommendationTracking record.
            price_history: Dictionary of dates to prices.

        Returns:
            Tuple of (exit_price, exit_date, exit_reason).
        """
        if not tracking.exit_rules or not price_history:
            return None, None, None

        rules = tracking.exit_rules
        sorted_dates = sorted(
            [d for d in price_history.keys() if d >= tracking.recommendation_date],
        )

        for date in sorted_dates:
            price = price_history[date]

            # Check target price
            if rules.target_price and price >= rules.target_price:
                return price, date, "target_hit"

            # Check stop loss
            if rules.stop_loss and price <= rules.stop_loss:
                return price, date, "stop_loss"

            # Check percentage-based target
            if rules.target_percentage:
                target_price = tracking.entry_price * (1 + rules.target_percentage / 100)
                if price >= target_price:
                    return price, date, "target_hit"

            # Check percentage-based stop loss
            if rules.stop_loss_percentage:
                stop_price = tracking.entry_price * (1 - rules.stop_loss_percentage / 100)
                if price <= stop_price:
                    return price, date, "stop_loss"

            # Check time-based exit
            if rules.time_based_exit_days:
                exit_date = tracking.recommendation_date + timedelta(days=rules.time_based_exit_days)
                if date >= exit_date:
                    return price, date, "time_exit"

        return None, None, None

    def update_tracking_with_current_price(
        self,
        tracking: RecommendationTracking,
        current_price: float,
        current_date: datetime | None = None,
    ) -> RecommendationTracking:
        """Update tracking record with current price.

        Args:
            tracking: RecommendationTracking record.
            current_price: Current stock price.
            current_date: Current date (defaults to now).

        Returns:
            Updated RecommendationTracking record.
        """
        if current_date is None:
            current_date = datetime.now()

        tracking.current_price = current_price
        tracking.updated_at = current_date

        # If position is exited, mark as inactive
        if tracking.performance and tracking.performance.exit_price:
            tracking.is_active = False

        return tracking
