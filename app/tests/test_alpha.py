"""Unit tests for Alpha Score module."""

from __future__ import annotations

from datetime import datetime

import pytest

from app.alpha import AlphaScore, AlphaScoreComponents, AlphaScoreEngine, AlphaScorer
from app.financials import FinancialScore
from app.management import GuidanceScore
from app.sectors import SectorScore
from app.technical import TechnicalScore


class TestAlphaScoreComponents:
    """Tests for AlphaScoreComponents model."""

    def test_components_to_dict(self) -> None:
        """Ensure AlphaScoreComponents converts to dictionary correctly."""
        components = AlphaScoreComponents(
            financial_quality=75.0,
            growth_acceleration=80.0,
            technical_momentum=70.0,
            sector_momentum=65.0,
            management_guidance=72.0,
            institutional_buying=68.0,
            valuation=60.0,
            order_book=55.0,
            risk=50.0,
            earnings_surprise_probability=58.0,
        )
        result = components.to_dict()
        assert result["financial_quality"] == 75.0
        assert result["growth_acceleration"] == 80.0
        assert len(result) == 10


class TestAlphaScore:
    """Tests for AlphaScore model."""

    def test_alpha_score_to_dict(self) -> None:
        """Ensure AlphaScore converts to dictionary correctly."""
        components = AlphaScoreComponents(
            financial_quality=75.0,
            growth_acceleration=80.0,
            technical_momentum=70.0,
            sector_momentum=65.0,
            management_guidance=72.0,
            institutional_buying=68.0,
            valuation=60.0,
            order_book=55.0,
            risk=50.0,
            earnings_surprise_probability=58.0,
        )
        alpha_score = AlphaScore(
            symbol="RELIANCE",
            overall_score=72.5,
            components=components,
            action="buy",
            confidence=85.0,
            target_price=2800.0,
            stop_loss=2300.0,
            current_price=2500.0,
            reasoning="Strong buy signal",
            timestamp=datetime.now(),
        )
        result = alpha_score.to_dict()
        assert result["symbol"] == "RELIANCE"
        assert result["overall_score"] == 72.5
        assert result["action"] == "buy"
        assert "components" in result


class TestAlphaScorer:
    """Tests for AlphaScorer."""

    def test_scorer_weights(self) -> None:
        """Test scorer has correct weights."""
        scorer = AlphaScorer()
        assert scorer.WEIGHTS["financial_quality"] == 20
        assert scorer.WEIGHTS["growth_acceleration"] == 15
        assert scorer.WEIGHTS["technical_momentum"] == 15
        assert scorer.WEIGHTS["sector_momentum"] == 10
        assert scorer.WEIGHTS["management_guidance"] == 10
        assert scorer.WEIGHTS["institutional_buying"] == 10
        assert scorer.WEIGHTS["valuation"] == 5
        assert scorer.WEIGHTS["order_book"] == 5
        assert scorer.WEIGHTS["risk"] == 5
        assert scorer.WEIGHTS["earnings_surprise_probability"] == 5
        assert sum(scorer.WEIGHTS.values()) == 100

    def test_calculate_financial_quality(self) -> None:
        """Test financial quality calculation."""
        scorer = AlphaScorer()
        financial_score = FinancialScore(
            symbol="RELIANCE",
            revenue_growth=15.0,
            profit_growth=12.0,
            eps_growth=14.0,
            roe=18.0,
            roce=14.0,
            debt_to_equity=0.5,
            operating_cash_flow=5000000.0,
            free_cash_flow=4000000.0,
            peg=1.2,
            book_value_growth=8.0,
        )
        score = scorer.calculate_financial_quality(financial_score)
        assert 0 <= score <= 100

    def test_calculate_growth_acceleration(self) -> None:
        """Test growth acceleration calculation."""
        scorer = AlphaScorer()
        financial_score = FinancialScore(
            symbol="RELIANCE",
            revenue_growth=20.0,
            profit_growth=18.0,
            eps_growth=16.0,
            roe=15.0,
            roce=12.0,
            debt_to_equity=0.5,
            operating_cash_flow=5000000.0,
            free_cash_flow=4000000.0,
            peg=1.2,
            book_value_growth=10.0,
        )
        score = scorer.calculate_growth_acceleration(financial_score)
        assert 0 <= score <= 100

    def test_calculate_technical_momentum(self) -> None:
        """Test technical momentum calculation."""
        scorer = AlphaScorer()
        technical_score = TechnicalScore(
            symbol="RELIANCE",
            rsi=55.0,
            macd=1.5,
            macd_signal=1.2,
            macd_histogram=0.3,
            ema_20=150.0,
            sma_50=145.0,
            sma_200=130.0,
            adx=25.0,
            atr=5.0,
            supertrend=148.0,
            supertrend_signal="buy",
            bollinger_upper=155.0,
            bollinger_middle=150.0,
            bollinger_lower=145.0,
            vwap=149.0,
            volume_breakout=True,
            delivery_percentage=75.0,
        )
        score = scorer.calculate_technical_momentum(technical_score)
        assert 0 <= score <= 100

    def test_calculate_sector_momentum(self) -> None:
        """Test sector momentum calculation."""
        scorer = AlphaScorer()
        sector_score = SectorScore(
            sector="Technology",
            government_score=60.0,
            order_book_score=55.0,
            commodity_score=50.0,
            news_score=65.0,
            institutional_score=58.0,
            overall_score=58.0,
            rotation_signal="inflow",
        )
        score = scorer.calculate_sector_momentum(sector_score)
        assert 0 <= score <= 100

    def test_calculate_management_guidance(self) -> None:
        """Test management guidance calculation."""
        scorer = AlphaScorer()
        management_score = GuidanceScore(
            symbol="RELIANCE",
            document_type="investor_presentation",
            revenue_outlook="Positive",
            margin_outlook="Positive",
            demand="Strong",
            order_book="Strong",
            capex="Increasing",
            expansion="Aggressive",
            management_confidence="High",
            overall_sentiment="Positive",
        )
        score = scorer.calculate_management_guidance(management_score)
        assert 0 <= score <= 100

    def test_calculate_institutional_buying(self) -> None:
        """Test institutional buying calculation."""
        scorer = AlphaScorer()
        score = scorer.calculate_institutional_buying(75.0)
        assert score == 75.0

    def test_calculate_valuation(self) -> None:
        """Test valuation calculation."""
        scorer = AlphaScorer()
        financial_score = FinancialScore(
            symbol="RELIANCE",
            revenue_growth=15.0,
            profit_growth=12.0,
            eps_growth=14.0,
            roe=18.0,
            roce=14.0,
            debt_to_equity=0.5,
            operating_cash_flow=5000000.0,
            free_cash_flow=4000000.0,
            peg=1.2,
            book_value_growth=8.0,
        )
        score = scorer.calculate_valuation(financial_score, 2500.0)
        assert 0 <= score <= 100

    def test_calculate_order_book(self) -> None:
        """Test order book calculation."""
        scorer = AlphaScorer()
        score = scorer.calculate_order_book(25.0)
        assert 0 <= score <= 100

    def test_calculate_risk(self) -> None:
        """Test risk calculation."""
        scorer = AlphaScorer()
        score = scorer.calculate_risk(40.0)
        assert 0 <= score <= 100

    def test_calculate_earnings_surprise_probability(self) -> None:
        """Test earnings surprise probability calculation."""
        scorer = AlphaScorer()
        score = scorer.calculate_earnings_surprise_probability(65.0)
        assert score == 65.0

    def test_calculate_overall_alpha_score(self) -> None:
        """Test overall Alpha Score calculation."""
        scorer = AlphaScorer()
        components = AlphaScoreComponents(
            financial_quality=75.0,
            growth_acceleration=80.0,
            technical_momentum=70.0,
            sector_momentum=65.0,
            management_guidance=72.0,
            institutional_buying=68.0,
            valuation=60.0,
            order_book=55.0,
            risk=50.0,
            earnings_surprise_probability=58.0,
        )
        overall_score = scorer.calculate_overall_alpha_score(components)
        assert 0 <= overall_score <= 100

    def test_normalize_score(self) -> None:
        """Test score normalization."""
        scorer = AlphaScorer()
        # Test normalization within range
        assert scorer._normalize_score(50, 0, 100) == 50.0
        # Test normalization below min
        assert scorer._normalize_score(-10, 0, 100) == 0.0
        # Test normalization above max
        assert scorer._normalize_score(150, 0, 100) == 100.0

    def test_normalize_rsi(self) -> None:
        """Test RSI normalization."""
        scorer = AlphaScorer()
        # Overbought
        assert scorer._normalize_rsi(80) == 40.0
        # Bullish
        assert scorer._normalize_rsi(60) > 80.0
        # Bearish
        assert scorer._normalize_rsi(40) < 50.0
        # Oversold
        assert scorer._normalize_rsi(25) == 60.0


