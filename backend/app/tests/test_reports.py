"""
Test suite for the reports endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_reports_returns_success():
    """GET /api/v1/reports should return 200 with pagination meta."""
    response = client.get("/api/v1/reports")
    assert response.status_code == 200
    body = response.json()
    assert body.get("success") is True
    assert "meta" in body


def test_list_reports_invalid_sort_order():
    """Invalid sort_order should fail validation."""
    response = client.get("/api/v1/reports?sort_order=sideways")
    assert response.status_code == 422


def test_get_nonexistent_report():
    """Fetching a non-existent report should return 404."""
    fake_id = "00000000-0000-0000-0000-000000000099"
    response = client.get(f"/api/v1/reports/{fake_id}")
    assert response.status_code == 404
    body = response.json()
    assert body.get("success") is False
    assert "REPORT_NOT_FOUND" in body.get("error_code", "")
