"""
Health check endpoint tests
"""

import pytest
from fastapi.testclient import TestClient


class TestHealthCheck:
    """Test suite for health check endpoint."""

    def test_health_check_success(self, client: TestClient) -> None:
        """Test successful health check."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0-alpha"
        assert data["environment"] in ["development", "staging", "production", "testing"]

    def test_root_endpoint(self, client: TestClient) -> None:
        """Test root endpoint."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "message" in data
        assert "docs" in data
        assert "health" in data
