"""Sector rotation engine for weekly ranking."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from app.differentiators.models import SectorRotationRanking


class SectorRotationEngine:
    """Engine for tracking and ranking sector rotation."""

    def __init__(self) -> None:
        """Initialize the sector rotation engine."""
        self.sectors: list[str] = [
            "Technology",
            "Financials",
            "Healthcare",
            "Consumer Discretionary",
            "Consumer Staples",
            "Energy",
            "Industrials",
            "Materials",
            "Utilities",
            "Real Estate",
            "Telecommunications",
            "Media",
        ]
        self.historical_rankings: list[SectorRotationRanking] = []

    def calculate_weekly_rankings(
        self,
        sector_data: dict[str, dict[str, Any]],
        week_ending: datetime | None = None,
    ) -> list[SectorRotationRanking]:
        """Calculate weekly sector rotation rankings.

        Args:
            sector_data: Dictionary of sector data with metrics.
            week_ending: Week ending date. Defaults to current week.

        Returns:
            List of SectorRotationRanking sorted by rank.
        """
        if week_ending is None:
            week_ending = datetime.now()

        rankings = []

        for sector in self.sectors:
            data = sector_data.get(sector, {})
            ranking = self._calculate_sector_ranking(
                sector,
                data,
                week_ending,
                len(self.sectors),
            )
            rankings.append(ranking)

        # Sort by momentum score (descending)
        rankings.sort(key=lambda x: x.momentum_score, reverse=True)

        # Assign ranks
        for i, ranking in enumerate(rankings, 1):
            ranking.rank = i

        self.historical_rankings.extend(rankings)

        return rankings

    def _calculate_sector_ranking(
        self,
        sector: str,
        data: dict[str, Any],
        week_ending: datetime,
        total_sectors: int,
    ) -> SectorRotationRanking:
        """Calculate ranking for a single sector.

        Args:
            sector: Sector name.
            data: Sector data dictionary.
            week_ending: Week ending date.
            total_sectors: Total number of sectors.

        Returns:
            SectorRotationRanking for the sector.
        """
        # Extract or calculate momentum score
        momentum_score = data.get("momentum_score", 50.0)
        if "price_change" in data:
            momentum_score = self._calculate_momentum_from_price_change(data["price_change"])

        # Extract inflow/outflow data
        inflow_outflow = data.get("inflow_outflow", 0.0)

        # Calculate relative strength
        relative_strength = self._calculate_relative_strength(
            momentum_score,
            data.get("market_return", 0.0),
        )

        # Determine rotation signal
        rotation_signal = self._determine_rotation_signal(
            inflow_outflow,
            momentum_score,
        )

        return SectorRotationRanking(
            sector=sector,
            rank=0,  # Will be assigned after sorting
            total_sectors=total_sectors,
            momentum_score=momentum_score,
            inflow_outflow=inflow_outflow,
            relative_strength=relative_strength,
            rotation_signal=rotation_signal,
            week_ending=week_ending,
        )

    def _calculate_momentum_from_price_change(self, price_change: float) -> float:
        """Calculate momentum score from price change.

        Args:
            price_change: Percentage price change.

        Returns:
            Momentum score (0-100).
        """
        # Normalize price change to 0-100 range
        # Assuming typical range of -20% to +20%
        normalized = ((price_change + 20) / 40) * 100
        return max(0, min(100, normalized))

    def _calculate_relative_strength(
        self,
        sector_momentum: float,
        market_return: float,
    ) -> float:
        """Calculate relative strength vs market.

        Args:
            sector_momentum: Sector momentum score.
            market_return: Market return percentage.

        Returns:
            Relative strength score (0-100).
        """
        # Simple relative strength calculation
        # In production, use more sophisticated measures
        sector_return = (sector_momentum - 50) * 0.4  # Convert score to approx return
        relative_return = sector_return - market_return

        # Normalize to 0-100
        relative_strength = 50 + relative_return * 2
        return max(0, min(100, relative_strength))

    def _determine_rotation_signal(
        self,
        inflow_outflow: float,
        momentum_score: float,
    ) -> str:
        """Determine rotation signal based on inflow and momentum.

        Args:
            inflow_outflow: Net inflow/outflow value.
            momentum_score: Momentum score.

        Returns:
            Rotation signal (inflow, outflow, neutral).
        """
        if inflow_outflow > 100 and momentum_score > 60:
            return "inflow"
        elif inflow_outflow < -100 and momentum_score < 40:
            return "outflow"
        else:
            return "neutral"

    def get_top_sectors(
        self,
        n: int = 3,
        weeks_back: int = 4,
    ) -> list[str]:
        """Get top performing sectors over recent weeks.

        Args:
            n: Number of top sectors to return.
            weeks_back: Number of weeks to consider.

        Returns:
            List of top sector names.
        """
        cutoff_date = datetime.now() - timedelta(weeks=weeks_back)
        recent_rankings = [
            r for r in self.historical_rankings
            if r.week_ending >= cutoff_date
        ]

        if not recent_rankings:
            return []

        # Calculate average momentum for each sector
        sector_momentum: dict[str, list[float]] = {}
        for ranking in recent_rankings:
            if ranking.sector not in sector_momentum:
                sector_momentum[ranking.sector] = []
            sector_momentum[ranking.sector].append(ranking.momentum_score)

        # Calculate averages
        avg_momentum = {
            sector: sum(scores) / len(scores)
            for sector, scores in sector_momentum.items()
        }

        # Sort by average momentum
        sorted_sectors = sorted(avg_momentum.items(), key=lambda x: x[1], reverse=True)

        return [sector for sector, _ in sorted_sectors[:n]]

    def get_rotation_signals(self) -> dict[str, str]:
        """Get current rotation signals for all sectors.

        Returns:
            Dictionary mapping sector to rotation signal.
        """
        if not self.historical_rankings:
            return {}

        # Get most recent rankings
        latest_date = max(r.week_ending for r in self.historical_rankings)
        latest_rankings = [
            r for r in self.historical_rankings
            if r.week_ending == latest_date
        ]

        return {r.sector: r.rotation_signal for r in latest_rankings}
