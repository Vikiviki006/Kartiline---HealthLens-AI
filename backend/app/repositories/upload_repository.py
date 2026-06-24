"""
UploadRepository: database interactions for UploadHistory.
"""

import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.models.upload_model import UploadHistory
from app.utils.logger import logger


class UploadRepository:
    """Data access layer for upload history records."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, **kwargs: Any) -> UploadHistory:
        record = UploadHistory(**kwargs)
        self._db.add(record)
        self._db.flush()
        logger.bind(upload_id=str(record.id)).debug("Upload history record created")
        return record

    def get_by_user(self, user_id: uuid.UUID, limit: int = 20) -> list[UploadHistory]:
        from sqlalchemy import desc
        return (
            self._db.query(UploadHistory)
            .filter(UploadHistory.user_id == user_id, UploadHistory.is_active == True)
            .order_by(desc(UploadHistory.created_at))
            .limit(limit)
            .all()
        )
