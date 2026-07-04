"""Crowd sentiment and popularity scoring."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.differentiators.models import CrowdSentiment


class CrowdSentimentScorer:
    """Scorer for crowd sentiment and popularity."""

    def calculate_crowd_score(
        self,
        symbol: str,
        social_media_mentions: int,
        news_volume: int,
        retail_interest: float,
        analyst_coverage: int,
        historical_data: dict[str, Any] | None = None,
    ) -> CrowdSentiment:
        """Calculate crowd sentiment score.

        Args:
            symbol: Stock symbol.
            social_media_mentions: Number of social media mentions.
            news_volume: Recent news article count.
            retail_interest: Retail interest score (0-100).
            analyst_coverage: Number of analysts covering.
            historical_data: Historical sentiment data.

        Returns:
            CrowdSentiment with crowd score.
        """
        # Score individual components
        popularity_score = self._calculate_popularity_score(
            social_media_mentions,
            news_volume,
            retail_interest,
            analyst_coverage,
        )

        # Calculate crowd score (inverse of popularity for contrarian opportunities)
        crowd_score = self._calculate_crowd_score(popularity_score)

        # Determine sentiment signal
        sentiment_signal = self._determine_sentiment_signal(crowd_score)

        return CrowdSentiment(
            symbol=symbol,
            social_media_mentions=social_media_mentions,
            news_volume=news_volume,
            retail_interest=retail_interest,
            analyst_coverage=analyst_coverage,
            popularity_score=popularity_score,
            crowd_score=crowd_score,
            sentiment_signal=sentiment_signal,
            timestamp=datetime.now(),
        )

    def _calculate_popularity_score(
        self,
        social_media_mentions: int,
        news_volume: int,
        retail_interest: float,
        analyst_coverage: int,
    ) -> float:
        """Calculate overall popularity score.

        Args:
            social_media_mentions: Social media mentions.
            news_volume: News article count.
            retail_interest: Retail interest score.
            analyst_coverage: Analyst count.

        Returns:
            Popularity score (0-100, higher = more popular).
        """
        # Normalize social media mentions (assuming 0-10000 range)
        social_score = min(100, social_media_mentions / 100)

        # Normalize news volume (assuming 0-100 range)
        news_score = min(100, news_volume)

        # Retail interest is already 0-100
        retail_score = retail_interest

        # Normalize analyst coverage (assuming 0-50 range)
        analyst_score = min(100, analyst_coverage * 2)

        # Weighted average
        popularity_score = (
            social_score * 0.30 +
            news_score * 0.25 +
            retail_score * 0.30 +
            analyst_score * 0.15
        )

        return popularity_score

    def _calculate_crowd_score(self, popularity_score: float) -> float:
        """Calculate crowd score (inverse of popularity).

        Args:
            popularity_score: Popularity score.

        Returns:
            Crowd score (0-100, lower = more contrarian opportunity).
        """
        # Invert popularity - high popularity = low crowd score
        # This is a contrarian indicator
        crowd_score = 100 - popularity_score
        return max(0, min(100, crowd_score))

    def _determine_sentiment_signal(self, crowd_score: float) -> str:
        """Determine sentiment signal based on crowd score.

        Args:
            crowd_score: Crowd score.

        Returns:
            Signal string (overheated, normal, contrarian).
        """
        if crowd_score <= 20:
            return "overheated"  # Too popular, avoid
        elif crowd_score >= 70:
            return "contrarian"  # Unpopular, opportunity
        else:
            return "normal"  # Balanced sentiment

    def get_popularity_trend(
        self,
        historical_data: dict[str, Any],
        periods: int = 4,
    ) -> str:
        """Get popularity trend over time.

        Args:
            historical_data: Historical popularity data.
            periods: Number of periods to analyze.

        Returns:
            Trend string (increasing, stable, decreasing).
        """
        if not historical_data or len(historical_data.get("popularity_scores", [])) < periods:
            return "insufficient_data"

        scores = historical_data["popularity_scores"][-periods:]
        if len(scores) < 2:
            return "stable"

        recent_avg = sum(scores[-2:]) / 2
        earlier_avg = sum(scores[:-2]) / (len(scores) - 2) if len(scores) > 2 else scores[0]

        change = ((recent_avg - earlier_avg) / earlier_avg) * 100 if earlier_avg != 0 else 0

        if change > 10:
            return "increasing"
        elif change < -10:
            return "decreasing"
        else:
            return "stable"
