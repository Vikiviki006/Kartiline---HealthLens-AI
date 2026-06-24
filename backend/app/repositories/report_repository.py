"""
ReportRepository: all database interactions for MedicalReport and ExtractedMarker.
"""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import and_, desc, asc, func
from sqlalchemy.orm import Session, joinedload

from app.models.report_model import MedicalReport
from app.models.extracted_marker_model import ExtractedMarker
from app.core.constants import ReportStatus, MarkerSeverity
from app.utils.logger import logger


class ReportRepository:
    """Data access layer for medical reports and their markers."""

    def __init__(self, db: Session) -> None:
        self._db = db

    # ── Create ────────────────────────────────────────────────────────────────

    def create(self, **kwargs: Any) -> MedicalReport:
        report = MedicalReport(**kwargs)
        self._db.add(report)
        self._db.flush()
        logger.bind(report_id=str(report.id)).debug("Report record created")
        return report

    def create_markers(self, report_id: uuid.UUID, markers: list[dict]) -> list[ExtractedMarker]:
        objs = [ExtractedMarker(report_id=report_id, **m) for m in markers]
        self._db.add_all(objs)
        self._db.flush()
        return objs

    # ── Read ──────────────────────────────────────────────────────────────────

    def get_by_id(self, report_id: uuid.UUID, user_id: uuid.UUID | None = None) -> MedicalReport | None:
        q = self._db.query(MedicalReport).options(joinedload(MedicalReport.markers))
        q = q.filter(MedicalReport.id == report_id, MedicalReport.is_active == True)
        if user_id:
            q = q.filter(MedicalReport.user_id == user_id)
        return q.first()

    def list_by_user(
        self,
        user_id: uuid.UUID,
        page: int = 1,
        page_size: int = 10,
        status: str | None = None,
        report_type: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[MedicalReport], int]:
        q = self._db.query(MedicalReport).filter(
            MedicalReport.user_id == user_id,
            MedicalReport.is_active == True,
        )
        if status:
            q = q.filter(MedicalReport.status == status)
        if report_type:
            q = q.filter(MedicalReport.report_type == report_type)

        total = q.count()

        sort_col = getattr(MedicalReport, sort_by, MedicalReport.created_at)
        q = q.order_by(desc(sort_col) if sort_order == "desc" else asc(sort_col))
        q = q.offset((page - 1) * page_size).limit(page_size)
        return q.all(), total

    def count_by_user(self, user_id: uuid.UUID) -> int:
        return (
            self._db.query(func.count(MedicalReport.id))
            .filter(MedicalReport.user_id == user_id, MedicalReport.is_active == True)
            .scalar()
            or 0
        )

    def count_abnormal_by_user(self, user_id: uuid.UUID) -> int:
        """Count reports that have at least one abnormal marker."""
        subq = (
            self._db.query(ExtractedMarker.report_id)
            .filter(ExtractedMarker.severity.in_(
                [MarkerSeverity.ABNORMAL.value, MarkerSeverity.CRITICAL.value]
            ))
            .distinct()
            .subquery()
        )
        return (
            self._db.query(func.count(MedicalReport.id))
            .filter(
                MedicalReport.user_id == user_id,
                MedicalReport.is_active == True,
                MedicalReport.id.in_(subq),
            )
            .scalar()
            or 0
        )

    def get_recent_by_user(self, user_id: uuid.UUID, limit: int = 5) -> list[MedicalReport]:
        return (
            self._db.query(MedicalReport)
            .filter(MedicalReport.user_id == user_id, MedicalReport.is_active == True)
            .order_by(desc(MedicalReport.created_at))
            .limit(limit)
            .all()
        )

    # ── Update ────────────────────────────────────────────────────────────────

    def update_status(self, report_id: uuid.UUID, status: str, error_message: str | None = None) -> None:
        self._db.query(MedicalReport).filter(MedicalReport.id == report_id).update(
            {"status": status, "error_message": error_message},
            synchronize_session=False,
        )

    def update(self, report_id: uuid.UUID, **kwargs: Any) -> MedicalReport | None:
        self._db.query(MedicalReport).filter(MedicalReport.id == report_id).update(
            kwargs, synchronize_session=False
        )
        return self.get_by_id(report_id)

    # ── Delete ────────────────────────────────────────────────────────────────

    def soft_delete(self, report_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        count = (
            self._db.query(MedicalReport)
            .filter(
                MedicalReport.id == report_id,
                MedicalReport.user_id == user_id,
                MedicalReport.is_active == True,
            )
            .update({"is_active": False}, synchronize_session=False)
        )
        return count > 0
