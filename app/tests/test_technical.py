"""Unit tests for the Technical Engine."""

from __future__ import annotations

import pytest

from app.core import ValidationError
from app.technical import (
    BollingerBandsResult,
    MACDResult,
    SuperTrendResult,
    TechnicalEngine,
    TechnicalScore,
)


class TestTechnicalScore:
    """Tests for TechnicalScore model."""

    def test_technical_score_to_dict(self) -> None:
        """Ensure TechnicalScore converts to dictionary correctly."""
        score = TechnicalScore(
            symbol="AAPL",
            rsi=65.0,
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
        result = score.to_dict()
        assert result["symbol"] == "AAPL"
        assert result["rsi"] == 65.0
        assert result["macd"] == 1.5


class TestTechnicalEngine:
    """Tests for TechnicalEngine calculations."""

    def test_calculate_sma(self) -> None:
        """Test SMA calculation."""
        engine = TechnicalEngine()
        prices = [100, 102, 104, 106, 108, 110, 112, 114, 116, 118]
        result = engine.calculate_sma(prices, 5)
        assert result == 114.0

    def test_calculate_sma_insufficient_data(self) -> None:
        """Test SMA with insufficient data."""
        engine = TechnicalEngine()
        prices = [100, 102, 104]
        with pytest.raises(ValidationError, match="Insufficient data for SMA"):
            engine.calculate_sma(prices, 5)

    def test_calculate_ema(self) -> None:
        """Test EMA calculation."""
        engine = TechnicalEngine()
        prices = [100, 102, 104, 106, 108, 110, 112, 114, 116, 118]
        result = engine.calculate_ema(prices, 5)
        assert result > 100
        assert result < 118

    def test_calculate_ema_insufficient_data(self) -> None:
        """Test EMA with insufficient data."""
        engine = TechnicalEngine()
        prices = [100, 102, 104]
        with pytest.raises(ValidationError, match="Insufficient data for EMA"):
            engine.calculate_ema(prices, 5)

    def test_calculate_rsi(self) -> None:
        """Test RSI calculation."""
        engine = TechnicalEngine()
        # Create prices with upward trend for higher RSI
        prices = [100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128]
        result = engine.calculate_rsi(prices)
        assert 0 <= result <= 100
        assert result > 50  # Should be > 50 for upward trend

    def test_calculate_rsi_insufficient_data(self) -> None:
        """Test RSI with insufficient data."""
        engine = TechnicalEngine()
        prices = [100, 102, 104]
        with pytest.raises(ValidationError, match="Insufficient data for RSI"):
            engine.calculate_rsi(prices)

    def test_calculate_macd(self) -> None:
        """Test MACD calculation."""
        engine = TechnicalEngine()
        prices = [100 + i for i in range(30)]  # 30 data points
        result = engine.calculate_macd(prices)
        assert isinstance(result, MACDResult)
        assert result.macd is not None
        assert result.signal is not None
        assert result.histogram is not None

    def test_calculate_macd_insufficient_data(self) -> None:
        """Test MACD with insufficient data."""
        engine = TechnicalEngine()
        prices = [100, 102, 104]
        with pytest.raises(ValidationError, match="Insufficient data for MACD"):
            engine.calculate_macd(prices)

    def test_calculate_atr(self) -> None:
        """Test ATR calculation."""
        engine = TechnicalEngine()
        high = [105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135]
        low = [95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125]
        close = [100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130]
        result = engine.calculate_atr(high, low, close)
        assert result > 0

    def test_calculate_atr_insufficient_data(self) -> None:
        """Test ATR with insufficient data."""
        engine = TechnicalEngine()
        high = [105, 107]
        low = [95, 97]
        close = [100, 102]
        with pytest.raises(ValidationError, match="Insufficient data for ATR"):
            engine.calculate_atr(high, low, close)

    def test_calculate_atr_mismatched_lengths(self) -> None:
        """Test ATR with mismatched array lengths."""
        engine = TechnicalEngine()
        high = [105 + i for i in range(20)]
        low = [95 + i for i in range(15)]
        close = [100 + i for i in range(20)]
        with pytest.raises(ValidationError, match="must have the same length"):
            engine.calculate_atr(high, low, close)

    def test_calculate_adx(self) -> None:
        """Test ADX calculation."""
        engine = TechnicalEngine()
        high = [100 + i for i in range(30)]
        low = [95 + i for i in range(30)]
        close = [97.5 + i for i in range(30)]
        result = engine.calculate_adx(high, low, close)
        assert result > 0

    def test_calculate_adx_insufficient_data(self) -> None:
        """Test ADX with insufficient data."""
        engine = TechnicalEngine()
        high = [105, 107]
        low = [95, 97]
        close = [100, 102]
        with pytest.raises(ValidationError, match="Insufficient data for ADX"):
            engine.calculate_adx(high, low, close)

    def test_calculate_supertrend(self) -> None:
        """Test SuperTrend calculation."""
        engine = TechnicalEngine()
        high = [105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125]
        low = [95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115]
        close = [100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120]
        result = engine.calculate_supertrend(high, low, close)
        assert isinstance(result, SuperTrendResult)
        assert result.supertrend is not None
        assert result.signal in ["buy", "sell"]

    def test_calculate_supertrend_insufficient_data(self) -> None:
        """Test SuperTrend with insufficient data."""
        engine = TechnicalEngine()
        high = [105, 107]
        low = [95, 97]
        close = [100, 102]
        with pytest.raises(ValidationError, match="Insufficient data for SuperTrend"):
            engine.calculate_supertrend(high, low, close)

    def test_calculate_bollinger_bands(self) -> None:
        """Test Bollinger Bands calculation."""
        engine = TechnicalEngine()
        prices = [100 + i for i in range(20)]
        result = engine.calculate_bollinger_bands(prices)
        assert isinstance(result, BollingerBandsResult)
        assert result.upper > result.middle
        assert result.middle > result.lower

    def test_calculate_bollinger_bands_insufficient_data(self) -> None:
        """Test Bollinger Bands with insufficient data."""
        engine = TechnicalEngine()
        prices = [100, 102, 104]
        with pytest.raises(ValidationError, match="Insufficient data for Bollinger Bands"):
            engine.calculate_bollinger_bands(prices)

    def test_calculate_vwap(self) -> None:
        """Test VWAP calculation."""
        engine = TechnicalEngine()
        high = [105, 107, 109, 111, 113]
        low = [95, 97, 99, 101, 103]
        close = [100, 102, 104, 106, 108]
        volume = [1000, 1200, 1100, 1300, 1400]
        result = engine.calculate_vwap(high, low, close, volume)
        assert result > 0
        assert result > min(close)
        assert result < max(close)

    def test_calculate_vwap_empty_data(self) -> None:
        """Test VWAP with empty data."""
        engine = TechnicalEngine()
        with pytest.raises(ValidationError, match="Empty data arrays"):
            engine.calculate_vwap([], [], [], [])

    def test_calculate_vwap_mismatched_lengths(self) -> None:
        """Test VWAP with mismatched array lengths."""
        engine = TechnicalEngine()
        high = [105, 107]
        low = [95, 97]
        close = [100]
        volume = [1000, 1200]
        with pytest.raises(ValidationError, match="must have the same length"):
            engine.calculate_vwap(high, low, close, volume)

    def test_calculate_volume_breakout(self) -> None:
        """Test volume breakout detection."""
        engine = TechnicalEngine()
        result = engine.calculate_volume_breakout(2000, 1000)
        assert result is True

    def test_calculate_volume_breakout_no_breakout(self) -> None:
        """Test no volume breakout."""
        engine = TechnicalEngine()
        result = engine.calculate_volume_breakout(1200, 1000)
        assert result is False

    def test_calculate_delivery_percentage(self) -> None:
        """Test delivery percentage calculation."""
        engine = TechnicalEngine()
        result = engine.calculate_delivery_percentage(750, 1000)
        assert result == 75.0

    def test_calculate_delivery_percentage_zero_total(self) -> None:
        """Test delivery percentage with zero total."""
        engine = TechnicalEngine()
        with pytest.raises(ValidationError, match="Total traded quantity cannot be zero"):
            engine.calculate_delivery_percentage(750, 0)

    def test_calculate_technical_score(self) -> None:
        """Test comprehensive technical score calculation."""
        engine = TechnicalEngine()
        prices = [100 + i for i in range(200)]
        high = [100 + i + 5 for i in range(200)]
        low = [100 + i - 5 for i in range(200)]
        volume = [1000 + i * 10 for i in range(200)]

        score = engine.calculate_technical_score(
            symbol="AAPL",
            prices=prices,
            high=high,
            low=low,
            volume=volume,
            delivered_quantity=750,
            total_traded_quantity=1000,
        )

        assert isinstance(score, TechnicalScore)
        assert score.symbol == "AAPL"
        assert score.rsi is not None
        assert score.sma_50 is not None
        assert score.sma_200 is not None
        assert score.ema_20 is not None
        assert score.delivery_percentage == 75.0

    def test_calculate_technical_score_insufficient_data(self) -> None:
        """Test technical score with minimal data."""
        engine = TechnicalEngine()
        prices = [100, 102, 104, 106, 108]
        high = [105, 107, 109, 111, 113]
        low = [95, 97, 99, 101, 103]
        volume = [1000, 1200, 1100, 1300, 1400]

        score = engine.calculate_technical_score(
            symbol="AAPL",
            prices=prices,
            high=high,
            low=low,
            volume=volume,
            delivered_quantity=750,
            total_traded_quantity=1000,
        )

        assert isinstance(score, TechnicalScore)
        assert score.symbol == "AAPL"
        # Some indicators should be None due to insufficient data
        assert score.sma_50 is None
        assert score.sma_200 is None
        assert score.delivery_percentage == 75.0
