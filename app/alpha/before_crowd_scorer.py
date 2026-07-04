"""Before the Crowd scorer for identifying stocks before retail crowd."""

from __future__ import annotations

from typing import Any

from app.alpha.before_crowd import BeforeTheCrowdFactors, BeforeTheCrowdScore


class BeforeTheCrowdScorer:
    """Scorer for calculating Before the Crowd score."""

    def __init__(self) -> None:
        """Initialize the scorer."""
        pass

    def calculate_before_crowd_score(
        self,
        symbol: str,
        factors: BeforeTheCrowdFactors,
    ) -> BeforeTheCrowdScore:
        """Calculate Before the Crowd score based on factors.

        Args:
            symbol: Stock symbol.
            factors: BeforeTheCrowdFactors with all scoring factors.

        Returns:
            BeforeTheCrowdScore with component scores and overall score.
        """
        # Calculate individual component scores
        analyst_score = self._score_analyst_coverage(factors.analyst_coverage)
        institutional_score = self._score_institutional_change(
            factors.institutional_ownership_change,
        )
        earnings_score = self._score_earnings_trend(factors.earnings_trend)
        order_book_score = self._score_order_book_trend(factors.order_book_trend)
        technical_score = self._score_technical_breakout(
            factors.technical_breakout_stage,
        )
        valuation_score = self._score_valuation(factors.valuation_score)

        # Calculate weighted score
        weighted_score = (
            analyst_score * 0.20 +
            institutional_score * 0.20 +
            earnings_score * 0.15 +
            order_book_score * 0.15 +
            technical_score * 0.15 +
            valuation_score * 0.15
        )

        # Calculate overall score (normalized to 0-100)
        max_possible_score = (
            20.0 * 0.20 +
            20.0 * 0.20 +
            15.0 * 0.15 +
            15.0 * 0.15 +
            15.0 * 0.15 +
            15.0 * 0.15
        )  # = 17.25
        
        overall_score = (weighted_score / max_possible_score) * 100

        # Determine signal
        signal = self._determine_signal(overall_score)

        # Generate reasoning
        reasoning = self._generate_reasoning(
            factors,
            overall_score,
            signal,
        )

        return BeforeTheCrowdScore(
            symbol=symbol,
            overall_score=round(overall_score, 1),
            analyst_coverage_score=round(analyst_score, 1),
            institutional_score=round(institutional_score, 1),
            earnings_score=round(earnings_score, 1),
            order_book_score=round(order_book_score, 1),
            technical_score=round(technical_score, 1),
            valuation_score=round(valuation_score, 1),
            before_crowd_signal=signal,
            reasoning=reasoning,
            timestamp=None,
        )

    def _score_analyst_coverage(self, coverage: int) -> float:
        """Score analyst coverage (lower is better).

        Args:
            coverage: Number of analysts covering.

        Returns:
            Score (0-20).
        """
        # Lower coverage = higher score (before the crowd)
        if coverage <= 5:
            return 20.0
        elif coverage <= 10:
            return 15.0
        elif coverage <= 15:
            return 10.0
        elif coverage <= 20:
            return 5.0
        else:
            return 0.0

    def _score_institutional_change(self, change: float) -> float:
        """Score institutional ownership change (higher is better).

        Args:
            change: Percentage change in institutional ownership.

        Returns:
            Score (0-20).
        """
        if change >= 10:
            return 20.0
        elif change >= 5:
            return 15.0
        elif change >= 3:
            return 10.0
        elif change >= 1:
            return 5.0
        elif change >= 0:
            return 2.5
        else:
            return 0.0

    def _score_earnings_trend(self, trend: str) -> float:
        """Score earnings trend (improving is best).

        Args:
            trend: Earnings trend (improving, stable, declining).

        Returns:
            Score (0-15).
        """
        trend_scores = {
            "improving": 15.0,
            "stable": 7.5,
            "declining": 0.0,
        }
        return trend_scores.get(trend.lower(), 5.0)

    def _score_order_book_trend(self, trend: str) -> float:
        """Score order book trend (increasing is best).

        Args:
            trend: Order book trend (increasing, stable, decreasing).

        Returns:
            Score (0-15).
        """
        trend_scores = {
            "increasing": 15.0,
            "stable": 7.5,
            "decreasing": 0.0,
        }
        return trend_scores.get(trend.lower(), 5.0)

    def _score_technical_breakout(self, stage: str) -> float:
        """Score technical breakout stage (early is best).

        Args:
            stage: Breakout stage (early, middle, late).

        Returns:
            Score (0-15).
        """
        stage_scores = {
            "early": 15.0,
            "middle": 7.5,
            "late": 0.0,
        }
        return stage_scores.get(stage.lower(), 5.0)

    def _score_valuation(self, valuation_score: float) -> float:
        """Score valuation (reasonable is best).

        Args:
            valuation_score: Valuation score (0-100).

        Returns:
            Score (0-15).
        """
        # Higher valuation score = better value
        return (valuation_score / 100) * 15

    def _determine_signal(self, overall_score: float) -> str:
        """Determine before the crowd signal.

        Args:
            overall_score: Overall score.

        Returns:
            Signal string (early, neutral, late).
        """
        if overall_score >= 70:
            return "early"
        elif overall_score <= 30:
            return "late"
        else:
            return "neutral"

    def _generate_reasoning(
        self,
        factors: BeforeTheCrowdFactors,
        overall_score: float,
        signal: str,
    ) -> str:
        """Generate reasoning for the score.

        Args:
            factors: BeforeTheCrowdFactors.
            overall_score: Overall score.
            signal: Before the crowd signal.

        Returns:
            Reasoning string.
        """
        strengths = []
        concerns = []

        if factors.analyst_coverage <= 10:
            strengths.append(f"low analyst coverage ({factors.analyst_coverage} analysts)")
        elif factors.analyst_coverage >= 20:
            concerns.append(f"high analyst coverage ({factors.analyst_coverage} analysts)")

        if factors.institutional_ownership_change >= 5:
            strengths.append(f"rising institutional ownership ({factors.institutional_ownership_change:.1f}%)")
        elif factors.institutional_ownership_change < 0:
            concerns.append(f"declining institutional ownership ({factors.institutional_ownership_change:.1f}%)")

        if factors.earnings_trend == "improving":
            strengths.append("improving earnings")
        elif factors.earnings_trend == "declining":
            concerns.append("declining earnings")

        if factors.order_book_trend == "increasing":
            strengths.append("increasing order book")
        elif factors.order_book_trend == "decreasing":
            concerns.append("decreasing order book")

        if factors.technical_breakout_stage == "early":
            strengths.append("early technical breakout")
        elif factors.technical_breakout_stage == "late":
            concerns.append("late technical breakout")

        reasoning = f"Overall Score: {overall_score:.1f}/100. "

        if signal == "early":
            reasoning += "Before the Crowd: EARLY. Stock shows signs of institutional interest before retail crowd. "
            if strengths:
                reasoning += "Key indicators: " + ", ".join(strengths) + ". "
            if concerns:
                reasoning += "Monitor: " + ", ".join(concerns) + "."
        elif signal == "late":
            reasoning += "Before the Crowd: LATE. Stock likely already discovered by retail crowd. "
            if concerns:
                reasoning += "Concerns: " + ", ".join(concerns) + ". "
            if strengths:
                reasoning += "Positive factors: " + ", ".join(strengths) + "."
        else:
            reasoning += "Before the Crowd: NEUTRAL. Mixed signals. "
            if strengths:
                reasoning += "Strengths: " + ", ".join(strengths) + ". "
            if concerns:
                reasoning += "Concerns: " + ", ".join(concerns) + "."

        return reasoning
