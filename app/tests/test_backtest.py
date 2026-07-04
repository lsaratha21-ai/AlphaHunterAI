"""Unit tests for backtracking functionality."""

from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from app.alpha import AlphaScore, AlphaScoreComponents, ComponentScore
from app.backtest import BacktestEngine, ExitRules, PerformanceMetrics, RecommendationTracker, RecommendationTracking


class TestExitRules:
    """Tests for ExitRules model."""

    def test_exit_rules_creation(self) -> None:
        """Test ExitRules creation."""
        rules = ExitRules(
            target_price=150.0,
            stop_loss=90.0,
            time_based_exit_days=180,
            stop_loss_percentage=10.0,
            target_percentage=20.0,
        )
        assert rules.target_price == 150.0
        assert rules.stop_loss == 90.0

    def test_exit_rules_to_dict(self) -> None:
        """Test ExitRules conversion to dictionary."""
        rules = ExitRules(target_price=150.0)
        result = rules.to_dict()
        assert result["target_price"] == 150.0


class TestPerformanceMetrics:
    """Tests for PerformanceMetrics model."""

    def test_performance_metrics_creation(self) -> None:
        """Test PerformanceMetrics creation."""
        metrics = PerformanceMetrics(
            return_1_month=5.5,
            return_3_month=12.3,
            return_6_month=18.7,
            max_drawdown=3.2,
            total_return=15.0,
            holding_period_days=90,
        )
        assert metrics.return_1_month == 5.5
        assert metrics.return_3_month == 12.3

    def test_performance_metrics_to_dict(self) -> None:
        """Test PerformanceMetrics conversion to dictionary."""
        metrics = PerformanceMetrics(return_1_month=5.5)
        result = metrics.to_dict()
        assert result["return_1_month"] == 5.5


class TestRecommendationTracking:
    """Tests for RecommendationTracking model."""

    def test_tracking_creation(self) -> None:
        """Test RecommendationTracking creation."""
        tracking = RecommendationTracking(
            id="REC-20240101120000",
            symbol="RELIANCE",
            alpha_score=85.0,
            recommendation_date=datetime.now(),
            entry_price=100.0,
        )
        assert tracking.symbol == "RELIANCE"
        assert tracking.alpha_score == 85.0

    def test_tracking_to_dict(self) -> None:
        """Test RecommendationTracking conversion to dictionary."""
        tracking = RecommendationTracking(
            id="REC-20240101120000",
            symbol="RELIANCE",
            alpha_score=85.0,
            recommendation_date=datetime.now(),
            entry_price=100.0,
        )
        result = tracking.to_dict()
        assert result["symbol"] == "RELIANCE"
        assert result["alpha_score"] == 85.0


class TestBacktestEngine:
    """Tests for BacktestEngine."""

    def test_engine_initialization(self) -> None:
        """Test engine initialization."""
        engine = BacktestEngine()
        assert engine is not None

    def test_calculate_return(self) -> None:
        """Test return calculation."""
        engine = BacktestEngine()
        entry_price = 100.0
        entry_date = datetime.now()
        price_history = {
            entry_date + timedelta(days=30): 105.0,
            entry_date + timedelta(days=90): 112.0,
            entry_date + timedelta(days=180): 118.0,
        }

        return_1_month = engine._calculate_return(entry_price, entry_date, price_history, 30)
        assert return_1_month == 5.0

    def test_calculate_max_drawdown(self) -> None:
        """Test maximum drawdown calculation."""
        engine = BacktestEngine()
        entry_price = 100.0
        entry_date = datetime.now()
        price_history = {
            entry_date: 100.0,
            entry_date + timedelta(days=10): 105.0,
            entry_date + timedelta(days=20): 95.0,
            entry_date + timedelta(days=30): 110.0,
        }

        max_dd, dd_date = engine._calculate_max_drawdown(entry_price, entry_date, price_history)
        assert max_dd is not None
        assert max_dd > 0

    def test_determine_exit_target_hit(self) -> None:
        """Test exit determination when target is hit."""
        engine = BacktestEngine()
        rules = ExitRules(target_price=110.0)
        tracking = RecommendationTracking(
            symbol="RELIANCE",
            alpha_score=85.0,
            recommendation_date=datetime.now(),
            entry_price=100.0,
            exit_rules=rules,
        )
        price_history = {
            tracking.recommendation_date + timedelta(days=10): 110.0,
        }

        exit_price, exit_date, exit_reason = engine._determine_exit(tracking, price_history)
        assert exit_price == 110.0
        assert exit_reason == "target_hit"

    def test_determine_exit_stop_loss(self) -> None:
        """Test exit determination when stop loss is hit."""
        engine = BacktestEngine()
        rules = ExitRules(stop_loss=95.0)
        tracking = RecommendationTracking(
            symbol="RELIANCE",
            alpha_score=85.0,
            recommendation_date=datetime.now(),
            entry_price=100.0,
            exit_rules=rules,
        )
        price_history = {
            tracking.recommendation_date + timedelta(days=5): 95.0,
        }

        exit_price, exit_date, exit_reason = engine._determine_exit(tracking, price_history)
        assert exit_price == 95.0
        assert exit_reason == "stop_loss"

    def test_calculate_performance(self) -> None:
        """Test full performance calculation."""
        engine = BacktestEngine()
        tracking = RecommendationTracking(
            symbol="RELIANCE",
            alpha_score=85.0,
            recommendation_date=datetime.now(),
            entry_price=100.0,
            exit_rules=ExitRules(target_price=110.0, stop_loss=95.0),
        )

        price_history = {
            tracking.recommendation_date: 100.0,
            tracking.recommendation_date + timedelta(days=30): 105.0,
            tracking.recommendation_date + timedelta(days=90): 112.0,
            tracking.recommendation_date + timedelta(days=180): 118.0,
            tracking.recommendation_date + timedelta(days=10): 95.0,  # Stop loss hit
        }

        performance = engine.calculate_performance(tracking, price_history)
        assert performance is not None
        assert performance.return_1_month is not None
        assert performance.max_drawdown is not None


class TestRecommendationTracker:
    """Tests for RecommendationTracker."""

    def test_tracker_initialization(self) -> None:
        """Test tracker initialization."""
        tracker = RecommendationTracker()
        assert tracker is not None
        assert tracker.recommendations == []

    def test_create_from_alpha_score(self) -> None:
        """Test creating tracking from AlphaScore."""
        tracker = RecommendationTracker()
        
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
        
        alpha_score = AlphaScore(
            symbol="RELIANCE",
            overall_score=85.0,
            components=components,
            action="buy",
            confidence=75.0,
            current_price=100.0,
            timestamp=datetime.now(),
        )

        tracking = tracker.create_from_alpha_score(alpha_score, entry_price=100.0)
        assert tracking.symbol == "RELIANCE"
        assert tracking.alpha_score == 85.0
        assert tracking.entry_price == 100.0
        assert tracking.id is not None

    def test_get_by_id(self) -> None:
        """Test getting recommendation by ID."""
        tracker = RecommendationTracker()
        
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
        
        alpha_score = AlphaScore(
            symbol="RELIANCE",
            overall_score=85.0,
            components=components,
            action="buy",
            confidence=75.0,
            current_price=100.0,
            timestamp=datetime.now(),
        )

        tracking = tracker.create_from_alpha_score(alpha_score, entry_price=100.0)
        retrieved = tracker.get_by_id(tracking.id)
        assert retrieved is not None
        assert retrieved.symbol == "RELIANCE"

    def test_get_by_symbol(self) -> None:
        """Test getting recommendations by symbol."""
        tracker = RecommendationTracker()
        
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
        
        alpha_score = AlphaScore(
            symbol="RELIANCE",
            overall_score=85.0,
            components=components,
            action="buy",
            confidence=75.0,
            current_price=100.0,
            timestamp=datetime.now(),
        )

        tracker.create_from_alpha_score(alpha_score, entry_price=100.0)
        recommendations = tracker.get_by_symbol("RELIANCE")
        assert len(recommendations) == 1
        assert recommendations[0].symbol == "RELIANCE"

    def test_get_active_recommendations(self) -> None:
        """Test getting active recommendations."""
        tracker = RecommendationTracker()
        
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
        
        alpha_score = AlphaScore(
            symbol="RELIANCE",
            overall_score=85.0,
            components=components,
            action="buy",
            confidence=75.0,
            current_price=100.0,
            timestamp=datetime.now(),
        )

        tracker.create_from_alpha_score(alpha_score, entry_price=100.0)
        active = tracker.get_active_recommendations()
        assert len(active) == 1

    def test_get_performance_summary(self) -> None:
        """Test getting performance summary."""
        tracker = RecommendationTracker()
        
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
        
        alpha_score = AlphaScore(
            symbol="RELIANCE",
            overall_score=85.0,
            components=components,
            action="buy",
            confidence=75.0,
            current_price=100.0,
            timestamp=datetime.now(),
        )

        tracker.create_from_alpha_score(alpha_score, entry_price=100.0)
        summary = tracker.get_performance_summary()
        assert summary is not None
        assert summary["total_recommendations"] == 1
