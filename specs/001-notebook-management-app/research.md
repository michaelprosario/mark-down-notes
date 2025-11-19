# Research & Technology Decisions

**Feature**: Notebook Management App  
**Date**: November 19, 2025  
**Phase**: Phase 0 - Research

## Executive Summary

This document captures technology choices, architectural patterns, and best practices for building a web-based notebook management application using FastAPI, Bootstrap, and clean architecture principles.

---

## Technology Stack Research

### Backend Framework: FastAPI

**Decision**: Use FastAPI 0.104+ as the backend web framework

**Rationale**:
- Modern async/await support for high performance (meets <100ms p95 requirement)
- Built-in OpenAPI documentation generation (supports API contracts requirement)
- Excellent type hint support with Pydantic (aligns with explicit over implicit principle)
- Native dependency injection system (enables interface-based design)
- Lightweight and minimal (supports minimal core dependencies principle)
- Strong community and production-ready ecosystem

**Alternatives Considered**:
- **Django**: Too heavyweight, ORM tightly coupled to framework, violates minimal dependencies
- **Flask**: Requires more manual setup, lacks built-in async support, no native DI
- **aiohttp**: Lower-level, more boilerplate, smaller ecosystem for business apps

**Best Practices**:
- Use `Depends()` for dependency injection of repository interfaces
- Leverage `APIRouter` for modular route organization by domain (notebooks, sections, pages)
- Use Pydantic models for request/response validation (separate from domain models)
- Configure CORS middleware for potential SPA frontend upgrade path
- Use `BackgroundTasks` for async operations like export generation

---

### Frontend Framework: Bootstrap 5

**Decision**: Use Bootstrap 5.3+ with server-side rendered Jinja2 templates

**Rationale**:
- Mature, battle-tested responsive CSS framework (meets desktop/tablet/mobile requirement)
- Minimal JavaScript dependencies (supports lightweight approach)
- Strong component library for rapid UI development (three-pane layout, modals, forms)
- Excellent browser compatibility (modern browser support guaranteed)
- Can integrate vanilla JavaScript for interactivity (auto-save, search, markdown editor)
- Server-side rendering reduces client complexity and supports progressive enhancement

**Alternatives Considered**:
- **React/Vue SPA**: Over-engineering for initial MVP, adds build complexity, requires separate API versioning
- **Tailwind CSS**: Requires build step, steeper learning curve, more configuration
- **Plain CSS**: Would require extensive custom responsive design work

**Best Practices**:
- Use Bootstrap grid system for responsive three-pane layout
- Leverage Bootstrap components: Cards (notebooks), Tabs (sections), List groups (pages)
- Use Bootstrap modals for confirmations (delete operations per FR-043)
- Implement custom CSS in `/static/css/custom.css` for brand-specific styling
- Use Bootstrap form validation for client-side validation feedback
- Integrate HTMX or Alpine.js for dynamic updates without full page reloads (future enhancement)

---

### Data Storage: SQLite/PostgreSQL with SQLAlchemy

**Decision**: SQLAlchemy 2.0+ ORM with SQLite for development, PostgreSQL for production

**Rationale**:
- SQLAlchemy supports repository pattern implementation (aligns with interface-based design)
- Async SQLAlchemy compatible with FastAPI's async nature
- Database-agnostic (SQLite dev, PostgreSQL prod, same code)
- Migration support via Alembic (schema evolution without data loss)
- Strong Python ecosystem integration

**Alternatives Considered**:
- **Direct SQL**: Violates DRY, no migration support, SQL injection risk
- **NoSQL (MongoDB)**: Overkill for hierarchical data, complicates querying nested structures
- **File-based storage**: Poor query performance, no ACID guarantees, difficult search implementation

**Schema Design Best Practices**:
- Use UUIDs for primary keys (enables distributed systems future upgrade)
- Index foreign keys (notebooks → sections → pages hierarchy)
- Full-text search index on page content (meets <1s search requirement per SC-009)
- `created_at` and `updated_at` timestamps on all entities (meets FR-014)
- Soft deletes with `deleted_at` column (enables undo functionality)
- JSONB column for page content/formatting (flexible schema evolution)

---

### Content Editing: Markdown with SimpleMDE/EasyMDE

**Decision**: Use Markdown as the content format with EasyMDE editor

**Rationale**:
- Markdown is portable, plain text, supports export/import (FR-039-FR-042)
- SimpleMDE/EasyMDE provides toolbar for formatting (meets FR-016 requirements)
- Renders to HTML for display (supports FR-020 preview mode)
- Supports images via markdown syntax `![alt](url)` (meets FR-019)
- Keyboard shortcuts built-in (supports FR-046)
- Lightweight JavaScript library (<50KB)

**Alternatives Considered**:
- **Rich text editors (TinyMCE, CKEditor)**: Heavier, HTML storage format less portable
- **Plain textarea**: No formatting support, poor UX
- **Notion-like block editor**: Over-engineering, complex state management

**Implementation Pattern**:
- Store raw markdown in database JSONB column
- Render to HTML server-side using `markdown-it-py` or `python-markdown`
- Use EasyMDE for client-side editing with auto-save via JavaScript
- Sanitize rendered HTML to prevent XSS (use `bleach` library)

---

### Testing Strategy

**Decision**: pytest + pytest-asyncio for unit/integration tests, coverage target >80%

**Rationale**:
- pytest is Python standard for testing (ecosystem maturity)
- pytest-asyncio enables testing FastAPI async services
- Fixtures support mock repository implementations (interface testing)
- Coverage.py integration for coverage reporting
- pytest-mock for mocking external dependencies

**Test Organization**:
```
tests/
├── unit/
│   ├── services/           # Test core services with mock repos
│   ├── domain/             # Test domain model validation
│   └── commands/           # Test command/query objects
├── integration/
│   ├── repositories/       # Test SQLAlchemy repos against test DB
│   └── api/                # Test FastAPI routes end-to-end
└── fixtures/
    ├── mock_repositories.py
    └── sample_data.py
```

**Best Practices**:
- Use `TestClient` from FastAPI for integration testing routes
- Create in-memory SQLite database for integration tests (fast, isolated)
- Mock file system for image upload/storage tests
- Use `pytest.mark.asyncio` for async test functions
- Parametrize tests for edge cases (empty names, special characters)

---

## Architectural Patterns

### Clean Architecture Implementation

**Pattern**: Hexagonal Architecture (Ports & Adapters) with CQRS

**Core Layer Structure**:
```python
# core/domain/notebook.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Notebook:
    id: str
    name: str
    color: str
    created_at: datetime
    updated_at: datetime
    
    def validate(self) -> list[str]:
        errors = []
        if not self.name or not self.name.strip():
            errors.append("Notebook name cannot be empty")
        if len(self.name) > 100:
            errors.append("Notebook name too long (max 100 chars)")
        return errors

# core/interfaces/repositories.py
from abc import ABC, abstractmethod
from typing import Optional, List
from core.domain.notebook import Notebook

class INotebookRepository(ABC):
    @abstractmethod
    async def save(self, notebook: Notebook) -> None:
        pass
    
    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[Notebook]:
        pass
    
    @abstractmethod
    async def find_all(self) -> List[Notebook]:
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> None:
        pass

# core/services/create_notebook_service.py
from core.commands.create_notebook_command import CreateNotebookCommand
from core.interfaces.repositories import INotebookRepository
from core.results.result import Result
from core.domain.notebook import Notebook
from datetime import datetime
import uuid

class CreateNotebookService:
    def __init__(self, repository: INotebookRepository):
        self._repository = repository
    
    async def execute(self, command: CreateNotebookCommand) -> Result[Notebook]:
        # Validation
        if not command.name or not command.name.strip():
            return Result.failure("Notebook name is required")
        
        # Business logic
        notebook = Notebook(
            id=str(uuid.uuid4()),
            name=command.name.strip(),
            color=command.color or "#0078D4",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        validation_errors = notebook.validate()
        if validation_errors:
            return Result.failure(", ".join(validation_errors))
        
        # Persistence
        await self._repository.save(notebook)
        
        return Result.success(notebook, "Notebook created successfully")
```

