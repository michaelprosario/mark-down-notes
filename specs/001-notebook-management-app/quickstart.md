# Quickstart Guide - Notebook Management App

**Feature**: 001-notebook-management-app  
**Last Updated**: November 19, 2025  
**Target Audience**: Developers setting up the project for the first time

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** - Download from [python.org](https://www.python.org/downloads/)
- **pip** - Package installer for Python (included with Python 3.11+)
- **PostgreSQL 14+** (for production) or SQLite (for development)
- **Git** - Version control system
- **Code Editor** - VS Code, PyCharm, or your preferred IDE

### Optional Tools
- **Docker** - For containerized deployment
- **Alembic** - Database migration tool (installed via requirements.txt)

---

## Project Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd mark-down-notes
git checkout 001-notebook-management-app
```

### 2. Create Virtual Environment

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Key Dependencies** (from `requirements.txt`):
```text
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy[asyncio]==2.0.23
alembic==1.12.1
pydantic==2.5.0
pydantic-settings==2.1.0
aiosqlite==0.19.0          # For async SQLite
asyncpg==0.29.0             # For async PostgreSQL
jinja2==3.1.2
python-multipart==0.0.6
markdown-it-py==3.0.0       # Markdown rendering
bleach==6.1.0               # HTML sanitization
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2               # For testing
coverage==7.3.2
```

### 4. Environment Configuration

Create a `.env` file in the `backend/` directory:

```bash
# backend/.env

# Application
APP_NAME="Notebook Management"
DEBUG=True
ENVIRONMENT=development

# Database (SQLite for development)
DATABASE_URL=sqlite+aiosqlite:///./notebooks.db

# For PostgreSQL (production):
# DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/notebooks

# File Storage
UPLOAD_DIR=./static/uploads
MAX_UPLOAD_SIZE_MB=5

# Security
SECRET_KEY=your-secret-key-change-in-production
CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Auto-save
AUTO_SAVE_INTERVAL_MS=3000
```

### 5. Initialize Database

**Apply migrations:**
```bash
# From backend/ directory
alembic upgrade head
```

**Seed demo data (optional):**
```bash
python -m src.scripts.seed_demo_data
```

This creates:
- 2 sample notebooks ("Work", "Personal")
- 4 sections across notebooks
- 8 pages with sample markdown content
- 5 tags ("urgent", "project-alpha", "reference", "ideas", "meeting-notes")

---

## Running the Application

### Development Mode

**Start the FastAPI server:**
```bash
# From backend/ directory
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Access the application:**
- Web UI: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs
- Alternative API Docs (ReDoc): http://localhost:8000/redoc

The `--reload` flag enables hot-reloading (auto-restart on code changes).

### Production Mode

**Using Uvicorn with workers:**
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Using Docker:**
```bash
# Build image
docker build -t notebook-app .

# Run container
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql+asyncpg://user:password@host:5432/db" \
  -v ./uploads:/app/static/uploads \
  notebook-app
```

---

## Project Structure Overview

```
backend/
├── src/
│   ├── core/                    # Business logic (framework-independent)
│   │   ├── domain/              # Entities: Notebook, Section, Page, Tag
│   │   ├── services/            # Use cases: CreateNotebookService, etc.
│   │   ├── interfaces/          # Repository interfaces
│   │   ├── commands/            # Command objects (input DTOs)
│   │   ├── queries/             # Query objects (input DTOs)
│   │   └── results/             # Result wrapper for success/failure
│   │
│   ├── infrastructure/          # Implementation details
│   │   ├── data/                # Database access
│   │   │   ├── models/          # SQLAlchemy ORM models
│   │   │   └── repositories/    # Repository implementations
│   │   ├── storage/             # File storage for images
│   │   └── config/              # Configuration management
│   │
│   ├── api/                     # FastAPI presentation layer
│   │   ├── routes/              # API endpoints (notebooks, sections, pages, etc.)
│   │   ├── templates/           # Jinja2 HTML templates
│   │   ├── static/              # CSS, JavaScript, images
│   │   └── middleware/          # Request/response middleware
│   │
│   ├── main.py                  # Application entry point & DI setup
│   └── scripts/                 # Utility scripts (seed data, migrations)
│
├── tests/
│   ├── unit/                    # Core business logic tests
│   ├── integration/             # Database & API tests
│   └── fixtures/                # Test data & mocks
│
├── migrations/                  # Alembic database migrations
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
├── .env                         # Environment variables (create this)
└── Dockerfile                   # Docker container definition
```

---

## Common Development Tasks

### Running Tests

**All tests:**
```bash
pytest
```

**With coverage:**
```bash
pytest --cov=src --cov-report=html
# View coverage report: open htmlcov/index.html
```

**Specific test file:**
```bash
pytest tests/unit/services/test_create_notebook_service.py
```

**Integration tests only:**
```bash
pytest tests/integration/
```

### Database Migrations

**Create a new migration:**
```bash
alembic revision --autogenerate -m "Add user_id column to notebooks"
```

**Apply migrations:**
```bash
alembic upgrade head
```

**Rollback one migration:**
```bash
alembic downgrade -1
```

**View migration history:**
```bash
alembic history
```

### Code Quality

**Format code with Black:**
```bash
black src/ tests/
```

**Lint with flake8:**
```bash
flake8 src/ tests/
```

**Type checking with mypy:**
```bash
mypy src/
```

---

## API Usage Examples

### Using cURL

**Create a notebook:**
```bash
curl -X POST http://localhost:8000/api/notebooks \
  -H "Content-Type: application/json" \
  -d '{"name": "My Notebook", "color": "#FF5733"}'
```

**List all notebooks:**
```bash
curl http://localhost:8000/api/notebooks
```

**Create a section:**
```bash
curl -X POST http://localhost:8000/api/notebooks/{notebook_id}/sections \
  -H "Content-Type: application/json" \
  -d '{"name": "My Section"}'
```

**Create a page:**
```bash
curl -X POST http://localhost:8000/api/sections/{section_id}/pages \
  -H "Content-Type: application/json" \
  -d '{"title": "My Page", "content": "# Hello World\n\nThis is my first page."}'
```

**Search pages:**
```bash
curl "http://localhost:8000/api/search?q=hello"
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Create notebook
response = requests.post(f"{BASE_URL}/notebooks", json={
    "name": "Work",
    "color": "#0078D4"
})
notebook = response.json()["data"]
print(f"Created notebook: {notebook['id']}")

# Create section
response = requests.post(
    f"{BASE_URL}/notebooks/{notebook['id']}/sections",
    json={"name": "Projects"}
)
section = response.json()["data"]

# Create page
response = requests.post(
    f"{BASE_URL}/sections/{section['id']}/pages",
    json={
        "title": "Q1 Planning",
        "content": "# Q1 Planning\n\n## Goals\n- Launch feature X\n- Improve performance",
        "tags": ["urgent", "planning"]
    }
)
page = response.json()["data"]
print(f"Created page: {page['title']}")

# Search
response = requests.get(f"{BASE_URL}/search", params={"q": "planning"})
results = response.json()["data"]["results"]
print(f"Found {len(results)} results")
```

---

## Frontend Development

### HTML Templates (Jinja2)

Templates are located in `backend/src/api/templates/`:

- `base.html` - Base layout with Bootstrap
- `index.html` - Main three-pane notebook interface
- `components/` - Reusable components (navbar, sidebar, modals)

**Example template usage:**
```html
<!-- templates/notebook.html -->
{% extends "base.html" %}

{% block content %}
<div class="container-fluid">
  <div class="row">
    <!-- Notebooks sidebar -->
    <div class="col-md-2">
      {% for notebook in notebooks %}
        <div class="notebook-item" style="border-left: 3px solid {{ notebook.color }}">
          {{ notebook.name }}
        </div>
      {% endfor %}
    </div>
    
    <!-- Sections -->
    <div class="col-md-3">
      <!-- Section tabs -->
    </div>
    
    <!-- Page content -->
    <div class="col-md-7">
      <!-- Markdown editor -->
    </div>
  </div>
</div>
{% endblock %}
```

### JavaScript (Vanilla JS + Bootstrap)

JavaScript files in `backend/src/api/static/js/`:

- `app.js` - Main application logic
- `auto-save.js` - Auto-save functionality
- `editor.js` - Markdown editor integration (EasyMDE)
- `search.js` - Search UI and highlighting

**Auto-save example:**
```javascript
// static/js/auto-save.js
const autoSave = new AutoSave('/api/pages/123/content', 3000);
editor.codemirror.on('change', () => {
    autoSave.scheduleSave(editor.value());
});
```

### Custom CSS

Located in `backend/src/api/static/css/custom.css`:

```css
/* Three-pane layout */
.notebooks-sidebar {
    border-right: 1px solid #dee2e6;
    height: 100vh;
    overflow-y: auto;
}

.notebook-item {
    padding: 0.5rem;
    cursor: pointer;
    border-left: 3px solid transparent;
}

.notebook-item:hover {
    background-color: #f8f9fa;
}

.notebook-item.active {
    background-color: #e9ecef;
    font-weight: bold;
}
```

---

## Architecture Patterns

### Clean Architecture Flow

```
User Request
    ↓
FastAPI Route (api/routes/notebooks.py)
    ↓
Pydantic Request Model → Command Object
    ↓
Service (core/services/create_notebook_service.py)
    ↓
Repository Interface (core/interfaces/repositories.py)
    ↓
Repository Implementation (infrastructure/data/repositories/)
    ↓
SQLAlchemy ORM Model
    ↓
Database
```

### Dependency Injection Setup

```python
# src/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from infrastructure.data.repositories.notebook_repository import NotebookRepository
from core.services.create_notebook_service import CreateNotebookService

# Database setup
engine = create_async_engine(settings.database_url)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency providers
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

def get_notebook_repository(db: AsyncSession = Depends(get_db)):
    return NotebookRepository(db)

def get_create_notebook_service(
    repo = Depends(get_notebook_repository)
):
    return CreateNotebookService(repo)

# Route usage
@router.post("/api/notebooks")
async def create_notebook(
    request: CreateNotebookRequest,
    service: CreateNotebookService = Depends(get_create_notebook_service)
):
    command = CreateNotebookCommand(name=request.name, color=request.color)
    result = await service.execute(command)
    return {"success": result.is_success, "data": result.value}
```

---

## Troubleshooting

### Common Issues

**Issue: "ModuleNotFoundError: No module named 'src'"**
- **Solution**: Ensure you're running commands from the `backend/` directory
- Or add `PYTHONPATH`: `export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"`

**Issue: "Database is locked" (SQLite)**
- **Solution**: SQLite doesn't support high concurrency. Use PostgreSQL for production.

**Issue: "Port 8000 already in use"**
- **Solution**: Kill the existing process: `lsof -ti:8000 | xargs kill -9`
- Or use a different port: `uvicorn src.main:app --port 8001`

**Issue: Auto-save not working**
- **Solution**: Check browser console for JavaScript errors
- Verify `/api/pages/{id}/content` endpoint is accessible
- Check network tab for failed requests

### Logging

Enable debug logging in `.env`:
```bash
DEBUG=True
LOG_LEVEL=DEBUG
```

View logs in console or configure file logging:
```python
# src/main.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
```

---

## Next Steps

1. **Implement Core Features**:
   - Follow `specs/001-notebook-management-app/tasks.md` (created by `/speckit.tasks`)
   - Start with P1 user stories (notebook/section/page creation)

2. **Customize UI**:
   - Modify Bootstrap theme in `static/css/custom.css`
   - Add company branding to templates

3. **Add Authentication** (Future):
   - Implement OAuth2 with JWT tokens
   - Add user management endpoints
   - Multi-tenancy support

4. **Deploy to Production**:
   - Set up PostgreSQL database
   - Configure environment variables
   - Use Docker or deploy to cloud platform (AWS, GCP, Azure)
   - Set up CI/CD pipeline (GitHub Actions, GitLab CI)

---

## Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy 2.0 Tutorial**: https://docs.sqlalchemy.org/en/20/tutorial/
- **Bootstrap 5 Docs**: https://getbootstrap.com/docs/5.3/
- **Alembic Tutorial**: https://alembic.sqlalchemy.org/en/latest/tutorial.html
- **Clean Architecture (Book)**: Robert C. Martin

---

## Support

For questions or issues:
1. Check the feature spec: `specs/001-notebook-management-app/spec.md`
2. Review architecture decisions: `specs/001-notebook-management-app/research.md`
3. Consult API contracts: `specs/001-notebook-management-app/contracts/openapi.yaml`
4. Open an issue on the project repository

**Happy coding! 🚀**
