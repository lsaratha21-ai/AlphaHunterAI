"""Unit tests for the AI Recommendation Engine."""

from __future__ import annotations

from datetime import datetime

from app.financials import FinancialScore
from app.recommendation import Recommendation, RecommendationEngine
from app.sectors import SectorScore
from app.technical import TechnicalScore


class TestRecommendation:
    """Tests for Recommendation model."""

    def test_recommendation_to_dict(self) -> None:
        """Ensure Recommendation converts to dictionary correctly."""
        rec = Recommendation(
            symbol="AAPL",
            overall_score=75.0,
            action="buy",
            confidence=85.0,
            target_price=175.0,
            stop_loss=145.0,
            current_price=150.0,
            reasoning="Strong buy recommendation",
            timestamp=datetime.now(),
            financial_score=80.0,
            technical_score=75.0,
        )
        result = rec.to_dict()
        assert result["symbol"] == "AAPL"
        assert result["overall_score"] == 75.0
        assert result["action"] == "buy"


class TestRecommendationEngine:
    """Tests for RecommendationEngine."""

    def test_engine_initialization(self) -> None:
        """Test engine initialization."""
        engine = RecommendationEngine()
        assert engine.weights["financial"] == 0.25
        assert engine.weights["technical"] == 0.20

    def test_calculate_financial_score_positive(self) -> None:
        """Test financial score calculation with positive metrics."""
        engine = RecommendationEngine()
        financial = FinancialScore(
            symbol="AAPL",
            revenue_growth=25.0,
            profit_growth=30.0,
            roe=22.0,
            debt_to_equity=0.3,
        )
        score = engine.calculate_financial_score(financial)
        assert score > 50  # Should be above base score

    def test_calculate_financial_score_negative(self) -> None:
        """Test financial score calculation with negative metrics."""
        engine = RecommendationEngine()
        financial = FinancialScore(
            symbol="LOSS",
            revenue_growth=-10.0,
            profit_growth=-15.0,
            roe=5.0,
            debt_to_equity=2.5,
        )
        score = engine.calculate_financial_score(financial)
        assert score < 50  # Should be below base score

    def test_calculate_financial_score_none(self) -> None:
        """Test financial score with no data."""
        engine = RecommendationEngine()
        financial = FinancialScore(symbol="AAPL")
        score = engine.calculate_financial_score(financial)
        assert score == 50.0  # Base score

    def test_calculate_technical_score_positive(self) -> None:
        """Test technical score calculation with positive indicators."""
        engine = RecommendationEngine()
        technical = TechnicalScore(
            symbol="AAPL",
            rsi=25.0,  # Oversold
            macd=1.5,
            macd_signal=1.0,
            ema_20=155.0,
            sma_50=150.0,
            volume_breakout=True,
        )
        score = engine.calculate_technical_score(technical)
        assert score > 50

    def test_calculate_technical_score_negative(self) -> None:
        """Test technical score calculation with negative indicators."""
        engine = RecommendationEngine()
        technical = TechnicalScore(
            symbol="AAPL",
            rsi=75.0,  # Overbought
            macd=-1.0,
            macd_signal=0.5,
            ema_20=145.0,
            sma_50=150.0,
        )
        score = engine.calculate_technical_score(technical)
        assert score < 50

    def test_calculate_technical_score_none(self) -> None:
        """Test technical score with no data."""
        engine = RecommendationEngine()
        technical = TechnicalScore(symbol="AAPL")
        score = engine.calculate_technical_score(technical)
        assert score == 50.0

    def test_calculate_sector_score(self) -> None:
        """Test sector score calculation."""
        engine = RecommendationEngine()
        sector = SectorScore(
            sector="Technology",
            overall_score=50.0,  # Mid-range
            rotation_signal="neutral",
        )
        score = engine.calculate_sector_score(sector)
        assert score == 75.0  # (50 + 100) / 2 = 75

    def test_calculate_sector_score_negative(self) -> None:
        """Test sector score with negative overall score."""
        engine = RecommendationEngine()
        sector = SectorScore(
            sector="Energy",
            overall_score=-50.0,
            rotation_signal="outflow",
        )
        score = engine.calculate_sector_score(sector)
        assert score == 25.0  # (-50 + 100) / 2 = 25

    def test_calculate_guidance_score(self) -> None:
        """Test guidance score calculation."""
        engine = RecommendationEngine()
        assert engine.calculate_guidance_score("positive") == 75.0
        assert engine.calculate_guidance_score("neutral") == 50.0
        assert engine.calculate_guidance_score("negative") == 25.0

    def test_calculate_valuation_score(self) -> None:
        """Test valuation score calculation."""
        engine = RecommendationEngine()
        # Low P/E and PEG should give high score
        score = engine.calculate_valuation_score(pe_ratio=12.0, peg_ratio=0.8)
        assert score > 50

        # High P/E and PEG should give low score
        score = engine.calculate_valuation_score(pe_ratio=45.0, peg_ratio=2.5)
        assert score < 50

    def test_calculate_institutional_score(self) -> None:
        """Test institutional score calculation."""
        engine = RecommendationEngine()
        # Positive institutional flow
        score = engine.calculate_institutional_score(50.0)
        assert score == 75.0  # (50 + 100) / 2

        # Negative institutional flow
        score = engine.calculate_institutional_score(-50.0)
        assert score == 25.0  # (-50 + 100) / 2

    def test_calculate_news_score(self) -> None:
        """Test news score calculation."""
        engine = RecommendationEngine()
        assert engine.calculate_news_score("positive") == 75.0
        assert engine.calculate_news_score("neutral") == 50.0
        assert engine.calculate_news_score("negative") == 25.0

    def test_calculate_risk_score(self) -> None:
        """Test risk score calculation."""
        engine = RecommendationEngine()
        # Low volatility and beta should give high score (low risk)
        score = engine.calculate_risk_score(volatility=15.0, beta=0.8)
        assert score > 50

        # High volatility and beta should give low score (high risk)
        score = engine.calculate_risk_score(volatility=45.0, beta=1.8)
        assert score < 50

    def test_calculate_overall_score(self) -> None:
        """Test overall score calculation."""
        engine = RecommendationEngine()
        overall = engine.calculate_overall_score(
            financial_score=80.0,
            technical_score=75.0,
            sector_score=70.0,
            guidance_score=75.0,
            valuation_score=70.0,
            institutional_score=75.0,
            news_score=75.0,
            risk_score=70.0,
        )
        assert 0 <= overall <= 100
        assert overall > 50  # Should be above average

    def test_determine_action_buy(self) -> None:
        """Test action determination for buy."""
        engine = RecommendationEngine()
        assert engine.determine_action(75.0) == "buy"
        assert engine.determine_action(70.0) == "buy"

    def test_determine_action_sell(self) -> None:
        """Test action determination for sell."""
        engine = RecommendationEngine()
        assert engine.determine_action(25.0) == "sell"
        assert engine.determine_action(30.0) == "sell"

    def test_determine_action_hold(self) -> None:
        """Test action determination for hold."""
        engine = RecommendationEngine()
        assert engine.determine_action(50.0) == "hold"
        assert engine.determine_action(60.0) == "hold"
        assert engine.determine_action(40.0) == "hold"

    def test_calculate_confidence(self) -> None:
        """Test confidence calculation."""
        engine = RecommendationEngine()
        confidence = engine.calculate_confidence(overall_score=80.0, data_completeness=0.8)
        assert 0 <= confidence <= 100

    def test_calculate_target_and_stop_loss_buy(self) -> None:
        """Test target and stop loss calculation for buy."""
        engine = RecommendationEngine()
        target, stop_loss = engine.calculate_target_and_stop_loss(
            current_price=150.0,
            action="buy",
            overall_score=75.0,
            volatility=20.0,
        )
        assert target is not None
        assert target > 150.0  # Target should be above current price
        assert stop_loss is not None
        assert stop_loss < 150.0  # Stop loss should be below current price

    def test_calculate_target_and_stop_loss_sell(self) -> None:
        """Test target and stop loss calculation for sell."""
        engine = RecommendationEngine()
        target, stop_loss = engine.calculate_target_and_stop_loss(
            current_price=150.0,
            action="sell",
            overall_score=25.0,
            volatility=20.0,
        )
        assert target is not None
        assert target < 150.0  # Target should be below current price
        assert stop_loss is not None
        assert stop_loss > 150.0  # Stop loss should be above current price

    def test_calculate_target_and_stop_loss_hold(self) -> None:
        """Test target and stop loss calculation for hold."""
        engine = RecommendationEngine()
        target, stop_loss = engine.calculate_target_and_stop_loss(
            current_price=150.0,
            action="hold",
            overall_score=50.0,
        )
        assert target is None
        assert stop_loss is None

    def test_generate_reasoning_buy(self) -> None:
        """Test reasoning generation for buy."""
        engine = RecommendationEngine()
        reasoning = engine.generate_reasoning(
            overall_score=75.0,
            action="buy",
            financial_score=80.0,
            technical_score=75.0,
            sector_score=70.0,
        )
        assert "buy" in reasoning.lower()
        assert "75.0" in reasoning

    def test_generate_reasoning_sell(self) -> None:
        """Test reasoning generation for sell."""
        engine = RecommendationEngine()
        reasoning = engine.generate_reasoning(
            overall_score=25.0,
            action="sell",
            financial_score=30.0,
            technical_score=25.0,
            sector_score=35.0,
        )
        assert "sell" in reasoning.lower()

    def test_generate_recommendation_buy(self) -> None:
        """Test full recommendation generation for buy."""
        engine = RecommendationEngine()
        financial = FinancialScore(
            symbol="AAPL",
            revenue_growth=25.0,
            profit_growth=30.0,
            roe=22.0,
            debt_to_equity=0.3,
        )
        technical = TechnicalScore(
            symbol="AAPL",
            rsi=25.0,
            ema_20=155.0,
            sma_50=150.0,
            volume_breakout=True,
        )
        sector = SectorScore(
            sector="Technology",
            overall_score=50.0,
            rotation_signal="neutral",
        )

        rec = engine.generate_recommendation(
            symbol="AAPL",
            current_price=150.0,
            financial_score=financial,
            technical_score=technical,
            sector_score=sector,
            guidance_sentiment="positive",
            pe_ratio=15.0,
            peg_ratio=1.2,
            institutional_activity=50.0,
            news_sentiment="positive",
            volatility=20.0,
            beta=1.0,
        )

        assert isinstance(rec, Recommendation)
        assert rec.symbol == "AAPL"
        assert rec.overall_score > 50
        assert rec.action == "buy"
        assert rec.target_price is not None
        assert rec.stop_loss is not None
        assert rec.reasoning is not None

    def test_generate_recommendation_sell(self) -> None:
        """Test full recommendation generation for sell."""
        engine = RecommendationEngine()
        financial = FinancialScore(
            symbol="LOSS",
            revenue_growth=-10.0,
            profit_growth=-15.0,
            roe=5.0,
            debt_to_equity=2.5,
        )
        technical = TechnicalScore(
            symbol="LOSS",
            rsi=75.0,
            ema_20=145.0,
            sma_50=150.0,
        )

        rec = engine.generate_recommendation(
            symbol="LOSS",
            current_price=150.0,
            financial_score=financial,
            technical_score=technical,
            guidance_sentiment="negative",
            pe_ratio=45.0,
            peg_ratio=2.5,
            institutional_activity=-50.0,
            news_sentiment="negative",
            volatility=45.0,
            beta=1.8,
        )

        assert isinstance(rec, Recommendation)
        assert rec.overall_score < 50
        assert rec.action == "sell"

    def test_generate_recommendation_minimal_data(self) -> None:
        """Test recommendation with minimal data."""
        engine = RecommendationEngine()
        rec = engine.generate_recommendation(
            symbol="TEST",
            current_price=100.0,
        )

        assert isinstance(rec, Recommendation)
        assert rec.symbol == "TEST"
        assert rec.overall_score is not None
        assert rec.action in ["buy", "hold", "sell"]
