"""Portfolio construction engine for building diversified portfolios."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.alpha import AlphaScore
from app.portfolio.models import Portfolio, Position, RiskProfile


class PortfolioConstructor:
    """Engine for constructing diversified portfolios from AlphaScore recommendations."""

    def __init__(self) -> None:
        """Initialize the PortfolioConstructor."""
        self.risk_profiles = self._get_default_risk_profiles()

    def _get_default_risk_profiles(self) -> dict[str, RiskProfile]:
        """Get default risk profiles.

        Returns:
            Dictionary of risk profiles.
        """
        return {
            "conservative": RiskProfile(
                risk_tolerance="conservative",
                max_position_size=15.0,  # Max 15% per position
                max_sector_exposure=30.0,
                stop_loss_percentage=8.0,
                target_percentage=15.0,
                max_positions=8,
                min_positions=5,
            ),
            "moderate": RiskProfile(
                risk_tolerance="moderate",
                max_position_size=20.0,  # Max 20% per position
                max_sector_exposure=40.0,
                stop_loss_percentage=12.0,
                target_percentage=20.0,
                max_positions=10,
                min_positions=5,
            ),
            "aggressive": RiskProfile(
                risk_tolerance="aggressive",
                max_position_size=25.0,  # Max 25% per position
                max_sector_exposure=50.0,
                stop_loss_percentage=15.0,
                target_percentage=30.0,
                max_positions=12,
                min_positions=4,
            ),
        }

    def construct_portfolio(
        self,
        alpha_scores: list[AlphaScore],
        total_capital: float,
        risk_tolerance: str = "moderate",
        horizon_months: int = 3,
        portfolio_name: str = "AlphaHunter Portfolio",
    ) -> Portfolio:
        """Construct a diversified portfolio from AlphaScore recommendations.

        Args:
            alpha_scores: List of AlphaScore recommendations.
            total_capital: Total capital amount in INR.
            risk_tolerance: Risk tolerance (conservative, moderate, aggressive).
            horizon_months: Investment horizon in months.
            portfolio_name: Name for the portfolio.

        Returns:
            Portfolio with constructed positions.
        """
        risk_profile = self.risk_profiles.get(risk_tolerance, self.risk_profiles["moderate"])

        # Filter for buy recommendations and sort by Alpha Score
        buy_recommendations = [s for s in alpha_scores if s.action == "buy"]
        buy_recommendations.sort(key=lambda x: x.overall_score, reverse=True)

        # Limit to max positions
        recommendations = buy_recommendations[: risk_profile.max_positions]

        if len(recommendations) < risk_profile.min_positions:
            # If not enough buy recommendations, include holds
            hold_recommendations = [s for s in alpha_scores if s.action == "hold"]
            hold_recommendations.sort(key=lambda x: x.overall_score, reverse=True)
            recommendations.extend(
                hold_recommendations[: risk_profile.min_positions - len(recommendations)],
            )

        # Calculate position sizes based on Alpha Score
        positions = []
        total_alpha_score = sum(s.overall_score for s in recommendations)

        for score in recommendations:
            # Weight based on Alpha Score
            weight = (score.overall_score / total_alpha_score) * 100

            # Cap weight at max position size
            weight = min(weight, risk_profile.max_position_size)

            # Calculate position size
            position_size = (weight / 100) * total_capital

            # Calculate shares
            entry_price = score.current_price or 1000.0  # Default if not available
            shares = int(position_size / entry_price)

            # Calculate entry range (±2%)
            entry_price_low = entry_price * 0.98
            entry_price_high = entry_price * 1.02

            # Calculate stop loss and target
            stop_loss = entry_price * (1 - risk_profile.stop_loss_percentage / 100)
            target_price = entry_price * (1 + risk_profile.target_percentage / 100)

            # Use provided target/stop loss if available
            if score.target_price:
                target_price = score.target_price
            if score.stop_loss:
                stop_loss = score.stop_loss

            position = Position(
                symbol=score.symbol,
                company_name=score.symbol,  # Would be company name in real implementation
                entry_price_low=round(entry_price_low, 2),
                entry_price_high=round(entry_price_high, 2),
                stop_loss=round(stop_loss, 2),
                target_price=round(target_price, 2),
                position_size=round(position_size, 2),
                shares=shares,
                weight=round(weight, 2),
                alpha_score=score.overall_score,
                action=score.action,
                reasoning=score.reasoning,
            )
            positions.append(position)

        # Calculate cash (uninvested capital)
        invested_amount = sum(p.position_size for p in positions)
        cash = total_capital - invested_amount

        return Portfolio(
            id=self._generate_portfolio_id(),
            name=portfolio_name,
            total_capital=total_capital,
            risk_profile=risk_profile,
            positions=positions,
            cash=round(cash, 2),
            created_at=datetime.now(),
            horizon_months=horizon_months,
        )

    def _generate_portfolio_id(self) -> str:
        """Generate a unique portfolio ID.

        Returns:
            Portfolio ID string.
        """
        return f"PF-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def get_risk_profile(self, risk_tolerance: str) -> RiskProfile:
        """Get risk profile by name.

        Args:
            risk_tolerance: Risk tolerance level.

        Returns:
            RiskProfile object.
        """
        return self.risk_profiles.get(risk_tolerance, self.risk_profiles["moderate"])
