"""
UserRepository: database interactions for User model.
"""

import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.models.user_model import User
from app.utils.logger import logger


class UserRepository:
    """Data access layer for users."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, **kwargs: Any) -> User:
        user = User(**kwargs)
        self._db.add(user)
        self._db.flush()
        logger.bind(user_id=str(user.id)).info("User created")
        return user

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return (
            self._db.query(User)
            .filter(User.id == user_id, User.is_active == True)
            .first()
        )

    def get_by_email(self, email: str) -> User | None:
        return (
            self._db.query(User)
            .filter(User.email == email.lower(), User.is_active == True)
            .first()
        )

    def exists_by_email(self, email: str) -> bool:
        return self._db.query(User.id).filter(User.email == email.lower()).first() is not None

    def update(self, user_id: uuid.UUID, **kwargs: Any) -> User | None:
        self._db.query(User).filter(User.id == user_id).update(kwargs, synchronize_session=False)
        return self.get_by_id(user_id)
