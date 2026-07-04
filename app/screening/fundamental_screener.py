"""Fundamental-focused screener prioritizing fundamentals over technicals."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class FundamentalScore:
    """Fundamental analysis score."""

    symbol: str
    financial_quality_score: float  # 0-100
    management_guidance_score: float  # 0-100
    sector_rotation_score: float  # 0-100
    institutional_buying_score: float  # 0-100
    valuation_score: float  # 0-100
    order_book_score: float  # 0-100
    risk_score: float  # 0-100
    before_crowd_score: float  # 0-100
    technical_confirmation_score: float  # 0-100  # Used only as confirmation

    def calculate_fundamental_weighted_score(self) -> float:
        """Calculate weighted score prioritizing fundamentals (75%) over technicals (25%).

        Returns:
            Weighted score (0-100).
        """
        # Fundamental factors (75% weight)
        fundamental_weight = 0.75
        technical_weight = 0.25

        # Fundamental component weights
        fin_quality_weight = 0.20
        mgmt_guidance_weight = 0.15
        sector_rotation_weight = 0.15
        institutional_weight = 0.15
        valuation_weight = 0.15
        order_book_weight = 0.10
        risk_weight = 0.10

        fundamental_score = (
            self.financial_quality_score * fin_quality_weight +
            self.management_guidance_score * mgmt_guidance_weight +
            self.sector_rotation_score * sector_rotation_weight +
            self.institutional_buying_score * institutional_weight +
            self.valuation_score * valuation_weight +
            self.order_book_score * order_book_weight +
            self.risk_score * risk_weight
        )

        # Before crowd bonus (can add up to 10 points)
        before_crowd_bonus = (self.before_crowd_score / 100) * 10

        # Technical confirmation (only 25% weight)
        technical_score = self.technical_confirmation_score

        weighted_score = (
            (fundamental_score + before_crowd_bonus) * fundamental_weight +
            technical_score * technical_weight
        )

        return min(weighted_score, 100.0)


@dataclass
class ScreeningResult:
    """Result of fundamental screening."""

    symbol: str
    company_name: str
    fundamental_score: FundamentalScore
    weighted_score: float
    probability_of_15pct_return: float
    acceptance_status: str  # accepted, rejected
    acceptance_reasoning: str | None = None
    rejection_reasoning: str | None = None
    ranking: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "company_name": self.company_name,
            "fundamental_score": {
                "financial_quality": self.fundamental_score.financial_quality_score,
                "management_guidance": self.fundamental_score.management_guidance_score,
                "sector_rotation": self.fundamental_score.sector_rotation_score,
                "institutional_buying": self.fundamental_score.institutional_buying_score,
                "valuation": self.fundamental_score.valuation_score,
                "order_book": self.fundamental_score.order_book_score,
                "risk": self.fundamental_score.risk_score,
                "before_crowd": self.fundamental_score.before_crowd_score,
                "technical_confirmation": self.fundamental_score.technical_confirmation_score,
            },
            "weighted_score": self.weighted_score,
            "probability_of_15pct_return": self.probability_of_15pct_return,
            "acceptance_status": self.acceptance_status,
            "acceptance_reasoning": self.acceptance_reasoning,
            "rejection_reasoning": self.rejection_reasoning,
            "ranking": self.ranking,
        }


class FundamentalScreener:
    """Screener that prioritizes fundamental factors over technicals."""

    def __init__(self) -> None:
        """Initialize the FundamentalScreener."""
        pass

    def screen_candidates(
        self,
        candidates: list[FundamentalScore],
        min_probability: float = 70.0,
        max_candidates: int = 5,
    ) -> list[ScreeningResult]:
        """Screen candidates based on fundamental factors.

        Args:
            candidates: List of FundamentalScore objects.
            min_probability: Minimum probability of 15% return (default 70%).
            max_candidates: Maximum number of candidates to accept.

        Returns:
            List of ScreeningResult objects.
        """
        results = []

        for candidate in candidates:
            weighted_score = candidate.calculate_fundamental_weighted_score()
            probability = self._calculate_return_probability(candidate, weighted_score)

            # Determine acceptance based on fundamental strength
            acceptance, reasoning = self._evaluate_acceptance(candidate, weighted_score, probability)

            result = ScreeningResult(
                symbol=candidate.symbol,
                company_name=candidate.symbol,  # Would be company name in real implementation
                fundamental_score=candidate,
                weighted_score=weighted_score,
                probability_of_15pct_return=probability,
                acceptance_status=acceptance,
                acceptance_reasoning=reasoning if acceptance == "accepted" else None,
                rejection_reasoning=reasoning if acceptance == "rejected" else None,
            )
            results.append(result)

        # Sort by weighted score
        results.sort(key=lambda x: x.weighted_score, reverse=True)

        # Set rankings
        for i, result in enumerate(results, 1):
            result.ranking = i

        return results

    def _calculate_return_probability(
        self,
        score: FundamentalScore,
        weighted_score: float,
    ) -> float:
        """Calculate probability of achieving 15% return.

        Args:
            score: FundamentalScore object.
            weighted_score: Weighted score.

        Returns:
            Probability percentage.
        """
        # Base probability from weighted score
        base_probability = weighted_score

        # Boost for strong fundamentals
        fundamental_boost = 0
        if score.financial_quality_score >= 80:
            fundamental_boost += 5
        if score.management_guidance_score >= 75:
            fundamental_boost += 5
        if score.institutional_buying_score >= 75:
            fundamental_boost += 5
        if score.before_crowd_score >= 70:
            fundamental_boost += 5

        return min(base_probability + fundamental_boost, 100.0)

    def _evaluate_acceptance(
        self,
        score: FundamentalScore,
        weighted_score: float,
        probability: float,
    ) -> tuple[str, str]:
        """Evaluate whether to accept or reject candidate.

        Args:
            score: FundamentalScore object.
            weighted_score: Weighted score.
            probability: Probability of 15% return.

        Returns:
            Tuple of (acceptance_status, reasoning).
        """
        # Minimum thresholds for acceptance
        min_financial_quality = 65
        min_management_guidance = 60
        min_valuation = 60
        min_weighted_score = 70
        min_probability = 70

        rejections = []

        # Check fundamental thresholds
        if score.financial_quality_score < min_financial_quality:
            rejections.append(f"Financial quality ({score.financial_quality_score:.1f}) below minimum ({min_financial_quality})")

        if score.management_guidance_score < min_management_guidance:
            rejections.append(f"Management guidance ({score.management_guidance_score:.1f}) below minimum ({min_management_guidance})")

        if score.valuation_score < min_valuation:
            rejections.append(f"Valuation ({score.valuation_score:.1f}) below minimum ({min_valuation})")

        # Check weighted score
        if weighted_score < min_weighted_score:
            rejections.append(f"Weighted score ({weighted_score:.1f}) below minimum ({min_weighted_score})")

        # Check probability
        if probability < min_probability:
            rejections.append(f"Probability of 15% return ({probability:.1f}%) below minimum ({min_probability}%)")

        # Check for technical-only candidates (high technical, low fundamentals)
        if score.technical_confirmation_score >= 80 and weighted_score < 75:
            rejections.append("Relies primarily on technical momentum without strong fundamental support")

        # Check for excessive risk
        if score.risk_score < 50:
            rejections.append(f"Risk score ({score.risk_score:.1f}) too low - insufficient risk control")

        if rejections:
            return "rejected", "; ".join(rejections)

        # Generate acceptance reasoning
        strengths = []
        if score.financial_quality_score >= 80:
            strengths.append(f"Strong financial quality ({score.financial_quality_score:.1f}/100)")
        if score.management_guidance_score >= 75:
            strengths.append(f"Positive management guidance ({score.management_guidance_score:.1f}/100)")
        if score.institutional_buying_score >= 75:
            strengths.append(f"Strong institutional buying ({score.institutional_buying_score:.1f}/100)")
        if score.sector_rotation_score >= 75:
            strengths.append(f"Positive sector rotation ({score.sector_rotation_score:.1f}/100)")
        if score.valuation_score >= 75:
            strengths.append(f"Attractive valuation ({score.valuation_score:.1f}/100)")
        if score.order_book_score >= 75:
            strengths.append(f"Strong order book ({score.order_book_score:.1f}/100)")
        if score.before_crowd_score >= 70:
            strengths.append(f"Before the crowd opportunity ({score.before_crowd_score:.1f}/100)")
        if score.technical_confirmation_score >= 70:
            strengths.append(f"Technical confirmation ({score.technical_confirmation_score:.1f}/100)")

        acceptance_reasoning = f"Weighted score {weighted_score:.1f}/100; " + "; ".join(strengths)
        return "accepted", acceptance_reasoning
