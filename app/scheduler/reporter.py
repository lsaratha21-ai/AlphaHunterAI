"""Report generator for scheduled tasks."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


class ReportGenerator:
    """Generator for PDF and Excel reports."""

    def __init__(self, output_dir: str = "reports") -> None:
        """Initialize the ReportGenerator.

        Args:
            output_dir: Directory to store generated reports.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_excel_report(
        self,
        scores: dict[str, Any],
        report_date: datetime,
    ) -> str:
        """Generate Excel report with all scores.

        Args:
            scores: Dictionary with all calculated scores.
            report_date: Date of the report.

        Returns:
            Path to generated Excel file.
        """
        filename = f"report_{report_date.strftime('%Y%m%d')}.xlsx"
        file_path = self.output_dir / filename

        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            # Financial scores
            if "financial_scores" in scores:
                financial_data = []
                for symbol, score in scores["financial_scores"].items():
                    financial_data.append({
                        "Symbol": symbol,
                        "Revenue Growth": score.revenue_growth,
                        "Profit Growth": score.profit_growth,
                        "EPS Growth": score.eps_growth,
                        "ROE": score.roe,
                        "ROCE": score.roce,
                        "Debt/Equity": score.debt_to_equity,
                        "Operating Cash Flow": score.operating_cash_flow,
                        "Free Cash Flow": score.free_cash_flow,
                        "PEG": score.peg,
                        "Book Value Growth": score.book_value_growth,
                    })
                pd.DataFrame(financial_data).to_excel(
                    writer,
                    sheet_name="Financial Scores",
                    index=False,
                )

            # Technical scores
            if "technical_scores" in scores:
                technical_data = []
                for symbol, score in scores["technical_scores"].items():
                    technical_data.append({
                        "Symbol": symbol,
                        "RSI": score.rsi,
                        "MACD": score.macd,
                        "MACD Signal": score.macd_signal,
                        "MACD Histogram": score.macd_histogram,
                        "EMA 20": score.ema_20,
                        "SMA 50": score.sma_50,
                        "SMA 200": score.sma_200,
                        "ADX": score.adx,
                        "ATR": score.atr,
                        "SuperTrend": score.supertrend,
                        "SuperTrend Signal": score.supertrend_signal,
                        "Bollinger Upper": score.bollinger_upper,
                        "Bollinger Middle": score.bollinger_middle,
                        "Bollinger Lower": score.bollinger_lower,
                        "VWAP": score.vwap,
                        "Volume Breakout": score.volume_breakout,
                        "Delivery %": score.delivery_percentage,
                    })
                pd.DataFrame(technical_data).to_excel(
                    writer,
                    sheet_name="Technical Scores",
                    index=False,
                )

            # Sector scores
            if "sector_scores" in scores:
                sector_data = []
                for sector, score in scores["sector_scores"].items():
                    sector_data.append({
                        "Sector": sector,
                        "Government Score": score.government_score,
                        "Order Book Score": score.order_book_score,
                        "Commodity Score": score.commodity_score,
                        "News Score": score.news_score,
                        "Institutional Score": score.institutional_score,
                        "Overall Score": score.overall_score,
                        "Rotation Signal": score.rotation_signal,
                    })
                pd.DataFrame(sector_data).to_excel(
                    writer,
                    sheet_name="Sector Scores",
                    index=False,
                )

            # Recommendations
            if "recommendations" in scores:
                recommendation_data = []
                for symbol, rec in scores["recommendations"].items():
                    recommendation_data.append({
                        "Symbol": symbol,
                        "Overall Score": rec.overall_score,
                        "Action": rec.action,
                        "Confidence": rec.confidence,
                        "Target Price": rec.target_price,
                        "Stop Loss": rec.stop_loss,
                        "Current Price": rec.current_price,
                        "Financial Score": rec.financial_score,
                        "Technical Score": rec.technical_score,
                        "Sector Score": rec.sector_score,
                        "Guidance Score": rec.guidance_score,
                        "Valuation Score": rec.valuation_score,
                        "Institutional Score": rec.institutional_score,
                        "News Score": rec.news_score,
                        "Risk Score": rec.risk_score,
                    })
                pd.DataFrame(recommendation_data).to_excel(
                    writer,
                    sheet_name="Recommendations",
                    index=False,
                )

        return str(file_path)

    def generate_pdf_report(
        self,
        scores: dict[str, Any],
        report_date: datetime,
    ) -> str:
        """Generate PDF report with all scores.

        Args:
            scores: Dictionary with all calculated scores.
            report_date: Date of the report.

        Returns:
            Path to generated PDF file.

        Raises:
            NotImplementedError: PDF generation requires additional libraries.
        """
        # PDF generation requires reportlab or similar library
        # For now, create a text-based report
        filename = f"report_{report_date.strftime('%Y%m%d')}.txt"
        file_path = self.output_dir / filename

        with open(file_path, "w") as f:
            f.write(f"AlphaHunter AI Report\n")
            f.write(f"Date: {report_date.strftime('%Y-%m-%d')}\n")
            f.write("=" * 50 + "\n\n")

            if "recommendations" in scores:
                f.write("RECOMMENDATIONS\n")
                f.write("-" * 50 + "\n")
                for symbol, rec in scores["recommendations"].items():
                    f.write(f"\n{symbol}\n")
                    f.write(f"  Action: {rec.action}\n")
                    f.write(f"  Overall Score: {rec.overall_score:.2f}\n")
                    f.write(f"  Confidence: {rec.confidence:.2f}%\n")
                    if rec.target_price:
                        f.write(f"  Target: {rec.target_price:.2f}\n")
                    if rec.stop_loss:
                        f.write(f"  Stop Loss: {rec.stop_loss:.2f}\n")
                    if rec.reasoning:
                        f.write(f"  Reasoning: {rec.reasoning}\n")

        return str(file_path)
