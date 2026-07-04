"""Application entry point for AlphaHunter AI.

Initializes configuration, logging, and database connection, then exposes a
FastAPI application instance.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import __app_name__, __version__
from app.config import get_settings
from app.database import get_database_connection
from app.utils import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Manage application lifespan events.

    Args:
        app: FastAPI application instance.
    """
    settings = get_settings()
    setup_logging(
        log_level=settings.log_level,
        log_format=settings.log_format,
        log_file=settings.log_file,
    )

    db = get_database_connection()
    db.connect()
    yield
    db.close()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI-powered investment research platform for Indian stock markets.",
        debug=settings.app_debug,
        lifespan=lifespan,
    )

    @app.get("/")
    def health_check() -> dict[str, str]:
        """Return a simple health check response."""
        return {
            "app": __app_name__,
            "version": __version__,
            "status": "ok",
        }

    @app.get("/health")
    def health() -> dict[str, str]:
        """Return detailed health status."""
        return {
            "app": settings.app_name,
            "version": settings.app_version,
            "environment": settings.app_env,
            "status": "healthy",
        }

    return app


app = create_app()
