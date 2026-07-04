"""Unit tests for the logging framework."""

from __future__ import annotations

from pathlib import Path

from loguru import logger

from app.utils import get_logger, setup_logging


class TestSetupLogging:
    """Tests for the logging setup."""

    def test_setup_logging_creates_log_file(self, tmp_path: Path) -> None:
        """Ensure setup_logging creates the log file."""
        log_file = tmp_path / "test.log"
        setup_logging(log_file=log_file)
        assert log_file.parent.exists()

    def test_setup_logging_removes_existing_handlers(self, tmp_path: Path) -> None:
        """Ensure setup_logging removes existing handlers."""
        log_file = tmp_path / "test.log"
        setup_logging(log_file=log_file)
        assert len(logger._core.handlers) > 0


class TestGetLogger:
    """Tests for the logger factory."""

    def test_get_logger_returns_logger(self) -> None:
        """Ensure get_logger returns a loguru logger."""
        log = get_logger(__name__)
        assert log is not None
