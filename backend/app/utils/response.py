"""
Standardised API response helpers.
Every endpoint returns a consistent envelope:

Success:
    {"success": true, "message": "...", "data": {...}, "meta": {...}}

Error:
    {"success": false, "message": "...", "error_code": "...", "errors": [...]}
"""

from typing import Any, TypeVar, Generic
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from fastapi import status


T = TypeVar("T")


# ── Response models ───────────────────────────────────────────────────────────

class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "OK"
    data: T | None = None
    meta: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: str
    errors: list[Any] | None = None


# ── Helper functions ──────────────────────────────────────────────────────────

def success_response(
    data: Any = None,
    message: str = "Request successful",
    status_code: int = status.HTTP_200_OK,
    meta: dict[str, Any] | None = None,
) -> JSONResponse:
    """Return a standardised success JSON response."""
    body = {
        "success": True,
        "message": message,
        "data": data,
    }
    if meta is not None:
        body["meta"] = meta
    return JSONResponse(content=body, status_code=status_code)


def created_response(data: Any = None, message: str = "Resource created successfully") -> JSONResponse:
    return success_response(data=data, message=message, status_code=status.HTTP_201_CREATED)


def error_response(
    message: str,
    error_code: str,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    errors: list[Any] | None = None,
) -> JSONResponse:
    """Return a standardised error JSON response."""
    body: dict[str, Any] = {
        "success": False,
        "message": message,
        "error_code": error_code,
    }
    if errors:
        body["errors"] = errors
    return JSONResponse(content=body, status_code=status_code)


def paginated_response(
    data: list[Any],
    page: int,
    page_size: int,
    total: int,
    message: str = "Data retrieved successfully",
) -> JSONResponse:
    """Return a success response with pagination metadata."""
    import math
    total_pages = math.ceil(total / page_size) if page_size > 0 else 0
    return success_response(
        data=data,
        message=message,
        meta={
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
        },
    )
