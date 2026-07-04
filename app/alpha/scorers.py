"""Alpha Score scorers for each component."""

from __future__ import annotations

from typing import Any

from app.alpha.models import AlphaScoreComponents
from app.financials import FinancialScore
from app.management import GuidanceScore
from app.recommendation import Recommendation
from app.sectors import SectorScore
from app.technical import TechnicalScore


class AlphaScorer:
    """Scorer for calculating Alpha Score components."""

    # Weight configuration
    WEIGHTS = {
        "financial_quality": 20,
        "growth_acceleration": 15,
        "technical_momentum": 15,
        "sector_momentum": 10,
        "management_guidance": 10,
        "institutional_buying": 10,
        "valuation": 5,
        "order_book": 5,
        "risk": 5,
        "earnings_surprise_probability": 5,
    }

    def calculate_financial_quality(
        self,
        financial_score: FinancialScore,
    ) -> float:
        """Calculate Financial Quality score (weight: 20).

        Args:
            financial_score: Financial score data.

        Returns:
            Normalized score (0-100).
        """
        # Key metrics for financial quality
        roe_score = self._normalize_score(financial_score.roe, 0, 30)  # Good ROE > 20%
        roce_score = self._normalize_score(financial_score.roce, 0, 25)  # Good ROCE > 15%
        debt_equity_score = self._normalize_score(
            -financial_score.debt_to_equity,
            -5,  # Bad: high debt
            0,  # Good: no debt
        )
        cash_flow_score = self._normalize_score(
            financial_score.operating_cash_flow,
            0,
            10000000,  # Good: strong cash flow
        )

        # Weighted average of components
        financial_quality = (
            roe_score * 0.30 +
            roce_score * 0.25 +
            debt_equity_score * 0.25 +
            cash_flow_score * 0.20
        )

        return financial_quality

    def calculate_growth_acceleration(
        self,
        financial_score: FinancialScore,
    ) -> float:
        """Calculate Growth Acceleration score (weight: 15).

        Args:
            financial_score: Financial score data.

        Returns:
            Normalized score (0-100).
        """
        revenue_growth_score = self._normalize_score(
            financial_score.revenue_growth,
            0,
            30,  # Good: > 20% revenue growth
        )
        profit_growth_score = self._normalize_score(
            financial_score.profit_growth,
            0,
            25,  # Good: > 15% profit growth
        )
        eps_growth_score = self._normalize_score(
            financial_score.eps_growth,
            0,
            25,  # Good: > 15% EPS growth
        )
        book_value_growth_score = self._normalize_score(
            financial_score.book_value_growth,
            0,
            20,  # Good: > 10% book value growth
        )

        # Weighted average of growth components
        growth_acceleration = (
            revenue_growth_score * 0.35 +
            profit_growth_score * 0.30 +
            eps_growth_score * 0.20 +
            book_value_growth_score * 0.15
        )

        return growth_acceleration

    def calculate_technical_momentum(
        self,
        technical_score: TechnicalScore,
    ) -> float:
        """Calculate Technical Momentum score (weight: 15).

        Args:
            technical_score: Technical score data.

        Returns:
            Normalized score (0-100).
        """
        rsi_score = self._normalize_rsi(technical_score.rsi)
        macd_score = self._normalize_score(
            technical_score.macd,
            -5,
            5,
        )
        adx_score = self._normalize_score(
            technical_score.adx,
            0,
            50,  # Strong trend > 25
        )
        ema_vs_sma_score = self._normalize_score(
            technical_score.ema_20 - technical_score.sma_50,
            -50,
            50,
        )
        volume_breakout_score = 100.0 if technical_score.volume_breakout else 50.0

        # Weighted average of technical components
        technical_momentum = (
            rsi_score * 0.25 +
            macd_score * 0.20 +
            adx_score * 0.20 +
            ema_vs_sma_score * 0.20 +
            volume_breakout_score * 0.15
        )

        return technical_momentum

    def calculate_sector_momentum(
        self,
        sector_score: SectorScore,
    ) -> float:
        """Calculate Sector Momentum score (weight: 10).

        Args:
            sector_score: Sector score data.

        Returns:
            Normalized score (0-100).
        """
        # Use overall sector score normalized to 0-100
        sector_momentum = self._normalize_score(
            sector_score.overall_score,
            0,
            100,
        )

        # Adjust based on rotation signal
        if sector_score.rotation_signal == "inflow":
            sector_momentum = min(100, sector_momentum + 20)
        elif sector_score.rotation_signal == "outflow":
            sector_momentum = max(0, sector_momentum - 20)

        return sector_momentum

    def calculate_management_guidance(
        self,
        management_score: GuidanceScore,
    ) -> float:
        """Calculate Management Guidance score (weight: 10).

        Args:
            management_score: Management score data.

        Returns:
            Normalized score (0-100).
        """
        revenue_outlook_score = self._normalize_sentiment(management_score.revenue_outlook)
        margin_outlook_score = self._normalize_sentiment(management_score.margin_outlook)
        demand_outlook_score = self._normalize_sentiment(management_score.demand)
        order_book_score = self._normalize_sentiment(management_score.order_book)
        capex_outlook_score = self._normalize_sentiment(management_score.capex)
        confidence_score = self._normalize_confidence(management_score.management_confidence)

        # Weighted average of guidance components
        management_guidance = (
            revenue_outlook_score * 0.25 +
            margin_outlook_score * 0.15 +
            demand_outlook_score * 0.15 +
            order_book_score * 0.15 +
            capex_outlook_score * 0.15 +
            confidence_score * 0.15
        )

        return management_guidance

    def calculate_institutional_buying(
        self,
        institutional_score: float,
    ) -> float:
        """Calculate Institutional Buying score (weight: 10).

        Args:
            institutional_score: Institutional score (0-100).

        Returns:
            Normalized score (0-100).
        """
        return self._normalize_score(institutional_score, 0, 100)

    def calculate_valuation(
        self,
        financial_score: FinancialScore,
        current_price: float,
    ) -> float:
        """Calculate Valuation score (weight: 5).

        Args:
            financial_score: Financial score data.
            current_price: Current stock price.

        Returns:
            Normalized score (0-100).
        """
        # Lower PEG is better (undervalued)
        peg_score = self._normalize_score(
            -financial_score.peg,
            -3,  # Overvalued
            0,  # Fair value
        )

        # Simple valuation check based on PEG
        valuation_score = peg_score

        return valuation_score

    def calculate_order_book(
        self,
        order_book_score: float,
    ) -> float:
        """Calculate Order Book score (weight: 5).

        Args:
            order_book_score: Order book score (-50 to 50).

        Returns:
            Normalized score (0-100).
        """
        return self._normalize_score(order_book_score, -50, 50)

    def calculate_risk(
        self,
        risk_score: float,
    ) -> float:
        """Calculate Risk score (weight: 5).

        Args:
            risk_score: Risk score (0-100, lower is better).

        Returns:
            Normalized score (0-100).
        """
        # Invert risk score - lower risk = higher score
        return 100 - self._normalize_score(risk_score, 0, 100)

    def calculate_earnings_surprise_probability(
        self,
        earnings_surprise_score: float,
    ) -> float:
        """Calculate Earnings Surprise Probability score (weight: 5).

        Args:
            earnings_surprise_score: Earnings surprise score (0-100).

        Returns:
            Normalized score (0-100).
        """
        return self._normalize_score(earnings_surprise_score, 0, 100)

    def calculate_all_components(
        self,
        financial_score: FinancialScore,
        technical_score: TechnicalScore,
        sector_score: SectorScore,
        management_score: GuidanceScore,
        institutional_score: float,
        current_price: float,
        order_book_score: float,
        risk_score: float,
        earnings_surprise_score: float,
    ) -> AlphaScoreComponents:
        """Calculate all Alpha Score components.

        Args:
            financial_score: Financial score data.
            technical_score: Technical score data.
            sector_score: Sector score data.
            management_score: Management score data.
            institutional_score: Institutional score.
            current_price: Current stock price.
            order_book_score: Order book score.
            risk_score: Risk score.
            earnings_surprise_score: Earnings surprise score.

        Returns:
            AlphaScoreComponents with all component scores.
        """
        components = AlphaScoreComponents(
            financial_quality=self.calculate_financial_quality(financial_score),
            growth_acceleration=self.calculate_growth_acceleration(financial_score),
            technical_momentum=self.calculate_technical_momentum(technical_score),
            sector_momentum=self.calculate_sector_momentum(sector_score),
            management_guidance=self.calculate_management_guidance(management_score),
            institutional_buying=self.calculate_institutional_buying(institutional_score),
            valuation=self.calculate_valuation(financial_score, current_price),
            order_book=self.calculate_order_book(order_book_score),
            risk=self.calculate_risk(risk_score),
            earnings_surprise_probability=self.calculate_earnings_surprise_probability(earnings_surprise_score),
        )

        return components

    def calculate_overall_alpha_score(
        self,
        components: AlphaScoreComponents,
    ) -> float:
        """Calculate overall Alpha Score using weighted average.

        Args:
            components: Alpha Score components.

        Returns:
            Overall Alpha Score (0-100).
        """
        overall_score = (
            components.financial_quality * self.WEIGHTS["financial_quality"] +
            components.growth_acceleration * self.WEIGHTS["growth_acceleration"] +
            components.technical_momentum * self.WEIGHTS["technical_momentum"] +
            components.sector_momentum * self.WEIGHTS["sector_momentum"] +
            components.management_guidance * self.WEIGHTS["management_guidance"] +
            components.institutional_buying * self.WEIGHTS["institutional_buying"] +
            components.valuation * self.WEIGHTS["valuation"] +
            components.order_book * self.WEIGHTS["order_book"] +
            components.risk * self.WEIGHTS["risk"] +
            components.earnings_surprise_probability * self.WEIGHTS["earnings_surprise_probability"]
        ) / 100

        return overall_score

    def _normalize_score(
        self,
        value: float,
        min_val: float,
        max_val: float,
    ) -> float:
        """Normalize a value to 0-100 range.

        Args:
            value: Value to normalize.
            min_val: Minimum expected value.
            max_val: Maximum expected value.

        Returns:
            Normalized value (0-100).
        """
        if max_val == min_val:
            return 50.0

        normalized = ((value - min_val) / (max_val - min_val)) * 100
        return max(0, min(100, normalized))

    def _normalize_rsi(self, rsi: float) -> float:
        """Normalize RSI to score (0-100).

        Args:
            rsi: RSI value.

        Returns:
            Normalized score.
        """
        # RSI > 50 is bullish, < 50 is bearish
        if rsi > 70:
            return 40.0  # Overbought - reduce score
        elif rsi > 50:
            return 80.0 + (rsi - 50)  # Bullish
        elif rsi > 30:
            return 40.0 - (50 - rsi)  # Bearish
        else:
            return 60.0  # Oversold - potential bounce

    def _normalize_sentiment(self, sentiment: str) -> float:
        """Normalize sentiment string to score (0-100).

        Args:
            sentiment: Sentiment string.

        Returns:
            Normalized score.
        """
        sentiment_lower = sentiment.lower()
        if "positive" in sentiment_lower or "strong" in sentiment_lower or "increasing" in sentiment_lower:
            return 80.0
        elif "negative" in sentiment_lower or "weak" in sentiment_lower or "decreasing" in sentiment_lower:
            return 30.0
        else:
            return 50.0

    def _normalize_confidence(self, confidence: str) -> float:
        """Normalize confidence string to score (0-100).

        Args:
            confidence: Confidence string.

        Returns:
            Normalized score.
        """
        confidence_lower = confidence.lower()
        if "high" in confidence_lower:
            return 85.0
        elif "medium" in confidence_lower:
            return 60.0
        else:
            return 40.0
