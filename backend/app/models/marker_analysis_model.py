"""
MarkerAnalysis ORM model.
"""

import uuid
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin

class MarkerAnalysis(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "marker_analysis"

    report_marker_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("report_markers.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    retrieved_knowledge_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("medical_markers.id", ondelete="SET NULL"), nullable=True)
    gemma_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    marker: Mapped["ReportMarker"] = relationship("ReportMarker", back_populates="analysis")
    knowledge: Mapped["MedicalMarker"] = relationship("MedicalMarker")

    def __repr__(self) -> str:
        return f"<MarkerAnalysis marker_id={self.report_marker_id}>"
