"""Unit tests for SmallCapScreener."""

from __future__ import annotations

from datetime import datetime

import pytest

from app.screeners import SmallCapScreener, SmallCapScreenerResult


class TestSmallCapScreener:
    """Tests for SmallCapScreener."""

    def test_screener_initialization(self) -> None:
        """Test screener initialization."""
        screener = SmallCapScreener()
        assert screener.max_market_cap == 2000000000
        assert screener.max_debt_to_equity == 1.0
        assert screener.min_roe == 10.0

    def test_screen_small_cap_companies(self) -> None:
        """Test screening small-cap companies."""
        screener = SmallCapScreener()

        companies = [
            {
                "symbol": "ABC",
                "company_name": "ABC Technologies",
                "market_cap": 1500000000,
                "roe": 15.5,
                "debt_to_equity": 0.4,
                "institutional_ownership": 25.0,
            },
            {
                "symbol": "XYZ",
                "company_name": "XYZ Manufacturing",
                "market_cap": 800000000,
                "roe": 18.2,
                "debt_to_equity": 0.3,
                "institutional_ownership": 30.0,
            },
        ]

        historical_data = {
            "ABC": {
                "roe_history": [12.0, 13.5, 14.8, 15.5],
                "institutional_ownership_history": [20.0, 22.0, 24.0, 25.0],
            },
            "XYZ": {
                "roe_history": [15.0, 16.5, 17.2, 18.2],
                "institutional_ownership_history": [25.0, 27.0, 29.0, 30.0],
            },
        }

        results = screener.screen_small_cap_companies(companies, historical_data)

        assert len(results) == 2
        assert results[0].symbol in ["ABC", "XYZ"]
        assert all(r.overall_score > 0 for r in results)

    def test_filters_large_cap(self) -> None:
        """Test that large-cap companies are filtered out."""
        screener = SmallCapScreener()

        companies = [
            {
                "symbol": "DEF",
                "company_name": "DEF Services",
                "market_cap": 2500000000,  # Too large
                "roe": 20.0,
                "debt_to_equity": 0.5,
                "institutional_ownership": 35.0,
            },
        ]

        results = screener.screen_small_cap_companies(companies)
        assert len(results) == 0

    def test_filters_high_debt(self) -> None:
        """Test that high debt companies are filtered out."""
        screener = SmallCapScreener()

        companies = [
            {
                "symbol": "JKL",
                "company_name": "JKL Corporation",
                "market_cap": 1800000000,
                "roe": 16.0,
                "debt_to_equity": 1.5,  # Too high
                "institutional_ownership": 28.0,
            },
        ]

        results = screener.screen_small_cap_companies(companies)
        assert len(results) == 0

    def test_filters_low_roe(self) -> None:
        """Test that low ROE companies are filtered out."""
        screener = SmallCapScreener()

        companies = [
            {
                "symbol": "GHI",
                "company_name": "GHI Industries",
                "market_cap": 1200000000,
                "roe": 8.0,  # Too low
                "debt_to_equity": 0.4,
                "institutional_ownership": 20.0,
            },
        ]

        results = screener.screen_small_cap_companies(companies)
        assert len(results) == 0

    def test_filters_declining_roe(self) -> None:
        """Test that declining ROE companies are filtered out."""
        screener = SmallCapScreener()

        companies = [
            {
                "symbol": "ABC",
                "company_name": "ABC Technologies",
                "market_cap": 1500000000,
                "roe": 15.5,
                "debt_to_equity": 0.4,
                "institutional_ownership": 25.0,
            },
        ]

        historical_data = {
            "ABC": {
                "roe_history": [18.0, 17.0, 16.0, 15.5],  # Declining
                "institutional_ownership_history": [25.0, 26.0, 27.0, 28.0],
            },
        }

        results = screener.screen_small_cap_companies(companies, historical_data)
        assert len(results) == 0

    def test_filters_decreasing_institutional(self) -> None:
        """Test that decreasing institutional ownership is filtered out."""
        screener = SmallCapScreener()

        companies = [
            {
                "symbol": "ABC",
                "company_name": "ABC Technologies",
                "market_cap": 1500000000,
                "roe": 15.5,
                "debt_to_equity": 0.4,
                "institutional_ownership": 25.0,
            },
        ]

        historical_data = {
            "ABC": {
                "roe_history": [12.0, 13.5, 14.8, 15.5],
                "institutional_ownership_history": [30.0, 28.0, 26.0, 25.0],  # Decreasing
            },
        }

        results = screener.screen_small_cap_companies(companies, historical_data)
        assert len(results) == 0

    def test_calculate_roe_trend(self) -> None:
        """Test ROE trend calculation."""
        screener = SmallCapScreener()

        # Improving trend
        assert screener._calculate_roe_trend("ABC", [12.0, 13.5, 14.8, 15.5]) == "improving"

        # Declining trend
        assert screener._calculate_roe_trend("ABC", [18.0, 17.0, 16.0, 15.5]) == "declining"

        # Stable trend
        assert screener._calculate_roe_trend("ABC", [15.0, 15.2, 14.8, 15.1]) == "stable"

    def test_calculate_institutional_trend(self) -> None:
        """Test institutional ownership trend calculation."""
        screener = SmallCapScreener()

        # Increasing trend
        assert screener._calculate_institutional_trend("ABC", [20.0, 22.0, 24.0, 25.0]) == "increasing"

        # Decreasing trend
        assert screener._calculate_institutional_trend("ABC", [30.0, 28.0, 26.0, 25.0]) == "decreasing"

        # Stable trend
        assert screener._calculate_institutional_trend("ABC", [25.0, 25.2, 24.8, 25.1]) == "stable"

    def test_get_screening_summary(self) -> None:
        """Test screening summary calculation."""
        screener = SmallCapScreener()

        results = [
            SmallCapScreenerResult(
                symbol="ABC",
                company_name="ABC Technologies",
                market_cap=1500000000,
                current_roe=15.5,
                roe_trend="improving",
                debt_to_equity=0.4,
                institutional_ownership=25.0,
                institutional_trend="increasing",
                overall_score=75.0,
                timestamp=None,
            ),
            SmallCapScreenerResult(
                symbol="XYZ",
                company_name="XYZ Manufacturing",
                market_cap=800000000,
                current_roe=18.2,
                roe_trend="improving",
                debt_to_equity=0.3,
                institutional_ownership=30.0,
                institutional_trend="increasing",
                overall_score=80.0,
                timestamp=None,
            ),
        ]

        summary = screener.get_screening_summary(results)
        assert summary["total_companies"] == 2
        assert summary["average_roe"] == 16.85
        assert summary["average_score"] == 77.5

    def test_result_to_dict(self) -> None:
        """Test SmallCapScreenerResult conversion to dictionary."""
        result = SmallCapScreenerResult(
            symbol="ABC",
            company_name="ABC Technologies",
            market_cap=1500000000,
            current_roe=15.5,
            roe_trend="improving",
            debt_to_equity=0.4,
            institutional_ownership=25.0,
            institutional_trend="increasing",
            overall_score=75.0,
            timestamp=datetime.now(),
        )

        result_dict = result.to_dict()
        assert result_dict["symbol"] == "ABC"
        assert result_dict["current_roe"] == 15.5
        assert result_dict["roe_trend"] == "improving"
