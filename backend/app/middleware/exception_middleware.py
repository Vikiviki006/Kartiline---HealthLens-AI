"""
Global exception handler middleware.
Catches all unhandled exceptions and returns consistent error envelopes.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import HTTPException

from app.core.exceptions import AppException
from app.utils.logger import logger


class ExceptionMiddleware(BaseHTTPMiddleware):
    """Translate exceptions to structured JSON error responses."""

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except AppException as exc:
            logger.warning(
                f"AppException [{exc.error_code}] {exc.message} "
                f"(status={exc.status_code})"
            )
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "message": exc.message,
                    "error_code": exc.error_code,
                },
            )
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "message": exc.detail,
                    "error_code": "HTTP_ERROR",
                },
                headers=exc.headers
            )
        except Exception as exc:
            logger.exception(f"Unhandled exception: {exc}")
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "An unexpected internal error occurred.",
                    "error_code": "INTERNAL_SERVER_ERROR",
                },
            )
