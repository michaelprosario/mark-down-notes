"""Pydantic schemas for API request/response models."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Notebook schemas
class NotebookCreate(BaseModel):
    """Schema for creating a notebook."""
    name: str = Field(..., min_length=1, max_length=100)
    color: str = Field(default="#0078D4", pattern=r'^#[0-9A-Fa-f]{6}$')


class NotebookUpdate(BaseModel):
    """Schema for updating a notebook."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')


class NotebookResponse(BaseModel):
    """Schema for notebook response."""
    id: str
    name: str
    color: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Section schemas
class SectionCreate(BaseModel):
    """Schema for creating a section."""
    name: str = Field(..., min_length=1, max_length=100)
    notebook_id: str
    display_order: int = Field(default=0, ge=0)


class SectionUpdate(BaseModel):
    """Schema for updating a section."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    display_order: Optional[int] = Field(None, ge=0)


class SectionResponse(BaseModel):
    """Schema for section response."""
    id: str
    notebook_id: str
    name: str
    display_order: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Page schemas
class PageCreate(BaseModel):
    """Schema for creating a page."""
    title: str = Field(..., min_length=1, max_length=255)
    section_id: str
    content: str = Field(default="")
    parent_page_id: Optional[str] = None
    display_order: int = Field(default=0, ge=0)


class PageUpdate(BaseModel):
    """Schema for updating a page."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    display_order: Optional[int] = Field(None, ge=0)


class PageResponse(BaseModel):
    """Schema for page response."""
    id: str
    section_id: str
    parent_page_id: Optional[str]
    title: str
    content: str
    content_plain: str
    display_order: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
