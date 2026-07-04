"""Unit tests for the Scheduler module."""

from __future__ import annotations

from datetime import datetime

import pytest

from app.scheduler import (
    DataDownloader,
    EmailSender,
    ReportArchiver,
    ReportGenerator,
    ReportStatus,
    ReportType,
    ScheduledReport,
    ScoreCalculator,
    WeeklyScheduler,
)
from app.core import ProviderError


class TestScheduledReport:
    """Tests for ScheduledReport model."""

    def test_scheduled_report_to_dict(self) -> None:
        """Ensure ScheduledReport converts to dictionary correctly."""
        report = ScheduledReport(
            report_id="test-123",
            report_date=datetime.now(),
            status=ReportStatus.COMPLETED,
            report_type=ReportType.PDF,
            file_path="/path/to/report.pdf",
        )
        result = report.to_dict()
        assert result["report_id"] == "test-123"
        assert result["status"] == "completed"
        assert result["report_type"] == "pdf"


class TestDataDownloader:
    """Tests for DataDownloader."""

    def test_download_stock_data(self) -> None:
        """Test stock data download."""
        downloader = DataDownloader()
        data = downloader.download_stock_data(["AAPL", "MSFT"])
        assert "AAPL" in data
        assert "MSFT" in data

    def test_save_data(self, tmp_path) -> None:
        """Test data saving."""
        downloader = DataDownloader(data_dir=str(tmp_path))
        data = {"AAPL": "mock_data", "MSFT": "mock_data"}
        file_path = downloader.save_data(data, "test.txt")
        assert file_path is not None


class TestScoreCalculator:
    """Tests for ScoreCalculator."""

    def test_calculate_financial_scores(self) -> None:
        """Test financial score calculation."""
        calculator = ScoreCalculator()
        scores = calculator.calculate_financial_scores(["AAPL", "MSFT"], {})
        assert "AAPL" in scores
        assert "MSFT" in scores
        assert scores["AAPL"].symbol == "AAPL"

    def test_calculate_technical_scores(self) -> None:
        """Test technical score calculation."""
        calculator = ScoreCalculator()
        scores = calculator.calculate_technical_scores(["AAPL", "MSFT"], {})
        assert "AAPL" in scores
        assert "MSFT" in scores

    def test_calculate_sector_scores(self) -> None:
        """Test sector score calculation."""
        calculator = ScoreCalculator()
        scores = calculator.calculate_sector_scores(["Technology", "Healthcare"])
        assert "Technology" in scores
        assert "Healthcare" in scores

    def test_calculate_recommendations(self) -> None:
        """Test recommendation calculation."""
        calculator = ScoreCalculator()
        financial_scores = calculator.calculate_financial_scores(["AAPL"], {})
        technical_scores = calculator.calculate_technical_scores(["AAPL"], {})
        recommendations = calculator.calculate_recommendations(
            ["AAPL"],
            financial_scores,
            technical_scores,
            {"AAPL": 150.0},
        )
        assert "AAPL" in recommendations
        assert recommendations["AAPL"].symbol == "AAPL"

    def test_calculate_all_scores(self) -> None:
        """Test all scores calculation."""
        calculator = ScoreCalculator()
        scores = calculator.calculate_all_scores(
            symbols=["AAPL"],
            sectors=["Technology"],
            financial_data={},
            price_data={},
            current_prices={"AAPL": 150.0},
        )
        assert "financial_scores" in scores
        assert "technical_scores" in scores
        assert "sector_scores" in scores
        assert "recommendations" in scores


class TestReportGenerator:
    """Tests for ReportGenerator."""

    def test_generate_excel_report(self, tmp_path) -> None:
        """Test Excel report generation."""
        generator = ReportGenerator(output_dir=str(tmp_path))
        scores = {
            "financial_scores": {},
            "technical_scores": {},
            "sector_scores": {},
            "recommendations": {},
        }
        file_path = generator.generate_excel_report(scores, datetime.now())
        assert file_path is not None
        assert ".xlsx" in file_path

    def test_generate_pdf_report(self, tmp_path) -> None:
        """Test PDF report generation."""
        generator = ReportGenerator(output_dir=str(tmp_path))
        scores = {
            "recommendations": {},
        }
        file_path = generator.generate_pdf_report(scores, datetime.now())
        assert file_path is not None


