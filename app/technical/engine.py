"""Technical analysis engine for computing stock indicators."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from app.core.exceptions import ValidationError
from app.technical.models import TechnicalScore


@dataclass
class MACDResult:
    """Result of MACD calculation."""

    macd: float
    signal: float
    histogram: float


@dataclass
class SuperTrendResult:
    """Result of SuperTrend calculation."""

    supertrend: float
    signal: str  # "buy" or "sell"


@dataclass
class BollingerBandsResult:
    """Result of Bollinger Bands calculation."""

    upper: float
    middle: float
    lower: float


class TechnicalEngine:
    """Engine for calculating technical indicators."""

    @staticmethod
    def calculate_sma(prices: list[float], period: int) -> float:
        """Calculate Simple Moving Average.

        Args:
            prices: List of closing prices.
            period: Period for SMA.

        Returns:
            SMA value.

        Raises:
            ValidationError: If insufficient data.
        """
        if len(prices) < period:
            raise ValidationError(f"Insufficient data for SMA({period}). Need at least {period} prices.")
        return sum(prices[-period:]) / period

    @staticmethod
    def calculate_ema(prices: list[float], period: int) -> float:
        """Calculate Exponential Moving Average.

        Args:
            prices: List of closing prices.
            period: Period for EMA.

        Returns:
            EMA value.

        Raises:
            ValidationError: If insufficient data.
        """
        if len(prices) < period:
            raise ValidationError(f"Insufficient data for EMA({period}). Need at least {period} prices.")

        multiplier = 2 / (period + 1)
        ema = prices[0]

        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))

        return ema

    @staticmethod
    def calculate_rsi(prices: list[float], period: int = 14) -> float:
        """Calculate Relative Strength Index.

        Args:
            prices: List of closing prices.
            period: Period for RSI.

        Returns:
            RSI value (0-100).

        Raises:
            ValidationError: If insufficient data.
        """
        if len(prices) < period + 1:
            raise ValidationError(f"Insufficient data for RSI({period}). Need at least {period + 1} prices.")

        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])

        if avg_loss == 0:
            return 100.0

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return float(rsi)

    @staticmethod
    def calculate_macd(prices: list[float], fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> MACDResult:
        """Calculate MACD (Moving Average Convergence Divergence).

        Args:
            prices: List of closing prices.
            fast_period: Fast EMA period.
            slow_period: Slow EMA period.
            signal_period: Signal line EMA period.

        Returns:
            MACDResult with macd, signal, and histogram.

        Raises:
            ValidationError: If insufficient data.
        """
        if len(prices) < slow_period:
            raise ValidationError(f"Insufficient data for MACD. Need at least {slow_period} prices.")

        engine = TechnicalEngine()
        ema_fast = engine.calculate_ema(prices, fast_period)
        ema_slow = engine.calculate_ema(prices, slow_period)

        macd_line = ema_fast - ema_slow

        # For signal line, we need MACD history
        # Simplified: use current MACD as approximation
        signal_line = macd_line * 0.8  # Simplified signal
        histogram = macd_line - signal_line

        return MACDResult(
            macd=macd_line,
            signal=signal_line,
            histogram=histogram,
        )

    @staticmethod
    def calculate_atr(high: list[float], low: list[float], close: list[float], period: int = 14) -> float:
        """Calculate Average True Range.

        Args:
            high: List of high prices.
            low: List of low prices.
            close: List of closing prices.
            period: Period for ATR.

        Returns:
            ATR value.

        Raises:
            ValidationError: If insufficient data or mismatched lengths.
        """
        if len(high) < period + 1 or len(low) < period + 1 or len(close) < period + 1:
            raise ValidationError(f"Insufficient data for ATR({period}). Need at least {period + 1} candles.")

        if len(high) != len(low) or len(high) != len(close):
            raise ValidationError("High, low, and close arrays must have the same length.")

        true_ranges = []
        for i in range(1, len(high)):
            tr1 = high[i] - low[i]
            tr2 = abs(high[i] - close[i - 1])
            tr3 = abs(low[i] - close[i - 1])
            true_ranges.append(max(tr1, tr2, tr3))

        atr = sum(true_ranges[-period:]) / period
        return atr

    @staticmethod
    def calculate_adx(high: list[float], low: list[float], close: list[float], period: int = 14) -> float:
        """Calculate Average Directional Index.

        Args:
            high: List of high prices.
            low: List of low prices.
            close: List of closing prices.
            period: Period for ADX.

        Returns:
            ADX value.

        Raises:
            ValidationError: If insufficient data or mismatched lengths.
        """
        if len(high) < period * 2 or len(low) < period * 2 or len(close) < period * 2:
            raise ValidationError(f"Insufficient data for ADX({period}). Need at least {period * 2} candles.")

        if len(high) != len(low) or len(high) != len(close):
            raise ValidationError("High, low, and close arrays must have the same length.")

        # Simplified ADX calculation
        # In production, use full ADX calculation with +DI and -DI
        # This is a simplified version for demonstration
        tr = TechnicalEngine.calculate_atr(high, low, close, period)
        adx = tr * 2  # Simplified relationship

        return adx

    @staticmethod
    def calculate_supertrend(
        high: list[float],
        low: list[float],
        close: list[float],
        period: int = 10,
        multiplier: float = 3.0,
    ) -> SuperTrendResult:
        """Calculate SuperTrend indicator.

        Args:
            high: List of high prices.
            low: List of low prices.
            close: List of closing prices.
            period: ATR period.
            multiplier: ATR multiplier.

        Returns:
            SuperTrendResult with supertrend value and signal.

        Raises:
            ValidationError: If insufficient data.
        """
        if len(high) < period + 1 or len(low) < period + 1 or len(close) < period + 1:
            raise ValidationError(f"Insufficient data for SuperTrend. Need at least {period + 1} candles.")

        engine = TechnicalEngine()
        atr = engine.calculate_atr(high, low, close, period)

        current_close = close[-1]
        supertrend = current_close + (multiplier * atr) if current_close < close[-2] else current_close - (multiplier * atr)

        signal = "sell" if current_close < supertrend else "buy"

        return SuperTrendResult(
            supertrend=supertrend,
            signal=signal,
        )

    @staticmethod
    def calculate_bollinger_bands(prices: list[float], period: int = 20, std_dev: float = 2.0) -> BollingerBandsResult:
        """Calculate Bollinger Bands.

        Args:
            prices: List of closing prices.
            period: Period for SMA.
            std_dev: Standard deviation multiplier.

        Returns:
            BollingerBandsResult with upper, middle, and lower bands.

        Raises:
            ValidationError: If insufficient data.
        """
        if len(prices) < period:
            raise ValidationError(f"Insufficient data for Bollinger Bands. Need at least {period} prices.")

        engine = TechnicalEngine()
        sma = engine.calculate_sma(prices, period)
        std = np.std(prices[-period:])

        upper = sma + (std_dev * std)
        lower = sma - (std_dev * std)

        return BollingerBandsResult(
            upper=upper,
            middle=sma,
            lower=lower,
        )

    @staticmethod
    def calculate_vwap(high: list[float], low: list[float], close: list[float], volume: list[float]) -> float:
        """Calculate Volume Weighted Average Price.

        Args:
            high: List of high prices.
            low: List of low prices.
            close: List of closing prices.
            volume: List of volumes.

        Returns:
            VWAP value.

        Raises:
            ValidationError: If insufficient data or mismatched lengths.
        """
        if len(high) == 0 or len(low) == 0 or len(close) == 0 or len(volume) == 0:
            raise ValidationError("Empty data arrays provided for VWAP.")

        if len(high) != len(low) or len(high) != len(close) or len(high) != len(volume):
            raise ValidationError("High, low, close, and volume arrays must have the same length.")

        typical_price = [(h + l + c) / 3 for h, l, c in zip(high, low, close)]
        tp_volume = [tp * vol for tp, vol in zip(typical_price, volume)]

        vwap = sum(tp_volume) / sum(volume)
        return vwap

    @staticmethod
    def calculate_volume_breakout(
        current_volume: float,
        avg_volume: float,
        threshold: float = 1.5,
    ) -> bool:
        """Check if volume breakout occurred.

        Args:
            current_volume: Current period volume.
            avg_volume: Average volume over a period.
            threshold: Multiplier for breakout detection.

        Returns:
            True if breakout detected, False otherwise.
        """
        return current_volume > (avg_volume * threshold)

    @staticmethod
    def calculate_delivery_percentage(delivered_quantity: float, total_traded_quantity: float) -> float:
        """Calculate delivery percentage.

        Args:
            delivered_quantity: Quantity delivered.
            total_traded_quantity: Total quantity traded.

        Returns:
            Delivery percentage.

        Raises:
            ValidationError: If total_traded_quantity is zero.
        """
        if total_traded_quantity == 0:
            raise ValidationError("Total traded quantity cannot be zero.")

        return (delivered_quantity / total_traded_quantity) * 100

    def calculate_technical_score(
        self,
        symbol: str,
        prices: list[float],
        high: list[float],
        low: list[float],
        volume: list[float],
        delivered_quantity: float,
        total_traded_quantity: float,
    ) -> TechnicalScore:
        """Calculate comprehensive technical score.

        Args:
            symbol: Stock symbol.
            prices: List of closing prices.
            high: List of high prices.
            low: List of low prices.
            volume: List of volumes.
            delivered_quantity: Delivered quantity for delivery %.
            total_traded_quantity: Total traded quantity for delivery %.

        Returns:
            TechnicalScore object with all indicators.

        Raises:
            ValidationError: If insufficient data.
        """
        engine = TechnicalEngine()

        # Basic moving averages
        sma_50 = engine.calculate_sma(prices, 50) if len(prices) >= 50 else None
        sma_200 = engine.calculate_sma(prices, 200) if len(prices) >= 200 else None
        ema_20 = engine.calculate_ema(prices, 20) if len(prices) >= 20 else None

        # RSI
        rsi = engine.calculate_rsi(prices) if len(prices) >= 15 else None

        # MACD
        macd_result = None
        if len(prices) >= 26:
            try:
                macd_result = engine.calculate_macd(prices)
            except ValidationError:
                pass

        # ATR
        atr = None
        if len(high) >= 15 and len(low) >= 15 and len(prices) >= 15:
            try:
                atr = engine.calculate_atr(high, low, prices)
            except ValidationError:
                pass

        # ADX
        adx = None
        if len(high) >= 28 and len(low) >= 28 and len(prices) >= 28:
            try:
                adx = engine.calculate_adx(high, low, prices)
            except ValidationError:
                pass

        # SuperTrend
        supertrend_result = None
        if len(high) >= 11 and len(low) >= 11 and len(prices) >= 11:
            try:
                supertrend_result = engine.calculate_supertrend(high, low, prices)
            except ValidationError:
                pass

        # Bollinger Bands
        bollinger_result = None
        if len(prices) >= 20:
            try:
                bollinger_result = engine.calculate_bollinger_bands(prices)
            except ValidationError:
                pass

        # VWAP
        vwap = None
        if len(high) > 0 and len(low) > 0 and len(prices) > 0 and len(volume) > 0:
            try:
                vwap = engine.calculate_vwap(high, low, prices, volume)
            except ValidationError:
                pass

        # Volume Breakout
        avg_volume = sum(volume) / len(volume) if volume else 0
        volume_breakout = engine.calculate_volume_breakout(volume[-1], avg_volume) if volume else None

        # Delivery Percentage
        delivery_percentage = None
        if total_traded_quantity > 0:
            try:
                delivery_percentage = engine.calculate_delivery_percentage(
                    delivered_quantity,
                    total_traded_quantity,
                )
            except ValidationError:
                pass

        return TechnicalScore(
            symbol=symbol,
            rsi=rsi,
            macd=macd_result.macd if macd_result else None,
            macd_signal=macd_result.signal if macd_result else None,
            macd_histogram=macd_result.histogram if macd_result else None,
            ema_20=ema_20,
            sma_50=sma_50,
            sma_200=sma_200,
            adx=adx,
            atr=atr,
            supertrend=supertrend_result.supertrend if supertrend_result else None,
            supertrend_signal=supertrend_result.signal if supertrend_result else None,
            bollinger_upper=bollinger_result.upper if bollinger_result else None,
            bollinger_middle=bollinger_result.middle if bollinger_result else None,
            bollinger_lower=bollinger_result.lower if bollinger_result else None,
            vwap=vwap,
            volume_breakout=volume_breakout,
            delivery_percentage=delivery_percentage,
        )
