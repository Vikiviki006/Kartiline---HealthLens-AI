"""
API v1 aggregator — mounts all v1 routers under /api/v1
"""

from fastapi import APIRouter

from app.api.v1.auth_router import router as auth_router
from app.api.v1.upload_router import router as upload_router
from app.api.v1.report_router import router as report_router
from app.api.v1.dashboard_router import router as dashboard_router
from app.api.v1.health_router import router as health_router
from app.api.v1.chat_router import router as chat_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(upload_router)
api_router.include_router(report_router)
api_router.include_router(dashboard_router)
api_router.include_router(health_router)
api_router.include_router(chat_router)
