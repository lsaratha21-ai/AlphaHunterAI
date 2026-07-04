"""Unit tests for differentiating features."""

from __future__ import annotations

from datetime import datetime

import pytest

from app.differentiators import (
    CrowdSentiment,
    CrowdSentimentScorer,
    GuidanceAccuracyHistory,
    GuidanceAccuracyTracker,
    LLMGuidanceAnalyzer,
    ManagementGuidanceAnalysis,
    OrderBookQuality,
    OrderBookQualityScorer,
    SectorRotationEngine,
    SectorRotationRanking,
    SmartMoneyActivity,
    SmartMoneyTracker,
)


class TestManagementGuidanceAnalysis:
    """Tests for ManagementGuidanceAnalysis model."""

    def test_guidance_analysis_to_dict(self) -> None:
        """Ensure ManagementGuidanceAnalysis converts to dictionary correctly."""
        analysis = ManagementGuidanceAnalysis(
            symbol="RELIANCE",
            document_type="investor_presentation",
            overall_sentiment="positive",
            confidence_level=85.0,
            key_insights=["Strong growth", "Expansion plans"],
            risk_factors=["Regulatory risk", "Currency risk"],
            growth_indicators=["New products", "Market expansion"],
            management_credibility=75.0,
            guidance_score=80.0,
            timestamp=datetime.now(),
        )
        result = analysis.to_dict()
        assert result["symbol"] == "RELIANCE"
        assert result["overall_sentiment"] == "positive"
        assert len(result["key_insights"]) == 2


class TestLLMGuidanceAnalyzer:
    """Tests for LLMGuidanceAnalyzer."""

    def test_analyzer_initialization(self) -> None:
        """Test analyzer initialization."""
        analyzer = LLMGuidanceAnalyzer()
        assert analyzer.model_name == "gpt-4"

    def test_analyze_guidance_document_sync(self) -> None:
        """Test synchronous document analysis."""
        analyzer = LLMGuidanceAnalyzer()
        document_text = "We expect strong growth in the coming quarters with expansion into new markets. Our management is confident about achieving our targets."
        analysis = analyzer.analyze_guidance_document_sync(
            symbol="RELIANCE",
            document_text=document_text,
            document_type="investor_presentation",
        )
        assert analysis.symbol == "RELIANCE"
        assert 0 <= analysis.guidance_score <= 100
        assert analysis.overall_sentiment in ["positive", "neutral", "negative"]


class TestGuidanceAccuracyTracker:
    """Tests for GuidanceAccuracyTracker."""

    def test_tracker_initialization(self) -> None:
        """Test tracker initialization."""
        tracker = GuidanceAccuracyTracker()
        assert tracker.guidance_history is not None

    def test_record_guidance(self) -> None:
        """Test recording guidance data."""
        tracker = GuidanceAccuracyTracker()
        tracker.record_guidance(
            symbol="RELIANCE",
            guidance_type="revenue",
            guidance_value=1000.0,
            actual_value=1050.0,
            period="Q1 2024",
        )
        assert len(tracker.guidance_history["RELIANCE"]["revenue"]) == 1

    def test_calculate_accuracy_score(self) -> None:
        """Test calculating accuracy score."""
        tracker = GuidanceAccuracyTracker()
        tracker.record_guidance("RELIANCE", "revenue", 1000.0, 1050.0, "Q1 2024")
        tracker.record_guidance("RELIANCE", "revenue", 1100.0, 1120.0, "Q2 2024")
        tracker.record_guidance("RELIANCE", "revenue", 1200.0, 1180.0, "Q3 2024")
        tracker.record_guidance("RELIANCE", "revenue", 1300.0, 1350.0, "Q4 2024")

        accuracy = tracker.calculate_accuracy_score("RELIANCE", "revenue")
        assert accuracy.symbol == "RELIANCE"
        assert accuracy.total_guidance_periods == 4
        assert 0 <= accuracy.accuracy_score <= 100

    def test_insufficient_data(self) -> None:
        """Test accuracy score with insufficient data."""
        tracker = GuidanceAccuracyTracker()
        tracker.record_guidance("RELIANCE", "revenue", 1000.0, 1050.0, "Q1 2024")

        accuracy = tracker.calculate_accuracy_score("RELIANCE", "revenue")
        assert accuracy.accuracy_score == 50.0
        assert accuracy.recent_accuracy_trend == "insufficient_data"


class TestOrderBookQuality:
    """Tests for OrderBookQuality model."""

    def test_order_book_quality_to_dict(self) -> None:
        """Ensure OrderBookQuality converts to dictionary correctly."""
        quality = OrderBookQuality(
            symbol="RELIANCE",
            total_order_book=500000000.0,
            book_to_bill_ratio=1.2,
            order_concentration=30.0,
            margin_profile=18.0,
            order_book_trend="increasing",
            quality_score=75.0,
            timestamp=datetime.now(),
        )
        result = quality.to_dict()
        assert result["symbol"] == "RELIANCE"
        assert result["quality_score"] == 75.0


class TestOrderBookQualityScorer:
    """Tests for OrderBookQualityScorer."""

    def test_calculate_order_book_quality(self) -> None:
        """Test order book quality calculation."""
        scorer = OrderBookQualityScorer()
        quality = scorer.calculate_order_book_quality(
            symbol="RELIANCE",
            total_order_book=500000000.0,
            book_to_bill_ratio=1.2,
            order_concentration_data={"customer_a": 200000000.0, "customer_b": 150000000.0},
            margin_profile=18.0,
        )
        assert quality.symbol == "RELIANCE"
        assert 0 <= quality.quality_score <= 100

    def test_score_book_to_bill_ratio(self) -> None:
        """Test book-to-bill ratio scoring."""
        scorer = OrderBookQualityScorer()
        assert scorer._score_book_to_bill_ratio(1.5) > 90
        assert scorer._score_book_to_bill_ratio(1.0) > 60
        assert scorer._score_book_to_bill_ratio(0.8) < 50


