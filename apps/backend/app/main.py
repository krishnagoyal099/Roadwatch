"""
RoadWatch — FastAPI Application Entry Point
Wires up all routers, middleware, and startup/shutdown hooks.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging import RequestLoggingMiddleware, setup_logging
from app.middleware.cors import add_cors_middleware
from app.middleware.error_handler import global_exception_handler
from app.routers import chatbot, complaints, health, road_quality, segments, spending

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    settings = get_settings()
    setup_logging(log_level=settings.log_level)
    logger.info(
        "roadwatch_starting",
        extra={
            "env": settings.app_env,
            "debug": settings.debug,
            "cv_mock": settings.cv_use_mock,
        },
    )
    yield
    logger.info("roadwatch_shutting_down")


def create_app() -> FastAPI:
    """Application factory — creates and configures the FastAPI instance."""
    settings = get_settings()

    app = FastAPI(
        title="RoadWatch API",
        description=(
            "AI-powered civic accountability platform for the BIMSTEC region. "
            "Citizens report road defects via a conversational chatbot, "
            "track complaints on a public dashboard, and monitor public spending."
        ),
        version="1.0.0",
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        lifespan=lifespan,
    )

    # ── Middleware (order matters — last added = first executed) ──
    add_cors_middleware(app)
    app.add_middleware(RequestLoggingMiddleware)

    # ── Global exception handler ───────────────────────────────
    app.add_exception_handler(Exception, global_exception_handler)

    # ── Routers ────────────────────────────────────────────────
    app.include_router(health.router, tags=["Health"])
    app.include_router(chatbot.router, prefix="/api", tags=["Chatbot"])
    app.include_router(complaints.router, prefix="/api", tags=["Complaints"])
    app.include_router(spending.router, prefix="/api", tags=["Spending"])
    app.include_router(road_quality.router, prefix="/api", tags=["Road Quality"])
    app.include_router(segments.router, prefix="/api", tags=["Segments"])

    logger.info("all_routers_registered")

    return app


# ── Uvicorn entry point ────────────────────────────────────────
app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.is_development,
    )