class TestEmailSender:
    """Tests for EmailSender."""

    def test_email_sender_initialization(self) -> None:
        """Test EmailSender initialization."""
        sender = EmailSender()
        assert sender.smtp_server == "smtp.gmail.com"
        assert sender.smtp_port == 587

    def test_send_email_no_credentials(self) -> None:
        """Test email sending without credentials."""
        sender = EmailSender()
        with pytest.raises(ProviderError, match="Email credentials not configured"):
            sender.send_report_email(
                ["test@example.com"],
                "Test Subject",
                "Test Body",
            )


class TestReportArchiver:
    """Tests for ReportArchiver."""

    def test_archiver_initialization(self, tmp_path) -> None:
        """Test ReportArchiver initialization."""
        archiver = ReportArchiver(archive_dir=str(tmp_path))
        assert archiver.archive_dir.exists()

    def test_archive_report(self, tmp_path) -> None:
        """Test report archiving."""
        archiver = ReportArchiver(archive_dir=str(tmp_path))
        
        # Create a test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        report = ScheduledReport(
            report_id="test-123",
            report_date=datetime.now(),
            status=ReportStatus.COMPLETED,
            report_type=ReportType.PDF,
        )
        
        archived_path = archiver.archive_report(report, str(test_file))
        assert archived_path is not None
        assert not test_file.exists()  # File should be moved

    def test_get_archived_reports(self, tmp_path) -> None:
        """Test getting archived reports."""
        archiver = ReportArchiver(archive_dir=str(tmp_path))
        reports = archiver.get_archived_reports()
        assert isinstance(reports, list)


class TestWeeklyScheduler:
    """Tests for WeeklyScheduler."""

    def test_scheduler_initialization(self) -> None:
        """Test WeeklyScheduler initialization."""
        scheduler = WeeklyScheduler()
        assert scheduler.downloader is not None
        assert scheduler.calculator is not None
        assert scheduler.reporter is not None
        assert scheduler.archiver is not None

    def test_download_data(self) -> None:
        """Test data download through scheduler."""
        scheduler = WeeklyScheduler()
        data = scheduler.download_data(["AAPL"])
        assert "AAPL" in data

    def test_calculate_scores(self) -> None:
        """Test score calculation through scheduler."""
        scheduler = WeeklyScheduler()
        scores = scheduler.calculate_scores(
            symbols=["AAPL"],
            sectors=["Technology"],
            financial_data={},
            price_data={},
            current_prices={"AAPL": 150.0},
        )
        assert "financial_scores" in scores
        assert "technical_scores" in scores

    def test_generate_reports(self, tmp_path) -> None:
        """Test report generation through scheduler."""
        scheduler = WeeklyScheduler(output_dir=str(tmp_path))
        scores = {
            "financial_scores": {},
            "technical_scores": {},
            "sector_scores": {},
            "recommendations": {},
        }
        report_files = scheduler.generate_reports(scores, datetime.now())
        assert len(report_files) > 0

    def test_archive_reports(self, tmp_path) -> None:
        """Test report archiving through scheduler."""
        scheduler = WeeklyScheduler(archive_dir=str(tmp_path))
        
        # Create test files
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        archived_paths = scheduler.archive_reports([str(test_file)], datetime.now())
        assert len(archived_paths) > 0

    def test_run_weekly_report(self) -> None:
        """Test complete weekly report run."""
        scheduler = WeeklyScheduler()
        report = scheduler.run_weekly_report(
            symbols=["AAPL"],
            sectors=["Technology"],
            recipients=None,
        )
        assert isinstance(report, ScheduledReport)
        assert report.report_id is not None
        assert report.status in [ReportStatus.COMPLETED, ReportStatus.FAILED]
