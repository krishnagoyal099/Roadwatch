"""
RoadWatch — Supabase Client Singleton
Provides a single, reusable Supabase client via FastAPI dependency injection.
All routers import the `get_supabase` dependency; tests override it.
"""

from __future__ import annotations

import logging
from functools import lru_cache

from supabase import Client, create_client

from app.core.config import get_settings

logger = logging.getLogger(__name__)


def _build_client() -> Client:
    """Create a Supabase client from current settings."""
    settings = get_settings()
    logger.info(
        "initialising_supabase_client",
        extra={"url": settings.supabase_url},
    )
    # Use service-role key for backend operations (bypasses RLS)
    return create_client(settings.supabase_url, settings.supabase_service_role_key)


@lru_cache(maxsize=1)
def _cached_client() -> Client:
    """Lazily created, cached client — only one per process."""
    return _build_client()


def get_supabase() -> Client:
    """
    FastAPI dependency that yields the Supabase client.
    Override in tests: `app.dependency_overrides[get_supabase] = lambda: mock_client`
    """
    return _cached_client()