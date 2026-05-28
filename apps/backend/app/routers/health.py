"""
RoadWatch — Health Check Router
Provides a liveness endpoint for Railway / monitoring.
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Liveness check")
async def health_check():
    """Returns 200 if the API process is alive."""
    return {"status": "ok", "service": "roadwatch-api"}