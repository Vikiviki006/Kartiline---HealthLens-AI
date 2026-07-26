"""
HealthLens AI — FastAPI Application Entry Point.

Initialises middleware, CORS, exception handlers, and mounts all routers.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from app.database.base import Base
from app.database.session import engine
from app.api.router import api_router
from app.core.config import settings
from app.middleware.exception_middleware import ExceptionMiddleware
from app.middleware.logging_middleware import LoggingMiddleware
from app.utils.logger import logger
import app.models


# ── Lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown hooks."""
    logger.info(
        f"[START] Starting {settings.APP_NAME} v{settings.APP_VERSION} "
        f"[env={settings.APP_ENV}]"
    )
    # Ensure upload directory exists
    from app.utils.file_helper import ensure_upload_dir
    try:
        ensure_upload_dir()
    except Exception as exc:
        logger.warning(f"Upload directory setup warning: {exc}")

    try:
        Base.metadata.create_all(bind=engine)
    except Exception as exc:
        logger.warning(f"Database schema auto-creation skipped or failed: {exc}")

    yield
    logger.info(f"[STOP] {settings.APP_NAME} shutting down")


# ── App factory ────────────────────────────────────────────────────────────────

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "HealthLens AI — Medical Report Intelligence Platform. "
            "Upload medical reports, extract health markers via OCR, "
            "analyse with AI, and track historical trends."
        ),
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
        lifespan=lifespan,
    )

    # ── Middleware (order matters — outermost added last) ─────────────────────
    app.add_middleware(ExceptionMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Pydantic validation error handler ─────────────────────────────────────
    @app.exception_handler(ValidationError)
    async def pydantic_validation_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "Request validation failed",
                "error_code": "VALIDATION_ERROR",
                "errors": exc.errors(),
            },
        )

    # ── Routers ───────────────────────────────────────────────────────────────
    app.include_router(api_router)

    # ── Root endpoint ─────────────────────────────────────────────────────────
    @app.get("/", tags=["Root"], include_in_schema=False)
    def root():
        return {
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "running",
            "docs": "/docs",
        }

    return app


app = create_app()
