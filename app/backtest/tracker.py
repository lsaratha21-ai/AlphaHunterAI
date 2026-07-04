"""Recommendation tracker for storing and retrieving recommendation records."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.alpha import AlphaScore
from app.backtest.engine import BacktestEngine
from app.backtest.models import ExitRules, PerformanceMetrics, RecommendationTracking


class RecommendationTracker:
    """Tracker for storing and retrieving recommendation records."""

    def __init__(self) -> None:
        """Initialize the RecommendationTracker."""
        self.backtest_engine = BacktestEngine()
        self.recommendations: list[RecommendationTracking] = []

    def create_from_alpha_score(
        self,
        alpha_score: AlphaScore,
        entry_price: float,
        exit_rules: ExitRules | None = None,
    ) -> RecommendationTracking:
        """Create a recommendation tracking record from AlphaScore.

        Args:
            alpha_score: AlphaScore from research profile.
            entry_price: Entry price for the recommendation.
            exit_rules: Exit rules for the recommendation.

        Returns:
            RecommendationTracking record.
        """
        tracking = RecommendationTracking(
            id=self._generate_id(),
            symbol=alpha_score.symbol,
            alpha_score=alpha_score.overall_score,
            recommendation_date=alpha_score.timestamp or datetime.now(),
            entry_price=entry_price,
            exit_rules=exit_rules or self._default_exit_rules(
                alpha_score.target_price,
                alpha_score.stop_loss,
            ),
            current_price=alpha_score.current_price,
            action=alpha_score.action,
            confidence=alpha_score.confidence,
            reasoning=alpha_score.reasoning,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        self.recommendations.append(tracking)
        return tracking

    def _default_exit_rules(
        self,
        target_price: float | None,
        stop_loss: float | None,
    ) -> ExitRules:
        """Create default exit rules from AlphaScore.

        Args:
            target_price: Target price from AlphaScore.
            stop_loss: Stop loss from AlphaScore.

        Returns:
            ExitRules object.
        """
        return ExitRules(
            target_price=target_price,
            stop_loss=stop_loss,
            time_based_exit_days=180,  # Default 6 months
        )

    def _generate_id(self) -> str:
        """Generate a unique ID for the recommendation.

        Returns:
            Unique ID string.
        """
        return f"REC-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def get_by_id(self, recommendation_id: str) -> RecommendationTracking | None:
        """Get recommendation by ID.

        Args:
            recommendation_id: Recommendation ID.

        Returns:
            RecommendationTracking record or None if not found.
        """
        for rec in self.recommendations:
            if rec.id == recommendation_id:
                return rec
        return None

    def get_by_symbol(self, symbol: str) -> list[RecommendationTracking]:
        """Get all recommendations for a symbol.

        Args:
            symbol: Stock symbol.

        Returns:
            List of RecommendationTracking records.
        """
        return [rec for rec in self.recommendations if rec.symbol == symbol]

    def get_active_recommendations(self) -> list[RecommendationTracking]:
        """Get all active recommendations.

        Returns:
            List of active RecommendationTracking records.
        """
        return [rec for rec in self.recommendations if rec.is_active]

    def get_recommendations_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> list[RecommendationTracking]:
        """Get recommendations within a date range.

        Args:
            start_date: Start date.
            end_date: End date.

        Returns:
            List of RecommendationTracking records.
        """
        return [
            rec
            for rec in self.recommendations
            if start_date <= rec.recommendation_date <= end_date
        ]

    def update_performance(
        self,
        tracking: RecommendationTracking,
        price_history: dict[datetime, float],
    ) -> RecommendationTracking:
        """Update performance metrics for a recommendation.

        Args:
            tracking: RecommendationTracking record.
            price_history: Dictionary of dates to prices.

        Returns:
            Updated RecommendationTracking record.
        """
        tracking.performance = self.backtest_engine.calculate_performance(
            tracking,
            price_history,
        )
        tracking.updated_at = datetime.now()

        # Mark as inactive if exited
        if tracking.performance and tracking.performance.exit_price:
            tracking.is_active = False

        return tracking

    def update_current_price(
        self,
        tracking: RecommendationTracking,
        current_price: float,
    ) -> RecommendationTracking:
        """Update current price for a recommendation.

        Args:
            tracking: RecommendationTracking record.
            current_price: Current stock price.

        Returns:
            Updated RecommendationTracking record.
        """
        return self.backtest_engine.update_tracking_with_current_price(
            tracking,
            current_price,
        )

    def get_performance_summary(self) -> dict[str, Any]:
        """Get summary statistics for all recommendations.

        Returns:
            Dictionary with summary statistics.
        """
        if not self.recommendations:
            return {}

        total_recommendations = len(self.recommendations)
        active_count = len(self.get_active_recommendations())
        exited_count = total_recommendations - active_count

        # Calculate average returns
        total_returns = []
        max_drawdowns = []

        for rec in self.recommendations:
            if rec.performance and rec.performance.total_return is not None:
                total_returns.append(rec.performance.total_return)
            if rec.performance and rec.performance.max_drawdown is not None:
                max_drawdowns.append(rec.performance.max_drawdown)

        avg_return = sum(total_returns) / len(total_returns) if total_returns else None
        avg_max_drawdown = sum(max_drawdowns) / len(max_drawdowns) if max_drawdowns else None

        # Win rate
        winning_trades = [r for r in total_returns if r > 0]
        win_rate = (len(winning_trades) / len(total_returns) * 100) if total_returns else None

        return {
            "total_recommendations": total_recommendations,
            "active_recommendations": active_count,
            "exited_recommendations": exited_count,
            "average_return": avg_return,
            "average_max_drawdown": avg_max_drawdown,
            "win_rate": win_rate,
            "total_winning_trades": len(winning_trades),
            "total_losing_trades": len(total_returns) - len(winning_trades) if total_returns else 0,
        }
