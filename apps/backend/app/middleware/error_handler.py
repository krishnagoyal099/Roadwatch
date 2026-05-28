"""
RoadWatch — Global Exception Handler
Catches every unhandled exception, logs the full traceback,
and returns a sanitized JSON error to the client.
No internal details leak in production.
"""

from __future__ import annotations

import logging
import traceback
import uuid

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.config import get_settings

logger = logging.getLogger(__name__)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catches any Exception bubbling up from route handlers.
    - Logs full traceback with a unique error ID.
    - Returns 500 with a generic message in production,
      or includes traceback in development.
    """
    error_id = str(uuid.uuid4())[:8]
    tb = traceback.format_exc()

    logger.exception(
        "unhandled_exception",
        extra={
            "error_id": error_id,
            "method": request.method,
            "path": str(request.url),
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "traceback": tb,
        },
    )

    settings = get_settings()

    if settings.is_production:
        detail = f"Internal server error. Reference: {error_id}"
    else:
        detail = f"{type(exc).__name__}: {exc} — ref {error_id}\n{tb}"

    return JSONResponse(
        status_code=500,
        content={"detail": detail, "error_id": error_id},
    )