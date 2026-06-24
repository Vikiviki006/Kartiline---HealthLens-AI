"""
MedicalReport ORM model.
"""

import uuid

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin
from app.core.constants import ReportStatus


class MedicalReport(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Represents a single uploaded medical report."""

    __tablename__ = "medical_reports"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    original_filename: Mapped[str] = mapped_column(String(512), nullable=False)
    stored_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(nullable=False, default=0)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False, default="application/pdf")
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=ReportStatus.PENDING.value, index=True
    )
    extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    ocr_engine_used: Mapped[str | None] = mapped_column(String(100), nullable=True)
    report_date: Mapped[str | None] = mapped_column(String(50), nullable=True)
    report_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Relationships ──────────────────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="reports")  # type: ignore[name-defined]
    markers: Mapped[list["ExtractedMarker"]] = relationship(  # type: ignore[name-defined]
        "ExtractedMarker", back_populates="report", cascade="all, delete-orphan"
    )
    analysis: Mapped["AIAnalysis | None"] = relationship(  # type: ignore[name-defined]
        "AIAnalysis", back_populates="report", uselist=False, cascade="all, delete-orphan"
    )
    upload_history: Mapped["UploadHistory | None"] = relationship(  # type: ignore[name-defined]
        "UploadHistory", back_populates="report", uselist=False
    )

    __table_args__ = (
        Index("ix_reports_user_status", "user_id", "status"),
        Index("ix_reports_user_created", "user_id", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<MedicalReport id={self.id} filename={self.original_filename} status={self.status}>"
