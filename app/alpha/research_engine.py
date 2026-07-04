"""Research Profile engine for generating investment research profiles."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.alpha.models import AlphaScore, AlphaScoreComponents
from app.alpha.research_scorers import ResearchScorer
from app.financials import FinancialEngine, FinancialScore
from app.management import GuidanceEngine, GuidanceScore
from app.sectors import SectorRotationEngine, SectorScore
from app.technical import TechnicalEngine, TechnicalScore


class ResearchProfileEngine:
    """Engine for generating Research Profiles with component-level scoring."""

    def __init__(self) -> None:
        """Initialize the ResearchProfileEngine."""
        self.scorer = ResearchScorer()
        self.financial_engine = FinancialEngine()
        self.technical_engine = TechnicalEngine()
        self.sector_engine = SectorRotationEngine()
        self.management_engine = GuidanceEngine()

    def generate_research_profile(
        self,
        symbol: str,
        current_price: float,
        financial_data: dict[str, Any],
        technical_data: dict[str, Any],
        sector_data: dict[str, Any],
        management_data: dict[str, Any],
        institutional_score: float,
        order_book_score: float,
        risk_score: float,
        earnings_surprise_score: float,
    ) -> AlphaScore:
        """Generate complete research profile for a stock.

        Args:
            symbol: Stock symbol.
            current_price: Current stock price.
            financial_data: Financial data dictionary.
            technical_data: Technical data dictionary.
            sector_data: Sector data dictionary.
            management_data: Management data dictionary.
            institutional_score: Institutional buying score (0-100).
            order_book_score: Order book score (0-100).
            risk_score: Risk score (0-100).
            earnings_surprise_score: Earnings surprise score (0-100).

        Returns:
            AlphaScore with research profile components.
        """
        # Calculate component scores using ResearchScorer
        financial_score = self._create_financial_score(financial_data)
        technical_score = self._create_technical_score(technical_data)
        sector_score = self._create_sector_score(sector_data)
        management_score = self._create_management_score(management_data)

        # Calculate component-level scores
        financial_quality = self.scorer.calculate_financial_quality(financial_score)
        growth_acceleration = self.scorer.calculate_growth_acceleration(financial_score)
        technical_momentum = self.scorer.calculate_technical_momentum(technical_score)
        sector_momentum = self.scorer.calculate_sector_momentum(sector_score)
        management_guidance = self.scorer.calculate_management_guidance(management_score)
        institutional_buying = self.scorer.calculate_institutional_buying(institutional_score)
        valuation = self.scorer.calculate_valuation(financial_data.get("valuation_score", 50))
        order_book = self.scorer.calculate_order_book(order_book_score)
        risk = self.scorer.calculate_risk(risk_score)
        earnings_surprise = self.scorer.calculate_earnings_surprise_probability(earnings_surprise_score)

        # Create components object
        components = AlphaScoreComponents(
            financial_quality=financial_quality,
            growth_acceleration=growth_acceleration,
            technical_momentum=technical_momentum,
            sector_momentum=sector_momentum,
            management_guidance=management_guidance,
            institutional_buying=institutional_buying,
            valuation=valuation,
            order_book=order_book,
            risk=risk,
            earnings_surprise_probability=earnings_surprise,
        )

        # Calculate overall score
        overall_score = self.scorer.calculate_overall_score(components)

        # Determine action and confidence
        action = self._determine_action(overall_score)
        confidence = self._calculate_confidence(overall_score, components)

        # Calculate target price and stop loss
        target_price, stop_loss = self._calculate_target_stop_loss(
            current_price,
            components,
            overall_score,
        )

        # Generate reasoning
        reasoning = self._generate_reasoning(components, overall_score, action)

        return AlphaScore(
            symbol=symbol,
            overall_score=overall_score,
            components=components,
            action=action,
            confidence=confidence,
            target_price=target_price,
            stop_loss=stop_loss,
            current_price=current_price,
            reasoning=reasoning,
            timestamp=datetime.now(),
        )

    def _create_financial_score(self, financial_data: dict[str, Any]) -> FinancialScore:
        """Create FinancialScore from dictionary data.

        Args:
            financial_data: Financial data dictionary.

        Returns:
            FinancialScore object.
        """
        return FinancialScore(
            symbol=financial_data.get("symbol", ""),
            revenue_growth=financial_data.get("revenue_growth", 0),
            profit_growth=financial_data.get("profit_growth", 0),
            eps_growth=financial_data.get("eps_growth", 0),
            roe=financial_data.get("roe", 0),
            roce=financial_data.get("roce", 0),
            debt_to_equity=financial_data.get("debt_to_equity", 0),
            operating_cash_flow=financial_data.get("operating_cash_flow", 0),
            free_cash_flow=financial_data.get("free_cash_flow", 0),
            peg=financial_data.get("peg", 0),
            book_value_growth=financial_data.get("book_value_growth", 0),
        )

    def _create_technical_score(self, technical_data: dict[str, Any]) -> TechnicalScore:
        """Create TechnicalScore from dictionary data.

        Args:
            technical_data: Technical data dictionary.

        Returns:
            TechnicalScore object.
        """
        return TechnicalScore(
            symbol=technical_data.get("symbol", ""),
            rsi=technical_data.get("rsi", 50),
            macd=technical_data.get("macd", 0),
            macd_signal=technical_data.get("macd_signal", 0),
            macd_histogram=technical_data.get("macd_histogram", 0),
            ema_20=technical_data.get("ema_20", 0),
            sma_50=technical_data.get("sma_50", 0),
            sma_200=technical_data.get("sma_200", 0),
            adx=technical_data.get("adx", 25),
            atr=technical_data.get("atr", 0),
            supertrend=technical_data.get("supertrend", 0),
            supertrend_signal=technical_data.get("supertrend_signal", "neutral"),
            bollinger_upper=technical_data.get("bollinger_upper", 0),
            bollinger_middle=technical_data.get("bollinger_middle", 0),
            bollinger_lower=technical_data.get("bollinger_lower", 0),
            vwap=technical_data.get("vwap", 0),
            volume_breakout=technical_data.get("volume_breakout", False),
            delivery_percentage=technical_data.get("delivery_percentage", 0),
        )

    def _create_sector_score(self, sector_data: dict[str, Any]) -> SectorScore:
        """Create SectorScore from dictionary data.

        Args:
            sector_data: Sector data dictionary.

        Returns:
            SectorScore object.
        """
        return SectorScore(
            sector=sector_data.get("sector", ""),
            government_score=sector_data.get("government_score", 50),
            order_book_score=sector_data.get("order_book_score", 50),
            commodity_score=sector_data.get("commodity_score", 50),
            news_score=sector_data.get("news_score", 50),
            institutional_score=sector_data.get("institutional_score", 50),
            overall_score=sector_data.get("overall_score", 50),
            rotation_signal=sector_data.get("rotation_signal", "neutral"),
        )

    def _create_management_score(self, management_data: dict[str, Any]) -> GuidanceScore:
        """Create GuidanceScore from dictionary data.

        Args:
            management_data: Management data dictionary.

        Returns:
            GuidanceScore object.
        """
        return GuidanceScore(
            symbol=management_data.get("symbol", ""),
            document_type=management_data.get("document_type", ""),
            revenue_outlook=management_data.get("revenue_outlook"),
            margin_outlook=management_data.get("margin_outlook"),
            demand=management_data.get("demand"),
            order_book=management_data.get("order_book"),
            capex=management_data.get("capex"),
            expansion=management_data.get("expansion"),
            management_confidence=management_data.get("management_confidence"),
            overall_sentiment=management_data.get("overall_sentiment"),
        )

    def _determine_action(self, overall_score: float) -> str:
        """Determine action based on overall score.

        Args:
            overall_score: Overall Alpha Score.

        Returns:
            Action string (buy, hold, sell).
        """
        if overall_score >= 70:
            return "buy"
        elif overall_score <= 30:
            return "sell"
        else:
            return "hold"

    def _calculate_confidence(
        self,
        overall_score: float,
        components: AlphaScoreComponents,
    ) -> float:
        """Calculate confidence level based on score and component consistency.

        Args:
            overall_score: Overall Alpha Score.
            components: Component scores.

        Returns:
            Confidence score (0-100).
        """
        # Base confidence from score extremeness
        if overall_score >= 80 or overall_score <= 20:
            base_confidence = 80
        elif overall_score >= 70 or overall_score <= 30:
            base_confidence = 70
        else:
            base_confidence = 50

        # Check component consistency
        component_scores = [
            components.financial_quality.percentage,
            components.growth_acceleration.percentage,
            components.technical_momentum.percentage,
        ]
        avg_component = sum(component_scores) / len(component_scores)
        variance = sum((score - avg_component) ** 2 for score in component_scores) / len(component_scores)

        # High variance reduces confidence
        consistency_penalty = min(20, variance / 100)

        return max(0, min(100, base_confidence - consistency_penalty))

    def _calculate_target_stop_loss(
        self,
        current_price: float,
        components: AlphaScoreComponents,
        overall_score: float,
    ) -> tuple[float, float]:
        """Calculate target price and stop loss.

        Args:
            current_price: Current stock price.
            components: Component scores.
            overall_score: Overall Alpha Score.

        Returns:
            Tuple of (target_price, stop_loss).
        """
        # Risk-adjusted target calculation
        risk_adjustment = (100 - components.risk.percentage) / 100
        growth_factor = components.growth_acceleration.percentage / 100

        target = current_price * (1 + (overall_score / 200) * growth_factor * risk_adjustment)
        stop_loss = current_price * (1 - (0.05 + (1 - overall_score / 100) * 0.10))

        return target, stop_loss

    def _generate_reasoning(
        self,
        components: AlphaScoreComponents,
        overall_score: float,
        action: str,
    ) -> str:
        """Generate reasoning for the recommendation.

        Args:
            components: Component scores.
            overall_score: Overall Alpha Score.
            action: Recommended action.

        Returns:
            Reasoning string.
        """
        strengths = []
        weaknesses = []

        if components.financial_quality.percentage >= 80:
            strengths.append("strong financial quality")
        elif components.financial_quality.percentage <= 40:
            weaknesses.append("weak financial quality")

        if components.growth_acceleration.percentage >= 80:
            strengths.append("strong growth momentum")
        elif components.growth_acceleration.percentage <= 40:
            weaknesses.append("weak growth momentum")

        if components.technical_momentum.percentage >= 80:
            strengths.append("positive technical momentum")
        elif components.technical_momentum.percentage <= 40:
            weaknesses.append("negative technical momentum")

        if components.management_guidance.percentage >= 80:
            strengths.append("confident management guidance")
        elif components.management_guidance.percentage <= 40:
            weaknesses.append("weak management guidance")

        if components.institutional_buying.percentage >= 80:
            strengths.append("strong institutional interest")
        elif components.institutional_buying.percentage <= 40:
            weaknesses.append("weak institutional interest")

        reasoning = f"Overall Score: {overall_score:.1f}/100. "

        if action == "buy":
            reasoning += "Recommendation: BUY. "
            if strengths:
                reasoning += "Key strengths: " + ", ".join(strengths) + ". "
            if weaknesses:
                reasoning += "Monitor: " + ", ".join(weaknesses) + "."
        elif action == "sell":
            reasoning += "Recommendation: SELL. "
            if weaknesses:
                reasoning += "Key concerns: " + ", ".join(weaknesses) + ". "
            if strengths:
                reasoning += "Offsetting factors: " + ", ".join(strengths) + "."
        else:
            reasoning += "Recommendation: HOLD. "
            if strengths:
                reasoning += "Strengths: " + ", ".join(strengths) + ". "
            if weaknesses:
                reasoning += "Concerns: " + ", ".join(weaknesses) + "."

        return reasoning
