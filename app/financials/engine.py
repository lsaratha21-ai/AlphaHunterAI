"""Financial calculation engine for computing key financial metrics."""

from __future__ import annotations

from app.core.exceptions import ValidationError
from app.financials.models import FinancialScore


class FinancialEngine:
    """Engine for calculating financial metrics and scores."""

    @staticmethod
    def calculate_revenue_growth(current_revenue: float, previous_revenue: float) -> float:
        """Calculate revenue growth percentage.

        Args:
            current_revenue: Current period revenue.
            previous_revenue: Previous period revenue.

        Returns:
            Revenue growth as percentage.

        Raises:
            ValidationError: If previous_revenue is zero or negative.
        """
        if previous_revenue <= 0:
            raise ValidationError("Previous revenue must be positive")
        return ((current_revenue - previous_revenue) / previous_revenue) * 100

    @staticmethod
    def calculate_profit_growth(current_profit: float, previous_profit: float) -> float:
        """Calculate profit growth percentage.

        Args:
            current_profit: Current period profit.
            previous_profit: Previous period profit.

        Returns:
            Profit growth as percentage.

        Raises:
            ValidationError: If previous_profit is zero.
        """
        if previous_profit == 0:
            raise ValidationError("Previous profit cannot be zero")
        return ((current_profit - previous_profit) / previous_profit) * 100

    @staticmethod
    def calculate_eps_growth(current_eps: float, previous_eps: float) -> float:
        """Calculate EPS growth percentage.

        Args:
            current_eps: Current period EPS.
            previous_eps: Previous period EPS.

        Returns:
            EPS growth as percentage.

        Raises:
            ValidationError: If previous_eps is zero.
        """
        if previous_eps == 0:
            raise ValidationError("Previous EPS cannot be zero")
        return ((current_eps - previous_eps) / previous_eps) * 100

    @staticmethod
    def calculate_roe(net_income: float, shareholder_equity: float) -> float:
        """Calculate Return on Equity (ROE).

        Args:
            net_income: Net income.
            shareholder_equity: Shareholder equity.

        Returns:
            ROE as percentage.

        Raises:
            ValidationError: If shareholder_equity is zero.
        """
        if shareholder_equity == 0:
            raise ValidationError("Shareholder equity cannot be zero")
        return (net_income / shareholder_equity) * 100

    @staticmethod
    def calculate_roce(
        ebit: float,
        capital_employed: float,
    ) -> float:
        """Calculate Return on Capital Employed (ROCE).

        Args:
            ebit: Earnings Before Interest and Taxes.
            capital_employed: Capital employed.

        Returns:
            ROCE as percentage.

        Raises:
            ValidationError: If capital_employed is zero.
        """
        if capital_employed == 0:
            raise ValidationError("Capital employed cannot be zero")
        return (ebit / capital_employed) * 100

    @staticmethod
    def calculate_debt_to_equity(total_debt: float, total_equity: float) -> float:
        """Calculate Debt to Equity ratio.

        Args:
            total_debt: Total debt.
            total_equity: Total equity.

        Returns:
            Debt to Equity ratio.

        Raises:
            ValidationError: If total_equity is zero.
        """
        if total_equity == 0:
            raise ValidationError("Total equity cannot be zero")
        return total_debt / total_equity

    @staticmethod
    def calculate_operating_cash_flow(
        net_income: float,
        depreciation: float,
        changes_in_working_capital: float,
    ) -> float:
        """Calculate Operating Cash Flow.

        Args:
            net_income: Net income.
            depreciation: Depreciation and amortization.
            changes_in_working_capital: Changes in working capital.

        Returns:
            Operating Cash Flow.
        """
        return net_income + depreciation + changes_in_working_capital

    @staticmethod
    def calculate_free_cash_flow(
        operating_cash_flow: float,
        capital_expenditure: float,
    ) -> float:
        """Calculate Free Cash Flow.

        Args:
            operating_cash_flow: Operating cash flow.
            capital_expenditure: Capital expenditure.

        Returns:
            Free Cash Flow.
        """
        return operating_cash_flow - capital_expenditure

    @staticmethod
    def calculate_peg(pe_ratio: float, earnings_growth: float) -> float:
        """Calculate Price/Earnings to Growth ratio (PEG).

        Args:
            pe_ratio: Price to Earnings ratio.
            earnings_growth: Earnings growth as percentage.

        Returns:
            PEG ratio.

        Raises:
            ValidationError: If earnings_growth is zero.
        """
        if earnings_growth == 0:
            raise ValidationError("Earnings growth cannot be zero")
        return pe_ratio / earnings_growth

    @staticmethod
    def calculate_book_value_growth(
        current_book_value: float,
        previous_book_value: float,
    ) -> float:
        """Calculate book value growth percentage.

        Args:
            current_book_value: Current book value per share.
            previous_book_value: Previous book value per share.

        Returns:
            Book value growth as percentage.

        Raises:
            ValidationError: If previous_book_value is zero.
        """
        if previous_book_value == 0:
            raise ValidationError("Previous book value cannot be zero")
        return ((current_book_value - previous_book_value) / previous_book_value) * 100

    def calculate_financial_score(
        self,
        symbol: str,
        current_revenue: float,
        previous_revenue: float,
        current_profit: float,
        previous_profit: float,
        current_eps: float,
        previous_eps: float,
        net_income: float,
        shareholder_equity: float,
        ebit: float,
        capital_employed: float,
        total_debt: float,
        total_equity: float,
        depreciation: float,
        changes_in_working_capital: float,
        capital_expenditure: float,
        pe_ratio: float,
        current_book_value: float,
        previous_book_value: float,
    ) -> FinancialScore:
        """Calculate comprehensive financial score.

        Args:
            symbol: Stock symbol.
            current_revenue: Current period revenue.
            previous_revenue: Previous period revenue.
            current_profit: Current period profit.
            previous_profit: Previous period profit.
            current_eps: Current period EPS.
            previous_eps: Previous period EPS.
            net_income: Net income.
            shareholder_equity: Shareholder equity.
            ebit: Earnings Before Interest and Taxes.
            capital_employed: Capital employed.
            total_debt: Total debt.
            total_equity: Total equity.
            depreciation: Depreciation and amortization.
            changes_in_working_capital: Changes in working capital.
            capital_expenditure: Capital expenditure.
            pe_ratio: Price to Earnings ratio.
            current_book_value: Current book value per share.
            previous_book_value: Previous book value per share.

        Returns:
            FinancialScore object with all calculated metrics.
        """
        revenue_growth = self.calculate_revenue_growth(current_revenue, previous_revenue)
        profit_growth = self.calculate_profit_growth(current_profit, previous_profit)
        eps_growth = self.calculate_eps_growth(current_eps, previous_eps)
        roe = self.calculate_roe(net_income, shareholder_equity)
        roce = self.calculate_roce(ebit, capital_employed)
        debt_to_equity = self.calculate_debt_to_equity(total_debt, total_equity)
        ocf = self.calculate_operating_cash_flow(
            net_income,
            depreciation,
            changes_in_working_capital,
        )
        fcf = self.calculate_free_cash_flow(ocf, capital_expenditure)
        peg = self.calculate_peg(pe_ratio, earnings_growth=profit_growth)
        book_value_growth = self.calculate_book_value_growth(
            current_book_value,
            previous_book_value,
        )

        return FinancialScore(
            symbol=symbol,
            revenue_growth=revenue_growth,
            profit_growth=profit_growth,
            eps_growth=eps_growth,
            roe=roe,
            roce=roce,
            debt_to_equity=debt_to_equity,
            operating_cash_flow=ocf,
            free_cash_flow=fcf,
            peg=peg,
            book_value_growth=book_value_growth,
        )
