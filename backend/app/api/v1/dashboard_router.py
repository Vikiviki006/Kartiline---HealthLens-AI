"""
Dashboard router — GET /api/v1/dashboard
"""

import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.controllers.dashboard_controller import DashboardController
from app.core.security import get_subject_from_token
from app.database.session import get_db

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def _get_user_id(request: Request) -> uuid.UUID:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return uuid.UUID(get_subject_from_token(auth[7:]))
    return uuid.UUID("00000000-0000-0000-0000-000000000001")


@router.get("", summary="Get dashboard summary data")
def get_dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Return aggregated dashboard data:
    - Total and abnormal report counts
    - Recent uploads
    - Top abnormal markers
    - Trend summaries
    - Latest AI analysis summary
    """
    user_id = _get_user_id(request)
    return DashboardController(db).get_dashboard(user_id)
