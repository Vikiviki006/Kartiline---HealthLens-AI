"""
Request/response logging middleware.
Logs every request with method, path, status code, and duration.
"""

import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.utils.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Structured per-request logging."""

    SKIP_PATHS = {"/api/v1/health/ping", "/favicon.ico"}

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in self.SKIP_PATHS:
            return await call_next(request)

        request_id = str(uuid.uuid4())[:8]
        start = time.monotonic()

        logger.bind(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client=request.client.host if request.client else "unknown",
        ).info("→ Request received")

        response = await call_next(request)
        elapsed_ms = int((time.monotonic() - start) * 1000)

        logger.bind(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=elapsed_ms,
        ).info("← Response sent")

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time-Ms"] = str(elapsed_ms)
        return response
