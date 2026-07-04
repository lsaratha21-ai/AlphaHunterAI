"""Unit tests for data connectors."""

from __future__ import annotations

from datetime import datetime

import pytest

from app.connectors import (
    CorporateAction,
    DocumentConnector,
    HoldingsConnector,
    NSEConnector,
    OHLCVData,
    ScreenerConnector,
    YahooFinanceConnector,
)
from app.core.exceptions import ProviderError


class TestOHLCVData:
    """Tests for OHLCVData model."""

    def test_ohlcv_data_to_dict(self) -> None:
        """Ensure OHLCVData converts to dictionary correctly."""
        data = OHLCVData(
            symbol="RELIANCE.NS",
            date=datetime.now(),
            open=2500.0,
            high=2550.0,
            low=2480.0,
            close=2520.0,
            volume=1000000,
            adjusted_close=2520.0,
        )
        result = data.to_dict()
        assert result["symbol"] == "RELIANCE.NS"
        assert result["open"] == 2500.0
        assert result["volume"] == 1000000


class TestCorporateAction:
    """Tests for CorporateAction model."""

    def test_corporate_action_to_dict(self) -> None:
        """Ensure CorporateAction converts to dictionary correctly."""
        action = CorporateAction(
            symbol="RELIANCE",
            action_type="dividend",
            announcement_date=datetime.now(),
            effective_date=datetime.now(),
            description="Dividend of Rs 10",
            amount=10.0,
        )
        result = action.to_dict()
        assert result["symbol"] == "RELIANCE"
        assert result["action_type"] == "dividend"
        assert result["amount"] == 10.0


class TestYahooFinanceConnector:
    """Tests for YahooFinanceConnector."""

    def test_connector_initialization(self) -> None:
        """Test connector initialization."""
        connector = YahooFinanceConnector()
        assert connector.timeout == 30
        assert connector.base_url == "https://query1.finance.yahoo.com"

    def test_fetch_ohlcv_data_sync_mock(self) -> None:
        """Test synchronous fetch with mock data."""
        connector = YahooFinanceConnector()
        pytest.skip("Requires API access or mocking setup")

    def test_fetch_ohlcv_data_invalid_symbol(self) -> None:
        """Test fetch with invalid symbol."""
        connector = YahooFinanceConnector()
        with pytest.raises(ProviderError):
            connector.fetch_ohlcv_data_sync("INVALID_SYMBOL_12345")


class TestNSEConnector:
    """Tests for NSEConnector."""

    def test_connector_initialization(self) -> None:
        """Test connector initialization."""
        connector = NSEConnector()
        assert connector.timeout == 30
        assert connector.base_url == "https://www.nseindia.com"

    def test_fetch_bhavcopy_sync_mock(self) -> None:
        """Test synchronous bhavcopy fetch."""
        connector = NSEConnector()
        pytest.skip("Requires API access or mocking setup")

    def test_fetch_corporate_actions_sync_mock(self) -> None:
        """Test synchronous corporate actions fetch."""
        connector = NSEConnector()
        pytest.skip("Requires API access or mocking setup")


class TestScreenerConnector:
    """Tests for ScreenerConnector."""

    def test_connector_initialization(self) -> None:
        """Test connector initialization."""
        connector = ScreenerConnector()
        assert connector.timeout == 30
        assert connector.base_url == "https://www.screener.in"

    def test_fetch_company_data_sync_mock(self) -> None:
        """Test synchronous company data fetch."""
        connector = ScreenerConnector()
        result = connector.fetch_company_data_sync("RELIANCE")
        assert result is not None
        assert "symbol" in result


class TestDocumentConnector:
    """Tests for DocumentConnector."""

    def test_connector_initialization(self) -> None:
        """Test connector initialization."""
        connector = DocumentConnector()
        assert connector.timeout == 30

    def test_fetch_investor_presentations_sync_mock(self) -> None:
        """Test synchronous investor presentations fetch."""
        connector = DocumentConnector()
        result = connector.fetch_investor_presentations_sync("RELIANCE")
        assert result is not None
        assert len(result) > 0

    def test_fetch_earnings_call_transcripts_sync_mock(self) -> None:
        """Test synchronous earnings call transcripts fetch."""
        connector = DocumentConnector()
        result = connector.fetch_earnings_call_transcripts_sync("RELIANCE")
        assert result is not None
        assert len(result) > 0


class TestHoldingsConnector:
    """Tests for HoldingsConnector."""

    def test_connector_initialization(self) -> None:
        """Test connector initialization."""
        connector = HoldingsConnector()
        assert connector.timeout == 30
        assert connector.base_url == "https://www.nseindia.com"

    def test_fetch_shareholding_pattern_sync_mock(self) -> None:
        """Test synchronous shareholding pattern fetch."""
        connector = HoldingsConnector()
        result = connector.fetch_shareholding_pattern_sync("RELIANCE")
        assert result is not None
        assert "symbol" in result
        assert "promoter_holding" in result

    def test_fetch_mutual_fund_holdings_sync_mock(self) -> None:
        """Test synchronous mutual fund holdings fetch."""
        connector = HoldingsConnector()
        result = connector.fetch_mutual_fund_holdings_sync("RELIANCE")
        assert result is not None
        assert "symbol" in result
        assert "total_mutual_fund_holding" in result

    def test_fetch_fii_dii_data_sync_mock(self) -> None:
        """Test synchronous FII/DII data fetch."""
        connector = HoldingsConnector()
        result = connector.fetch_fii_dii_data_sync()
        assert result is not None
        assert "fii" in result
        assert "dii" in result
