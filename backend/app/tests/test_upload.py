"""
Test suite for the upload endpoint.
"""

import io
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _make_pdf_file(content: bytes = b"%PDF-1.4 fake content") -> tuple:
    return ("test_report.pdf", io.BytesIO(content), "application/pdf")


def test_upload_no_file():
    """Should return 422 when no file is provided."""
    response = client.post("/api/v1/upload")
    assert response.status_code == 422


def test_upload_invalid_extension():
    """Should reject files with invalid extensions."""
    response = client.post(
        "/api/v1/upload",
        files={"file": ("malware.exe", io.BytesIO(b"bad"), "application/octet-stream")},
    )
    assert response.status_code in (400, 422, 500)
    body = response.json()
    assert body.get("success") is False


def test_health_ping():
    """Health ping should always return 200."""
    response = client.get("/api/v1/health/ping")
    assert response.status_code == 200
    assert response.json()["ping"] == "pong"


def test_root():
    """Root endpoint should return app info."""
    response = client.get("/")
    assert response.status_code == 200
    assert "app" in response.json()
