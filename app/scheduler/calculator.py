"""Score calculation orchestrator for scheduled tasks."""

from __future__ import annotations

from typing import Any

from app.financials import FinancialEngine, FinancialScore
from app.recommendation import RecommendationEngine, Recommendation
from app.sectors import SectorRotationEngine, SectorScore
from app.technical import TechnicalEngine, TechnicalScore


class ScoreCalculator:
    """Orchestrator for calculating all scores."""

    def __init__(self) -> None:
        """Initialize the ScoreCalculator."""
        self.financial_engine = FinancialEngine()
        self.technical_engine = TechnicalEngine()
        self.sector_engine = SectorRotationEngine()
        self.recommendation_engine = RecommendationEngine()

    def calculate_financial_scores(
        self,
        symbols: list[str],
        financial_data: dict[str, Any],
    ) -> dict[str, FinancialScore]:
        """Calculate financial scores for all symbols.

        Args:
            symbols: List of stock symbols.
            financial_data: Financial data dictionary.

        Returns:
            Dictionary of FinancialScore objects by symbol.
        """
        scores = {}
        for symbol in symbols:
            # Mock calculation - in production, use actual financial data
            scores[symbol] = FinancialScore(
                symbol=symbol,
                revenue_growth=10.0,
                profit_growth=8.0,
                eps_growth=12.0,
                roe=15.0,
                roce=12.0,
                debt_to_equity=0.5,
                operating_cash_flow=1000000.0,
                free_cash_flow=800000.0,
                peg=1.2,
                book_value_growth=5.0,
            )
        return scores

    def calculate_technical_scores(
        self,
        symbols: list[str],
        price_data: dict[str, Any],
    ) -> dict[str, TechnicalScore]:
        """Calculate technical scores for all symbols.

        Args:
            symbols: List of stock symbols.
            price_data: Price data dictionary.

        Returns:
            Dictionary of TechnicalScore objects by symbol.
        """
        scores = {}
        for symbol in symbols:
            # Mock calculation - in production, use actual price data
            scores[symbol] = TechnicalScore(
                symbol=symbol,
                rsi=55.0,
                macd=1.5,
                macd_signal=1.2,
                macd_histogram=0.3,
                ema_20=150.0,
                sma_50=145.0,
                sma_200=130.0,
                adx=25.0,
                atr=5.0,
                supertrend=148.0,
                supertrend_signal="buy",
                bollinger_upper=155.0,
                bollinger_middle=150.0,
                bollinger_lower=145.0,
                vwap=149.0,
                volume_breakout=True,
                delivery_percentage=75.0,
            )
        return scores

    def calculate_sector_scores(
        self,
        sectors: list[str],
    ) -> dict[str, SectorScore]:
        """Calculate sector scores for all sectors.

        Args:
            sectors: List of sector names.

        Returns:
            Dictionary of SectorScore objects by sector.
        """
        scores = {}
        for sector in sectors:
            scores[sector] = SectorScore(
                sector=sector,
                government_score=50.0,
                order_book_score=55.0,
                commodity_score=45.0,
                news_score=60.0,
                institutional_score=52.0,
                overall_score=52.0,
                rotation_signal="neutral",
            )
        return scores

    def calculate_recommendations(
        self,
        symbols: list[str],
        financial_scores: dict[str, FinancialScore],
        technical_scores: dict[str, TechnicalScore],
        current_prices: dict[str, float],
    ) -> dict[str, Recommendation]:
        """Calculate recommendations for all symbols.

        Args:
            symbols: List of stock symbols.
            financial_scores: Financial scores by symbol.
            technical_scores: Technical scores by symbol.
            current_prices: Current prices by symbol.

        Returns:
            Dictionary of Recommendation objects by symbol.
        """
        recommendations = {}
        for symbol in symbols:
            recommendations[symbol] = self.recommendation_engine.generate_recommendation(
                symbol=symbol,
                current_price=current_prices.get(symbol, 100.0),
                financial_score=financial_scores.get(symbol),
                technical_score=technical_scores.get(symbol),
            )
        return recommendations

    def calculate_all_scores(
        self,
        symbols: list[str],
        sectors: list[str],
        financial_data: dict[str, Any],
        price_data: dict[str, Any],
        current_prices: dict[str, float],
    ) -> dict[str, Any]:
        """Calculate all scores in one pass.

        Args:
            symbols: List of stock symbols.
            sectors: List of sector names.
            financial_data: Financial data dictionary.
            price_data: Price data dictionary.
            current_prices: Current prices by symbol.

        Returns:
            Dictionary with all calculated scores.
        """
        financial_scores = self.calculate_financial_scores(symbols, financial_data)
        technical_scores = self.calculate_technical_scores(symbols, price_data)
        sector_scores = self.calculate_sector_scores(sectors)
        recommendations = self.calculate_recommendations(
            symbols,
            financial_scores,
            technical_scores,
            current_prices,
        )

        return {
            "financial_scores": financial_scores,
            "technical_scores": technical_scores,
            "sector_scores": sector_scores,
            "recommendations": recommendations,
        }
