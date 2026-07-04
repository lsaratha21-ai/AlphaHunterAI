"""Unit tests for the FastAPI application."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app


class TestCreateApp:
    """Tests for the create_app function."""

    def test_create_app_returns_fastapi_instance(self) -> None:
        """Ensure create_app returns a FastAPI instance."""
        app = create_app()
        assert app is not None
        assert app.title == "AlphaHunterAI"

    def test_health_check_endpoint(self) -> None:
        """Test the health check endpoint returns correct response."""
        app = create_app()
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["app"] == "AlphaHunter AI"
        assert data["status"] == "ok"

    def test_health_endpoint(self) -> None:
        """Test the detailed health endpoint returns correct response."""
        app = create_app()
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["app"] == "AlphaHunterAI"
        assert data["version"] == "0.1.0"
        assert data["environment"] == "development"
        assert data["status"] == "healthy"
