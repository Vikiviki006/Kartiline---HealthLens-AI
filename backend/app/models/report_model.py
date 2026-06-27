"""
Report ORM model.
"""

import uuid
from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin
from app.core.constants import ReportStatus

class Report(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "reports"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    original_filename: Mapped[str] = mapped_column(String(512), nullable=False)
    stored_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default=ReportStatus.PENDING.value, index=True)
    extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_size_bytes: Mapped[int] = mapped_column(nullable=False, default=0)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False, default="application/pdf")
    ocr_engine_used: Mapped[str | None] = mapped_column(String(100), nullable=True)
    report_date: Mapped[str | None] = mapped_column(String(50), nullable=True)
    report_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="reports")
    markers: Mapped[list["ReportMarker"]] = relationship("ReportMarker", back_populates="report", cascade="all, delete-orphan")
    upload_history: Mapped["UploadHistory | None"] = relationship("UploadHistory", back_populates="report", uselist=False)

    def __repr__(self) -> str:
        return f"<Report id={self.id} status={self.status}>"
