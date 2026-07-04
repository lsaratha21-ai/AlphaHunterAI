"""DuckDB connection manager for AlphaHunter AI.

Provides a thin, reusable abstraction over DuckDB with connection pooling
and lifecycle management.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import duckdb

from app.config import get_settings
from app.utils import get_logger

logger = get_logger(__name__)


class DuckDBConnection:
    """Manages DuckDB database connections and operations."""

    def __init__(self, database_url: str | None = None) -> None:
        """Initialize a DuckDB connection manager.

        Args:
            database_url: DuckDB connection string. Defaults to settings value.
        """
        self._settings = get_settings()
        self._database_url = database_url or self._settings.database_url
        self._connection: duckdb.DuckDBPyConnection | None = None
        self._parsed_url = urlparse(self._database_url)

    @property
    def database_path(self) -> Path:
        """Return the resolved database file path."""
        if self._parsed_url.scheme == "duckdb":
            path = self._parsed_url.path
            if path.startswith("/"):
                path = path[1:]
            return Path(path).resolve()
        return Path(self._database_url).resolve()

    def connect(self) -> duckdb.DuckDBPyConnection:
        """Establish and return a DuckDB connection.

        Returns:
            Active DuckDB connection.
        """
        if self._connection is None:
            self.database_path.parent.mkdir(parents=True, exist_ok=True)
            self._connection = duckdb.connect(str(self.database_path))
            logger.info(
                "DuckDB connection established",
                extra={"database_path": str(self.database_path)},
            )
        return self._connection

    def close(self) -> None:
        """Close the active DuckDB connection."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
            logger.info("DuckDB connection closed")

    def execute(self, query: str, parameters: dict[str, Any] | None = None) -> duckdb.DuckDBPyRelation:
        """Execute a SQL query.

        Args:
            query: SQL query string.
            parameters: Optional query parameters.

        Returns:
            DuckDB relation object.
        """
        conn = self.connect()
        if parameters:
            return conn.execute(query, parameters)
        return conn.execute(query)

    def fetch_one(self, query: str, parameters: dict[str, Any] | None = None) -> tuple[Any, ...] | None:
        """Execute a query and return the first row.

        Args:
            query: SQL query string.
            parameters: Optional query parameters.

        Returns:
            First row of the result or None.
        """
        conn = self.connect()
        if parameters:
            return conn.execute(query, parameters).fetchone()
        return conn.execute(query).fetchone()

    def fetch_all(self, query: str, parameters: dict[str, Any] | None = None) -> list[tuple[Any, ...]]:
        """Execute a query and return all rows.

        Args:
            query: SQL query string.
            parameters: Optional query parameters.

        Returns:
            List of result rows.
        """
        conn = self.connect()
        if parameters:
            return conn.execute(query, parameters).fetchall()
        return conn.execute(query).fetchall()

    def __enter__(self) -> DuckDBConnection:
        """Enter context manager and open connection."""
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context manager and close connection."""
        self.close()


def get_database_connection(database_url: str | None = None) -> DuckDBConnection:
    """Factory function for DuckDB connection.

    Args:
        database_url: Optional DuckDB connection string.

    Returns:
        DuckDBConnection instance.
    """
    return DuckDBConnection(database_url)
