"""
Database initialisation helpers.
Imports all models so Alembic and create_all can discover them.
"""

from app.database.base import Base
from app.database.session import engine

# ── Import all models to register them with metadata ──────────────────────────
from app.models.user_model import User  # noqa: F401
from app.models.report_model import MedicalReport  # noqa: F401
from app.models.extracted_marker_model import ExtractedMarker  # noqa: F401
from app.models.analysis_model import AIAnalysis  # noqa: F401
from app.models.upload_model import UploadHistory  # noqa: F401


def init_db() -> None:
    """Create all tables. Should only be used in development / tests."""
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """Drop all tables. DANGER: use only in test environments."""
    Base.metadata.drop_all(bind=engine)
