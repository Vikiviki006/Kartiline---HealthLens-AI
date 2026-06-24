"""
Common / shared Pydantic schemas.
"""

from typing import Any, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema with shared config."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PaginationParams(BaseModel):
    """Query parameters for paginated endpoints."""
    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(default=10, ge=1, le=100, description="Items per page")


class PaginationMeta(BaseSchema):
    page: int
    page_size: int
    total: int
    total_pages: int


class PaginatedResponse(BaseSchema, Generic[T]):
    success: bool = True
    message: str = "Data retrieved successfully"
    data: list[T]
    meta: PaginationMeta


class MessageResponse(BaseSchema):
    success: bool = True
    message: str


class ErrorDetail(BaseSchema):
    field: str | None = None
    message: str


class ErrorResponseSchema(BaseSchema):
    success: bool = False
    message: str
    error_code: str
    errors: list[ErrorDetail] | None = None
