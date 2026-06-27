"""
Dashboard router — GET /api/v1/dashboard
"""

import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.controllers.dashboard_controller import DashboardController
from app.api.deps import get_current_user_id
from app.database.session import get_db

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", summary="Get dashboard summary data")
def get_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    """
    Return aggregated dashboard data:
    - Total and abnormal report counts
    - Recent uploads
    - Top abnormal markers
    - Trend summaries
    - Latest AI analysis summary
    """
    return DashboardController(db).get_dashboard(user_id)
