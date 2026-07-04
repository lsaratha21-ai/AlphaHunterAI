"""Risk-adjusted return calculator for opportunity ranking."""

from __future__ import annotations

from typing import Any

from app.alpha import AlphaScore, AlphaScoreComponents
from app.ranking.models import RiskAdjustedMetrics


class RiskAdjustedCalculator:
    """Calculator for risk-adjusted performance metrics."""

    def __init__(self) -> None:
        """Initialize the calculator."""
        pass

    def calculate_metrics(
        self,
        alpha_score: AlphaScore,
        target_return: float = 15.0,
        max_downside: float = 8.0,
        time_horizon_months: int = 3,
    ) -> RiskAdjustedMetrics:
        """Calculate risk-adjusted metrics for an opportunity.

        Args:
            alpha_score: AlphaScore from research profile.
            target_return: Target return percentage (default 15%).
            max_downside: Maximum acceptable downside percentage (default 8%).
            time_horizon_months: Investment horizon in months (default 3).

        Returns:
            RiskAdjustedMetrics with calculated metrics.
        """
        # Calculate expected return range based on Alpha Score
        overall_score = alpha_score.overall_score
        
        # Higher Alpha Score = higher expected returns, lower risk
        expected_return_min = self._calculate_min_return(overall_score, target_return)
        expected_return_max = self._calculate_max_return(overall_score, target_return)
        expected_return_avg = (expected_return_min + expected_return_max) / 2
        
        # Calculate downside risk
        downside_risk = self._calculate_downside_risk(overall_score, max_downside)
        
        # Calculate probability of success
        probability_of_success = self._calculate_success_probability(overall_score, alpha_score.confidence)
        
        # Calculate risk/reward ratio
        risk_reward_ratio = self._calculate_risk_reward_ratio(
            expected_return_avg,
            downside_risk,
        )
        
        # Calculate Sharpe ratio (simplified)
        sharpe_ratio = self._calculate_sharpe_ratio(
            expected_return_avg,
            downside_risk,
        )
        
        # Calculate max drawdown risk
        max_drawdown_risk = self._calculate_max_drawdown_risk(
            overall_score,
            alpha_score.components,
        )
        
        # Calculate volatility risk
        volatility_risk = self._calculate_volatility_risk(
            overall_score,
            alpha_score.components,
        )
        
        return RiskAdjustedMetrics(
            expected_return_min=round(expected_return_min, 1),
            expected_return_max=round(expected_return_max, 1),
            expected_return_avg=round(expected_return_avg, 1),
            downside_risk=round(downside_risk, 1),
            probability_of_success=round(probability_of_success, 1),
            risk_reward_ratio=round(risk_reward_ratio, 2),
            sharpe_ratio=round(sharpe_ratio, 2),
            max_drawdown_risk=round(max_drawdown_risk, 1),
            volatility_risk=round(volatility_risk, 1),
        )

    def _calculate_min_return(self, alpha_score: float, target_return: float) -> float:
        """Calculate minimum expected return based on Alpha Score.

        Args:
            alpha_score: Overall Alpha Score (0-100).
            target_return: Target return percentage.

        Returns:
            Minimum expected return percentage.
        """
        # Lower bound: target_return * (alpha_score / 100) * 0.6
        return target_return * (alpha_score / 100) * 0.6

    def _calculate_max_return(self, alpha_score: float, target_return: float) -> float:
        """Calculate maximum expected return based on Alpha Score.

        Args:
            alpha_score: Overall Alpha Score (0-100).
            target_return: Target return percentage.

        Returns:
            Maximum expected return percentage.
        """
        # Upper bound: target_return * (alpha_score / 100) * 1.4
        return target_return * (alpha_score / 100) * 1.4

    def _calculate_downside_risk(self, alpha_score: float, max_downside: float) -> float:
        """Calculate downside risk based on Alpha Score.

        Args:
            alpha_score: Overall Alpha Score (0-100).
            max_downside: Maximum acceptable downside percentage.

        Returns:
            Estimated downside risk percentage.
        """
        # Higher Alpha Score = lower downside risk
        risk_factor = 1 - (alpha_score / 100)
        return max_downside * risk_factor

    def _calculate_success_probability(
        self,
        alpha_score: float,
        confidence: float,
    ) -> float:
        """Calculate probability of achieving target return.

        Args:
            alpha_score: Overall Alpha Score (0-100).
            confidence: Confidence score (0-100).

        Returns:
            Probability of success percentage.
        """
        # Weighted average of alpha score and confidence
        return (alpha_score * 0.6 + confidence * 0.4)

    def _calculate_risk_reward_ratio(
        self,
        expected_return: float,
        downside_risk: float,
    ) -> float:
        """Calculate risk/reward ratio.

        Args:
            expected_return: Expected return percentage.
            downside_risk: Downside risk percentage.

        Returns:
            Risk/reward ratio.
        """
        if downside_risk == 0:
            return 0.0
        return expected_return / downside_risk

    def _calculate_sharpe_ratio(
        self,
        expected_return: float,
        downside_risk: float,
    ) -> float:
        """Calculate simplified Sharpe ratio.

        Args:
            expected_return: Expected return percentage.
            downside_risk: Downside risk percentage.

        Returns:
            Sharpe ratio.
        """
        # Assuming risk-free rate of 5%
        risk_free_rate = 5.0
        excess_return = expected_return - risk_free_rate
        
        if downside_risk == 0:
            return 0.0
        return excess_return / downside_risk

    def _calculate_max_drawdown_risk(
        self,
        alpha_score: float,
        components: AlphaScoreComponents,
    ) -> float:
        """Calculate maximum drawdown risk.

        Args:
            alpha_score: Overall Alpha Score.
            components: Component scores.

        Returns:
            Maximum drawdown risk percentage.
        """
        # Risk component inversely affects drawdown risk
        risk_score = components.risk.percentage if components.risk else 50.0
        base_drawdown = 15.0  # Base drawdown risk
        
        # Higher risk score = lower drawdown risk
        risk_adjustment = 1 - (risk_score / 100)
        return base_drawdown * risk_adjustment

    def _calculate_volatility_risk(
        self,
        alpha_score: float,
        components: AlphaScoreComponents,
    ) -> float:
        """Calculate volatility risk.

        Args:
            alpha_score: Overall Alpha Score.
            components: Component scores.

        Returns:
            Volatility risk percentage.
        """
        # Technical momentum affects volatility
        tech_score = components.technical_momentum.percentage if components.technical_momentum else 50.0
        base_volatility = 20.0  # Base volatility risk
        
        # Higher technical score = lower volatility risk
        volatility_adjustment = 1 - (tech_score / 100)
        return base_volatility * volatility_adjustment
