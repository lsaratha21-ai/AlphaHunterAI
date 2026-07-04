"""Report archiver for scheduled tasks."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from shutil import copy2, move
from typing import Any

from app.scheduler.models import ScheduledReport


class ReportArchiver:
    """Archiver for storing and organizing reports."""

    def __init__(self, archive_dir: str = "archive") -> None:
        """Initialize the ReportArchiver.

        Args:
            archive_dir: Directory to store archived reports.
        """
        self.archive_dir = Path(archive_dir)
        self.archive_dir.mkdir(exist_ok=True)

    def archive_report(
        self,
        report: ScheduledReport,
        source_file: str,
    ) -> str:
        """Archive a report file.

        Args:
            report: ScheduledReport metadata.
            source_file: Path to the source file.

        Returns:
            Path to archived file.
        """
        # Create directory structure: archive/YYYY/MM/
        year_month_dir = self.archive_dir / str(report.report_date.year) / f"{report.report_date.month:02d}"
        year_month_dir.mkdir(parents=True, exist_ok=True)

        source_path = Path(source_file)
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_file}")

        # Archive with timestamp
        archived_filename = f"{report.report_id}_{source_path.name}"
        archived_path = year_month_dir / archived_filename

        # Move or copy the file
        move(source_path, archived_path)

        return str(archived_path)

    def get_archived_reports(
        self,
        year: int | None = None,
        month: int | None = None,
    ) -> list[Path]:
        """Get list of archived reports.

        Args:
            year: Filter by year.
            month: Filter by month.

        Returns:
            List of paths to archived reports.
        """
        if year and month:
            search_dir = self.archive_dir / str(year) / f"{month:02d}"
        elif year:
            search_dir = self.archive_dir / str(year)
        else:
            search_dir = self.archive_dir

        if not search_dir.exists():
            return []

        return list(search_dir.glob("**/*.*"))
