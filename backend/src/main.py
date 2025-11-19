"""FastAPI application entry point and dependency injection setup."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.config.settings import get_settings
from src.infrastructure.config.database import init_db
from src.api.middleware.error_handler import error_handler_middleware

# Import routers
from src.api.routes import notebooks, sections, pages, tags, search


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

# Error handling middleware
app.middleware("http")(error_handler_middleware)

# Include API routers
app.include_router(notebooks.router)
app.include_router(sections.router)
app.include_router(pages.router)
app.include_router(tags.router)
app.include_router(search.router)

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
    return templates.TemplateResponse("index_tree.html", {"request": request})

# Legacy UI endpoint
@app.get("/legacy")
async def legacy_ui(request: Request):
    """Legacy UI endpoint."""
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
