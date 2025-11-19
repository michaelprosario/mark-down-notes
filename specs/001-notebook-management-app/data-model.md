# Data Model Specification

**Feature**: Notebook Management App  
**Date**: November 19, 2025  
**Phase**: Phase 1 - Design

## Overview

This document defines the domain entities, their relationships, validation rules, and state transitions for the Notebook Management application. The model supports a three-level hierarchy: Notebooks → Sections → Pages, with cross-cutting Tags.

---

## Entity Definitions

### Notebook

**Description**: Top-level organizational container representing a collection of related content (e.g., "Work", "Personal", "Learning").

**Attributes**:

| Field | Type | Required | Constraints | Default | Notes |
|-------|------|----------|-------------|---------|-------|
| `id` | UUID | Yes | Unique, Primary Key | Generated | Auto-generated UUID v4 |
| `name` | String | Yes | 1-100 characters, not empty after trim | - | User-defined name |
| `color` | String | No | Valid hex color (#RRGGBB) | `#0078D4` | For visual distinction |
| `created_at` | DateTime | Yes | UTC timestamp | Now | Auto-set on creation |
| `updated_at` | DateTime | Yes | UTC timestamp | Now | Auto-updated on change |
| `deleted_at` | DateTime | No | UTC timestamp, null if active | null | Soft delete support |

**Relationships**:
- **Has Many** Sections (1:N) - cascade delete
- **Has Many** Pages (transitive through Sections)

**Validation Rules**:
- `name`: Must not be empty after trimming whitespace
- `name`: Length between 1 and 100 characters
- `color`: Must match regex `^#[0-9A-Fa-f]{6}$` if provided
- Business rule: Cannot delete notebook if it contains sections (must confirm cascade)

**Indexes**:
- Primary key: `id`
- Index on: `created_at` (for sorting)
- Index on: `deleted_at` (for filtering active records)

---

### Section

**Description**: Mid-level organizational unit within a notebook representing a subtopic or category (e.g., "Projects", "Meeting Notes", "Ideas").

**Attributes**:

| Field | Type | Required | Constraints | Default | Notes |
|-------|------|----------|-------------|---------|-------|
| `id` | UUID | Yes | Unique, Primary Key | Generated | Auto-generated UUID v4 |
| `notebook_id` | UUID | Yes | Foreign Key → Notebook.id | - | Parent notebook |
| `name` | String | Yes | 1-100 characters | - | User-defined name |
| `display_order` | Integer | Yes | Non-negative | 0 | For manual reordering |
| `created_at` | DateTime | Yes | UTC timestamp | Now | Auto-set on creation |
| `updated_at` | DateTime | Yes | UTC timestamp | Now | Auto-updated on change |
| `deleted_at` | DateTime | No | UTC timestamp | null | Soft delete support |

**Relationships**:
- **Belongs To** Notebook (N:1)
- **Has Many** Pages (1:N) - cascade delete

**Validation Rules**:
- `name`: Must not be empty after trimming
- `name`: Length between 1 and 100 characters
- `notebook_id`: Must reference an existing, non-deleted notebook
- `display_order`: Must be >= 0
- Business rule: Section names must be unique within a notebook

**Indexes**:
- Primary key: `id`
- Foreign key: `notebook_id`
- Composite index: `(notebook_id, display_order)` for sorted listing
- Index on: `deleted_at`

---

### Page

**Description**: Individual note or document within a section containing formatted content. Supports hierarchical nesting (subpages).

**Attributes**:

| Field | Type | Required | Constraints | Default | Notes |
|-------|------|----------|-------------|---------|-------|
| `id` | UUID | Yes | Unique, Primary Key | Generated | Auto-generated UUID v4 |
| `section_id` | UUID | Yes | Foreign Key → Section.id | - | Parent section |
| `parent_page_id` | UUID | No | Foreign Key → Page.id, nullable | null | For subpages/nesting |
| `title` | String | Yes | 1-255 characters | - | Page title |
| `content` | Text/JSONB | No | Markdown format | Empty string | Page content |
| `content_plain` | Text | No | Plain text (for search) | - | Auto-generated from markdown |
| `search_vector` | TSVector | No | PostgreSQL full-text | - | Auto-generated for search |
| `display_order` | Integer | Yes | Non-negative | 0 | Ordering within section |
| `created_at` | DateTime | Yes | UTC timestamp | Now | Auto-set on creation |
| `updated_at` | DateTime | Yes | UTC timestamp | Now | Auto-updated on change |
| `deleted_at` | DateTime | No | UTC timestamp | null | Soft delete support |

**Relationships**:
- **Belongs To** Section (N:1)
- **Belongs To** Page (self-referential, optional) - for subpages
- **Has Many** Pages (self-referential) - child pages
- **Has Many** PageTags (1:N)
- **Has Many** Tags (N:M through PageTags)

**Validation Rules**:
- `title`: Must not be empty after trimming
- `title`: Length between 1 and 255 characters
- `section_id`: Must reference existing, non-deleted section
- `parent_page_id`: If set, must reference existing page in same section
- `parent_page_id`: Cannot create circular references (page cannot be ancestor of itself)
- `content`: Must be valid markdown (syntax check)
- `display_order`: Must be >= 0
- Business rule: Subpage depth limited to 3 levels

**Indexes**:
- Primary key: `id`
- Foreign key: `section_id`
- Foreign key: `parent_page_id`
- Composite index: `(section_id, display_order)` for sorted listing
- GIN index: `search_vector` for full-text search
- Index on: `deleted_at`
- Index on: `updated_at` (for recent pages query)

**State Transitions**:
- **Draft → Published**: No explicit state, but could track via `published_at` field (future enhancement)
- **Active → Deleted**: Set `deleted_at` timestamp (soft delete)
- **Deleted → Active**: Clear `deleted_at` (restore from trash)

---

### Tag

**Description**: Cross-cutting label for categorizing pages across notebook/section boundaries (e.g., "urgent", "project-alpha", "reference").

**Attributes**:

| Field | Type | Required | Constraints | Default | Notes |
|-------|------|----------|-------------|---------|-------|
| `id` | UUID | Yes | Unique, Primary Key | Generated | Auto-generated UUID v4 |
| `name` | String | Yes | 1-50 characters, lowercase | - | Tag name |
| `color` | String | No | Valid hex color | `#6C757D` | For visual distinction |
| `created_at` | DateTime | Yes | UTC timestamp | Now | Auto-set on creation |
| `updated_at` | DateTime | Yes | UTC timestamp | Now | Auto-updated on change |

**Relationships**:
- **Has Many** PageTags (1:N)
- **Has Many** Pages (N:M through PageTags)

**Validation Rules**:
- `name`: Must not be empty after trimming
- `name`: Length between 1 and 50 characters
- `name`: Auto-convert to lowercase for consistency
- `name`: Must be unique (case-insensitive)
- `name`: Allowed characters: alphanumeric, hyphen, underscore
- `color`: Must match regex `^#[0-9A-Fa-f]{6}$` if provided

**Indexes**:
- Primary key: `id`
- Unique index: `name` (case-insensitive)

---

### PageTag (Join Table)

**Description**: Many-to-many relationship between Pages and Tags.

**Attributes**:

| Field | Type | Required | Constraints | Default | Notes |
|-------|------|----------|-------------|---------|-------|
| `page_id` | UUID | Yes | Foreign Key → Page.id | - | - |
| `tag_id` | UUID | Yes | Foreign Key → Tag.id | - | - |
| `created_at` | DateTime | Yes | UTC timestamp | Now | When tag was added to page |

**Relationships**:
- **Belongs To** Page (N:1)
- **Belongs To** Tag (N:1)

**Validation Rules**:
- Composite primary key: `(page_id, tag_id)` - prevents duplicate tags on same page
- `page_id`: Must reference existing, non-deleted page
- `tag_id`: Must reference existing tag

**Indexes**:
- Primary key: `(page_id, tag_id)`
- Index on: `tag_id` (for "find all pages with tag X" queries)
- Index on: `page_id` (for "find all tags on page Y" queries)

---

## Entity Relationship Diagram

```
┌─────────────┐
│  Notebook   │
│─────────────│
│ id (PK)     │
│ name        │
│ color       │
│ created_at  │
│ updated_at  │
│ deleted_at  │
└──────┬──────┘
       │
       │ 1:N
       │
┌──────▼──────┐
│   Section   │
│─────────────│
│ id (PK)     │
│ notebook_id │◄─── FK
│ name        │
│ display_ord │
│ created_at  │
│ updated_at  │
│ deleted_at  │
└──────┬──────┘
       │
       │ 1:N
       │
┌──────▼──────┐         ┌─────────────┐
│    Page     │         │   PageTag   │
│─────────────│         │─────────────│
│ id (PK)     │◄────────┤ page_id (FK)│
│ section_id  │◄─── FK  │ tag_id (FK) │
│ parent_id   │◄─┐      │ created_at  │
│ title       │  │      └──────┬──────┘
│ content     │  │             │
│ content_txt │  │             │ N:M
│ search_vec  │  │             │
│ display_ord │  │      ┌──────▼──────┐
│ created_at  │  │      │     Tag     │
│ updated_at  │  │      │─────────────│
│ deleted_at  │  │      │ id (PK)     │
└─────────────┘  │      │ name (UQ)   │
       │         │      │ color       │
       └─────────┘      │ created_at  │
       (self-ref)       │ updated_at  │
                        └─────────────┘
```

---

## Domain Logic & Business Rules

### Hierarchical Constraints

1. **Cascade Deletes**:
   - Deleting a Notebook soft-deletes all child Sections and Pages
   - Deleting a Section soft-deletes all child Pages
   - Deleting a Page soft-deletes all child subpages
   - Deletions are soft (set `deleted_at`) to enable undo/restore

2. **Nesting Depth**:
   - Maximum subpage depth: 3 levels (Page → Subpage → Sub-subpage → Sub-sub-subpage)
   - Enforced at service layer, not database constraint
   - Prevents infinite recursion and UI complexity

3. **Ordering**:
   - Sections ordered by `display_order` within a Notebook
   - Pages ordered by `display_order` within a Section
   - Reordering updates `display_order` values
   - Use gap numbering (10, 20, 30) to minimize updates when inserting

### Uniqueness Constraints

1. **Notebook names**: Can duplicate across different users (future multi-user support)
2. **Section names**: Must be unique within a Notebook
3. **Page titles**: Can duplicate (same title in different sections allowed)
4. **Tag names**: Globally unique (case-insensitive)

### Content Validation

1. **Markdown Sanitization**:
   - Strip potentially harmful HTML/JavaScript from markdown
   - Allow safe HTML subset: headings, lists, links, images, emphasis
   - Use `bleach` library for sanitization during rendering

2. **Image References**:
   - Images stored in `/static/uploads/{uuid}.{ext}`
   - Markdown images use relative paths: `![alt](/static/uploads/abc123.jpg)`
   - Validate image uploads: max 5MB, types: jpg, png, gif, webp
   - Orphan images (referenced in deleted pages) cleaned up weekly via background job

3. **Search Index**:
   - `search_vector` auto-updates on Page insert/update via database trigger
   - Combines `title` (weight A) and `content_plain` (weight B) for ranking
   - Language: English (configurable for i18n)

---

## Database Schema (PostgreSQL DDL)

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Notebooks table
CREATE TABLE notebooks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL CHECK (trim(name) != ''),
    color VARCHAR(7) DEFAULT '#0078D4' CHECK (color ~ '^#[0-9A-Fa-f]{6}$'),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_notebooks_created_at ON notebooks(created_at);
CREATE INDEX idx_notebooks_deleted_at ON notebooks(deleted_at) WHERE deleted_at IS NULL;

-- Sections table
CREATE TABLE sections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    notebook_id UUID NOT NULL REFERENCES notebooks(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL CHECK (trim(name) != ''),
    display_order INTEGER NOT NULL DEFAULT 0 CHECK (display_order >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    UNIQUE (notebook_id, name) WHERE deleted_at IS NULL
);

CREATE INDEX idx_sections_notebook_id ON sections(notebook_id);
CREATE INDEX idx_sections_notebook_order ON sections(notebook_id, display_order);
CREATE INDEX idx_sections_deleted_at ON sections(deleted_at) WHERE deleted_at IS NULL;

-- Pages table
CREATE TABLE pages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    section_id UUID NOT NULL REFERENCES sections(id) ON DELETE CASCADE,
    parent_page_id UUID REFERENCES pages(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL CHECK (trim(title) != ''),
    content TEXT DEFAULT '',
    content_plain TEXT DEFAULT '',
    search_vector TSVECTOR,
    display_order INTEGER NOT NULL DEFAULT 0 CHECK (display_order >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_pages_section_id ON pages(section_id);
CREATE INDEX idx_pages_parent_page_id ON pages(parent_page_id);
CREATE INDEX idx_pages_section_order ON pages(section_id, display_order);
CREATE INDEX idx_pages_search_vector ON pages USING GIN(search_vector);
CREATE INDEX idx_pages_updated_at ON pages(updated_at);
CREATE INDEX idx_pages_deleted_at ON pages(deleted_at) WHERE deleted_at IS NULL;

-- Auto-update search_vector trigger
CREATE TRIGGER pages_search_vector_update
BEFORE INSERT OR UPDATE OF title, content_plain ON pages
FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(search_vector, 'pg_catalog.english', title, content_plain);

-- Tags table
CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL UNIQUE CHECK (trim(name) != '' AND name = lower(name)),
    color VARCHAR(7) DEFAULT '#6C757D' CHECK (color ~ '^#[0-9A-Fa-f]{6}$'),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_tags_name_lower ON tags(LOWER(name));

-- PageTags join table
CREATE TABLE page_tags (
    page_id UUID NOT NULL REFERENCES pages(id) ON DELETE CASCADE,
    tag_id UUID NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (page_id, tag_id)
);

CREATE INDEX idx_page_tags_tag_id ON page_tags(tag_id);
CREATE INDEX idx_page_tags_page_id ON page_tags(page_id);

-- Auto-update updated_at triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_notebooks_updated_at BEFORE UPDATE ON notebooks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sections_updated_at BEFORE UPDATE ON sections
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_pages_updated_at BEFORE UPDATE ON pages
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tags_updated_at BEFORE UPDATE ON tags
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

## SQLAlchemy ORM Models

```python
# infrastructure/data/models/base.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from datetime import datetime
import uuid

Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True)

# infrastructure/data/models/notebook_model.py
from sqlalchemy import Column, String, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin, SoftDeleteMixin

class NotebookModel(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "notebooks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    color = Column(String(7), nullable=False, default="#0078D4")
    
    # Relationships
    sections = relationship("SectionModel", back_populates="notebook", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint("trim(name) != ''", name="notebooks_name_not_empty"),
        CheckConstraint("color ~ '^#[0-9A-Fa-f]{6}$'", name="notebooks_color_format"),
    )

# infrastructure/data/models/section_model.py
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin, SoftDeleteMixin

class SectionModel(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "sections"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    notebook_id = Column(UUID(as_uuid=True), ForeignKey("notebooks.id"), nullable=False)
    name = Column(String(100), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)
    
    # Relationships
    notebook = relationship("NotebookModel", back_populates="sections")
    pages = relationship("PageModel", back_populates="section", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint("notebook_id", "name", name="uq_section_name_per_notebook"),
    )

# infrastructure/data/models/page_model.py
from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin, SoftDeleteMixin

class PageModel(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "pages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    section_id = Column(UUID(as_uuid=True), ForeignKey("sections.id"), nullable=False)
    parent_page_id = Column(UUID(as_uuid=True), ForeignKey("pages.id"), nullable=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False, default="")
    content_plain = Column(Text, nullable=False, default="")
    search_vector = Column(TSVECTOR)
    display_order = Column(Integer, nullable=False, default=0)
    
    # Relationships
    section = relationship("SectionModel", back_populates="pages")
    parent_page = relationship("PageModel", remote_side=[id], back_populates="subpages")
    subpages = relationship("PageModel", back_populates="parent_page")
    page_tags = relationship("PageTagModel", back_populates="page", cascade="all, delete-orphan")
    tags = relationship("TagModel", secondary="page_tags", back_populates="pages")

# infrastructure/data/models/tag_model.py
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class TagModel(Base, TimestampMixin):
    __tablename__ = "tags"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, unique=True)
    color = Column(String(7), nullable=False, default="#6C757D")
    
    # Relationships
    page_tags = relationship("PageTagModel", back_populates="tag", cascade="all, delete-orphan")
    pages = relationship("PageModel", secondary="page_tags", back_populates="tags")

# infrastructure/data/models/page_tag_model.py
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class PageTagModel(Base, TimestampMixin):
    __tablename__ = "page_tags"
    
    page_id = Column(UUID(as_uuid=True), ForeignKey("pages.id"), primary_key=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True)
    
    # Relationships
    page = relationship("PageModel", back_populates="page_tags")
    tag = relationship("TagModel", back_populates="page_tags")
```

---

## Sample Data

```python
# Example data for testing/demo
sample_data = {
    "notebook": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Work",
        "color": "#0078D4"
    },
    "sections": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440001",
            "notebook_id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Projects",
            "display_order": 10
        },
        {
            "id": "550e8400-e29b-41d4-a716-446655440002",
            "notebook_id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Meeting Notes",
            "display_order": 20
        }
    ],
    "pages": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440003",
            "section_id": "550e8400-e29b-41d4-a716-446655440001",
            "title": "Q1 Planning",
            "content": "# Q1 Planning\n\n## Objectives\n- Launch new feature\n- Improve performance",
            "display_order": 10
        }
    ],
    "tags": [
        {"id": "550e8400-e29b-41d4-a716-446655440010", "name": "urgent", "color": "#DC3545"},
        {"id": "550e8400-e29b-41d4-a716-446655440011", "name": "project-alpha", "color": "#28A745"}
    ]
}
```

---

## Migration Strategy

### Phase 1: Initial Schema
- Create tables: `notebooks`, `sections`, `pages`, `tags`, `page_tags`
- Add indexes, triggers, constraints
- Seed with sample data for demo

### Phase 2: Enhancements (Future)
- Add `users` table for multi-user support
- Add `notebook_shares` for collaboration
- Add `page_versions` for version history
- Add `attachments` for file uploads beyond images

### Data Migration
- Export format: JSON with full hierarchy
- Import: Validate UUIDs, preserve relationships, handle conflicts
- Rollback: Keep deleted_at records for 30 days before hard delete
