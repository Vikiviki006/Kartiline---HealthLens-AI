"""
Report Pydantic schemas.
"""

from datetime import datetime
from uuid import UUID

from pydantic import Field
from app.schemas.common_schema import BaseSchema


# ── Marker schemas ────────────────────────────────────────────────────────────

class MarkerResponse(BaseSchema):
    id: UUID
    marker_name: str
    value: str | None = None
    unit: str | None = None
    reference_range: str | None = None
    severity: str
    numeric_value: float | None = None
    category: str | None = None


# ── Report schemas ────────────────────────────────────────────────────────────

class ReportListResponse(BaseSchema):
    """Compact report summary for list views."""
    id: UUID
    original_filename: str
    file_size_bytes: int
    status: str
    report_type: str | None = None
    report_date: str | None = None
    created_at: datetime
    total_markers: int = 0
    abnormal_markers: int = 0


class ReportDetailResponse(ReportListResponse):
    """Full report with markers and extracted text."""
    stored_path: str
    mime_type: str
    ocr_engine_used: str | None = None
    extracted_text: str | None = None
    markers: list[MarkerResponse] = Field(default_factory=list)


class ReportFilterParams(BaseSchema):
    """Query parameters for filtering/sorting report lists."""
    status: str | None = None
    report_type: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    sort_by: str = "created_at"
    sort_order: str = "desc"
