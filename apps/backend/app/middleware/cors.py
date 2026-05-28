"""
RoadWatch — CORS Middleware Configuration
Allows the Vite frontend (and any future client) to call the API.
"""

from __future__ import annotations

from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings


def add_cors_middleware(app) -> None:
    """Attach CORS middleware to the FastAPI app instance."""
    settings = get_settings()

    # In production, only allow the deployed frontend URL.
    # In development, allow common local dev origins.
    if settings.is_production:
        allow_origins = [settings.frontend_url]
    else:
        allow_origins = [
            settings.frontend_url,
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000",
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )