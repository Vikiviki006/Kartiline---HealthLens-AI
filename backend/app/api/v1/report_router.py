"""
Reports router — CRUD + analysis endpoints.
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.controllers.report_controller import ReportController
from app.core.security import get_subject_from_token
from app.database.session import get_db

router = APIRouter(prefix="/reports", tags=["Reports"])


def _get_user_id(request: Request) -> uuid.UUID:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        subject = get_subject_from_token(auth[7:])
        try:
            # Try to parse as UUID
            return uuid.UUID(subject)
        except ValueError:
            # If it's an email (demo mode), generate a consistent UUID from it
            return uuid.uuid5(uuid.NAMESPACE_DNS, subject)
    return uuid.UUID("00000000-0000-0000-0000-000000000001")


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
):
    """Paginated, filtered, sorted list of the user's medical reports."""
    user_id = _get_user_id(request)
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
):
    """Return full report detail including extracted markers."""
    user_id = _get_user_id(request)
    return ReportController(db).get_report(report_id, user_id)


@router.delete("/{report_id}", summary="Soft-delete a report")
def delete_report(
    report_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    """Soft-delete a report (marks is_active=False)."""
    user_id = _get_user_id(request)
    return ReportController(db).delete_report(report_id, user_id)


@router.post("/{report_id}/analyze", summary="Run AI analysis on a report")
def analyze_report(
    report_id: uuid.UUID,
    request: Request,
    force: bool = Query(default=False, description="Force regeneration even if analysis exists"),
    db: Session = Depends(get_db),
):
    """
    Trigger AI-powered health analysis for a report.
    Returns health summary, abnormal markers, recommendations, and doctor questions.
    """
    user_id = _get_user_id(request)
    return ReportController(db).trigger_analysis(report_id, user_id, force)
