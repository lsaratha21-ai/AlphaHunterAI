"""Unit tests for the Financial Engine."""

from __future__ import annotations

import pytest

from app.core import ValidationError
from app.financials import FinancialEngine, FinancialScore


class TestFinancialScore:
    """Tests for FinancialScore model."""

    def test_financial_score_to_dict(self) -> None:
        """Ensure FinancialScore converts to dictionary correctly."""
        score = FinancialScore(
            symbol="AAPL",
            revenue_growth=20.0,
            profit_growth=15.0,
            eps_growth=10.0,
            roe=25.0,
            roce=20.0,
            debt_to_equity=0.5,
            operating_cash_flow=1000000.0,
            free_cash_flow=800000.0,
            peg=1.5,
            book_value_growth=12.0,
        )
        result = score.to_dict()
        assert result["symbol"] == "AAPL"
        assert result["revenue_growth"] == 20.0
        assert result["profit_growth"] == 15.0


class TestFinancialEngine:
    """Tests for FinancialEngine calculations."""

    def test_calculate_revenue_growth(self) -> None:
        """Test revenue growth calculation."""
        engine = FinancialEngine()
        result = engine.calculate_revenue_growth(120, 100)
        assert result == 20.0

    def test_calculate_revenue_growth_negative(self) -> None:
        """Test revenue growth with decline."""
        engine = FinancialEngine()
        result = engine.calculate_revenue_growth(80, 100)
        assert result == -20.0

    def test_calculate_revenue_growth_zero_previous(self) -> None:
        """Test revenue growth with zero previous revenue."""
        engine = FinancialEngine()
        with pytest.raises(ValidationError, match="Previous revenue must be positive"):
            engine.calculate_revenue_growth(100, 0)

    def test_calculate_profit_growth(self) -> None:
        """Test profit growth calculation."""
        engine = FinancialEngine()
        result = engine.calculate_profit_growth(150, 100)
        assert result == 50.0

    def test_calculate_profit_growth_negative_profit(self) -> None:
        """Test profit growth with negative previous profit."""
        engine = FinancialEngine()
        result = engine.calculate_profit_growth(50, -100)
        assert result == -150.0

    def test_calculate_profit_growth_zero_previous(self) -> None:
        """Test profit growth with zero previous profit."""
        engine = FinancialEngine()
        with pytest.raises(ValidationError, match="Previous profit cannot be zero"):
            engine.calculate_profit_growth(100, 0)

    def test_calculate_eps_growth(self) -> None:
        """Test EPS growth calculation."""
        engine = FinancialEngine()
        result = engine.calculate_eps_growth(12, 10)
        assert result == 20.0

    def test_calculate_eps_growth_zero_previous(self) -> None:
        """Test EPS growth with zero previous EPS."""
        engine = FinancialEngine()
        with pytest.raises(ValidationError, match="Previous EPS cannot be zero"):
            engine.calculate_eps_growth(10, 0)

    def test_calculate_roe(self) -> None:
        """Test ROE calculation."""
        engine = FinancialEngine()
        result = engine.calculate_roe(25, 100)
        assert result == 25.0

    def test_calculate_roe_zero_equity(self) -> None:
        """Test ROE with zero equity."""
        engine = FinancialEngine()
        with pytest.raises(ValidationError, match="Shareholder equity cannot be zero"):
            engine.calculate_roe(25, 0)

    def test_calculate_roce(self) -> None:
        """Test ROCE calculation."""
        engine = FinancialEngine()
        result = engine.calculate_roce(20, 100)
        assert result == 20.0

    def test_calculate_roce_zero_capital(self) -> None:
        """Test ROCE with zero capital employed."""
        engine = FinancialEngine()
        with pytest.raises(ValidationError, match="Capital employed cannot be zero"):
            engine.calculate_roce(20, 0)

    def test_calculate_debt_to_equity(self) -> None:
        """Test Debt to Equity calculation."""
        engine = FinancialEngine()
        result = engine.calculate_debt_to_equity(50, 100)
        assert result == 0.5

    def test_calculate_debt_to_equity_zero_equity(self) -> None:
        """Test Debt to Equity with zero equity."""
        engine = FinancialEngine()
        with pytest.raises(ValidationError, match="Total equity cannot be zero"):
            engine.calculate_debt_to_equity(50, 0)

    def test_calculate_operating_cash_flow(self) -> None:
        """Test Operating Cash Flow calculation."""
        engine = FinancialEngine()
        result = engine.calculate_operating_cash_flow(100, 20, 30)
        assert result == 150

    def test_calculate_operating_cash_flow_negative_working_capital(self) -> None:
        """Test OCF with negative working capital changes."""
        engine = FinancialEngine()
        result = engine.calculate_operating_cash_flow(100, 20, -30)
        assert result == 90

    def test_calculate_free_cash_flow(self) -> None:
        """Test Free Cash Flow calculation."""
        engine = FinancialEngine()
        result = engine.calculate_free_cash_flow(150, 50)
        assert result == 100

    def test_calculate_free_cash_flow_negative(self) -> None:
        """Test FCF when capex exceeds OCF."""
        engine = FinancialEngine()
        result = engine.calculate_free_cash_flow(50, 100)
        assert result == -50

    def test_calculate_peg(self) -> None:
        """Test PEG ratio calculation."""
        engine = FinancialEngine()
        result = engine.calculate_peg(30, 20)
        assert result == 1.5

    def test_calculate_peg_zero_growth(self) -> None:
        """Test PEG with zero growth."""
        engine = FinancialEngine()
        with pytest.raises(ValidationError, match="Earnings growth cannot be zero"):
            engine.calculate_peg(30, 0)

    def test_calculate_book_value_growth(self) -> None:
        """Test book value growth calculation."""
        engine = FinancialEngine()
        result = engine.calculate_book_value_growth(110, 100)
        assert result == 10.0

    def test_calculate_book_value_growth_zero_previous(self) -> None:
        """Test book value growth with zero previous book value."""
        engine = FinancialEngine()
        with pytest.raises(ValidationError, match="Previous book value cannot be zero"):
            engine.calculate_book_value_growth(110, 0)

    def test_calculate_financial_score(self) -> None:
        """Test comprehensive financial score calculation."""
        engine = FinancialEngine()
        score = engine.calculate_financial_score(
            symbol="AAPL",
            current_revenue=120,
            previous_revenue=100,
            current_profit=150,
            previous_profit=100,
            current_eps=12,
            previous_eps=10,
            net_income=25,
            shareholder_equity=100,
            ebit=20,
            capital_employed=100,
            total_debt=50,
            total_equity=100,
            depreciation=20,
            changes_in_working_capital=30,
            capital_expenditure=50,
            pe_ratio=30,
            current_book_value=110,
            previous_book_value=100,
        )

        assert isinstance(score, FinancialScore)
        assert score.symbol == "AAPL"
        assert score.revenue_growth == 20.0
        assert score.profit_growth == 50.0
        assert score.eps_growth == 20.0
        assert score.roe == 25.0
        assert score.roce == 20.0
        assert score.debt_to_equity == 0.5
        assert score.operating_cash_flow == 75
        assert score.free_cash_flow == 25
        assert score.peg == 0.6
        assert score.book_value_growth == 10.0

    def test_calculate_financial_score_with_negative_values(self) -> None:
        """Test financial score with negative metrics."""
        engine = FinancialEngine()
        score = engine.calculate_financial_score(
            symbol="LOSS",
            current_revenue=80,
            previous_revenue=100,
            current_profit=-20,
            previous_profit=10,
            current_eps=-2,
            previous_eps=1,
            net_income=-20,
            shareholder_equity=100,
            ebit=-15,
            capital_employed=100,
            total_debt=80,
            total_equity=100,
            depreciation=10,
            changes_in_working_capital=-5,
            capital_expenditure=30,
            pe_ratio=15,
            current_book_value=90,
            previous_book_value=100,
        )

        assert score.revenue_growth == -20.0
        assert score.profit_growth == -300.0
        assert score.eps_growth == -300.0
        assert score.roe == -20.0
        assert score.roce == -15.0
        assert score.debt_to_equity == 0.8
        assert score.operating_cash_flow == -15
        assert score.free_cash_flow == -45
        assert score.book_value_growth == -10.0
