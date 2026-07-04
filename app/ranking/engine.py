"""Opportunity ranking engine for risk-adjusted opportunity selection."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.alpha import AlphaScore
from app.ranking.calculator import RiskAdjustedCalculator
from app.ranking.models import Catalyst, Evidence, OpportunityRanking, RiskAdjustedMetrics


class OpportunityRankingEngine:
    """Engine for ranking opportunities by risk-adjusted returns."""

    def __init__(self) -> None:
        """Initialize the OpportunityRankingEngine."""
        self.calculator = RiskAdjustedCalculator()

    def rank_opportunities(
        self,
        alpha_scores: list[AlphaScore],
        target_return: float = 15.0,
        max_downside: float = 8.0,
        time_horizon_months: int = 3,
        max_opportunities: int = 10,
    ) -> list[OpportunityRanking]:
        """Rank opportunities by risk-adjusted returns.

        Args:
            alpha_scores: List of AlphaScore recommendations.
            target_return: Target return percentage (default 15%).
            max_downside: Maximum acceptable downside percentage (default 8%).
            time_horizon_months: Investment horizon in months (default 3).
            max_opportunities: Maximum number of opportunities to return.

        Returns:
            List of OpportunityRanking sorted by risk-adjusted return.
        """
        opportunities = []

        for alpha_score in alpha_scores:
            # Calculate risk-adjusted metrics
            metrics = self.calculator.calculate_metrics(
                alpha_score,
                target_return,
                max_downside,
                time_horizon_months,
            )

            # Generate catalysts
            catalysts = self._generate_catalysts(alpha_score)

            # Generate evidence
            evidence = self._generate_evidence(alpha_score)

            # Calculate position size based on risk-adjusted metrics
            position_size = self._calculate_position_size(metrics, alpha_score)

            # Calculate entry range
            current_price = alpha_score.current_price or 1000.0
            entry_range_low = current_price * 0.98
            entry_range_high = current_price * 1.02

            # Calculate target and stop loss
            target_price = alpha_score.target_price or (current_price * 1.20)
            stop_loss = alpha_score.stop_loss or (current_price * 0.88)

            # Create opportunity ranking
            opportunity = OpportunityRanking(
                symbol=alpha_score.symbol,
                company_name=alpha_score.symbol,  # Would be company name in real implementation
                alpha_score=alpha_score.overall_score,
                confidence_score=alpha_score.confidence,
                risk_adjusted_metrics=metrics,
                catalysts=catalysts,
                evidence=evidence,
                position_size=position_size,
                ranking=0,  # Will be set after sorting
                current_price=current_price,
                entry_range_low=round(entry_range_low, 2),
                entry_range_high=round(entry_range_high, 2),
                target_price=round(target_price, 2),
                stop_loss=round(stop_loss, 2),
                time_horizon_months=time_horizon_months,
                reasoning=alpha_score.reasoning,
                created_at=datetime.now(),
            )

            opportunities.append(opportunity)

        # Sort by risk-adjusted return (Sharpe ratio)
        opportunities.sort(
            key=lambda x: (
                x.risk_adjusted_metrics.sharpe_ratio,
                x.risk_adjusted_metrics.probability_of_success,
            ),
            reverse=True,
        )

        # Filter by criteria
        filtered_opportunities = [
            op
            for op in opportunities
            if (
                op.risk_adjusted_metrics.downside_risk <= max_downside
                and op.risk_adjusted_metrics.probability_of_success >= 60
            )
        ]

        # Limit to max opportunities
        filtered_opportunities = filtered_opportunities[:max_opportunities]

        # Set rankings
        for i, op in enumerate(filtered_opportunities, 1):
            op.ranking = i

        return filtered_opportunities

    def _generate_catalysts(self, alpha_score: AlphaScore) -> list[Catalyst]:
        """Generate catalysts based on AlphaScore components.

        Args:
            alpha_score: AlphaScore from research profile.

        Returns:
            List of Catalyst objects.
        """
        catalysts = []

        # Growth catalyst
        if alpha_score.components.growth_acceleration.percentage >= 75:
            catalysts.append(Catalyst(
                type="earnings",
                description="Strong growth acceleration expected",
                expected_impact="high",
                timeline="short-term",
                probability=alpha_score.components.growth_acceleration.percentage,
            ))

        # Technical catalyst
        if alpha_score.components.technical_momentum.percentage >= 75:
            catalysts.append(Catalyst(
                type="technical",
                description="Positive technical momentum breakout",
                expected_impact="medium",
                timeline="short-term",
                probability=alpha_score.components.technical_momentum.percentage,
            ))

        # Institutional catalyst
        if alpha_score.components.institutional_buying.percentage >= 75:
            catalysts.append(Catalyst(
                type="institutional",
                description="Rising institutional ownership",
                expected_impact="high",
                timeline="medium-term",
                probability=alpha_score.components.institutional_buying.percentage,
            ))

        # Sector catalyst
        if alpha_score.components.sector_momentum.percentage >= 75:
            catalysts.append(Catalyst(
                type="sector_rotation",
                description="Positive sector momentum",
                expected_impact="medium",
                timeline="medium-term",
                probability=alpha_score.components.sector_momentum.percentage,
            ))

        return catalysts

    def _generate_evidence(self, alpha_score: AlphaScore) -> list[Evidence]:
        """Generate supporting evidence based on AlphaScore components.

        Args:
            alpha_score: AlphaScore from research profile.

        Returns:
            List of Evidence objects.
        """
        evidence = []

        # Financial evidence
        if alpha_score.components.financial_quality.percentage >= 80:
            evidence.append(Evidence(
                type="financial",
                description="Strong financial quality metrics",
                strength="strong",
                data_point=f"Financial Quality: {alpha_score.components.financial_quality}",
            ))

        # Technical evidence
        if alpha_score.components.technical_momentum.percentage >= 75:
            evidence.append(Evidence(
                type="technical",
                description="Positive technical indicators",
                strength="strong",
                data_point=f"Technical Momentum: {alpha_score.components.technical_momentum}",
            ))

        # Management evidence
        if alpha_score.components.management_guidance.percentage >= 75:
            evidence.append(Evidence(
                type="management",
                description="Confident management guidance",
                strength="moderate",
                data_point=f"Management Guidance: {alpha_score.components.management_guidance}",
            ))

        return evidence

    def _calculate_position_size(
        self,
        metrics: RiskAdjustedMetrics,
        alpha_score: AlphaScore,
    ) -> float:
        """Calculate recommended position size based on risk-adjusted metrics.

        Args:
            metrics: Risk-adjusted metrics.
            alpha_score: AlphaScore from research profile.

        Returns:
            Recommended position size percentage.
        """
        # Base position size based on Sharpe ratio
        base_size = min(metrics.sharpe_ratio * 5, 25)  # Max 25%

        # Adjust for confidence
        confidence_adjustment = alpha_score.confidence / 100

        # Adjust for downside risk
        risk_adjustment = 1 - (metrics.downside_risk / 15)

        # Calculate final position size
        position_size = base_size * confidence_adjustment * risk_adjustment

        # Ensure reasonable bounds
        return max(5.0, min(position_size, 20.0))  # Between 5% and 20%
