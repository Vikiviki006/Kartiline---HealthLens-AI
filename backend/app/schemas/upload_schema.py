"""
Upload Pydantic schemas.
"""

from uuid import UUID
from pydantic import Field
from app.schemas.common_schema import BaseSchema


class UploadResponse(BaseSchema):
    """Returned after a successful file upload and OCR pass."""
    report_id: UUID
    original_filename: str
    stored_path: str
    file_size_bytes: int
    mime_type: str
    status: str
    ocr_engine_used: str | None = None
    extracted_text_preview: str | None = None
    message: str = "File uploaded and processed successfully"


class UploadHistoryResponse(BaseSchema):
    """Single upload history record."""
    id: UUID
    original_filename: str
    file_size_bytes: int
    upload_status: str
    created_at: str
