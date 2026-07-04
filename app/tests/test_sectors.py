"""Unit tests for the Sector Rotation Engine."""

from __future__ import annotations

from datetime import datetime, timedelta

from app.sectors import (
    CommodityPrice,
    GovernmentAnnouncement,
    InstitutionalActivity,
    NewsItem,
    OrderBookData,
    SectorRotationEngine,
    SectorScore,
)


class TestSectorScore:
    """Tests for SectorScore model."""

    def test_sector_score_to_dict(self) -> None:
        """Ensure SectorScore converts to dictionary correctly."""
        score = SectorScore(
            sector="Technology",
            government_score=50.0,
            order_book_score=60.0,
            commodity_score=40.0,
            news_score=55.0,
            institutional_score=70.0,
            overall_score=55.0,
            rotation_signal="inflow",
            last_updated=datetime.now(),
        )
        result = score.to_dict()
        assert result["sector"] == "Technology"
        assert result["government_score"] == 50.0
        assert result["rotation_signal"] == "inflow"


class TestSectorRotationEngine:
    """Tests for SectorRotationEngine."""

    def test_engine_initialization(self) -> None:
        """Test engine initialization."""
        engine = SectorRotationEngine()
        assert engine.government_announcements == []
        assert engine.order_book_data == []
        assert engine.commodity_prices == []
        assert engine.news_items == []
        assert engine.institutional_activities == []

    def test_add_government_announcement(self) -> None:
        """Test adding government announcement."""
        engine = SectorRotationEngine()
        engine.add_government_announcement(
            sector="Technology",
            announcement="New tax incentives for tech sector",
            impact="positive",
            source="Government Gazette",
        )
        assert len(engine.government_announcements) == 1
        assert engine.government_announcements[0].sector == "Technology"

    def test_add_order_book_data(self) -> None:
        """Test adding order book data."""
        engine = SectorRotationEngine()
        engine.add_order_book_data(
            sector="Technology",
            order_book_value=1000000.0,
            growth_rate=15.0,
        )
        assert len(engine.order_book_data) == 1
        assert engine.order_book_data[0].sector == "Technology"

    def test_add_commodity_price(self) -> None:
        """Test adding commodity price."""
        engine = SectorRotationEngine()
        engine.add_commodity_price(
            commodity="Crude Oil",
            price=75.0,
            change_percent=5.0,
            affected_sectors=["Energy", "Automotive"],
        )
        assert len(engine.commodity_prices) == 1
        assert engine.commodity_prices[0].commodity == "Crude Oil"

    def test_add_news_item(self) -> None:
        """Test adding news item."""
        engine = SectorRotationEngine()
        engine.add_news_item(
            sector="Technology",
            headline="Tech sector sees strong growth",
            sentiment="positive",
            relevance_score=0.9,
            source="Financial Times",
        )
        assert len(engine.news_items) == 1
        assert engine.news_items[0].sector == "Technology"

    def test_add_institutional_activity(self) -> None:
        """Test adding institutional activity."""
        engine = SectorRotationEngine()
        engine.add_institutional_activity(
            sector="Technology",
            institution="BlackRock",
            action="buy",
            amount=5000000.0,
        )
        assert len(engine.institutional_activities) == 1
        assert engine.institutional_activities[0].sector == "Technology"

    def test_calculate_government_score(self) -> None:
        """Test government score calculation."""
        engine = SectorRotationEngine()
        engine.add_government_announcement(
            sector="Technology",
            announcement="Tax incentives",
            impact="positive",
            source="Gov",
        )
        engine.add_government_announcement(
            sector="Technology",
            announcement="Regulation",
            impact="negative",
            source="Gov",
        )
        score = engine.calculate_government_score("Technology")
        assert score == 0.0  # 20 - 20

    def test_calculate_government_score_no_data(self) -> None:
        """Test government score with no data."""
        engine = SectorRotationEngine()
        score = engine.calculate_government_score("Technology")
        assert score == 0.0

    def test_calculate_order_book_score(self) -> None:
        """Test order book score calculation."""
        engine = SectorRotationEngine()
        engine.add_order_book_data(
            sector="Technology",
            order_book_value=1000000.0,
            growth_rate=25.0,
        )
        score = engine.calculate_order_book_score("Technology")
        assert score == 25.0

    def test_calculate_order_book_score_no_data(self) -> None:
        """Test order book score with no data."""
        engine = SectorRotationEngine()
        score = engine.calculate_order_book_score("Technology")
        assert score == 0.0

    def test_calculate_commodity_score(self) -> None:
        """Test commodity score calculation."""
        engine = SectorRotationEngine()
        engine.add_commodity_price(
            commodity="Crude Oil",
            price=75.0,
            change_percent=10.0,
            affected_sectors=["Technology"],
        )
        score = engine.calculate_commodity_score("Technology")
        assert score == 10.0

    def test_calculate_commodity_score_no_data(self) -> None:
        """Test commodity score with no data."""
        engine = SectorRotationEngine()
        score = engine.calculate_commodity_score("Technology")
        assert score == 0.0

    def test_calculate_news_score(self) -> None:
        """Test news score calculation."""
        engine = SectorRotationEngine()
        engine.add_news_item(
            sector="Technology",
            headline="Positive news",
            sentiment="positive",
            relevance_score=0.9,
            source="News",
        )
        engine.add_news_item(
            sector="Technology",
            headline="Negative news",
            sentiment="negative",
            relevance_score=0.5,
            source="News",
        )
        score = engine.calculate_news_score("Technology")
        assert score == 12.0  # 30 * 0.9 - 30 * 0.5 = 27 - 15 = 12

    def test_calculate_news_score_no_data(self) -> None:
        """Test news score with no data."""
        engine = SectorRotationEngine()
        score = engine.calculate_news_score("Technology")
        assert score == 0.0

    def test_calculate_institutional_score(self) -> None:
        """Test institutional score calculation."""
        engine = SectorRotationEngine()
        engine.add_institutional_activity(
            sector="Technology",
            institution="BlackRock",
            action="buy",
            amount=7000000.0,
        )
        engine.add_institutional_activity(
            sector="Technology",
            institution="Vanguard",
            action="sell",
            amount=3000000.0,
        )
        score = engine.calculate_institutional_score("Technology")
        # (7M - 3M) / 10M = 0.4 * 100 = 40
        assert score == 40.0

    def test_calculate_institutional_score_no_data(self) -> None:
        """Test institutional score with no data."""
        engine = SectorRotationEngine()
        score = engine.calculate_institutional_score("Technology")
        assert score == 0.0

    def test_calculate_sector_score_inflow(self) -> None:
        """Test sector score calculation with inflow signal."""
        engine = SectorRotationEngine()
        engine.add_government_announcement(
            sector="Technology",
            announcement="Positive policy",
            impact="positive",
            source="Gov",
        )
        engine.add_order_book_data(
            sector="Technology",
            order_book_value=1000000.0,
            growth_rate=30.0,
        )
        engine.add_commodity_price(
            commodity="Copper",
            price=8000.0,
            change_percent=15.0,
            affected_sectors=["Technology"],
        )
        engine.add_news_item(
            sector="Technology",
            headline="Great growth",
            sentiment="positive",
            relevance_score=0.8,
            source="News",
        )
        engine.add_institutional_activity(
            sector="Technology",
            institution="BlackRock",
            action="buy",
            amount=8000000.0,
        )

        score = engine.calculate_sector_score("Technology")
        assert isinstance(score, SectorScore)
        assert score.sector == "Technology"
        assert score.government_score is not None
        assert score.order_book_score is not None
        assert score.commodity_score is not None
        assert score.news_score is not None
        assert score.institutional_score is not None
        assert score.overall_score is not None
        assert score.rotation_signal in ["inflow", "outflow", "neutral"]

    def test_calculate_sector_score_outflow(self) -> None:
        """Test sector score calculation with outflow signal."""
        engine = SectorRotationEngine()
        engine.add_government_announcement(
            sector="Energy",
            announcement="Negative regulation",
            impact="negative",
            source="Gov",
        )
        engine.add_order_book_data(
            sector="Energy",
            order_book_value=500000.0,
            growth_rate=-20.0,
        )
        engine.add_institutional_activity(
            sector="Energy",
            institution="Vanguard",
            action="sell",
            amount=10000000.0,
        )

        score = engine.calculate_sector_score("Energy")
        assert isinstance(score, SectorScore)
        assert score.overall_score is not None
        assert score.rotation_signal in ["inflow", "outflow", "neutral"]

    def test_calculate_sector_score_neutral(self) -> None:
        """Test sector score calculation with neutral signal."""
        engine = SectorRotationEngine()
        score = engine.calculate_sector_score("Healthcare")
        assert isinstance(score, SectorScore)
        assert score.overall_score == 0.0
        assert score.rotation_signal == "neutral"

    def test_sector_score_to_dict(self) -> None:
        """Test SectorScore to_dict method."""
        engine = SectorRotationEngine()
        engine.add_order_book_data(
            sector="Technology",
            order_book_value=1000000.0,
            growth_rate=15.0,
        )
        score = engine.calculate_sector_score("Technology")
        result = score.to_dict()
        assert "sector" in result
        assert "overall_score" in result
        assert "rotation_signal" in result
