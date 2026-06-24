"""
Dashboard Controller — aggregates dashboard data.
"""

import uuid

from sqlalchemy.orm import Session

from app.services.dashboard_service import DashboardService
from app.services.trend_service import TrendService
from app.utils.response import success_response
from fastapi.responses import JSONResponse


class DashboardController:
    """Coordinates dashboard data aggregation."""

    def __init__(self, db: Session) -> None:
        self._dashboard_svc = DashboardService(db)
        self._trend_svc = TrendService(db)

    def get_dashboard(self, user_id: uuid.UUID) -> JSONResponse:
        data = self._dashboard_svc.get_dashboard_data(user_id)
        trends = self._trend_svc.get_marker_trends(user_id)

        return success_response(
            data={
                "total_reports": data["total_reports"],
                "total_abnormal_reports": data["total_abnormal_reports"],
                "pending_reports": data["pending_reports"],
                "recent_uploads": [
                    {
                        "id": str(r.id),
                        "original_filename": r.original_filename,
                        "status": r.status,
                        "created_at": r.created_at.isoformat(),
                    }
                    for r in data["recent_uploads"]
                ],
                "top_abnormal_markers": data["top_abnormal_markers"],
                "trend_summaries": trends,
                "latest_analysis": (
                    {
                        "report_id": str(data["latest_analysis"].report_id),
                        "health_summary": data["latest_analysis"].health_summary,
                        "abnormal_count": len(data["latest_analysis"].abnormal_markers or []),
                        "recommendations_count": len(data["latest_analysis"].recommendations or []),
                    }
                    if data.get("latest_analysis")
                    else None
                ),
            }
        )
