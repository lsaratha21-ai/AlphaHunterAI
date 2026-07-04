"""Unit tests for the CLI module."""

from __future__ import annotations

from typer.testing import CliRunner

from app.__main__ import cli

runner = CliRunner()


class TestCLI:
    """Tests for the CLI commands."""

    def test_version_command(self) -> None:
        """Test the version command prints correct version."""
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        assert "AlphaHunter AI" in result.stdout
        assert "0.1.0" in result.stdout

    def test_help_command(self) -> None:
        """Test the help command displays help text."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "AlphaHunter AI CLI" in result.stdout
