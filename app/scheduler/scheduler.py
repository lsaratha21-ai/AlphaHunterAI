"""Main scheduler for weekly report generation."""

from __future__ import annotations

from datetime import datetime
from typing import Any
import uuid

from app.scheduler.archiver import ReportArchiver
from app.scheduler.calculator import ScoreCalculator
from app.scheduler.downloader import DataDownloader
from app.scheduler.emailer import EmailSender
from app.scheduler.models import ReportStatus, ReportType, ScheduledReport
from app.scheduler.reporter import ReportGenerator


class WeeklyScheduler:
    """Scheduler for weekly Saturday report generation."""

    def __init__(
        self,
        data_dir: str = "data",
        output_dir: str = "reports",
        archive_dir: str = "archive",
        email_config: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the WeeklyScheduler.

        Args:
            data_dir: Directory for downloaded data.
            output_dir: Directory for generated reports.
            archive_dir: Directory for archived reports.
            email_config: Email configuration dict.
        """
        self.downloader = DataDownloader(data_dir)
        self.calculator = ScoreCalculator()
        self.reporter = ReportGenerator(output_dir)
        self.archiver = ReportArchiver(archive_dir)

        if email_config:
            self.emailer = EmailSender(
                smtp_server=email_config.get("smtp_server", "smtp.gmail.com"),
                smtp_port=email_config.get("smtp_port", 587),
                email=email_config.get("email"),
                password=email_config.get("password"),
            )
        else:
            self.emailer = None

        self.reports: list[ScheduledReport] = []

    def download_data(self, symbols: list[str]) -> dict[str, Any]:
        """Download latest data for given symbols.

        Args:
            symbols: List of stock symbols.

        Returns:
            Dictionary with downloaded data.
        """
        return self.downloader.download_stock_data(symbols)

    def calculate_scores(
        self,
        symbols: list[str],
        sectors: list[str],
        financial_data: dict[str, Any],
        price_data: dict[str, Any],
        current_prices: dict[str, float],
    ) -> dict[str, Any]:
        """Calculate all scores.

        Args:
            symbols: List of stock symbols.
            sectors: List of sector names.
            financial_data: Financial data.
            price_data: Price data.
            current_prices: Current prices.

        Returns:
            Dictionary with all calculated scores.
        """
        return self.calculator.calculate_all_scores(
            symbols,
            sectors,
            financial_data,
            price_data,
            current_prices,
        )

    def generate_reports(
        self,
        scores: dict[str, Any],
        report_date: datetime,
        report_type: ReportType = ReportType.BOTH,
    ) -> list[str]:
        """Generate reports.

        Args:
            scores: Dictionary with all calculated scores.
            report_date: Date of the report.
            report_type: Type of report to generate.

        Returns:
            List of generated report file paths.
        """
        report_files = []

        if report_type in [ReportType.PDF, ReportType.BOTH]:
            pdf_file = self.reporter.generate_pdf_report(scores, report_date)
            report_files.append(pdf_file)

        if report_type in [ReportType.EXCEL, ReportType.BOTH]:
            excel_file = self.reporter.generate_excel_report(scores, report_date)
            report_files.append(excel_file)

        return report_files

    def send_email(
        self,
        recipients: list[str],
        report_date: str,
        report_files: list[str],
    ) -> None:
        """Send email with reports.

        Args:
            recipients: List of recipient email addresses.
            report_date: Date of the report.
            report_files: List of report file paths.
        """
        if self.emailer:
            self.emailer.send_report_notification(recipients, report_date, report_files)

    def archive_reports(
        self,
        report_files: list[str],
        report_date: datetime,
    ) -> list[str]:
        """Archive generated reports.

        Args:
            report_files: List of report file paths.
            report_date: Date of the reports.

        Returns:
            List of archived file paths.
        """
        archived_paths = []
        for file_path in report_files:
            report = ScheduledReport(
                report_id=str(uuid.uuid4()),
                report_date=report_date,
                status=ReportStatus.COMPLETED,
                report_type=ReportType.BOTH,
            )
            archived_path = self.archiver.archive_report(report, file_path)
            archived_paths.append(archived_path)
        return archived_paths

    def run_weekly_report(
        self,
        symbols: list[str],
        sectors: list[str],
        recipients: list[str] | None = None,
        current_prices: dict[str, float] | None = None,
    ) -> ScheduledReport:
        """Run the complete weekly report generation.

        Args:
            symbols: List of stock symbols to analyze.
            sectors: List of sectors to analyze.
            recipients: List of email recipients.
            current_prices: Current prices for symbols.

        Returns:
            ScheduledReport with execution details.
        """
        report_id = str(uuid.uuid4())
        report_date = datetime.now()

        report = ScheduledReport(
            report_id=report_id,
            report_date=report_date,
            status=ReportStatus.IN_PROGRESS,
            report_type=ReportType.BOTH,
            created_at=report_date,
        )

        try:
            # Download data
            financial_data = self.download_data(symbols)
            price_data = self.download_data(symbols)  # In production, separate calls

            # Calculate scores
            if current_prices is None:
                current_prices = {symbol: 100.0 for symbol in symbols}

            scores = self.calculate_scores(
                symbols,
                sectors,
                financial_data,
                price_data,
                current_prices,
            )

            # Generate reports
            report_files = self.generate_reports(scores, report_date)

            # Send email
            if recipients and self.emailer:
                self.send_email(recipients, report_date.strftime("%Y-%m-%d"), report_files)

            # Archive reports
            self.archive_reports(report_files, report_date)

            report.status = ReportStatus.COMPLETED
            report.file_path = report_files[0] if report_files else None
            report.completed_at = datetime.now()

        except Exception as e:
            report.status = ReportStatus.FAILED
            report.error_message = str(e)
            report.completed_at = datetime.now()

        self.reports.append(report)
        return report
