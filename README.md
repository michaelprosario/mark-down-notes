# Notebook Management Application

A web-based notebook management application built with FastAPI, SQLAlchemy, and Clean Architecture principles. Create, organize, and manage your notes across multiple notebooks with sections and pages.

## Features

- 📚 **Notebook Management** - Create and organize multiple notebooks
- 📑 **Sections & Pages** - Structure your notes with sections and individual pages
- ✏️ **Markdown Support** - Write notes in Markdown with live preview
- 🏷️ **Tagging System** - Tag and categorize your notes
- 🔍 **Search Functionality** - Quick search across all notes
- 💾 **Auto-save** - Automatic saving while you type
- 🎨 **Clean UI** - Modern, responsive interface built with Bootstrap 5

## Architecture

This project follows Clean Architecture principles with clear separation of concerns:

```
backend/
├── src/
│   ├── api/              # Presentation layer (FastAPI routes, templates)
│   ├── core/             # Business logic (domain, services, commands, queries)
│   └── infrastructure/   # External concerns (database, config)
├── migrations/           # Database migrations (Alembic)
└── tests/               # Unit and integration tests
```

See [CLEAN_ARCHITECTURE.md](CLEAN_ARCHITECTURE.md) for detailed architecture documentation.

## Prerequisites

- **Python 3.11+** (recommended: 3.11 or 3.12)
- **pip** (Python package manager)
- **Git** (for cloning the repository)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd mark-down-notes
```

### 2. Set Up Python Environment

Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Environment

Copy the example environment file and configure as needed:

```bash
cp .env.example .env
```

Edit `.env` if you need to change default settings:
- Database connection (defaults to SQLite)
- Server host and port (defaults to 0.0.0.0:8000)
- Upload directory and size limits
- CORS origins

**Note:** The default SQLite configuration works out of the box for development.

### 5. Initialize the Database

Run database migrations to create the schema:

```bash
# From the backend directory
alembic upgrade head
```

This will create a `notebooks.db` SQLite file in the backend directory.

### 6. Start the Application

```bash
# From the backend directory
python -m src.main
```

Or using uvicorn directly:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Access the Application

Open your browser and navigate to:
- **Main Application:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Alternative API Docs:** http://localhost:8000/redoc

## Development

### Project Structure

```
backend/
├── src/
│   ├── api/
│   │   ├── routes/           # API endpoints
│   │   ├── schemas.py        # Pydantic request/response models
│   │   ├── dependencies.py   # Dependency injection
│   │   ├── static/           # CSS, JavaScript, images
│   │   └── templates/        # Jinja2 HTML templates
│   ├── core/
│   │   ├── domain/           # Domain entities
│   │   ├── services/         # Business logic services
│   │   ├── commands/         # Command handlers (writes)
│   │   ├── queries/          # Query handlers (reads)
│   │   └── interfaces/       # Repository interfaces
│   └── infrastructure/
│       ├── config/           # Settings and database config
│       └── data/
│           ├── models/       # SQLAlchemy ORM models
│           └── repositories/ # Repository implementations
├── migrations/               # Alembic database migrations
├── tests/                    # Test suite
├── requirements.txt          # Python dependencies
└── pytest.ini               # Pytest configuration
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_services_layer.py

# Run integration tests
pytest tests/integration/
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Check current version
alembic current
```

### Code Quality

```bash
# Format code with Black
black src/

# Run linter
flake8 src/

# Type checking
mypy src/
```

## Configuration

### Environment Variables

Key environment variables you can configure in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./notebooks.db` | Database connection string |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |
| `DEBUG` | `True` | Debug mode |
| `RELOAD` | `True` | Auto-reload on code changes |
| `MAX_UPLOAD_SIZE_MB` | `5` | Maximum file upload size |
| `AUTO_SAVE_INTERVAL_MS` | `3000` | Auto-save interval in milliseconds |

### Database Options

**SQLite (Development - Default):**
```env
DATABASE_URL=sqlite+aiosqlite:///./notebooks.db
```

**PostgreSQL (Production):**
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/notebooks
```

## API Endpoints

### Notebooks
- `GET /api/notebooks` - List all notebooks
- `POST /api/notebooks` - Create notebook
- `PUT /api/notebooks/{id}` - Update notebook
- `DELETE /api/notebooks/{id}` - Delete notebook

### Sections
- `GET /api/notebooks/{notebook_id}/sections` - List sections
- `POST /api/sections` - Create section
- `PUT /api/sections/{id}` - Update section
- `DELETE /api/sections/{id}` - Delete section
- `PUT /api/sections/reorder` - Reorder sections

### Pages
- `GET /api/sections/{section_id}/pages` - List pages
- `POST /api/pages` - Create page
- `GET /api/pages/{id}` - Get page
- `PUT /api/pages/{id}` - Update page
- `DELETE /api/pages/{id}` - Delete page

### Search
- `GET /api/search?q={query}` - Search across notebooks, sections, and pages

See the full API documentation at http://localhost:8000/docs when the app is running.

## Troubleshooting

### Port Already in Use

If port 8000 is already in use:

```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Or run on a different port
uvicorn src.main:app --reload --port 8001
```

### Database Issues

If you encounter database errors:

```bash
# Delete the database and start fresh
rm notebooks.db

# Re-run migrations
alembic upgrade head
```

### Import Errors

Make sure you're in the backend directory and your virtual environment is activated:

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Format code (`black src/`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on GitHub.