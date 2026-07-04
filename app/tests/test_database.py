"""Unit tests for the DuckDB connection manager."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.database import DuckDBConnection, get_database_connection


class TestDuckDBConnection:
    """Tests for DuckDBConnection."""

    def test_database_path_resolution(self, tmp_path: Path) -> None:
        """Ensure database path is resolved correctly."""
        db_path = tmp_path / "test.db"
        conn = DuckDBConnection(f"duckdb:///{db_path}")
        assert conn.database_path == db_path.resolve()

    def test_connect_creates_database(self, tmp_path: Path) -> None:
        """Ensure connect creates the database file."""
        db_path = tmp_path / "nested" / "test.db"
        conn = DuckDBConnection(f"duckdb:///{db_path}")
        conn.connect()
        assert db_path.exists()
        conn.close()

    def test_execute_and_fetch(self, tmp_path: Path) -> None:
        """Ensure execute and fetch work correctly."""
        db_path = tmp_path / "test.db"
        conn = DuckDBConnection(f"duckdb:///{db_path}")
        conn.execute("CREATE TABLE test (id INTEGER, name VARCHAR)")
        conn.execute("INSERT INTO test VALUES (1, 'AlphaHunter')")
        rows = conn.fetch_all("SELECT * FROM test")
        assert rows == [(1, "AlphaHunter")]
        conn.close()

    def test_context_manager(self, tmp_path: Path) -> None:
        """Ensure context manager opens and closes connection."""
        db_path = tmp_path / "test.db"
        with DuckDBConnection(f"duckdb:///{db_path}") as conn:
            conn.execute("CREATE TABLE cm (id INTEGER)")
        assert db_path.exists()


class TestGetDatabaseConnection:
    """Tests for the database connection factory."""

    def test_get_database_connection(self, tmp_path: Path) -> None:
        """Ensure factory returns a DuckDBConnection instance."""
        db_path = tmp_path / "test.db"
        conn = get_database_connection(f"duckdb:///{db_path}")
        assert isinstance(conn, DuckDBConnection)
