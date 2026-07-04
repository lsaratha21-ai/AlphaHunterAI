"""Unit tests for Before the Crowd scoring."""

from __future__ import annotations

import pytest

from app.alpha import BeforeTheCrowdFactors, BeforeTheCrowdScore, BeforeTheCrowdScorer


class TestBeforeTheCrowdFactors:
    """Tests for BeforeTheCrowdFactors model."""

    def test_factors_creation(self) -> None:
        """Test BeforeTheCrowdFactors creation."""
        factors = BeforeTheCrowdFactors(
            analyst_coverage=5,
            institutional_ownership_change=8.5,
            earnings_trend="improving",
            order_book_trend="increasing",
            technical_breakout_stage="early",
            valuation_score=65.0,
        )
        assert factors.analyst_coverage == 5
        assert factors.institutional_ownership_change == 8.5
        assert factors.earnings_trend == "improving"

    def test_factors_to_dict(self) -> None:
        """Test BeforeTheCrowdFactors conversion to dictionary."""
        factors = BeforeTheCrowdFactors(
            analyst_coverage=5,
            institutional_ownership_change=8.5,
            earnings_trend="improving",
            order_book_trend="increasing",
            technical_breakout_stage="early",
            valuation_score=65.0,
        )
        result = factors.to_dict()
        assert result["analyst_coverage"] == 5
        assert result["earnings_trend"] == "improving"


class TestBeforeTheCrowdScore:
    """Tests for BeforeTheCrowdScore model."""

    def test_score_creation(self) -> None:
        """Test BeforeTheCrowdScore creation."""
        score = BeforeTheCrowdScore(
            symbol="RELIANCE",
            overall_score=78.5,
            analyst_coverage_score=18.0,
            institutional_score=16.0,
            earnings_score=12.0,
            order_book_score=14.0,
            technical_score=13.0,
            valuation_score=10.0,
            before_crowd_signal="early",
            reasoning="Strong early indicators",
            timestamp=None,
        )
        assert score.symbol == "RELIANCE"
        assert score.overall_score == 78.5
        assert score.before_crowd_signal == "early"

    def test_score_to_dict(self) -> None:
        """Test BeforeTheCrowdScore conversion to dictionary."""
        score = BeforeTheCrowdScore(
            symbol="RELIANCE",
            overall_score=78.5,
            analyst_coverage_score=18.0,
            institutional_score=16.0,
            earnings_score=12.0,
            order_book_score=14.0,
            technical_score=13.0,
            valuation_score=10.0,
            before_crowd_signal="early",
            reasoning="Strong early indicators",
            timestamp=None,
        )
        result = score.to_dict()
        assert result["symbol"] == "RELIANCE"
        assert result["overall_score"] == 78.5
        assert result["before_crowd_signal"] == "early"


class TestBeforeTheCrowdScorer:
    """Tests for BeforeTheCrowdScorer."""

    def test_scorer_initialization(self) -> None:
        """Test scorer initialization."""
        scorer = BeforeTheCrowdScorer()
        assert scorer is not None

    def test_calculate_before_crowd_score(self) -> None:
        """Test Before the Crowd score calculation."""
        scorer = BeforeTheCrowdScorer()
        factors = BeforeTheCrowdFactors(
            analyst_coverage=5,
            institutional_ownership_change=8.5,
            earnings_trend="improving",
            order_book_trend="increasing",
            technical_breakout_stage="early",
            valuation_score=65.0,
        )
        score = scorer.calculate_before_crowd_score("RELIANCE", factors)
        assert score.symbol == "RELIANCE"
        assert 0 <= score.overall_score <= 100
        assert score.before_crowd_signal in ["early", "neutral", "late"]

    def test_score_analyst_coverage(self) -> None:
        """Test analyst coverage scoring (lower is better)."""
        scorer = BeforeTheCrowdScorer()
        assert scorer._score_analyst_coverage(3) == 20.0
        assert scorer._score_analyst_coverage(8) == 15.0
        assert scorer._score_analyst_coverage(12) == 10.0
        assert scorer._score_analyst_coverage(18) == 5.0
        assert scorer._score_analyst_coverage(25) == 0.0

    def test_score_institutional_change(self) -> None:
        """Test institutional ownership change scoring."""
        scorer = BeforeTheCrowdScorer()
        assert scorer._score_institutional_change(12.0) == 20.0
        assert scorer._score_institutional_change(6.0) == 15.0
        assert scorer._score_institutional_change(4.0) == 10.0
        assert scorer._score_institutional_change(2.0) == 5.0
        assert scorer._score_institutional_change(0.5) == 2.5
        assert scorer._score_institutional_change(-2.0) == 0.0

    def test_score_earnings_trend(self) -> None:
        """Test earnings trend scoring."""
        scorer = BeforeTheCrowdScorer()
        assert scorer._score_earnings_trend("improving") == 15.0
        assert scorer._score_earnings_trend("stable") == 7.5
        assert scorer._score_earnings_trend("declining") == 0.0

    def test_score_order_book_trend(self) -> None:
        """Test order book trend scoring."""
        scorer = BeforeTheCrowdScorer()
        assert scorer._score_order_book_trend("increasing") == 15.0
        assert scorer._score_order_book_trend("stable") == 7.5
        assert scorer._score_order_book_trend("decreasing") == 0.0

    def test_score_technical_breakout(self) -> None:
        """Test technical breakout stage scoring."""
        scorer = BeforeTheCrowdScorer()
        assert scorer._score_technical_breakout("early") == 15.0
        assert scorer._score_technical_breakout("middle") == 7.5
        assert scorer._score_technical_breakout("late") == 0.0

    def test_score_valuation(self) -> None:
        """Test valuation scoring."""
        scorer = BeforeTheCrowdScorer()
        assert scorer._score_valuation(80.0) == 12.0
        assert scorer._score_valuation(50.0) == 7.5
        assert scorer._score_valuation(20.0) == 3.0

    def test_determine_signal(self) -> None:
        """Test signal determination."""
        scorer = BeforeTheCrowdScorer()
        assert scorer._determine_signal(75) == "early"
        assert scorer._determine_signal(50) == "neutral"
        assert scorer._determine_signal(25) == "late"

    def test_early_stage_stock(self) -> None:
        """Test scoring for early stage stock (before the crowd)."""
        scorer = BeforeTheCrowdScorer()
        factors = BeforeTheCrowdFactors(
            analyst_coverage=3,  # Low coverage
            institutional_ownership_change=10.0,  # Rising institutional
            earnings_trend="improving",
            order_book_trend="increasing",
            technical_breakout_stage="early",
            valuation_score=70.0,
        )
        score = scorer.calculate_before_crowd_score("RELIANCE", factors)
        assert score.overall_score >= 70
        assert score.before_crowd_signal == "early"

    def test_late_stage_stock(self) -> None:
        """Test scoring for late stage stock (after the crowd)."""
        scorer = BeforeTheCrowdScorer()
        factors = BeforeTheCrowdFactors(
            analyst_coverage=25,  # High coverage
            institutional_ownership_change=-5.0,  # Declining institutional
            earnings_trend="declining",
            order_book_trend="decreasing",
            technical_breakout_stage="late",
            valuation_score=30.0,
        )
        score = scorer.calculate_before_crowd_score("RELIANCE", factors)
        assert score.overall_score <= 30
        assert score.before_crowd_signal == "late"
