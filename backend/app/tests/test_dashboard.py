"""
Test suite for the dashboard endpoint.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard_returns_success():
    """GET /api/v1/dashboard should return 200."""
    response = client.get("/api/v1/dashboard")
    assert response.status_code == 200
    body = response.json()
    assert body.get("success") is True
    data = body.get("data", {})
    assert "total_reports" in data
    assert "recent_uploads" in data
    assert "trend_summaries" in data
