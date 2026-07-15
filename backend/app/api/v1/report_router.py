"""
Reports router — CRUD + analysis endpoints.
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.controllers.report_controller import ReportController
from app.api.deps import get_current_user_id
from app.database.session import get_db

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("", summary="List all reports for the current user")
def list_reports(
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    status: Optional[str] = Query(default=None),
    report_type: Optional[str] = Query(default=None),
    sort_by: str = Query(default="created_at"),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    """Paginated, filtered, sorted list of the user's medical reports."""
    ctrl = ReportController(db)
    return ctrl.list_reports(
        user_id=user_id,
        page=page,
        page_size=page_size,
        status=status,
        report_type=report_type,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/{report_id}", summary="Get a single report by ID")
def get_report(
    report_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    """Return full report detail including extracted markers."""
    return ReportController(db).get_report(report_id, user_id)


@router.delete("/{report_id}", summary="Soft-delete a report")
def delete_report(
    report_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    """Soft-delete a report (marks is_active=False)."""
    return ReportController(db).delete_report(report_id, user_id)


@router.post("/{report_id}/analyze", summary="Run AI analysis on a report")
def analyze_report(
    report_id: uuid.UUID,
    request: Request,
    force: bool = Query(default=False, description="Force regeneration even if analysis exists"),
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    """
    Trigger AI-powered health analysis for a report.
    Returns health summary, abnormal markers, recommendations, and doctor questions.
    """
    return ReportController(db).trigger_analysis(report_id, user_id, force)


@router.get("/{report_id}/pdf", summary="Export report analysis as PDF")
def export_report_pdf(
    report_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    """Generate and return a beautifully structured PDF summary of the report analysis."""
    from app.services.pdf_service import PDFService
    from fastapi.responses import StreamingResponse
    
    pdf_service = PDFService(db)
    pdf_buffer = pdf_service.generate_report_pdf(report_id, user_id)
    
    filename = f"HealthLens_Summary_{report_id}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
