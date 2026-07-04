"""Alpha Score engine with layered scoring model."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.alpha.models import AlphaScore, AlphaScoreComponents
from app.alpha.scorers import AlphaScorer
from app.financials import FinancialEngine, FinancialScore
from app.management import GuidanceEngine, GuidanceScore
from app.recommendation import Recommendation
from app.sectors import SectorRotationEngine, SectorScore
from app.technical import TechnicalEngine, TechnicalScore


class AlphaScoreEngine:
    """Engine for calculating Alpha Score with layered scoring model."""

    def __init__(self) -> None:
        """Initialize the AlphaScoreEngine."""
        self.scorer = AlphaScorer()
        self.financial_engine = FinancialEngine()
        self.technical_engine = TechnicalEngine()
        self.sector_engine = SectorRotationEngine()
        self.management_engine = GuidanceEngine()

    def calculate_alpha_score(
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
        """Calculate Alpha Score for a stock.

        Args:
            symbol: Stock symbol.
            current_price: Current stock price.
            financial_data: Financial data dictionary.
            technical_data: Technical data dictionary.
            sector_data: Sector data dictionary.
            management_data: Management data dictionary.
            institutional_score: Institutional buying score (0-100).
            order_book_score: Order book score (-50 to 50).
            risk_score: Risk score (0-100, lower is better).
            earnings_surprise_score: Earnings surprise probability (0-100).

        Returns:
            AlphaScore with all components and overall score.
        """
        # Calculate individual scores
        financial_score = self.financial_engine.calculate_financial_score(financial_data)
        technical_score = self.technical_engine.calculate_technical_score(technical_data)
        sector_score = self.sector_engine.calculate_sector_score(sector_data)
        management_score = self.management_engine.calculate_guidance_score(management_data)

        # Calculate Alpha Score components
        components = self.scorer.calculate_all_components(
            financial_score=financial_score,
            technical_score=technical_score,
            sector_score=sector_score,
            management_score=management_score,
            institutional_score=institutional_score,
            current_price=current_price,
            order_book_score=order_book_score,
            risk_score=risk_score,
            earnings_surprise_score=earnings_surprise_score,
        )

        # Calculate overall Alpha Score
        overall_score = self.scorer.calculate_overall_alpha_score(components)

        # Determine action based on overall score
        action = self._determine_action(overall_score)

        # Calculate confidence
        confidence = self._calculate_confidence(components, overall_score)

        # Calculate target and stop loss
        target_price, stop_loss = self._calculate_target_stop_loss(
            current_price,
            components,
            overall_score,
        )

        # Generate reasoning
        reasoning = self._generate_reasoning(components, overall_score, action)

        alpha_score = AlphaScore(
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

        return alpha_score

    def _determine_action(self, overall_score: float) -> str:
        """Determine buy/hold/sell action based on overall score.

        Args:
            overall_score: Overall Alpha Score (0-100).

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
        components: AlphaScoreComponents,
        overall_score: float,
    ) -> float:
        """Calculate confidence level for the recommendation.

        Args:
            components: Alpha Score components.
            overall_score: Overall Alpha Score.

        Returns:
            Confidence score (0-100).
        """
        # Higher confidence when scores are extreme and consistent
        score_extremeness = abs(overall_score - 50) * 2  # 0-100

        # Check consistency of components (all high or all low)
        component_values = [
            components.financial_quality,
            components.growth_acceleration,
            components.technical_momentum,
            components.sector_momentum,
            components.management_guidance,
            components.institutional_buying,
        ]

        avg_component = sum(component_values) / len(component_values)
        variance = sum((x - avg_component) ** 2 for x in component_values) / len(component_values)
        consistency = max(0, 100 - variance)  # Lower variance = higher consistency

        confidence = (score_extremeness * 0.6) + (consistency * 0.4)
        return min(100, max(0, confidence))

    def _calculate_target_stop_loss(
        self,
        current_price: float,
        components: AlphaScoreComponents,
        overall_score: float,
    ) -> tuple[float, float]:
        """Calculate target price and stop loss.

        Args:
            current_price: Current stock price.
            components: Alpha Score components.
            overall_score: Overall Alpha Score.

        Returns:
            Tuple of (target_price, stop_loss).
        """
        # Risk-adjusted target based on overall score
        risk_factor = 1 + (overall_score - 50) / 100  # 0.5 to 1.5

        # Use risk score to adjust volatility assumption
        volatility_factor = 1 + (components.risk - 50) / 100

        # Target price: 10-20% upside for good scores
        if overall_score >= 70:
            target_price = current_price * 1.15 * risk_factor
        elif overall_score <= 30:
            target_price = current_price * 0.85 * risk_factor
        else:
            target_price = current_price * 1.05 * risk_factor

        # Stop loss: 8-12% downside
        stop_loss = current_price * (1 - 0.10 * volatility_factor)

        return round(target_price, 2), round(stop_loss, 2)

    def _generate_reasoning(
        self,
        components: AlphaScoreComponents,
        overall_score: float,
        action: str,
    ) -> str:
        """Generate reasoning text for the recommendation.

        Args:
            components: Alpha Score components.
            overall_score: Overall Alpha Score.
            action: Recommended action.

        Returns:
            Reasoning string.
        """
        reasoning_parts = []

        # Overall assessment
        reasoning_parts.append(f"Alpha Score: {overall_score:.1f}/100")

        # Highlight top strengths
        component_scores = components.to_dict()
        top_components = sorted(
            component_scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )[:3]

        reasoning_parts.append("Key strengths:")
        for name, score in top_components:
            if score >= 70:
                reasoning_parts.append(f"- {name.replace('_', ' ').title()}: {score:.1f}")

        # Highlight weaknesses
        weak_components = [
            (name, score) for name, score in component_scores.items()
            if score <= 40
        ]

        if weak_components:
            reasoning_parts.append("Areas of concern:")
            for name, score in weak_components[:2]:
                reasoning_parts.append(f"- {name.replace('_', ' ').title()}: {score:.1f}")

        # Action rationale
        if action == "buy":
            reasoning_parts.append("Strong BUY signal based on layered scoring model.")
        elif action == "sell":
            reasoning_parts.append("SELL signal due to weak fundamentals and technicals.")
        else:
            reasoning_parts.append("HOLD position - mixed signals.")

        return " | ".join(reasoning_parts)

    def calculate_alpha_scores_batch(
        self,
        symbols: list[str],
        data_sources: dict[str, dict[str, Any]],
    ) -> dict[str, AlphaScore]:
        """Calculate Alpha Scores for multiple stocks.

        Args:
            symbols: List of stock symbols.
            data_sources: Dictionary containing all data sources for each symbol.

        Returns:
            Dictionary mapping symbols to AlphaScore objects.
        """
        alpha_scores = {}

        for symbol in symbols:
            try:
                symbol_data = data_sources.get(symbol, {})
                alpha_score = self.calculate_alpha_score(
                    symbol=symbol,
                    current_price=symbol_data.get("current_price", 100.0),
                    financial_data=symbol_data.get("financial_data", {}),
                    technical_data=symbol_data.get("technical_data", {}),
                    sector_data=symbol_data.get("sector_data", {}),
                    management_data=symbol_data.get("management_data", {}),
                    institutional_score=symbol_data.get("institutional_score", 50.0),
                    order_book_score=symbol_data.get("order_book_score", 0.0),
                    risk_score=symbol_data.get("risk_score", 50.0),
                    earnings_surprise_score=symbol_data.get("earnings_surprise_score", 50.0),
                )
                alpha_scores[symbol] = alpha_score
            except Exception as e:
                print(f"Error calculating Alpha Score for {symbol}: {e}")
                continue

        return alpha_scores
