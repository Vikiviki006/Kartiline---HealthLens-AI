"""
ChatInteraction ORM model.
"""
from sqlalchemy import Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid

from app.database.base import Base, UUIDMixin, TimestampMixin

class ChatInteraction(Base, UUIDMixin, TimestampMixin):
    """Stores Q&A history for a given report."""
    __tablename__ = 'chat_interactions'
    
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    report_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('reports.id', ondelete='CASCADE'), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Relationships
    user = relationship("User", backref="chats")
    report = relationship("Report", backref="chats")