**Infrastructure Layer Implementation**:
```python
# infrastructure/data/repositories/notebook_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Optional, List
from core.interfaces.repositories import INotebookRepository
from core.domain.notebook import Notebook
from infrastructure.data.models.notebook_model import NotebookModel

class NotebookRepository(INotebookRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def save(self, notebook: Notebook) -> None:
        model = NotebookModel(
            id=notebook.id,
            name=notebook.name,
            color=notebook.color,
            created_at=notebook.created_at,
            updated_at=notebook.updated_at
        )
        self._session.add(model)
        await self._session.commit()
    
    async def find_by_id(self, id: str) -> Optional[Notebook]:
        stmt = select(NotebookModel).where(NotebookModel.id == id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            return None
        
        return Notebook(
            id=model.id,
            name=model.name,
            color=model.color,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
```

**Presentation Layer (FastAPI)**:
```python
# api/routes/notebooks.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from core.services.create_notebook_service import CreateNotebookService
from core.commands.create_notebook_command import CreateNotebookCommand
from api.dependencies import get_notebook_service

router = APIRouter(prefix="/api/notebooks", tags=["notebooks"])

class CreateNotebookRequest(BaseModel):
    name: str
    color: str | None = None

@router.post("/")
async def create_notebook(
    request: CreateNotebookRequest,
    service: CreateNotebookService = Depends(get_notebook_service)
):
    command = CreateNotebookCommand(name=request.name, color=request.color)
    result = await service.execute(command)
    
    if not result.is_success:
        return {"success": False, "error": result.error}
    
    return {
        "success": True,
        "data": {
            "id": result.value.id,
            "name": result.value.name,
            "color": result.value.color
        },
        "message": result.message
    }
```

---

### Auto-Save Implementation

**Pattern**: Debounced AJAX requests with optimistic UI updates

**Client-Side JavaScript**:
```javascript
// static/js/auto-save.js
class AutoSave {
    constructor(saveUrl, debounceMs = 3000) {
        this.saveUrl = saveUrl;
        this.debounceMs = debounceMs;
        this.timeoutId = null;
        this.lastSaved = null;
    }
    
    scheduleeSave(content) {
        if (this.timeoutId) {
            clearTimeout(this.timeoutId);
        }
        
        this.timeoutId = setTimeout(() => {
            this.save(content);
        }, this.debounceMs);
    }
    
    async save(content) {
        try {
            const response = await fetch(this.saveUrl, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({content: content})
            });
            
            if (response.ok) {
                this.lastSaved = new Date();
                this.updateSaveIndicator('Saved');
            } else {
                this.updateSaveIndicator('Error saving');
            }
        } catch (error) {
            this.updateSaveIndicator('Save failed');
        }
    }
    
    updateSaveIndicator(message) {
        document.getElementById('save-status').textContent = message;
    }
}

// Usage
const editor = new SimpleMDE();
const autoSave = new AutoSave('/api/pages/123');
editor.codemirror.on('change', () => {
    autoSave.scheduleSave(editor.value());
});
```

**Backend Endpoint**:
```python
@router.put("/api/pages/{page_id}")
async def update_page_content(
    page_id: str,
    request: UpdateContentRequest,
    service: UpdatePageService = Depends(get_page_service)
):
    command = UpdatePageContentCommand(page_id=page_id, content=request.content)
    result = await service.execute(command)
    return {"success": result.is_success}
```

---

### Search Implementation