class TestSectorRotationRanking:
    """Tests for SectorRotationRanking model."""

    def test_sector_ranking_to_dict(self) -> None:
        """Ensure SectorRotationRanking converts to dictionary correctly."""
        ranking = SectorRotationRanking(
            sector="Technology",
            rank=1,
            total_sectors=12,
            momentum_score=85.0,
            inflow_outflow=500.0,
            relative_strength=75.0,
            rotation_signal="inflow",
            week_ending=datetime.now(),
        )
        result = ranking.to_dict()
        assert result["sector"] == "Technology"
        assert result["rank"] == 1


class TestSectorRotationEngine:
    """Tests for SectorRotationEngine."""

    def test_engine_initialization(self) -> None:
        """Test engine initialization."""
        engine = SectorRotationEngine()
        assert len(engine.sectors) == 12
        assert engine.historical_rankings == []

    def test_calculate_weekly_rankings(self) -> None:
        """Test weekly ranking calculation."""
        engine = SectorRotationEngine()
        sector_data = {
            "Technology": {"price_change": 15.0, "inflow_outflow": 500.0},
            "Financials": {"price_change": 5.0, "inflow_outflow": -200.0},
            "Healthcare": {"price_change": 8.0, "inflow_outflow": 100.0},
        }
        rankings = engine.calculate_weekly_rankings(sector_data)
        assert len(rankings) == 12
        assert rankings[0].rank == 1
        assert all(0 <= r.momentum_score <= 100 for r in rankings)

    def test_get_top_sectors(self) -> None:
        """Test getting top sectors."""
        engine = SectorRotationEngine()
        sector_data = {
            "Technology": {"price_change": 15.0, "inflow_outflow": 500.0},
            "Financials": {"price_change": 5.0, "inflow_outflow": -200.0},
        }
        engine.calculate_weekly_rankings(sector_data)
        top_sectors = engine.get_top_sectors(n=2)
        assert len(top_sectors) == 2


class TestSmartMoneyActivity:
    """Tests for SmartMoneyActivity model."""

    def test_smart_money_activity_to_dict(self) -> None:
        """Ensure SmartMoneyActivity converts to dictionary correctly."""
        activity = SmartMoneyActivity(
            symbol="RELIANCE",
            promoter_buying=80.0,
            promoter_selling=20.0,
            fii_dii_change=5.0,
            mutual_fund_ownership_change=3.0,
            block_deal_activity=70.0,
            insider_confidence=85.0,
            smart_money_score=75.0,
            signal="bullish",
            timestamp=datetime.now(),
        )
        result = activity.to_dict()
        assert result["symbol"] == "RELIANCE"
        assert result["signal"] == "bullish"


class TestSmartMoneyTracker:
    """Tests for SmartMoneyTracker."""

    def test_calculate_smart_money_score(self) -> None:
        """Test smart money score calculation."""
        tracker = SmartMoneyTracker()
        activity = tracker.calculate_smart_money_score(
            symbol="RELIANCE",
            promoter_data={"buying_percentage": 3.0, "selling_percentage": 0.5},
            fii_dii_data={"change_percentage": 5.0},
            mutual_fund_data={"change_percentage": 3.0, "ownership_percentage": 10.0},
            block_deal_data={"deal_type": "bulk_buy", "deal_value": 50000000.0},
        )
        assert activity.symbol == "RELIANCE"
        assert 0 <= activity.smart_money_score <= 100
        assert activity.signal in ["bullish", "bearish", "neutral"]


class TestCrowdSentiment:
    """Tests for CrowdSentiment model."""

    def test_crowd_sentiment_to_dict(self) -> None:
        """Ensure CrowdSentiment converts to dictionary correctly."""
        sentiment = CrowdSentiment(
            symbol="RELIANCE",
            social_media_mentions=5000,
            news_volume=25,
            retail_interest=70.0,
            analyst_coverage=15,
            popularity_score=75.0,
            crowd_score=25.0,
            sentiment_signal="overheated",
            timestamp=datetime.now(),
        )
        result = sentiment.to_dict()
        assert result["symbol"] == "RELIANCE"
        assert result["sentiment_signal"] == "overheated"


class TestCrowdSentimentScorer:
    """Tests for CrowdSentimentScorer."""

    def test_calculate_crowd_score(self) -> None:
        """Test crowd score calculation."""
        scorer = CrowdSentimentScorer()
        sentiment = scorer.calculate_crowd_score(
            symbol="RELIANCE",
            social_media_mentions=5000,
            news_volume=25,
            retail_interest=70.0,
            analyst_coverage=15,
        )
        assert sentiment.symbol == "RELIANCE"
        assert 0 <= sentiment.crowd_score <= 100
        assert sentiment.sentiment_signal in ["overheated", "normal", "contrarian"]

    def test_popularity_scoring(self) -> None:
        """Test popularity score calculation."""
        scorer = CrowdSentimentScorer()
        popularity = scorer._calculate_popularity_score(
            social_media_mentions=5000,
            news_volume=25,
            retail_interest=70.0,
            analyst_coverage=15,
        )
        assert 0 <= popularity <= 100

    def test_crowd_score_inverse(self) -> None:
        """Test that crowd score is inverse of popularity."""
        scorer = CrowdSentimentScorer()
        popularity = 80.0
        crowd_score = scorer._calculate_crowd_score(popularity)
        assert crowd_score == 20.0
