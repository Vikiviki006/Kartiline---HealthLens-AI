"""
AnalysisService: coordinates the new AI pipeline on a medical report.
Upload -> OCR -> Parser -> Rule Engine -> RAG -> Gemma -> Store
"""

import uuid
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.core.constants import ReportStatus
from app.core.exceptions import ReportNotFoundException
from app.repositories.report_repository import ReportRepository
from app.services.parser_service import parser_service
from app.services.rule_engine import rule_engine
from app.services.retrieval_service import retrieval_service
from app.services.prompt_builder import prompt_builder
from app.services.gemma_service import gemma_service
from app.models.report_marker_model import ReportMarker
from app.models.marker_analysis_model import MarkerAnalysis
from app.utils.logger import logger

class AnalysisService:
    """Orchestrates the structured pipeline for health analysis."""

    def __init__(self, db: Session) -> None:
        self._db = db
        self._report_repo = ReportRepository(db)

    def run_analysis(self, report_id: uuid.UUID, user_id: uuid.UUID, force: bool = False):
        report = self._report_repo.get_by_id(report_id, user_id=user_id)
        if not report:
            raise ReportNotFoundException(str(report_id))

        if not report.extracted_text:
            logger.warning(f"Report {report_id} has no extracted text.")
            return report
            
        # Clean existing markers if forcing
        if force:
            self._db.query(ReportMarker).filter(ReportMarker.report_id == report.id).delete()
            self._db.commit()
        else:
            existing = self._db.query(ReportMarker).filter(ReportMarker.report_id == report.id).first()
            if existing:
                return report

        try:
            # 1. Parse OCR -> JSON
            parsed_data = parser_service.parse(report.extracted_text)
            patient_info = parsed_data.get("patient", {})
            markers = parsed_data.get("markers", [])

            # 2. Rule Engine
            markers = rule_engine.process_markers(markers)

            # 3. RAG + Gemma for each marker
            for m in markers:
                rm = ReportMarker(
                    report_id=report.id,
                    marker_name=m.get("name", "Unknown"),
                    value=str(m.get("value", "")),
                    unit=m.get("unit", ""),
                    reference_range=m.get("reference_range", ""),
                    status=m.get("status", "Unknown")
                )
                self._db.add(rm)
                self._db.commit()
                self._db.refresh(rm)

                knowledge = retrieval_service.retrieve_knowledge(self._db, rm.marker_name)
                
                gemma_summary = None
                if rm.status in ["Low", "High", "Critical"]:
                    prompt = prompt_builder.build_prompt(patient_info, m, knowledge)
                    try:
                        gemma_summary = gemma_service.generate_summary(prompt)
                    except Exception as e:
                        logger.error(f"Gemma failed for marker {rm.marker_name}: {e}")
                
                ma = MarkerAnalysis(
                    report_marker_id=rm.id,
                    retrieved_knowledge_id=knowledge.id if knowledge else None,
                    gemma_summary=gemma_summary
                )
                self._db.add(ma)

            self._db.commit()
            
            # update report status
            report.status = ReportStatus.COMPLETED.value
            self._db.commit()
            
            logger.bind(report_id=str(report_id)).info("AI structured analysis completed")
            return report
            
        except Exception as exc:
            logger.error(f"Analysis failed for report {report_id}: {exc}")
            report.status = ReportStatus.FAILED.value
            self._db.commit()
            raise exc

    def get_analysis(self, report_id: uuid.UUID, user_id: uuid.UUID):
        # We return the report with its markers and analysis
        report = self._db.query(self._report_repo._model).filter_by(id=report_id, user_id=user_id).first()
        if not report:
             raise ReportNotFoundException(str(report_id))
        return report
