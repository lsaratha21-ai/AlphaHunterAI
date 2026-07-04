"""CLI entry point for AlphaHunter AI."""

from __future__ import annotations

import typer
import uvicorn

from app import __app_name__, __version__
from app.config import get_settings
from app.utils import setup_logging

cli = typer.Typer(name=__app_name__, help="AlphaHunter AI CLI")


@cli.command()
def serve(
    host: str = typer.Option(None, help="API host"),
    port: int = typer.Option(None, help="API port"),
    reload: bool = typer.Option(None, help="Enable auto-reload"),
) -> None:
    """Run the AlphaHunter AI API server."""
    settings = get_settings()
    setup_logging(
        log_level=settings.log_level,
        log_format=settings.log_format,
        log_file=settings.log_file,
    )

    uvicorn.run(
        "app.main:app",
        host=host or settings.api_host,
        port=port or settings.api_port,
        reload=reload if reload is not None else settings.api_reload,
    )


@cli.command()
def version() -> None:
    """Print the AlphaHunter AI version."""
    typer.echo(f"{__app_name__} {__version__}")


if __name__ == "__main__":
    cli()
