"""Data models for scheduled reports."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class ReportStatus(str, Enum):
    """Status of report generation."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ReportType(str, Enum):
    """Type of report."""

    PDF = "pdf"
    EXCEL = "excel"
    BOTH = "both"


@dataclass
class ScheduledReport:
    """Scheduled report metadata."""

    report_id: str
    report_date: datetime
    status: ReportStatus
    report_type: ReportType
    file_path: str | None = None
    error_message: str | None = None
    created_at: datetime | None = None
    completed_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "report_id": self.report_id,
            "report_date": self.report_date.isoformat(),
            "status": self.status.value,
            "report_type": self.report_type.value,
            "file_path": self.file_path,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