**Pattern**: PostgreSQL full-text search with GIN index

**Database Setup**:
```sql
-- Add tsvector column for full-text search
ALTER TABLE pages ADD COLUMN search_vector tsvector;

-- Create GIN index for fast text search
CREATE INDEX pages_search_idx ON pages USING GIN(search_vector);

-- Trigger to auto-update search vector
CREATE TRIGGER pages_search_update
BEFORE INSERT OR UPDATE ON pages
FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(search_vector, 'pg_catalog.english', title, content);
```

**Repository Method**:
```python
async def search(self, query: str) -> List[Page]:
    stmt = select(PageModel).where(
        PageModel.search_vector.match(query)
    ).order_by(
        func.ts_rank(PageModel.search_vector, func.plainto_tsquery(query)).desc()
    )
    result = await self._session.execute(stmt)
    return [self._to_domain(model) for model in result.scalars()]
```

---

## Performance Considerations

### Caching Strategy

**Decision**: Use FastAPI's `@lru_cache` for frequently accessed data

```python
from functools import lru_cache

@lru_cache(maxsize=128)
async def get_notebook_tree(notebook_id: str) -> NotebookTree:
    # Expensive operation to build full hierarchy
    pass
```

### Database Query Optimization

- Use `selectinload()` for eager loading related entities (avoid N+1 queries)
- Index foreign keys and frequently queried columns
- Use database connection pooling (SQLAlchemy default: 5-20 connections)
- Implement pagination for large result sets (sections/pages lists)

### Image Handling

- Store images in `/static/uploads/` with UUID filenames
- Resize images on upload (max 1920px width) to save storage
- Use lazy loading for images in markdown preview
- Implement content-type validation (only allow jpg, png, gif, webp)

---

## Security Best Practices

### Input Validation

- Sanitize all user inputs using Pydantic validators
- Escape HTML in markdown rendering to prevent XSS
- Validate file uploads (size limits, content type verification)
- Rate limit API endpoints to prevent abuse

### Authentication (Future Enhancement)

- Use FastAPI's OAuth2 password flow for user authentication
- Store password hashes using bcrypt (via passlib)
- Implement JWT tokens for stateless session management
- Add RBAC for multi-user deployments

### Data Protection

- Use parameterized queries (SQLAlchemy prevents SQL injection)
- Enable HTTPS in production deployment
- Implement CORS policies to restrict API access
- Sanitize export data to prevent information disclosure

---

## Deployment Considerations

### Docker Containerization

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/src ./src
COPY backend/migrations ./migrations

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Configuration

```python
# infrastructure/config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./notebooks.db"
    debug: bool = False
    upload_dir: str = "./uploads"
    max_upload_size: int = 5 * 1024 * 1024  # 5MB
    
    class Config:
        env_file = ".env"
```

### Database Migrations

- Use Alembic for schema migrations
- Auto-generate migrations: `alembic revision --autogenerate -m "description"`
- Apply migrations: `alembic upgrade head`
- Include seed data for demo/testing purposes

---

## Open Questions & Future Research

### Resolved in This Phase:
- ✅ Backend framework selection
- ✅ Frontend approach (server-rendered vs SPA)
- ✅ Data storage strategy
- ✅ Content editing format
- ✅ Testing approach
- ✅ Architecture patterns

### Future Phases:
- Real-time collaboration (WebSockets, operational transforms)
- Offline support (Service Workers, local storage sync)
- Mobile apps (React Native, Flutter)
- Advanced search (fuzzy matching, faceted search)
- Version history (event sourcing, snapshots)

---

## References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Bootstrap 5 Docs: https://getbootstrap.com/docs/5.3/
- SQLAlchemy 2.0: https://docs.sqlalchemy.org/
- Clean Architecture (Robert C. Martin)
- EasyMDE: https://github.com/Ionaru/easy-markdown-editor
- pytest Best Practices: https://docs.pytest.org/
