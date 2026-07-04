"""Research Profile scorers with component-level scoring (e.g., 18/20)."""

from __future__ import annotations

from typing import Any

from app.alpha.models import AlphaScoreComponents, ComponentScore
from app.financials import FinancialScore
from app.management import GuidanceScore
from app.sectors import SectorScore
from app.technical import TechnicalScore


class ResearchScorer:
    """Scorer for calculating Research Profile components with component-level scoring."""

    # Max scores for each component (for research profile display)
    MAX_SCORES = {
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

    # Weight configuration (same as before)
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
    ) -> ComponentScore:
        """Calculate Financial Quality score (max: 20, weight: 20).

        Args:
            financial_score: Financial score data.

        Returns:
            ComponentScore with research profile format.
        """
        # Normalize individual metrics to 0-100
        roe_score = self._normalize_score(financial_score.roe, 0, 30)
        roce_score = self._normalize_score(financial_score.roce, 0, 25)
        debt_score = self._normalize_score(
            -financial_score.debt_to_equity,
            -5,
            0,
        )
        cash_flow_score = self._normalize_score(
            financial_score.operating_cash_flow,
            0,
            10000000000,
        )

        # Weighted average (0-100)
        quality_100 = (
            roe_score * 0.3 +
            roce_score * 0.25 +
            debt_score * 0.25 +
            cash_flow_score * 0.2
        )

        # Convert to component score (0-20)
        component_score = (quality_100 / 100) * self.MAX_SCORES["financial_quality"]

        details = f"ROE: {financial_score.roe:.1f}%, ROCE: {financial_score.roce:.1f}%, D/E: {financial_score.debt_to_equity:.2f}"

        return ComponentScore(
            name="Financial Quality",
            score=round(component_score, 1),
            max_score=self.MAX_SCORES["financial_quality"],
            weight=self.WEIGHTS["financial_quality"],
            details=details,
        )

    def calculate_growth_acceleration(
        self,
        financial_score: FinancialScore,
    ) -> ComponentScore:
        """Calculate Growth Acceleration score (max: 15, weight: 15).

        Args:
            financial_score: Financial score data.

        Returns:
            ComponentScore with research profile format.
        """
        revenue_score = self._normalize_score(financial_score.revenue_growth, 0, 30)
        profit_score = self._normalize_score(financial_score.profit_growth, 0, 25)
        eps_score = self._normalize_score(financial_score.eps_growth, 0, 25)
        book_value_score = self._normalize_score(financial_score.book_value_growth, 0, 20)

        # Weighted average (0-100)
        growth_100 = (
            revenue_score * 0.35 +
            profit_score * 0.30 +
            eps_score * 0.20 +
            book_value_score * 0.15
        )

        # Convert to component score (0-15)
        component_score = (growth_100 / 100) * self.MAX_SCORES["growth_acceleration"]

        details = f"Revenue Growth: {financial_score.revenue_growth:.1f}%, EPS Growth: {financial_score.eps_growth:.1f}%"

        return ComponentScore(
            name="Growth Acceleration",
            score=round(component_score, 1),
            max_score=self.MAX_SCORES["growth_acceleration"],
            weight=self.WEIGHTS["growth_acceleration"],
            details=details,
        )

    def calculate_technical_momentum(
        self,
        technical_score: TechnicalScore,
    ) -> ComponentScore:
        """Calculate Technical Momentum score (max: 15, weight: 15).

        Args:
            technical_score: Technical score data.

        Returns:
            ComponentScore with research profile format.
        """
        rsi_score = self._normalize_rsi(technical_score.rsi)
        macd_score = self._normalize_macd(technical_score.macd, technical_score.macd_signal)
        adx_score = self._normalize_score(technical_score.adx, 0, 50)
        ema_trend_score = self._normalize_ema_trend(
            technical_score.ema_20,
            technical_score.sma_50,
        )

        # Weighted average (0-100)
        momentum_100 = (
            rsi_score * 0.25 +
            macd_score * 0.30 +
            adx_score * 0.25 +
            ema_trend_score * 0.20
        )

        # Convert to component score (0-15)
        component_score = (momentum_100 / 100) * self.MAX_SCORES["technical_momentum"]

        details = f"RSI: {technical_score.rsi:.1f}, MACD: {technical_score.macd:.2f}, ADX: {technical_score.adx:.1f}"

        return ComponentScore(
            name="Technical Momentum",
            score=round(component_score, 1),
            max_score=self.MAX_SCORES["technical_momentum"],
            weight=self.WEIGHTS["technical_momentum"],
            details=details,
        )

    def calculate_sector_momentum(
        self,
        sector_score: SectorScore,
    ) -> ComponentScore:
        """Calculate Sector Momentum score (max: 10, weight: 10).

        Args:
            sector_score: Sector score data.

        Returns:
            ComponentScore with research profile format.
        """
        # Use overall sector score (0-100) and convert to component score
        sector_100 = sector_score.overall_score
        component_score = (sector_100 / 100) * self.MAX_SCORES["sector_momentum"]

        details = f"Sector: {sector_score.sector}, Signal: {sector_score.rotation_signal}"

        return ComponentScore(
            name="Sector Momentum",
            score=round(component_score, 1),
            max_score=self.MAX_SCORES["sector_momentum"],
            weight=self.WEIGHTS["sector_momentum"],
            details=details,
        )

    def calculate_management_guidance(
        self,
        management_score: GuidanceScore,
    ) -> ComponentScore:
        """Calculate Management Guidance score (max: 10, weight: 10).

        Args:
            management_score: Management guidance data.

        Returns:
            ComponentScore with research profile format.
        """
        # Simple scoring based on sentiment
        sentiment_map = {"Positive": 90, "Neutral": 50, "Negative": 20}
        base_score = sentiment_map.get(management_score.overall_sentiment, 50)

        # Adjust for confidence
        confidence_map = {"High": 10, "Medium": 0, "Low": -10}
        confidence_adj = confidence_map.get(management_score.management_confidence, 0)

        guidance_100 = base_score + confidence_adj
        component_score = (guidance_100 / 100) * self.MAX_SCORES["management_guidance"]

        details = f"Sentiment: {management_score.overall_sentiment}, Confidence: {management_score.management_confidence}"

        return ComponentScore(
            name="Management Guidance",
            score=round(component_score, 1),
            max_score=self.MAX_SCORES["management_guidance"],
            weight=self.WEIGHTS["management_guidance"],
            details=details,
        )

    def calculate_institutional_buying(
        self,
        institutional_score: float,
    ) -> ComponentScore:
        """Calculate Institutional Buying score (max: 10, weight: 10).

        Args:
            institutional_score: Institutional buying score (0-100).

        Returns:
            ComponentScore with research profile format.
        """
        component_score = (institutional_score / 100) * self.MAX_SCORES["institutional_buying"]

        details = f"Institutional Score: {institutional_score:.1f}/100"

        return ComponentScore(
            name="Institutional Buying",
            score=round(component_score, 1),
            max_score=self.MAX_SCORES["institutional_buying"],
            weight=self.WEIGHTS["institutional_buying"],
            details=details,
        )

    def calculate_valuation(
        self,
        valuation_score: float,
    ) -> ComponentScore:
        """Calculate Valuation score (max: 5, weight: 5).

        Args:
            valuation_score: Valuation score (0-100).

        Returns:
            ComponentScore with research profile format.
        """
        component_score = (valuation_score / 100) * self.MAX_SCORES["valuation"]

        details = f"Valuation Score: {valuation_score:.1f}/100"

        return ComponentScore(
            name="Valuation",
            score=round(component_score, 1),
            max_score=self.MAX_SCORES["valuation"],
            weight=self.WEIGHTS["valuation"],
            details=details,
        )

    def calculate_order_book(
        self,
        order_book_score: float,
    ) -> ComponentScore:
        """Calculate Order Book score (max: 5, weight: 5).

        Args:
            order_book_score: Order book score (0-100).

        Returns:
            ComponentScore with research profile format.
        """
        component_score = (order_book_score / 100) * self.MAX_SCORES["order_book"]

        details = f"Order Book Score: {order_book_score:.1f}/100"

        return ComponentScore(
            name="Order Book",
            score=round(component_score, 1),
            max_score=self.MAX_SCORES["order_book"],
            weight=self.WEIGHTS["order_book"],
            details=details,
        )

    def calculate_risk(
        self,
        risk_score: float,
    ) -> ComponentScore:
        """Calculate Risk score (max: 5, weight: 5).

        Args:
            risk_score: Risk score (0-100).

        Returns:
            ComponentScore with research profile format.
        """
        component_score = (risk_score / 100) * self.MAX_SCORES["risk"]

        details = f"Risk Score: {risk_score:.1f}/100"

        return ComponentScore(
            name="Risk",
            score=round(component_score, 1),
            max_score=self.MAX_SCORES["risk"],
            weight=self.WEIGHTS["risk"],
            details=details,
        )

    def calculate_earnings_surprise_probability(
        self,
        earnings_score: float,
    ) -> ComponentScore:
        """Calculate Earnings Surprise Probability score (max: 5, weight: 5).

        Args:
            earnings_score: Earnings surprise score (0-100).

        Returns:
            ComponentScore with research profile format.
        """
        component_score = (earnings_score / 100) * self.MAX_SCORES["earnings_surprise_probability"]

        details = f"Earnings Surprise Score: {earnings_score:.1f}/100"

        return ComponentScore(
            name="Earnings Surprise Probability",
            score=round(component_score, 1),
            max_score=self.MAX_SCORES["earnings_surprise_probability"],
            weight=self.WEIGHTS["earnings_surprise_probability"],
            details=details,
        )

    def calculate_overall_score(self, components: AlphaScoreComponents) -> float:
        """Calculate overall Alpha Score from components.

        Args:
            components: AlphaScoreComponents with ComponentScore objects.

        Returns:
            Overall score (0-100).
        """
        total_weighted = 0
        total_weight = 0

        for component in [
            components.financial_quality,
            components.growth_acceleration,
            components.technical_momentum,
            components.sector_momentum,
            components.management_guidance,
            components.institutional_buying,
            components.valuation,
            components.order_book,
            components.risk,
            components.earnings_surprise_probability,
        ]:
            total_weighted += component.score * component.weight
            total_weight += component.weight

        return total_weighted / total_weight if total_weight > 0 else 0

    def _normalize_score(self, value: float, min_val: float, max_val: float) -> float:
        """Normalize a value to 0-100 range.

        Args:
            value: Value to normalize.
            min_val: Minimum expected value.
            max_val: Maximum expected value.

        Returns:
            Normalized score (0-100).
        """
        if max_val == min_val:
            return 50.0

        normalized = ((value - min_val) / (max_val - min_val)) * 100
        return max(0, min(100, normalized))

    def _normalize_rsi(self, rsi: float) -> float:
        """Normalize RSI to 0-100 score.

        Args:
            rsi: RSI value.

        Returns:
            Normalized score (0-100).
        """
        # RSI > 50 is bullish, RSI < 50 is bearish
        if rsi >= 50:
            return min(100, 50 + (rsi - 50) * 2)
        else:
            return max(0, 50 + (rsi - 50) * 2)

    def _normalize_macd(self, macd: float, signal: float) -> float:
        """Normalize MACD to 0-100 score.

        Args:
            macd: MACD value.
            signal: MACD signal line.

        Returns:
            Normalized score (0-100).
        """
        if macd > signal:
            return min(100, 50 + (macd - signal) * 20)
        else:
            return max(0, 50 + (macd - signal) * 20)

    def _normalize_ema_trend(self, ema_20: float, sma_50: float) -> float:
        """Normalize EMA trend to 0-100 score.

        Args:
            ema_20: 20-day EMA.
            sma_50: 50-day SMA.

        Returns:
            Normalized score (0-100).
        """
        if ema_20 > sma_50:
            return min(100, 50 + ((ema_20 - sma_50) / sma_50) * 500)
        else:
            return max(0, 50 + ((ema_20 - sma_50) / sma_50) * 500)
