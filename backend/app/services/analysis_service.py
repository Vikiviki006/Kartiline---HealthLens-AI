"""
AnalysisService: coordinates AI analysis on a medical report.
"""

import uuid
import time

from sqlalchemy.orm import Session

from app.core.constants import AnalysisStatus
from app.core.exceptions import ReportNotFoundException, AnalysisNotFoundException
from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.report_repository import ReportRepository
from app.services.ai_service import ai_service
from app.models.analysis_model import AIAnalysis
from app.utils.logger import logger


class AnalysisService:
    """Orchestrates AI-powered health analysis for a report."""

    def __init__(self, db: Session) -> None:
        self._analysis_repo = AnalysisRepository(db)
        self._report_repo = ReportRepository(db)

    def run_analysis(self, report_id: uuid.UUID, user_id: uuid.UUID, force: bool = False) -> AIAnalysis:
        # Verify report ownership
        report = self._report_repo.get_by_id(report_id, user_id=user_id)
        if not report:
            raise ReportNotFoundException(str(report_id))

        # Check for existing analysis
        existing = self._analysis_repo.get_by_report_id(report_id)
        if existing and not force:
            return existing

        # Create or reset analysis record
        if existing:
            analysis = self._analysis_repo.update(
                existing.id, status=AnalysisStatus.RUNNING.value
            )
        else:
            analysis = self._analysis_repo.create(
                report_id=report_id,
                status=AnalysisStatus.RUNNING.value,
            )

        try:
            result = ai_service.analyze_report(report.extracted_text or "")
            self._analysis_repo.update(
                analysis.id,
                status=AnalysisStatus.COMPLETED.value,
                health_summary=result.get("health_summary"),
                abnormal_markers=result.get("abnormal_markers", []),
                recommendations=result.get("recommendations", []),
                doctor_questions=result.get("doctor_questions", []),
                ai_provider=result.get("ai_provider"),
                model_used=result.get("model_used"),
                processing_time_ms=result.get("processing_time_ms"),
            )
            logger.bind(report_id=str(report_id)).info("AI analysis completed")
        except Exception as exc:
            logger.error(f"AI analysis failed for report {report_id}: {exc}")
            self._analysis_repo.update(
                analysis.id,
                status=AnalysisStatus.FAILED.value,
                error_message=str(exc),
            )

        return self._analysis_repo.get_by_report_id(report_id)  # type: ignore

    def get_analysis(self, report_id: uuid.UUID, user_id: uuid.UUID) -> AIAnalysis:
        report = self._report_repo.get_by_id(report_id, user_id=user_id)
        if not report:
            raise ReportNotFoundException(str(report_id))
        analysis = self._analysis_repo.get_by_report_id(report_id)
        if not analysis:
            raise AnalysisNotFoundException(str(report_id))
        return analysis
