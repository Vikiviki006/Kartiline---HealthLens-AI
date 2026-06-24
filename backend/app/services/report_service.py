"""
ReportService: business logic for report management.
"""

import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.core.constants import ReportStatus, MarkerSeverity
from app.core.exceptions import ReportNotFoundException
from app.models.extracted_marker_model import ExtractedMarker
from app.models.report_model import MedicalReport
from app.repositories.report_repository import ReportRepository
from app.services.ocr_service import ocr_service
from app.utils.logger import logger


class ReportService:
    """Orchestrates report creation, OCR processing, and retrieval."""

    def __init__(self, db: Session) -> None:
        self._repo = ReportRepository(db)

    def process_report(
        self,
        user_id: uuid.UUID,
        original_filename: str,
        stored_path: str,
        file_size_bytes: int,
        mime_type: str,
    ) -> MedicalReport:
        """
        Create a new report record, run OCR, persist extracted text.
        """
        # Create report in PENDING state
        report = self._repo.create(
            user_id=user_id,
            original_filename=original_filename,
            stored_path=stored_path,
            file_size_bytes=file_size_bytes,
            mime_type=mime_type,
            status=ReportStatus.PENDING.value,
        )

        try:
            self._repo.update_status(report.id, ReportStatus.PROCESSING.value)
            extracted_text, engine_used = ocr_service.extract_text(stored_path)

            self._repo.update(
                report.id,
                status=ReportStatus.COMPLETED.value,
                extracted_text=extracted_text,
                ocr_engine_used=engine_used,
            )
            logger.bind(report_id=str(report.id)).info("Report OCR completed")
        except Exception as exc:
            logger.error(f"OCR failed for report {report.id}: {exc}")
            self._repo.update_status(
                report.id, ReportStatus.FAILED.value, error_message=str(exc)
            )

        return self._repo.get_by_id(report.id)  # type: ignore

    def get_report(self, report_id: uuid.UUID, user_id: uuid.UUID) -> MedicalReport:
        report = self._repo.get_by_id(report_id, user_id=user_id)
        if not report:
            raise ReportNotFoundException(str(report_id))
        return report

    def list_reports(
        self,
        user_id: uuid.UUID,
        page: int,
        page_size: int,
        status: str | None = None,
        report_type: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[MedicalReport], int]:
        return self._repo.list_by_user(
            user_id=user_id,
            page=page,
            page_size=page_size,
            status=status,
            report_type=report_type,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    def delete_report(self, report_id: uuid.UUID, user_id: uuid.UUID) -> None:
        deleted = self._repo.soft_delete(report_id, user_id)
        if not deleted:
            raise ReportNotFoundException(str(report_id))

    def save_markers(self, report_id: uuid.UUID, markers: list[dict]) -> None:
        self._repo.create_markers(report_id, markers)
