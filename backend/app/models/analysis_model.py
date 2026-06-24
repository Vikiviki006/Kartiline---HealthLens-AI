"""
AIAnalysis ORM model.
Stores the structured AI-generated analysis for a medical report.
"""

import uuid

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin
from app.core.constants import AnalysisStatus


class AIAnalysis(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """AI-generated health analysis linked to a MedicalReport (1:1)."""

    __tablename__ = "ai_analyses"

    report_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("medical_reports.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=AnalysisStatus.PENDING.value
    )
    ai_provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    model_used: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Structured JSON output columns
    health_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    abnormal_markers: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    recommendations: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    doctor_questions: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    raw_response: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    processing_time_ms: Mapped[int | None] = mapped_column(nullable=True)

    # ── Relationships ──────────────────────────────────────────────────────────
    report: Mapped["MedicalReport"] = relationship("MedicalReport", back_populates="analysis")  # type: ignore[name-defined]

    __table_args__ = (Index("ix_analyses_report_status", "report_id", "status"),)

    def __repr__(self) -> str:
        return f"<AIAnalysis id={self.id} report={self.report_id} status={self.status}>"
