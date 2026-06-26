"""
Report Controller — coordinates report CRUD and analysis requests.
"""

import uuid
import math

from sqlalchemy.orm import Session

from app.services.report_service import ReportService
from app.services.analysis_service import AnalysisService
from app.utils.response import success_response, paginated_response
from fastapi.responses import JSONResponse


class ReportController:
    """Coordinates report listing, retrieval, deletion, and analysis."""

    def __init__(self, db: Session) -> None:
        self._report_svc = ReportService(db)
        self._analysis_svc = AnalysisService(db)

    def list_reports(
        self,
        user_id: uuid.UUID,
        page: int,
        page_size: int,
        status: str | None,
        report_type: str | None,
        sort_by: str,
        sort_order: str,
    ) -> JSONResponse:
        reports, total = self._report_svc.list_reports(
            user_id=user_id,
            page=page,
            page_size=page_size,
            status=status,
            report_type=report_type,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        data = [
            {
                "id": str(r.id),
                "original_filename": r.original_filename,
                "file_size_bytes": r.file_size_bytes,
                "status": r.status,
                "report_type": r.report_type,
                "report_date": r.report_date,
                "created_at": r.created_at.isoformat(),
                "total_markers": len(r.markers) if hasattr(r, "markers") else 0,
                "abnormal_markers": sum(
                    1 for m in (r.markers or [])
                    if m.status in ("abnormal", "critical")
                ),
            }
            for r in reports
        ]
        return paginated_response(data=data, page=page, page_size=page_size, total=total)

    def get_report(self, report_id: uuid.UUID, user_id: uuid.UUID) -> JSONResponse:
        report = self._report_svc.get_report(report_id, user_id)
        return success_response(
            data={
                "id": str(report.id),
                "original_filename": report.original_filename,
                "stored_path": report.stored_path,
                "file_size_bytes": report.file_size_bytes,
                "mime_type": report.mime_type,
                "status": report.status,
                "report_type": report.report_type,
                "report_date": report.report_date,
                "ocr_engine_used": report.ocr_engine_used,
                "extracted_text": report.extracted_text,
                "created_at": report.created_at.isoformat(),
                "markers": [
                    {
                        "id": str(m.id),
                        "marker_name": m.marker_name,
                        "value": m.value,
                        "unit": m.unit,
                        "reference_range": m.reference_range,
                        "severity": m.status,
                        "numeric_value": float(m.numeric_value) if m.numeric_value else None,
                        "category": m.category,
                    }
                    for m in (report.markers or [])
                ],
            }
        )

    def delete_report(self, report_id: uuid.UUID, user_id: uuid.UUID) -> JSONResponse:
        self._report_svc.delete_report(report_id, user_id)
        return success_response(message="Report deleted successfully")

    def trigger_analysis(
        self, report_id: uuid.UUID, user_id: uuid.UUID, force: bool = False
    ) -> JSONResponse:
        report = self._analysis_svc.run_analysis(report_id, user_id, force)
        return success_response(
            data={
                "report_id": str(report.id),
                "status": report.status,
                "message": "Analysis completed successfully"
            }
        )
