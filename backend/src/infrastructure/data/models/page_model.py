"""SQLAlchemy model for Page."""

from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.infrastructure.data.models.base import TimestampMixin, SoftDeleteMixin
from src.infrastructure.config.database import Base


class PageModel(Base, TimestampMixin, SoftDeleteMixin):
    """SQLAlchemy model for Page table."""
    
    __tablename__ = "pages"
    
    id = Column(String(36), primary_key=True)
    section_id = Column(String(36), ForeignKey("sections.id", ondelete="CASCADE"), nullable=False)
    parent_page_id = Column(String(36), ForeignKey("pages.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False, default="")
    content_plain = Column(Text, nullable=False, default="")
    search_vector = Column(Text, nullable=True)
    display_order = Column(Integer, nullable=False, default=0)
    
    # Relationships
    section = relationship("SectionModel", back_populates="pages")
    parent_page = relationship("PageModel", remote_side=[id], backref="subpages")
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "section_id": self.section_id,
            "parent_page_id": self.parent_page_id,
            "title": self.title,
            "content": self.content,
            "content_plain": self.content_plain,
            "display_order": self.display_order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }
