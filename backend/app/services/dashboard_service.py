"""
DashboardService: aggregates data for the dashboard endpoint.
"""

import uuid

from sqlalchemy.orm import Session

from app.repositories.report_repository import ReportRepository
from app.repositories.analysis_repository import AnalysisRepository
from app.models.report_marker_model import ReportMarker
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
            latest_report = recent_reports[0]
            from app.models.marker_analysis_model import MarkerAnalysis
            
            abnormal_markers = self._db.query(ReportMarker).filter(
                ReportMarker.report_id == latest_report.id,
                ReportMarker.status.in_(["High", "Low", "Critical"])
            ).all()
            
            health_summary_parts = []
            for rm in abnormal_markers:
                ma = self._db.query(MarkerAnalysis).filter(MarkerAnalysis.report_marker_id == rm.id).first()
                if ma and ma.gemma_summary:
                    health_summary_parts.append(f"{rm.marker_name}: {ma.gemma_summary}")
                    
            latest_analysis = {
                "report_id": str(latest_report.id),
                "health_summary": "\n\n".join(health_summary_parts) if health_summary_parts else "All markers are normal.",
                "abnormal_markers": abnormal_markers,
                "recommendations": []
            }

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
        from app.models.report_model import Report

        result = (
            self._db.query(ReportMarker.marker_name, func.count(ReportMarker.id).label("cnt"))
            .join(Report, Report.id == ReportMarker.report_id)
            .filter(
                Report.user_id == user_id,
                ReportMarker.status.in_(
                    ["High", "Critical"]
                ),
            )
            .group_by(ReportMarker.marker_name)
            .order_by(func.count(ReportMarker.id).desc())
            .limit(limit)
            .all()
        )
        return [row.marker_name for row in result]
