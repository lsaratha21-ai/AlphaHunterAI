"""Unit tests for data providers."""

from __future__ import annotations

import pytest
from pytest_mock import MockerFixture

from app.core import ProviderError, ValidationError
from app.providers import (
    ManualCSVProvider,
    ManualCSVProviderConfig,
    NSEProvider,
    NSEProviderConfig,
    ProviderFactory,
    ScreenerProvider,
    ScreenerProviderConfig,
    StockData,
    YahooFinanceProvider,
    YahooFinanceProviderConfig,
)


class TestStockData:
    """Tests for StockData model."""

    def test_stock_data_to_dict(self) -> None:
        """Ensure StockData converts to dictionary correctly."""
        data = StockData(
            symbol="AAPL",
            name="Apple Inc",
            price=150.0,
            market_cap=2500000000000.0,
            pe_ratio=25.0,
            debt_to_equity=0.3,
            revenue_growth=10.0,
            earnings_growth=15.0,
            promoter_holdings=60.0,
            sector="Technology",
        )
        result = data.to_dict()
        assert result["symbol"] == "AAPL"
        assert result["name"] == "Apple Inc"
        assert result["price"] == 150.0
        assert result["market_cap"] == 2500000000000.0


class TestYahooFinanceProvider:
    """Tests for YahooFinanceProvider."""

    @pytest.mark.asyncio
    async def test_fetch_stock_data(self) -> None:
        """Test fetching single stock data."""
        provider = YahooFinanceProvider()
        data = await provider.fetch_stock_data("AAPL")
        assert isinstance(data, StockData)
        assert data.symbol == "AAPL"
        assert data.price == 100.0

    @pytest.mark.asyncio
    async def test_fetch_multiple_stocks(self) -> None:
        """Test fetching multiple stocks."""
        provider = YahooFinanceProvider()
        data = await provider.fetch_multiple_stocks(["AAPL", "GOOGL"])
        assert len(data) == 2
        assert all(isinstance(d, StockData) for d in data)

    def test_provider_name(self) -> None:
        """Test provider name property."""
        provider = YahooFinanceProvider()
        assert provider.provider_name == "Yahoo Finance"


class TestNSEProvider:
    """Tests for NSEProvider."""

    @pytest.mark.asyncio
    async def test_fetch_stock_data(self) -> None:
        """Test fetching single stock data."""
        provider = NSEProvider()
        data = await provider.fetch_stock_data("RELIANCE")
        assert isinstance(data, StockData)
        assert data.symbol == "RELIANCE"
        assert data.price == 500.0

    @pytest.mark.asyncio
    async def test_fetch_multiple_stocks(self) -> None:
        """Test fetching multiple stocks."""
        provider = NSEProvider()
        data = await provider.fetch_multiple_stocks(["RELIANCE", "TCS"])
        assert len(data) == 2
        assert all(isinstance(d, StockData) for d in data)

    def test_provider_name(self) -> None:
        """Test provider name property."""
        provider = NSEProvider()
        assert provider.provider_name == "NSE"


class TestScreenerProvider:
    """Tests for ScreenerProvider."""

    @pytest.mark.asyncio
    async def test_fetch_stock_data(self) -> None:
        """Test fetching single stock data."""
        provider = ScreenerProvider()
        data = await provider.fetch_stock_data("TATAMOTORS")
        assert isinstance(data, StockData)
        assert data.symbol == "TATAMOTORS"
        assert data.price == 250.0

    @pytest.mark.asyncio
    async def test_fetch_multiple_stocks(self) -> None:
        """Test fetching multiple stocks."""
        provider = ScreenerProvider()
        data = await provider.fetch_multiple_stocks(["TATAMOTORS", "MARUTI"])
        assert len(data) == 2
        assert all(isinstance(d, StockData) for d in data)

    def test_provider_name(self) -> None:
        """Test provider name property."""
        provider = ScreenerProvider()
        assert provider.provider_name == "Screener.in"


