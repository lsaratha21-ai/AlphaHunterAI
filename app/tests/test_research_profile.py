"""Unit tests for Research Profile with component-level scoring."""

from __future__ import annotations

from datetime import datetime

import pytest

from app.alpha import ComponentScore, ResearchProfileEngine, ResearchScorer
from app.financials import FinancialScore
from app.management import GuidanceScore
from app.sectors import SectorScore
from app.technical import TechnicalScore


class TestComponentScore:
    """Tests for ComponentScore model."""

    def test_component_score_creation(self) -> None:
        """Test ComponentScore creation."""
        score = ComponentScore(
            name="Financial Quality",
            score=18.0,
            max_score=20.0,
            weight=20.0,
            details="ROE: 15.5%, ROCE: 14.2%",
        )
        assert score.name == "Financial Quality"
        assert score.score == 18.0
        assert score.max_score == 20.0
        assert score.weight == 20.0
        assert score.percentage == 90.0
        assert str(score) == "18.0/20.0"

    def test_component_score_percentage(self) -> None:
        """Test percentage calculation."""
        score = ComponentScore("Test", 15.0, 20.0, 10.0)
        assert score.percentage == 75.0

    def test_component_score_to_dict(self) -> None:
        """Test conversion to dictionary."""
        score = ComponentScore("Test", 15.0, 20.0, 10.0, "Details")
        # Note: ComponentScore doesn't have to_dict, but it's used in AlphaScoreComponents


class TestResearchScorer:
    """Tests for ResearchScorer."""

    def test_scorer_initialization(self) -> None:
        """Test scorer initialization."""
        scorer = ResearchScorer()
        assert scorer.MAX_SCORES["financial_quality"] == 20
        assert scorer.MAX_SCORES["growth_acceleration"] == 15
        assert scorer.WEIGHTS["financial_quality"] == 20

    def test_calculate_financial_quality(self) -> None:
        """Test financial quality calculation with component score."""
        scorer = ResearchScorer()
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
        component_score = scorer.calculate_financial_quality(financial_score)
        assert component_score.name == "Financial Quality"
        assert component_score.max_score == 20.0
        assert 0 <= component_score.score <= 20.0
        assert component_score.percentage >= 0
        assert component_score.percentage <= 100

    def test_calculate_growth_acceleration(self) -> None:
        """Test growth acceleration calculation with component score."""
        scorer = ResearchScorer()
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
        component_score = scorer.calculate_growth_acceleration(financial_score)
        assert component_score.name == "Growth Acceleration"
        assert component_score.max_score == 15.0
        assert 0 <= component_score.score <= 15.0

    def test_calculate_technical_momentum(self) -> None:
        """Test technical momentum calculation with component score."""
        scorer = ResearchScorer()
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
        component_score = scorer.calculate_technical_momentum(technical_score)
        assert component_score.name == "Technical Momentum"
        assert component_score.max_score == 15.0
        assert 0 <= component_score.score <= 15.0

    def test_calculate_sector_momentum(self) -> None:
        """Test sector momentum calculation with component score."""
        scorer = ResearchScorer()
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
        component_score = scorer.calculate_sector_momentum(sector_score)
        assert component_score.name == "Sector Momentum"
        assert component_score.max_score == 10.0
        assert 0 <= component_score.score <= 10.0

    def test_calculate_management_guidance(self) -> None:
        """Test management guidance calculation with component score."""
        scorer = ResearchScorer()
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
        component_score = scorer.calculate_management_guidance(management_score)
        assert component_score.name == "Management Guidance"
        assert component_score.max_score == 10.0
        assert 0 <= component_score.score <= 10.0

    def test_calculate_institutional_buying(self) -> None:
        """Test institutional buying calculation with component score."""
        scorer = ResearchScorer()
        component_score = scorer.calculate_institutional_buying(75.0)
        assert component_score.name == "Institutional Buying"
        assert component_score.max_score == 10.0
        assert 0 <= component_score.score <= 10.0

    def test_calculate_valuation(self) -> None:
        """Test valuation calculation with component score."""
        scorer = ResearchScorer()
        component_score = scorer.calculate_valuation(60.0)
        assert component_score.name == "Valuation"
        assert component_score.max_score == 5.0
        assert 0 <= component_score.score <= 5.0

    def test_calculate_order_book(self) -> None:
        """Test order book calculation with component score."""
        scorer = ResearchScorer()
        component_score = scorer.calculate_order_book(55.0)
        assert component_score.name == "Order Book"
        assert component_score.max_score == 5.0
        assert 0 <= component_score.score <= 5.0

    def test_calculate_risk(self) -> None:
        """Test risk calculation with component score."""
        scorer = ResearchScorer()
        component_score = scorer.calculate_risk(50.0)
        assert component_score.name == "Risk"
        assert component_score.max_score == 5.0
        assert 0 <= component_score.score <= 5.0

    def test_calculate_earnings_surprise_probability(self) -> None:
        """Test earnings surprise probability calculation with component score."""
        scorer = ResearchScorer()
        component_score = scorer.calculate_earnings_surprise_probability(58.0)
        assert component_score.name == "Earnings Surprise Probability"
        assert component_score.max_score == 5.0
        assert 0 <= component_score.score <= 5.0


