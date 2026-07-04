"""Centralized logging framework for AlphaHunter AI.

Provides structured logging with rotation, JSON formatting, and console output.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from loguru import logger

DEFAULT_LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

JSON_LOG_FORMAT = (
    '{"timestamp": "{time:YYYY-MM-DD HH:mm:ss.SSSZ}", '
    '"level": "{level}", '
    '"name": "{name}", '
    '"function": "{function}", '
    '"line": {line}, '
    '"message": "{message}", '
    '"extra": {extra}}'
)


class InterceptHandler:
    """Intercept standard library logging and redirect to loguru."""

    def emit(self, record: Any) -> None:  # noqa: D102
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == __file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging(
    log_level: str = "INFO",
    log_format: str = "text",
    log_file: str | Path = "logs/alphahunter.log",
    rotation: str = "10 MB",
    retention: str = "30 days",
) -> None:
    """Configure the global logging framework.

    Args:
        log_level: Minimum log level to capture (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_format: Output format, either 'text' or 'json'.
        log_file: Path to the log file.
        rotation: Rotation policy for the log file.
        retention: Retention policy for rotated logs.
    """
    logger.remove()

    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    format_string = JSON_LOG_FORMAT if log_format == "json" else DEFAULT_LOG_FORMAT

    logger.add(
        sys.stdout,
        level=log_level,
        format=format_string,
        colorize=True,
        enqueue=True,
    )

    logger.add(
        log_file,
        level=log_level,
        format=format_string,
        rotation=rotation,
        retention=retention,
        compression="zip",
        enqueue=True,
        diagnose=False,
    )

    logger.info(
        "Logging initialized",
        extra={"log_level": log_level, "log_format": log_format, "log_file": str(log_file)},
    )


def get_logger(name: str) -> Any:
    """Return a logger instance bound to the given module name.

    Args:
        name: Typically the module's __name__.

    Returns:
        A loguru logger instance.
    """
    return logger.bind(name=name)
