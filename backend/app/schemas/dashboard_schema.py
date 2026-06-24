"""
Dashboard Pydantic schemas.
"""

from datetime import datetime
from uuid import UUID

from app.schemas.common_schema import BaseSchema


class TrendPoint(BaseSchema):
    date: str
    value: float
    severity: str


class MarkerTrend(BaseSchema):
    marker_name: str
    unit: str | None = None
    category: str | None = None
    data_points: list[TrendPoint]


class RecentUploadItem(BaseSchema):
    id: UUID
    original_filename: str
    status: str
    created_at: datetime


class AnalysisSummary(BaseSchema):
    report_id: UUID
    health_summary: str | None = None
    abnormal_count: int = 0
    recommendations_count: int = 0


class DashboardResponse(BaseSchema):
    """Full dashboard payload."""
    total_reports: int
    total_abnormal_reports: int
    pending_reports: int
    recent_uploads: list[RecentUploadItem]
    top_abnormal_markers: list[str]
    trend_summaries: list[MarkerTrend]
    latest_analysis: AnalysisSummary | None = None


# ── Analysis schemas ──────────────────────────────────────────────────────────

class AnalysisRequest(BaseSchema):
    force_regenerate: bool = False


class AnalysisResponse(BaseSchema):
    id: UUID
    report_id: UUID
    status: str
    ai_provider: str | None = None
    model_used: str | None = None
    health_summary: str | None = None
    abnormal_markers: list[dict] | None = None
    recommendations: list[dict] | None = None
    doctor_questions: list[str] | None = None
    processing_time_ms: int | None = None
    created_at: datetime