class TestManualCSVProvider:
    """Tests for ManualCSVProvider."""

    @pytest.mark.asyncio
    async def test_fetch_stock_data_success(self, tmp_path: MockerFixture) -> None:
        """Test successful CSV data fetch."""
        import pandas as pd

        csv_file = tmp_path / "test_stocks.csv"
        df = pd.DataFrame({
            "symbol": ["AAPL", "GOOGL"],
            "name": ["Apple Inc", "Google Inc"],
            "price": [150.0, 200.0],
            "market_cap": [2500000000000.0, 1500000000000.0],
            "pe_ratio": [25.0, 20.0],
            "debt_to_equity": [0.3, 0.2],
            "revenue_growth": [10.0, 15.0],
            "earnings_growth": [15.0, 20.0],
            "promoter_holdings": [60.0, 55.0],
            "sector": ["Technology", "Technology"],
        })
        df.to_csv(csv_file, index=False)

        config = ManualCSVProviderConfig(file_path=str(csv_file))
        provider = ManualCSVProvider(config)
        data = await provider.fetch_stock_data("AAPL")
        assert data.symbol == "AAPL"
        assert data.price == 150.0

    @pytest.mark.asyncio
    async def test_fetch_stock_data_file_not_found(self) -> None:
        """Test CSV file not found error."""
        config = ManualCSVProviderConfig(file_path="nonexistent.csv")
        provider = ManualCSVProvider(config)
        with pytest.raises(ProviderError, match="CSV file not found"):
            await provider.fetch_stock_data("AAPL")

    @pytest.mark.asyncio
    async def test_fetch_stock_data_symbol_not_found(self, tmp_path: MockerFixture) -> None:
        """Test symbol not found in CSV."""
        import pandas as pd

        csv_file = tmp_path / "test_stocks.csv"
        df = pd.DataFrame({
            "symbol": ["AAPL"],
            "name": ["Apple Inc"],
            "price": [150.0],
        })
        df.to_csv(csv_file, index=False)

        config = ManualCSVProviderConfig(file_path=str(csv_file))
        provider = ManualCSVProvider(config)
        with pytest.raises(ValidationError, match="not found in CSV"):
            await provider.fetch_stock_data("GOOGL")

    @pytest.mark.asyncio
    async def test_fetch_stock_data_missing_required_columns(self, tmp_path: MockerFixture) -> None:
        """Test CSV missing required columns."""
        import pandas as pd

        csv_file = tmp_path / "test_stocks.csv"
        df = pd.DataFrame({"symbol": ["AAPL"]})
        df.to_csv(csv_file, index=False)

        config = ManualCSVProviderConfig(file_path=str(csv_file))
        provider = ManualCSVProvider(config)
        with pytest.raises(ValidationError, match="must contain columns"):
            await provider.fetch_stock_data("AAPL")

    @pytest.mark.asyncio
    async def test_fetch_multiple_stocks(self, tmp_path: MockerFixture) -> None:
        """Test fetching multiple stocks from CSV."""
        import pandas as pd

        csv_file = tmp_path / "test_stocks.csv"
        df = pd.DataFrame({
            "symbol": ["AAPL", "GOOGL", "MSFT"],
            "name": ["Apple Inc", "Google Inc", "Microsoft Inc"],
            "price": [150.0, 200.0, 180.0],
        })
        df.to_csv(csv_file, index=False)

        config = ManualCSVProviderConfig(file_path=str(csv_file))
        provider = ManualCSVProvider(config)
        data = await provider.fetch_multiple_stocks(["AAPL", "MSFT"])
        assert len(data) == 2
        assert data[0].symbol == "AAPL"
        assert data[1].symbol == "MSFT"

    def test_provider_name(self) -> None:
        """Test provider name property."""
        provider = ManualCSVProvider()
        assert provider.provider_name == "Manual CSV"


class TestProviderFactory:
    """Tests for ProviderFactory."""

    def test_create_yahoo_provider(self) -> None:
        """Test creating Yahoo Finance provider."""
        provider = ProviderFactory.create_provider("yahoo")
        assert isinstance(provider, YahooFinanceProvider)

    def test_create_nse_provider(self) -> None:
        """Test creating NSE provider."""
        provider = ProviderFactory.create_provider("nse")
        assert isinstance(provider, NSEProvider)

    def test_create_screener_provider(self) -> None:
        """Test creating Screener provider."""
        provider = ProviderFactory.create_provider("screener")
        assert isinstance(provider, ScreenerProvider)

    def test_create_manual_provider(self) -> None:
        """Test creating Manual CSV provider."""
        provider = ProviderFactory.create_provider("manual")
        assert isinstance(provider, ManualCSVProvider)

    def test_create_provider_with_config(self) -> None:
        """Test creating provider with custom config."""
        config = YahooFinanceProviderConfig(timeout=60)
        provider = ProviderFactory.create_provider("yahoo", config)
        assert provider.config.timeout == 60

    def test_create_provider_invalid_type(self) -> None:
        """Test creating provider with invalid type."""
        with pytest.raises(ProviderError, match="Unknown provider type"):
            ProviderFactory.create_provider("invalid")

    def test_create_provider_wrong_config_type(self) -> None:
        """Test creating provider with wrong config type."""
        wrong_config = NSEProviderConfig()
        with pytest.raises(ProviderError, match="Invalid config type"):
            ProviderFactory.create_provider("yahoo", wrong_config)

    def test_list_providers(self) -> None:
        """Test listing registered providers."""
        providers = ProviderFactory.list_providers()
        assert "yahoo" in providers
        assert "nse" in providers
        assert "screener" in providers
        assert "manual" in providers

    def test_register_provider(self) -> None:
        """Test registering a custom provider."""
        from app.providers.base import Provider, ProviderConfig

        class CustomProvider(Provider):
            async def fetch_stock_data(self, symbol: str) -> StockData:
                return StockData(symbol=symbol, name="Custom", price=0.0)

            async def fetch_multiple_stocks(self, symbols: list[str]) -> list[StockData]:
                return []

            @property
            def provider_name(self) -> str:
                return "Custom"

        class CustomConfig(ProviderConfig):
            pass

        ProviderFactory.register_provider("custom", CustomProvider, CustomConfig)
        provider = ProviderFactory.create_provider("custom")
        assert isinstance(provider, CustomProvider)

        # Clean up
        del ProviderFactory._providers["custom"]
