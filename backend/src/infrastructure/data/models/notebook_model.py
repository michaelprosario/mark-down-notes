"""SQLAlchemy model for Notebook."""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.infrastructure.data.models.base import TimestampMixin, SoftDeleteMixin
from src.infrastructure.config.database import Base


class NotebookModel(Base, TimestampMixin, SoftDeleteMixin):
    """SQLAlchemy model for Notebook table."""
    
    __tablename__ = "notebooks"
    
    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    color = Column(String(7), nullable=False, default="#0078D4")
    
    # Relationships
    sections = relationship(
        "SectionModel",
        back_populates="notebook",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }
