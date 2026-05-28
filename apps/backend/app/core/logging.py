"""
RoadWatch — Structured Logging Configuration
Sets up structlog + stdlib logging for JSON-friendly, debuggable output.
Call `setup_logging()` once at application startup.
"""

from __future__ import annotations

import logging
import sys
import time
from typing import Any

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure structured logging for the entire application.
    - stdlib handlers use a plain console formatter in dev,
      JSON formatter in production.
    - structlog is configured to wrap stdlib loggers.
    """
    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    # Choose renderer based on whether we want pretty console or JSON
    if log_level.upper() == "DEBUG":
        renderer = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
        foreign_pre_chain=shared_processors,
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Quiet noisy libraries
    for noisy in ("uvicorn.access", "httpx", "httpcore", "urllib3"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    logging.getLogger("app").setLevel(getattr(logging, log_level.upper(), logging.INFO))


# ── Request Logging Middleware ──────────────────────────────────

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs method, path, status code, and duration for every request.
    Attach to the FastAPI app in main.py.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        logger = structlog.get_logger("request")
        logger.info(
            "http_request",
            method=request.method,
            path=request.url.path,
            query=str(request.query_params),
            status_code=response.status_code,
            duration_ms=duration_ms,
        )

        return response