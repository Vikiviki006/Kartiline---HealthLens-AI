"""
ReportMarker ORM model.
"""

import uuid
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin

class ReportMarker(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "report_markers"

    report_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("reports.id", ondelete="CASCADE"), nullable=False, index=True)
    marker_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    value: Mapped[str | None] = mapped_column(String(100), nullable=True)
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    reference_range: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    numeric_value: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)

    report: Mapped["Report"] = relationship("Report", back_populates="markers")
    analysis: Mapped["MarkerAnalysis"] = relationship("MarkerAnalysis", back_populates="marker", uselist=False, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<ReportMarker {self.marker_name}={self.value}>"