class TestResearchProfileEngine:
    """Tests for ResearchProfileEngine."""

    def test_engine_initialization(self) -> None:
        """Test engine initialization."""
        engine = ResearchProfileEngine()
        assert engine.scorer is not None
        assert engine.financial_engine is not None

    def test_generate_research_profile(self) -> None:
        """Test research profile generation."""
        engine = ResearchProfileEngine()

        financial_data = {
            "symbol": "RELIANCE",
            "revenue_growth": 15.0,
            "profit_growth": 12.0,
            "eps_growth": 14.0,
            "roe": 18.0,
            "roce": 14.0,
            "debt_to_equity": 0.5,
            "operating_cash_flow": 5000000.0,
            "free_cash_flow": 4000000.0,
            "peg": 1.2,
            "book_value_growth": 8.0,
            "valuation_score": 60.0,
        }

        technical_data = {
            "symbol": "RELIANCE",
            "rsi": 55.0,
            "macd": 1.5,
            "macd_signal": 1.2,
            "macd_histogram": 0.3,
            "ema_20": 150.0,
            "sma_50": 145.0,
            "sma_200": 130.0,
            "adx": 25.0,
            "atr": 5.0,
            "supertrend": 148.0,
            "supertrend_signal": "buy",
            "bollinger_upper": 155.0,
            "bollinger_middle": 150.0,
            "bollinger_lower": 145.0,
            "vwap": 149.0,
            "volume_breakout": True,
            "delivery_percentage": 75.0,
        }

        sector_data = {
            "sector": "Technology",
            "government_score": 60.0,
            "order_book_score": 55.0,
            "commodity_score": 50.0,
            "news_score": 65.0,
            "institutional_score": 58.0,
            "overall_score": 58.0,
            "rotation_signal": "inflow",
        }

        management_data = {
            "symbol": "RELIANCE",
            "document_type": "investor_presentation",
            "revenue_outlook": "Positive",
            "margin_outlook": "Positive",
            "demand": "Strong",
            "order_book": "Strong",
            "capex": "Increasing",
            "expansion": "Aggressive",
            "management_confidence": "High",
            "overall_sentiment": "Positive",
        }

        profile = engine.generate_research_profile(
            symbol="RELIANCE",
            current_price=2500.0,
            financial_data=financial_data,
            technical_data=technical_data,
            sector_data=sector_data,
            management_data=management_data,
            institutional_score=68.0,
            order_book_score=55.0,
            risk_score=50.0,
            earnings_surprise_score=58.0,
        )

        assert profile.symbol == "RELIANCE"
        assert profile.current_price == 2500.0
        assert 0 <= profile.overall_score <= 100
        assert profile.action in ["buy", "hold", "sell"]
        assert profile.confidence is not None

        # Verify component scores have proper format
        assert profile.components.financial_quality.max_score == 20.0
        assert profile.components.growth_acceleration.max_score == 15.0
        assert profile.components.technical_momentum.max_score == 15.0
        assert profile.components.sector_momentum.max_score == 10.0
        assert profile.components.management_guidance.max_score == 10.0
        assert profile.components.institutional_buying.max_score == 10.0
        assert profile.components.valuation.max_score == 5.0
        assert profile.components.order_book.max_score == 5.0
        assert profile.components.risk.max_score == 5.0
        assert profile.components.earnings_surprise_probability.max_score == 5.0

    def test_determine_action(self) -> None:
        """Test action determination."""
        engine = ResearchProfileEngine()
        assert engine._determine_action(75) == "buy"
        assert engine._determine_action(25) == "sell"
        assert engine._determine_action(50) == "hold"

    def test_calculate_confidence(self) -> None:
        """Test confidence calculation."""
        engine = ResearchProfileEngine()
        # Test with mock components
        from app.alpha.models import AlphaScoreComponents

        components = AlphaScoreComponents(
            financial_quality=ComponentScore("Financial Quality", 18.0, 20.0, 20.0),
            growth_acceleration=ComponentScore("Growth Acceleration", 14.0, 15.0, 15.0),
            technical_momentum=ComponentScore("Technical Momentum", 13.0, 15.0, 15.0),
            sector_momentum=ComponentScore("Sector Momentum", 9.0, 10.0, 10.0),
            management_guidance=ComponentScore("Management Guidance", 9.0, 10.0, 10.0),
            institutional_buying=ComponentScore("Institutional Buying", 9.0, 10.0, 10.0),
            valuation=ComponentScore("Valuation", 4.0, 5.0, 5.0),
            order_book=ComponentScore("Order Book", 4.0, 5.0, 5.0),
            risk=ComponentScore("Risk", 4.0, 5.0, 5.0),
            earnings_surprise_probability=ComponentScore("Earnings Surprise Probability", 4.0, 5.0, 5.0),
        )

        confidence = engine._calculate_confidence(85.0, components)
        assert 0 <= confidence <= 100
