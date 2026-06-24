"""
ExtractedMarker ORM model.
Stores individual health markers parsed from a medical report.
"""

import uuid

from sqlalchemy import ForeignKey, Index, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin
from app.core.constants import MarkerSeverity


class ExtractedMarker(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """A single health marker extracted from a medical report."""

    __tablename__ = "extracted_markers"

    report_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("medical_reports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    marker_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    value: Mapped[str | None] = mapped_column(String(100), nullable=True)
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    reference_range: Mapped[str | None] = mapped_column(String(100), nullable=True)
    severity: Mapped[str] = mapped_column(
        String(50), nullable=False, default=MarkerSeverity.NORMAL.value, index=True
    )
    numeric_value: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True)
    reference_min: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True)
    reference_max: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # ── Relationships ──────────────────────────────────────────────────────────
    report: Mapped["MedicalReport"] = relationship("MedicalReport", back_populates="markers")  # type: ignore[name-defined]

    __table_args__ = (
        Index("ix_markers_report_severity", "report_id", "severity"),
        Index("ix_markers_name", "marker_name"),
    )

    def __repr__(self) -> str:
        return f"<ExtractedMarker {self.marker_name}={self.value} {self.unit} [{self.severity}]>"
