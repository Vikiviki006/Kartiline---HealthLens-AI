"""
AnalysisRepository: database interactions for AIAnalysis model.
"""

import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.models.analysis_model import AIAnalysis
from app.core.constants import AnalysisStatus
from app.utils.logger import logger


class AnalysisRepository:
    """Data access layer for AI analysis records."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, **kwargs: Any) -> AIAnalysis:
        obj = AIAnalysis(**kwargs)
        self._db.add(obj)
        self._db.flush()
        return obj

    def get_by_report_id(self, report_id: uuid.UUID) -> AIAnalysis | None:
        return (
            self._db.query(AIAnalysis)
            .filter(AIAnalysis.report_id == report_id, AIAnalysis.is_active == True)
            .first()
        )

    def update(self, analysis_id: uuid.UUID, **kwargs: Any) -> AIAnalysis | None:
        self._db.query(AIAnalysis).filter(AIAnalysis.id == analysis_id).update(
            kwargs, synchronize_session=False
        )
        return self._db.query(AIAnalysis).get(analysis_id)
