"""
MedicalMarker ORM model.
Stores curated medical knowledge for every laboratory marker.
"""

from sqlalchemy import String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin

class MedicalMarker(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Knowledge base entry for a medical marker."""

    __tablename__ = "medical_markers"

    marker_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    category: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    purpose: Mapped[str | None] = mapped_column(Text, nullable=True)
    normal_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    low_meaning: Mapped[str | None] = mapped_column(Text, nullable=True)
    high_meaning: Mapped[str | None] = mapped_column(Text, nullable=True)
    possible_causes_low: Mapped[str | None] = mapped_column(Text, nullable=True)
    possible_causes_high: Mapped[str | None] = mapped_column(Text, nullable=True)
    lifestyle_recommendations: Mapped[str | None] = mapped_column(Text, nullable=True)
    diet_recommendations: Mapped[str | None] = mapped_column(Text, nullable=True)
    exercise_recommendations: Mapped[str | None] = mapped_column(Text, nullable=True)
    doctor_advice: Mapped[str | None] = mapped_column(Text, nullable=True)
    severity_information: Mapped[str | None] = mapped_column(Text, nullable=True)
    references: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<MedicalMarker {self.marker_name}>"
