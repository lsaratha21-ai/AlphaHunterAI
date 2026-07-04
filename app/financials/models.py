"""Data models for financial calculations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class FinancialScore:
    """Comprehensive financial score for a company."""

    symbol: str
    revenue_growth: float | None = None
    profit_growth: float | None = None
    eps_growth: float | None = None
    roe: float | None = None
    roce: float | None = None
    debt_to_equity: float | None = None
    operating_cash_flow: float | None = None
    free_cash_flow: float | None = None
    peg: float | None = None
    book_value_growth: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "symbol": self.symbol,
            "revenue_growth": self.revenue_growth,
            "profit_growth": self.profit_growth,
            "eps_growth": self.eps_growth,
            "roe": self.roe,
            "roce": self.roce,
            "debt_to_equity": self.debt_to_equity,
            "operating_cash_flow": self.operating_cash_flow,
            "free_cash_flow": self.free_cash_flow,
            "peg": self.peg,
            "book_value_growth": self.book_value_growth,
        }
