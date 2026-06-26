"""
Models initialization for SQLAlchemy declarative base.
All models must be imported here to be registered with Alembic/SQLAlchemy.
"""

from app.models.user_model import User  # noqa: F401
from app.models.report_marker_model import ReportMarker  # noqa: F401
from app.models.marker_analysis_model import MarkerAnalysis  # noqa: F401
from app.models.report_model import Report  # noqa: F401
from app.models.upload_model import UploadHistory  # noqa: F401
from app.models.medical_marker_model import MedicalMarker  # noqa: F401