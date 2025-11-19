"""FastAPI application entry point and dependency injection setup."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.config.settings import get_settings
from src.infrastructure.config.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    settings = get_settings()
    await init_db()
    yield
    # Shutdown
    pass


# Initialize FastAPI app
app = FastAPI(
    title="Notebook Management API",
    description="REST API for managing notebooks, sections, pages, and tags",
    version="1.0.0",
    lifespan=lifespan,
)

# Get settings
settings = get_settings()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="src/api/static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="src/api/templates")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "notebook-management"}


# Root endpoint
@app.get("/")
async def root(request: Request):
    """Root endpoint - serves the main UI."""
    from fastapi import Request
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
