"""
Main FastAPI application factory
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from backend.app.config import settings
from backend.app.database import init_db
from backend.app.api import health, auth, tutor


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    Handles startup and shutdown events.
    """
    # Startup
    print("Starting up thinkloop AI backend...")
    init_db()
    print("✓ Database initialized")
    yield
    # Shutdown
    print("Shutting down thinkloop AI backend...")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title="thinkloop AI API",
        description="Intelligent Tutoring System using Socratic Method",
        version="1.0.0-alpha",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
        lifespan=lifespan,
    )

    # Middleware: Trusted Host
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "localhost",
            "127.0.0.1",
            "*.thinkloop.ai",
            "thinkloop.ai",
        ],
    )

    # Middleware: CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    # API Routes
    app.include_router(health.router)
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(tutor.router, prefix="/api/v1")

    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "Welcome to thinkloop AI",
            "docs": "/docs",
            "health": "/health",
        }

    return app


# Create application instance
app = create_app()
