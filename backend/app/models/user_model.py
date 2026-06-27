"""
User ORM model.
"""

import uuid

from sqlalchemy import Boolean, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin
from app.core.constants import UserRole


class User(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Represents an authenticated platform user."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        String(50), nullable=False, default=UserRole.PATIENT.value
    )
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    encrypted_identifier: Mapped[str] = mapped_column(String(255), nullable=True)

    # ── Relationships ──────────────────────────────────────────────────────────
    reports: Mapped[list["Report"]] = relationship(  # type: ignore[name-defined]
        "Report", back_populates="user", cascade="all, delete-orphan"
    )
    upload_history: Mapped[list["UploadHistory"]] = relationship(  # type: ignore[name-defined]
        "UploadHistory", back_populates="user", cascade="all, delete-orphan"
    )

    # ── Composite indexes ──────────────────────────────────────────────────────
    __table_args__ = (
        Index("ix_users_email_active", "email", "is_active"),
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"
