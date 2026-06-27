"""
Upload Controller — coordinates upload request handling.
"""

import uuid
from fastapi import UploadFile, Request

from sqlalchemy.orm import Session

from app.services.report_service import ReportService
from app.repositories.upload_repository import UploadRepository
from app.utils.file_helper import save_upload_file
from app.utils.validators import validate_file_extension, validate_file_size
from app.utils.response import created_response
from app.utils.logger import logger
from fastapi.responses import JSONResponse


class UploadController:
    """Coordinates file validation, storage, and OCR trigger."""

    def __init__(self, db: Session) -> None:
        self._report_service = ReportService(db)
        self._upload_repo = UploadRepository(db)

    async def handle_upload(
        self,
        file: UploadFile,
        user_id: uuid.UUID,
        request: Request,
    ) -> JSONResponse:
        file_bytes = await file.read()
        filename = file.filename or "unknown"
        mime_type = file.content_type or "application/octet-stream"

        # Validate
        validate_file_extension(filename)
        validate_file_size(len(file_bytes))

        # Persist to disk
        stored_path = save_upload_file(file_bytes, filename)

        # Create report + run OCR
        report = self._report_service.process_report(
            user_id=user_id,
            original_filename=filename,
            stored_path=stored_path,
            file_size_bytes=len(file_bytes),
            mime_type=mime_type,
        )

        # Audit trail
        self._upload_repo.create(
            user_id=user_id,
            report_id=report.id,
            original_filename=filename,
            file_size_bytes=len(file_bytes),
            mime_type=mime_type,
            upload_status="success",
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
        self._upload_repo._db.commit()

        preview = (report.extracted_text or "")[:300]
        return created_response(
            data={
                "report_id": str(report.id),
                "original_filename": report.original_filename,
                "stored_path": report.stored_path,
                "file_size_bytes": report.file_size_bytes,
                "mime_type": report.mime_type,
                "status": report.status,
                "ocr_engine_used": report.ocr_engine_used,
                "extracted_text_preview": preview,
            },
            message="File uploaded and OCR processed successfully",
        )
