"""AI Recommendation Engine combining multiple analysis sources."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.financials import FinancialScore
from app.recommendation.models import Recommendation
from app.sectors import SectorScore
from app.technical import TechnicalScore


class RecommendationEngine:
    """Engine for generating AI-powered stock recommendations."""

    def __init__(self) -> None:
        """Initialize the Recommendation Engine."""
        # Weights for different components
        self.weights = {
            "financial": 0.25,
            "technical": 0.20,
            "sector": 0.15,
            "guidance": 0.10,
            "valuation": 0.10,
            "institutional": 0.10,
            "news": 0.05,
            "risk": 0.05,
        }

    def calculate_financial_score(self, financial_score: FinancialScore) -> float:
        """Calculate normalized financial score from FinancialScore.

        Args:
            financial_score: FinancialScore object.

        Returns:
            Normalized score (0 to 100).
        """
        score = 50.0  # Base score

        if financial_score.revenue_growth:
            if financial_score.revenue_growth > 20:
                score += 15
            elif financial_score.revenue_growth > 10:
                score += 10
            elif financial_score.revenue_growth > 0:
                score += 5
            else:
                score -= 10

        if financial_score.profit_growth:
            if financial_score.profit_growth > 20:
                score += 15
            elif financial_score.profit_growth > 10:
                score += 10
            elif financial_score.profit_growth > 0:
                score += 5
            else:
                score -= 10

        if financial_score.roe:
            if financial_score.roe > 20:
                score += 10
            elif financial_score.roe > 15:
                score += 5

        if financial_score.debt_to_equity:
            if financial_score.debt_to_equity < 0.5:
                score += 5
            elif financial_score.debt_to_equity > 2:
                score -= 10

        return max(0, min(100, score))

    def calculate_technical_score(self, technical_score: TechnicalScore) -> float:
        """Calculate normalized technical score from TechnicalScore.

        Args:
            technical_score: TechnicalScore object.

        Returns:
            Normalized score (0 to 100).
        """
        score = 50.0  # Base score

        # RSI scoring
        if technical_score.rsi:
            if 30 < technical_score.rsi < 70:
                score += 10
            elif technical_score.rsi < 30:
                score += 15  # Oversold - potential buy
            elif technical_score.rsi > 70:
                score -= 15  # Overbought - potential sell

        # MACD scoring
        if technical_score.macd and technical_score.macd_signal:
            if technical_score.macd > technical_score.macd_signal:
                score += 10
            else:
                score -= 10

        # Moving average scoring
        if technical_score.ema_20 and technical_score.sma_50:
            if technical_score.ema_20 > technical_score.sma_50:
                score += 10
            else:
                score -= 10

        # ADX scoring (trend strength)
        if technical_score.adx:
            if technical_score.adx > 25:
                score += 5  # Strong trend

        # Volume breakout
        if technical_score.volume_breakout:
            score += 10

        return max(0, min(100, score))

    def calculate_sector_score(self, sector_score: SectorScore) -> float:
        """Calculate normalized sector score from SectorScore.

        Args:
            sector_score: SectorScore object.

        Returns:
            Normalized score (0 to 100).
        """
        if sector_score.overall_score is None:
            return 50.0

        # Normalize from -100 to 100 range to 0 to 100
        return (sector_score.overall_score + 100) / 2

    def calculate_guidance_score(self, guidance_sentiment: str | None) -> float:
        """Calculate normalized guidance score from sentiment.

        Args:
            guidance_sentiment: Sentiment string (positive, neutral, negative).

        Returns:
            Normalized score (0 to 100).
        """
        if guidance_sentiment == "positive":
            return 75.0
        elif guidance_sentiment == "negative":
            return 25.0
        else:
            return 50.0

    def calculate_valuation_score(self, pe_ratio: float | None, peg_ratio: float | None) -> float:
        """Calculate valuation score.

        Args:
            pe_ratio: P/E ratio.
            peg_ratio: PEG ratio.

        Returns:
            Normalized score (0 to 100).
        """
        score = 50.0

        if pe_ratio:
            if pe_ratio < 15:
                score += 20
            elif pe_ratio < 25:
                score += 10
            elif pe_ratio > 40:
                score -= 20

        if peg_ratio:
            if peg_ratio < 1:
                score += 20
            elif peg_ratio < 1.5:
                score += 10
            elif peg_ratio > 2:
                score -= 20

        return max(0, min(100, score))

    def calculate_institutional_score(self, institutional_activity: float) -> float:
        """Calculate institutional score from activity.

        Args:
            institutional_activity: Net institutional flow (-100 to 100).

        Returns:
            Normalized score (0 to 100).
        """
        # Normalize from -100 to 100 range to 0 to 100
        return (institutional_activity + 100) / 2

    def calculate_news_score(self, news_sentiment: str | None) -> float:
        """Calculate news score from sentiment.

        Args:
            news_sentiment: Sentiment string (positive, neutral, negative).

        Returns:
            Normalized score (0 to 100).
        """
        if news_sentiment == "positive":
            return 75.0
        elif news_sentiment == "negative":
            return 25.0
        else:
            return 50.0

    def calculate_risk_score(self, volatility: float | None, beta: float | None) -> float:
        """Calculate risk score (lower risk = higher score).

        Args:
            volatility: Volatility measure.
            beta: Beta value.

        Returns:
            Normalized score (0 to 100).
        """
        score = 50.0

        if volatility:
            if volatility < 20:
                score += 20
            elif volatility > 40:
                score -= 20

        if beta:
            if beta < 1:
                score += 15
            elif beta > 1.5:
                score -= 15

        return max(0, min(100, score))

    def calculate_overall_score(
        self,
        financial_score: float,
        technical_score: float,
        sector_score: float,
        guidance_score: float,
        valuation_score: float,
        institutional_score: float,
        news_score: float,
        risk_score: float,
    ) -> float:
        """Calculate weighted overall score.

        Args:
            financial_score: Financial component score.
            technical_score: Technical component score.
            sector_score: Sector component score.
            guidance_score: Guidance component score.
            valuation_score: Valuation component score.
            institutional_score: Institutional component score.
            news_score: News component score.
            risk_score: Risk component score.

        Returns:
            Weighted overall score (0 to 100).
        """
        overall = (
            financial_score * self.weights["financial"]
            + technical_score * self.weights["technical"]
            + sector_score * self.weights["sector"]
            + guidance_score * self.weights["guidance"]
            + valuation_score * self.weights["valuation"]
            + institutional_score * self.weights["institutional"]
            + news_score * self.weights["news"]
            + risk_score * self.weights["risk"]
        )

        return max(0, min(100, overall))

    def determine_action(self, overall_score: float) -> str:
        """Determine buy/hold/sell action based on overall score.

        Args:
            overall_score: Overall score (0 to 100).

        Returns:
            Action string (buy, hold, sell).
        """
        if overall_score >= 70:
            return "buy"
        elif overall_score <= 30:
            return "sell"
        else:
            return "hold"

    def calculate_confidence(
        self,
        overall_score: float,
        data_completeness: float,  # 0 to 1, percentage of available data
    ) -> float:
        """Calculate confidence level in the recommendation.

        Args:
            overall_score: Overall score.
            data_completeness: Data completeness percentage.

        Returns:
            Confidence level (0 to 100).
        """
        # Confidence based on how extreme the score is and data completeness
        extremeness = abs(overall_score - 50) / 50  # 0 to 1
        confidence = (extremeness * 30) + (data_completeness * 70)
        return max(0, min(100, confidence))

    def calculate_target_and_stop_loss(
        self,
        current_price: float,
        action: str,
        overall_score: float,
        volatility: float | None = None,
    ) -> tuple[float | None, float | None]:
        """Calculate target price and stop loss.

        Args:
            current_price: Current stock price.
            action: Recommended action.
            overall_score: Overall score.
            volatility: Volatility for stop loss calculation.

        Returns:
            Tuple of (target_price, stop_loss).
        """
        if action == "buy":
            # Target based on score strength
            strength = (overall_score - 50) / 50  # 0 to 1 for scores > 50
            target_multiplier = 1.05 + (strength * 0.15)  # 5% to 20% upside
            target_price = current_price * target_multiplier

            # Stop loss based on volatility or default 10%
            stop_loss_multiplier = 0.90
            if volatility:
                stop_loss_multiplier = 1 - (volatility / 100 * 2)
                stop_loss_multiplier = max(0.85, min(0.95, stop_loss_multiplier))
            stop_loss = current_price * stop_loss_multiplier

            return target_price, stop_loss

        elif action == "sell":
            # For sell, target is lower price
            strength = (50 - overall_score) / 50  # 0 to 1 for scores < 50
            target_multiplier = 0.95 - (strength * 0.15)  # 5% to 20% downside
            target_price = current_price * target_multiplier

            # Stop loss is above current price for short positions
            stop_loss_multiplier = 1.10
            if volatility:
                stop_loss_multiplier = 1 + (volatility / 100 * 2)
                stop_loss_multiplier = max(1.05, min(1.15, stop_loss_multiplier))
            stop_loss = current_price * stop_loss_multiplier

            return target_price, stop_loss

        else:  # hold
            return None, None

    def generate_reasoning(
        self,
        overall_score: float,
        action: str,
        financial_score: float,
        technical_score: float,
        sector_score: float,
    ) -> str:
        """Generate reasoning for the recommendation.

        Args:
            overall_score: Overall score.
            action: Recommended action.
            financial_score: Financial component score.
            technical_score: Technical component score.
            sector_score: Sector component score.

        Returns:
            Reasoning string.
        """
        reasoning_parts = []

        if action == "buy":
            reasoning_parts.append("Strong buy recommendation based on:")
            if financial_score > 60:
                reasoning_parts.append(f"- Solid financial metrics (score: {financial_score:.1f})")
            if technical_score > 60:
                reasoning_parts.append(f"- Positive technical indicators (score: {technical_score:.1f})")
            if sector_score > 60:
                reasoning_parts.append(f"- Favorable sector trends (score: {sector_score:.1f})")
        elif action == "sell":
            reasoning_parts.append("Sell recommendation based on:")
            if financial_score < 40:
                reasoning_parts.append(f"- Weakening financial metrics (score: {financial_score:.1f})")
            if technical_score < 40:
                reasoning_parts.append(f"- Negative technical indicators (score: {technical_score:.1f})")
            if sector_score < 40:
                reasoning_parts.append(f"- Unfavorable sector trends (score: {sector_score:.1f})")
        else:
            reasoning_parts.append("Hold recommendation due to mixed signals.")

        reasoning_parts.append(f"Overall score: {overall_score:.1f}/100")

        return "\n".join(reasoning_parts)

    def generate_recommendation(
        self,
        symbol: str,
        current_price: float,
        financial_score: FinancialScore | None = None,
        technical_score: TechnicalScore | None = None,
        sector_score: SectorScore | None = None,
        guidance_sentiment: str | None = None,
        pe_ratio: float | None = None,
        peg_ratio: float | None = None,
        institutional_activity: float = 50.0,
        news_sentiment: str | None = None,
        volatility: float | None = None,
        beta: float | None = None,
    ) -> Recommendation:
        """Generate comprehensive stock recommendation.

        Args:
            symbol: Stock symbol.
            current_price: Current stock price.
            financial_score: FinancialScore object.
            technical_score: TechnicalScore object.
            sector_score: SectorScore object.
            guidance_sentiment: Management guidance sentiment.
            pe_ratio: P/E ratio.
            peg_ratio: PEG ratio.
            institutional_activity: Institutional activity score (-100 to 100).
            news_sentiment: News sentiment.
            volatility: Volatility measure.
            beta: Beta value.

        Returns:
            Recommendation object with all details.
        """
        # Calculate component scores
        fin_score = (
            self.calculate_financial_score(financial_score)
            if financial_score
            else 50.0
        )
        tech_score = (
            self.calculate_technical_score(technical_score)
            if technical_score
            else 50.0
        )
        sec_score = (
            self.calculate_sector_score(sector_score)
            if sector_score
            else 50.0
        )
        guid_score = self.calculate_guidance_score(guidance_sentiment)
        val_score = self.calculate_valuation_score(pe_ratio, peg_ratio)
        inst_score = self.calculate_institutional_score(institutional_activity)
        news_score = self.calculate_news_score(news_sentiment)
        risk_score = self.calculate_risk_score(volatility, beta)

        # Calculate overall score
        overall = self.calculate_overall_score(
            fin_score,
            tech_score,
            sec_score,
            guid_score,
            val_score,
            inst_score,
            news_score,
            risk_score,
        )

        # Determine action
        action = self.determine_action(overall)

        # Calculate confidence
        data_count = sum([
            1 if financial_score else 0,
            1 if technical_score else 0,
            1 if sector_score else 0,
            1 if guidance_sentiment else 0,
            1 if pe_ratio or peg_ratio else 0,
        ])
        data_completeness = data_count / 5.0
        confidence = self.calculate_confidence(overall, data_completeness)

        # Calculate target and stop loss
        target, stop_loss = self.calculate_target_and_stop_loss(
            current_price,
            action,
            overall,
            volatility,
        )

        # Generate reasoning
        reasoning = self.generate_reasoning(
            overall,
            action,
            fin_score,
            tech_score,
            sec_score,
        )

        return Recommendation(
            symbol=symbol,
            overall_score=overall,
            action=action,
            confidence=confidence,
            target_price=target,
            stop_loss=stop_loss,
            current_price=current_price,
            reasoning=reasoning,
            timestamp=datetime.now(),
            financial_score=fin_score,
            technical_score=tech_score,
            sector_score=sec_score,
            guidance_score=guid_score,
            valuation_score=val_score,
            institutional_score=inst_score,
            news_score=news_score,
            risk_score=risk_score,
        )
