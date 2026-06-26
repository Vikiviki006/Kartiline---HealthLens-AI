import os

models_dir = "app/models"
services_dir = "app/services"
repositories_dir = "app/repositories"
schemas_dir = "app/schemas"

# 1. Models
report_model_code = '''"""
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

    user: Mapped["User"] = relationship("User", back_populates="reports")
    markers: Mapped[list["ReportMarker"]] = relationship("ReportMarker", back_populates="report", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Report id={self.id} status={self.status}>"
'''

report_marker_model_code = '''"""
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

    report: Mapped["Report"] = relationship("Report", back_populates="markers")
    analysis: Mapped["MarkerAnalysis"] = relationship("MarkerAnalysis", back_populates="marker", uselist=False, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<ReportMarker {self.marker_name}={self.value}>"
'''

marker_analysis_model_code = '''"""
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
'''

with open(f"{models_dir}/report_model.py", "w") as f: f.write(report_model_code)
with open(f"{models_dir}/report_marker_model.py", "w") as f: f.write(report_marker_model_code)
with open(f"{models_dir}/marker_analysis_model.py", "w") as f: f.write(marker_analysis_model_code)
