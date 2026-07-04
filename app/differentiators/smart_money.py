"""Smart money activity tracking."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.differentiators.models import SmartMoneyActivity


class SmartMoneyTracker:
    """Tracker for smart money activity."""

    def calculate_smart_money_score(
        self,
        symbol: str,
        promoter_data: dict[str, Any],
        fii_dii_data: dict[str, Any],
        mutual_fund_data: dict[str, Any],
        block_deal_data: dict[str, Any],
    ) -> SmartMoneyActivity:
        """Calculate smart money score based on various indicators.

        Args:
            symbol: Stock symbol.
            promoter_data: Promoter buying/selling data.
            fii_dii_data: FII/DII activity data.
            mutual_fund_data: Mutual fund ownership data.
            block_deal_data: Block deal activity data.

        Returns:
            SmartMoneyActivity with smart money score.
        """
        # Score individual components
        promoter_buying_score = self._score_promoter_activity(promoter_data)
        promoter_selling_score = self._score_promoter_selling(promoter_data)
        fii_dii_score = self._score_fii_dii_activity(fii_dii_data)
        mutual_fund_score = self._score_mutual_fund_activity(mutual_fund_data)
        block_deal_score = self._score_block_deal_activity(block_deal_data)

        # Calculate insider confidence
        insider_confidence = self._calculate_insider_confidence(
            promoter_buying_score,
            promoter_selling_score,
        )

        # Calculate overall smart money score
        smart_money_score = (
            promoter_buying_score * 0.25 +
            fii_dii_score * 0.25 +
            mutual_fund_score * 0.20 +
            block_deal_score * 0.15 +
            insider_confidence * 0.15
        )

        # Determine signal
        signal = self._determine_smart_money_signal(smart_money_score)

        # Extract changes
        fii_dii_change = fii_dii_data.get("change_percentage", 0.0)
        mutual_fund_ownership_change = mutual_fund_data.get("change_percentage", 0.0)

        return SmartMoneyActivity(
            symbol=symbol,
            promoter_buying=promoter_buying_score,
            promoter_selling=promoter_selling_score,
            fii_dii_change=fii_dii_change,
            mutual_fund_ownership_change=mutual_fund_ownership_change,
            block_deal_activity=block_deal_score,
            insider_confidence=insider_confidence,
            smart_money_score=smart_money_score,
            signal=signal,
            timestamp=datetime.now(),
        )

    def _score_promoter_activity(self, promoter_data: dict[str, Any]) -> float:
        """Score promoter buying activity.

        Args:
            promoter_data: Promoter activity data.

        Returns:
            Score (0-100).
        """
        buying_amount = promoter_data.get("buying_amount", 0.0)
        buying_percentage = promoter_data.get("buying_percentage", 0.0)

        # Score based on buying intensity
        if buying_percentage >= 5:
            return 90.0
        elif buying_percentage >= 3:
            return 80.0
        elif buying_percentage >= 2:
            return 70.0
        elif buying_percentage >= 1:
            return 60.0
        elif buying_percentage >= 0.5:
            return 50.0
        else:
            return 40.0

    def _score_promoter_selling(self, promoter_data: dict[str, Any]) -> float:
        """Score promoter selling activity (inverted - high selling = low score).

        Args:
            promoter_data: Promoter activity data.

        Returns:
            Score (0-100, lower = more selling).
        """
        selling_percentage = promoter_data.get("selling_percentage", 0.0)

        # Invert score - more selling = lower score
        if selling_percentage >= 5:
            return 10.0
        elif selling_percentage >= 3:
            return 20.0
        elif selling_percentage >= 2:
            return 30.0
        elif selling_percentage >= 1:
            return 40.0
        elif selling_percentage >= 0.5:
            return 50.0
        else:
            return 60.0

    def _score_fii_dii_activity(self, fii_dii_data: dict[str, Any]) -> float:
        """Score FII/DII activity.

        Args:
            fii_dii_data: FII/DII activity data.

        Returns:
            Score (0-100).
        """
        change_percentage = fii_dii_data.get("change_percentage", 0.0)
        net_value = fii_dii_data.get("net_value", 0.0)

        # Score based on net buying intensity
        if change_percentage >= 10:
            return 95.0
        elif change_percentage >= 5:
            return 85.0
        elif change_percentage >= 3:
            return 75.0
        elif change_percentage >= 1:
            return 65.0
        elif change_percentage >= 0:
            return 55.0
        elif change_percentage >= -3:
            return 40.0
        elif change_percentage >= -5:
            return 30.0
        else:
            return 20.0

    def _score_mutual_fund_activity(self, mutual_fund_data: dict[str, Any]) -> float:
        """Score mutual fund activity.

        Args:
            mutual_fund_data: Mutual fund activity data.

        Returns:
            Score (0-100).
        """
        change_percentage = mutual_fund_data.get("change_percentage", 0.0)
        ownership_percentage = mutual_fund_data.get("ownership_percentage", 0.0)

        # Score based on ownership change and level
        ownership_score = min(100, ownership_percentage * 5)  # Max at 20% ownership
        change_score = 50 + change_percentage * 3

        return (ownership_score * 0.4 + change_score * 0.6)

    def _score_block_deal_activity(self, block_deal_data: dict[str, Any]) -> float:
        """Score block deal activity.

        Args:
            block_deal_data: Block deal activity data.

        Returns:
            Score (0-100).
        """
        deal_type = block_deal_data.get("deal_type", "neutral")
        deal_value = block_deal_data.get("deal_value", 0.0)

        # Score based on deal type and value
        if deal_type == "bulk_buy":
            value_score = min(100, deal_value / 10000000 * 10)  # Scale by 10Cr
            return 80 + value_score * 0.2
        elif deal_type == "bulk_sell":
            value_score = min(100, deal_value / 10000000 * 10)
            return 20 + value_score * 0.2
        else:
            return 50.0

    def _calculate_insider_confidence(
        self,
        buying_score: float,
        selling_score: float,
    ) -> float:
        """Calculate overall insider confidence.

        Args:
            buying_score: Promoter buying score.
            selling_score: Promoter selling score.

        Returns:
            Insider confidence score (0-100).
        """
        # Higher confidence when buying is high and selling is low
        confidence = (buying_score + (100 - selling_score)) / 2
        return confidence

    def _determine_smart_money_signal(self, score: float) -> str:
        """Determine smart money signal based on score.

        Args:
            score: Smart money score.

        Returns:
            Signal string (bullish, bearish, neutral).
        """
        if score >= 70:
            return "bullish"
        elif score <= 30:
            return "bearish"
        else:
            return "neutral"
