"""
Health check router — GET /api/v1/health
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import check_db_connection, get_db
from app.core.config import settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", summary="System health check")
def health_check(db: Session = Depends(get_db)):
    """Returns liveness and readiness status of the application."""
    db_ok = check_db_connection()
    return {
        "status": "healthy" if db_ok else "degraded",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "database": "connected" if db_ok else "unreachable",
    }


@router.get("/ping", summary="Liveness ping")
def ping():
    """Simple ping — no database check."""
    return {"ping": "pong"}
