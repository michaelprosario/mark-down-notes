"""SQLAlchemy model for Section."""

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.infrastructure.data.models.base import TimestampMixin, SoftDeleteMixin
from src.infrastructure.config.database import Base


class SectionModel(Base, TimestampMixin, SoftDeleteMixin):
    """SQLAlchemy model for Section table."""
    
    __tablename__ = "sections"
    
    id = Column(String(36), primary_key=True)
    notebook_id = Column(String(36), ForeignKey("notebooks.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)
    
    # Relationships
    notebook = relationship("NotebookModel", back_populates="sections")
    pages = relationship(
        "PageModel",
        back_populates="section",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "notebook_id": self.notebook_id,
            "name": self.name,
            "display_order": self.display_order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }
