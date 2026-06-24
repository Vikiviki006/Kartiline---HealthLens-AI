"""
TrendService: historical trend analysis across multiple reports.
"""

import uuid
from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.extracted_marker_model import ExtractedMarker
from app.models.report_model import MedicalReport
from app.services.ai_service import ai_service
from app.utils.logger import logger


class TrendService:
    """Analyses marker trends across a user's historical reports."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_marker_trends(self, user_id: uuid.UUID) -> list[dict]:
        """
        Build time-series data for each unique health marker across all user reports.
        Returns list of marker trend dicts with data_points.
        """
        rows = (
            self._db.query(
                ExtractedMarker.marker_name,
                ExtractedMarker.numeric_value,
                ExtractedMarker.unit,
                ExtractedMarker.severity,
                ExtractedMarker.category,
                MedicalReport.created_at,
            )
            .join(MedicalReport, MedicalReport.id == ExtractedMarker.report_id)
            .filter(
                MedicalReport.user_id == user_id,
                MedicalReport.is_active == True,
                ExtractedMarker.numeric_value.isnot(None),
            )
            .order_by(MedicalReport.created_at.asc())
            .all()
        )

        # Group by marker name
        by_marker: dict[str, dict] = defaultdict(
            lambda: {"data_points": [], "unit": None, "category": None}
        )
        for row in rows:
            entry = by_marker[row.marker_name]
            entry["unit"] = row.unit
            entry["category"] = row.category
            entry["data_points"].append(
                {
                    "date": row.created_at.strftime("%Y-%m-%d"),
                    "value": float(row.numeric_value),
                    "severity": row.severity,
                }
            )

        trends = []
        for marker_name, data in by_marker.items():
            if len(data["data_points"]) >= 2:  # only meaningful with 2+ points
                trends.append(
                    {
                        "marker_name": marker_name,
                        "unit": data["unit"],
                        "category": data["category"],
                        "data_points": data["data_points"],
                    }
                )
        return trends

    def get_ai_trend_analysis(self, user_id: uuid.UUID, marker_name: str) -> dict:
        """Get AI-powered analysis for a specific marker's trend."""
        trends = self.get_marker_trends(user_id)
        marker_trend = next((t for t in trends if t["marker_name"] == marker_name), None)
        if not marker_trend or len(marker_trend["data_points"]) < 2:
            return {"trend": "insufficient_data", "analysis": "Not enough data points", "recommendation": ""}
        return ai_service.analyze_trend(marker_name, marker_trend["data_points"])
