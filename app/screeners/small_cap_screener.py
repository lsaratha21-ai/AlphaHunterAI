"""Small-cap company screener for specific criteria."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.financials import FinancialScore


@dataclass
class SmallCapScreenerResult:
    """Result from small-cap screener."""

    symbol: str
    company_name: str
    market_cap: float
    current_roe: float
    roe_trend: str  # improving, stable, declining
    debt_to_equity: float
    institutional_ownership: float
    institutional_trend: str  # increasing, stable, decreasing
    overall_score: float  # 0-100
    timestamp: datetime

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "company_name": self.company_name,
            "market_cap": self.market_cap,
            "current_roe": self.current_roe,
            "roe_trend": self.roe_trend,
            "debt_to_equity": self.debt_to_equity,
            "institutional_ownership": self.institutional_ownership,
            "institutional_trend": self.institutional_trend,
            "overall_score": self.overall_score,
            "timestamp": self.timestamp.isoformat(),
        }


class SmallCapScreener:
    """Screener for small-cap companies with specific criteria."""

    def __init__(
        self,
        max_market_cap: float = 2000000000,  # $2B for small-cap
        max_debt_to_equity: float = 1.0,  # Low debt threshold
        min_roe: float = 10.0,  # Minimum ROE
    ) -> None:
        """Initialize the small-cap screener.

        Args:
            max_market_cap: Maximum market cap for small-cap classification.
            max_debt_to_equity: Maximum debt-to-equity ratio.
            min_roe: Minimum ROE threshold.
        """
        self.max_market_cap = max_market_cap
        self.max_debt_to_equity = max_debt_to_equity
        self.min_roe = min_roe

    def screen_small_cap_companies(
        self,
        companies: list[dict[str, Any]],
        historical_data: dict[str, dict[str, Any]] | None = None,
    ) -> list[SmallCapScreenerResult]:
        """Screen small-cap companies based on criteria.

        Args:
            companies: List of company data dictionaries.
            historical_data: Historical data for trend analysis.

        Returns:
            List of SmallCapScreenerResult matching criteria.
        """
        results = []

        for company in companies:
            symbol = company.get("symbol")
            if not symbol:
                continue

            # Apply filters
            if not self._meets_criteria(company, historical_data):
                continue

            # Calculate scores
            result = self._calculate_screener_result(
                company,
                historical_data,
            )
            results.append(result)

        # Sort by overall score
        results.sort(key=lambda x: x.overall_score, reverse=True)

        return results

    def _meets_criteria(
        self,
        company: dict[str, Any],
        historical_data: dict[str, dict[str, Any]] | None,
    ) -> bool:
        """Check if company meets screening criteria.

        Args:
            company: Company data dictionary.
            historical_data: Historical data.

        Returns:
            True if company meets all criteria.
        """
        symbol = company.get("symbol")
        market_cap = company.get("market_cap", 0)
        debt_to_equity = company.get("debt_to_equity", 999)
        current_roe = company.get("roe", 0)

        # Small-cap filter
        if market_cap > self.max_market_cap:
            return False

        # Low debt filter
        if debt_to_equity > self.max_debt_to_equity:
            return False

        # Minimum ROE filter
        if current_roe < self.min_roe:
            return False

        # Improving ROE filter
        if historical_data and symbol in historical_data:
            roe_trend = self._calculate_roe_trend(
                symbol,
                historical_data[symbol].get("roe_history", []),
            )
            if roe_trend != "improving":
                return False

        # Increasing institutional ownership filter
        if historical_data and symbol in historical_data:
            institutional_trend = self._calculate_institutional_trend(
                symbol,
                historical_data[symbol].get("institutional_ownership_history", []),
            )
            if institutional_trend != "increasing":
                return False

        return True

    def _calculate_screener_result(
        self,
        company: dict[str, Any],
        historical_data: dict[str, dict[str, Any]] | None,
    ) -> SmallCapScreenerResult:
        """Calculate screener result for a company.

        Args:
            company: Company data dictionary.
            historical_data: Historical data.

        Returns:
            SmallCapScreenerResult.
        """
        symbol = company.get("symbol", "")
        company_name = company.get("company_name", "")
        market_cap = company.get("market_cap", 0)
        current_roe = company.get("roe", 0)
        debt_to_equity = company.get("debt_to_equity", 0)
        institutional_ownership = company.get("institutional_ownership", 0)

        # Calculate trends
        if historical_data and symbol in historical_data:
            roe_trend = self._calculate_roe_trend(
                symbol,
                historical_data[symbol].get("roe_history", []),
            )
            institutional_trend = self._calculate_institutional_trend(
                symbol,
                historical_data[symbol].get("institutional_ownership_history", []),
            )
        else:
            roe_trend = "stable"
            institutional_trend = "stable"

        # Calculate overall score
        overall_score = self._calculate_overall_score(
            current_roe,
            debt_to_equity,
            institutional_ownership,
            roe_trend,
            institutional_trend,
        )

        return SmallCapScreenerResult(
            symbol=symbol,
            company_name=company_name,
            market_cap=market_cap,
            current_roe=current_roe,
            roe_trend=roe_trend,
            debt_to_equity=debt_to_equity,
            institutional_ownership=institutional_ownership,
            institutional_trend=institutional_trend,
            overall_score=overall_score,
            timestamp=datetime.now(),
        )

    def _calculate_roe_trend(
        self,
        symbol: str,
        roe_history: list[float],
    ) -> str:
        """Calculate ROE trend from historical data.

        Args:
            symbol: Stock symbol.
            roe_history: List of historical ROE values.

        Returns:
            Trend string (improving, stable, declining).
        """
        if len(roe_history) < 2:
            return "stable"

        recent_avg = sum(roe_history[-2:]) / 2
        earlier_avg = sum(roe_history[:-2]) / (len(roe_history) - 2) if len(roe_history) > 2 else roe_history[0]

        if earlier_avg == 0:
            return "stable"

        change = ((recent_avg - earlier_avg) / earlier_avg) * 100

        if change > 5:
            return "improving"
        elif change < -5:
            return "declining"
        else:
            return "stable"

    def _calculate_institutional_trend(
        self,
        symbol: str,
        ownership_history: list[float],
    ) -> str:
        """Calculate institutional ownership trend.

        Args:
            symbol: Stock symbol.
            ownership_history: List of historical ownership percentages.

        Returns:
            Trend string (increasing, stable, decreasing).
        """
        if len(ownership_history) < 2:
            return "stable"

        recent_avg = sum(ownership_history[-2:]) / 2
        earlier_avg = sum(ownership_history[:-2]) / (len(ownership_history) - 2) if len(ownership_history) > 2 else ownership_history[0]

        if earlier_avg == 0:
            return "stable"

        change = ((recent_avg - earlier_avg) / earlier_avg) * 100

        if change > 2:
            return "increasing"
        elif change < -2:
            return "decreasing"
        else:
            return "stable"

    def _calculate_overall_score(
        self,
        roe: float,
        debt_to_equity: float,
        institutional_ownership: float,
        roe_trend: str,
        institutional_trend: str,
    ) -> float:
        """Calculate overall screener score.

        Args:
            roe: Current ROE.
            debt_to_equity: Debt-to-equity ratio.
            institutional_ownership: Institutional ownership percentage.
            roe_trend: ROE trend.
            institutional_trend: Institutional ownership trend.

        Returns:
            Overall score (0-100).
        """
        # Score individual components
        roe_score = min(100, roe * 4)  # Max at 25% ROE
        debt_score = max(0, 100 - debt_to_equity * 50)  # Lower debt = higher score
        institutional_score = min(100, institutional_ownership * 2)  # Max at 50% ownership

        # Trend bonuses
        roe_trend_bonus = 10 if roe_trend == "improving" else 0
        institutional_trend_bonus = 10 if institutional_trend == "increasing" else 0

        # Weighted average
        overall_score = (
            roe_score * 0.35 +
            debt_score * 0.25 +
            institutional_score * 0.25 +
            roe_trend_bonus * 0.08 +
            institutional_trend_bonus * 0.07
        )

        return max(0, min(100, overall_score))

    def get_screening_summary(
        self,
        results: list[SmallCapScreenerResult],
    ) -> dict[str, Any]:
        """Get summary of screening results.

        Args:
            results: List of screener results.

        Returns:
            Summary statistics.
        """
        if not results:
            return {
                "total_companies": 0,
                "average_roe": 0,
                "average_debt_to_equity": 0,
                "average_institutional_ownership": 0,
                "average_score": 0,
            }

        return {
            "total_companies": len(results),
            "average_roe": sum(r.current_roe for r in results) / len(results),
            "average_debt_to_equity": sum(r.debt_to_equity for r in results) / len(results),
            "average_institutional_ownership": sum(r.institutional_ownership for r in results) / len(results),
            "average_score": sum(r.overall_score for r in results) / len(results),
        }
