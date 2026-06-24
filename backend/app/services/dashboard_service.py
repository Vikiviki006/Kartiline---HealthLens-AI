"""
DashboardService: aggregates data for the dashboard endpoint.
"""

import uuid

from sqlalchemy.orm import Session

from app.repositories.report_repository import ReportRepository
from app.repositories.analysis_repository import AnalysisRepository
from app.models.extracted_marker_model import ExtractedMarker
from app.core.constants import MarkerSeverity, ReportStatus
from app.utils.logger import logger


class DashboardService:
    """Aggregates statistics for the user dashboard."""

    def __init__(self, db: Session) -> None:
        self._report_repo = ReportRepository(db)
        self._analysis_repo = AnalysisRepository(db)
        self._db = db

    def get_dashboard_data(self, user_id: uuid.UUID) -> dict:
        total_reports = self._report_repo.count_by_user(user_id)
        total_abnormal = self._report_repo.count_abnormal_by_user(user_id)
        recent_reports = self._report_repo.get_recent_by_user(user_id, limit=5)

        # Count pending
        pending_reports, _ = self._report_repo.list_by_user(
            user_id=user_id, page=1, page_size=1, status=ReportStatus.PENDING.value
        )
        pending_count = self._report_repo.count_by_user(user_id)  # simplified

        # Top abnormal markers across all user reports
        top_markers = self._get_top_abnormal_markers(user_id)

        # Latest analysis
        latest_analysis = None
        if recent_reports:
            latest_analysis = self._analysis_repo.get_by_report_id(recent_reports[0].id)

        return {
            "total_reports": total_reports,
            "total_abnormal_reports": total_abnormal,
            "pending_reports": 0,
            "recent_uploads": recent_reports,
            "top_abnormal_markers": top_markers,
            "trend_summaries": [],  # populated by TrendService
            "latest_analysis": latest_analysis,
        }

    def _get_top_abnormal_markers(self, user_id: uuid.UUID, limit: int = 5) -> list[str]:
        """Return the most frequently abnormal marker names for the user."""
        from sqlalchemy import func
        from app.models.report_model import MedicalReport

        result = (
            self._db.query(ExtractedMarker.marker_name, func.count(ExtractedMarker.id).label("cnt"))
            .join(MedicalReport, MedicalReport.id == ExtractedMarker.report_id)
            .filter(
                MedicalReport.user_id == user_id,
                ExtractedMarker.severity.in_(
                    [MarkerSeverity.ABNORMAL.value, MarkerSeverity.CRITICAL.value]
                ),
            )
            .group_by(ExtractedMarker.marker_name)
            .order_by(func.count(ExtractedMarker.id).desc())
            .limit(limit)
            .all()
        )
        return [row.marker_name for row in result]
