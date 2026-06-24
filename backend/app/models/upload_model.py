"""
UploadHistory ORM model.
Tracks every file upload attempt with metadata.
"""

import uuid

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class UploadHistory(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Audit record for every upload attempt."""

    __tablename__ = "upload_history"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    report_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("medical_reports.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    original_filename: Mapped[str] = mapped_column(String(512), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(nullable=False, default=0)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    upload_status: Mapped[str] = mapped_column(String(50), nullable=False, default="success")
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(512), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Relationships ──────────────────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="upload_history")  # type: ignore[name-defined]
    report: Mapped["MedicalReport | None"] = relationship(  # type: ignore[name-defined]
        "MedicalReport", back_populates="upload_history"
    )

    __table_args__ = (
        Index("ix_upload_history_user_created", "user_id", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<UploadHistory id={self.id} file={self.original_filename} status={self.upload_status}>"