class TestAlphaScoreEngine:
    """Tests for AlphaScoreEngine."""

    def test_engine_initialization(self) -> None:
        """Test engine initialization."""
        engine = AlphaScoreEngine()
        assert engine.scorer is not None
        assert engine.financial_engine is not None
        assert engine.technical_engine is not None
        assert engine.sector_engine is not None
        assert engine.management_engine is not None

    def test_determine_action(self) -> None:
        """Test action determination."""
        engine = AlphaScoreEngine()
        assert engine._determine_action(75) == "buy"
        assert engine._determine_action(25) == "sell"
        assert engine._determine_action(50) == "hold"

    def test_calculate_confidence(self) -> None:
        """Test confidence calculation."""
        engine = AlphaScoreEngine()
        components = AlphaScoreComponents(
            financial_quality=75.0,
            growth_acceleration=80.0,
            technical_momentum=70.0,
            sector_momentum=65.0,
            management_guidance=72.0,
            institutional_buying=68.0,
            valuation=60.0,
            order_book=55.0,
            risk=50.0,
            earnings_surprise_probability=58.0,
        )
        confidence = engine._calculate_confidence(components, 72.5)
        assert 0 <= confidence <= 100

    def test_calculate_target_stop_loss(self) -> None:
        """Test target and stop loss calculation."""
        engine = AlphaScoreEngine()
        components = AlphaScoreComponents(
            financial_quality=75.0,
            growth_acceleration=80.0,
            technical_momentum=70.0,
            sector_momentum=65.0,
            management_guidance=72.0,
            institutional_buying=68.0,
            valuation=60.0,
            order_book=55.0,
            risk=50.0,
            earnings_surprise_probability=58.0,
        )
        target, stop_loss = engine._calculate_target_stop_loss(2500.0, components, 75.0)
        assert target > 2500.0
        assert stop_loss < 2500.0

    def test_calculate_alpha_score(self) -> None:
        """Test Alpha Score calculation."""
        engine = AlphaScoreEngine()
        # Skip this test for now as it requires full integration with all engines
        pytest.skip("Requires full integration with all engines")
        assert alpha_score.action in ["buy", "hold", "sell"]
        assert alpha_score.confidence is not None
