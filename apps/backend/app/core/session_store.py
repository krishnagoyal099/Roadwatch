"""
RoadWatch — In-Memory Session Store
Manages conversational state for the chatbot.
Each session stores the current intent, uploaded image, coordinates,
matched road segment, and last-active timestamp.
Sessions expire after a configurable TTL (default 30 minutes).
"""

from __future__ import annotations

import logging
import threading
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class SessionData:
    """State for a single chatbot conversation."""

    __slots__ = (
        "session_id",
        "intent",
        "image_base64",
        "lat",
        "lng",
        "matched_segment_id",
        "last_active",
    )

    def __init__(self, session_id: str) -> None:
        self.session_id: str = session_id
        self.intent: Optional[str] = None
        self.image_base64: Optional[str] = None
        self.lat: Optional[float] = None
        self.lng: Optional[float] = None
        self.matched_segment_id: Optional[str] = None
        self.last_active: datetime = datetime.now(timezone.utc)

    def touch(self) -> None:
        self.last_active = datetime.now(timezone.utc)

    def is_expired(self, ttl_minutes: int) -> bool:
        return (
            datetime.now(timezone.utc) - self.last_active
        ) > timedelta(minutes=ttl_minutes)

    def as_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "intent": self.intent,
            "image_base64": self.image_base64 is not None,
            "lat": self.lat,
            "lng": self.lng,
            "matched_segment_id": self.matched_segment_id,
            "last_active": self.last_active.isoformat(),
        }


class SessionStore:
    """
    Thread-safe in-memory session store with TTL expiry.
    A background purge runs on every `get` or `set` call to
    keep the store clean without a separate timer thread.
    """

    def __init__(self, ttl_minutes: int | None = None) -> None:
        settings = get_settings()
        self._ttl = ttl_minutes or settings.session_ttl_minutes
        self._store: dict[str, SessionData] = {}
        self._lock = threading.Lock()

    # ── Public API ─────────────────────────────────────────────

    def get_or_create(self, session_id: str | None = None) -> SessionData:
        """Return existing session or create a new one."""
        self._purge_expired()

        if session_id and session_id in self._store:
            session = self._store[session_id]
            session.touch()
            logger.debug("session_retrieved", extra={"session_id": session_id})
            return session

        new_id = session_id or str(uuid.uuid4())
        session = SessionData(new_id)
        with self._lock:
            self._store[new_id] = session
        logger.info("session_created", extra={"session_id": new_id})
        return session

    def update(
        self,
        session_id: str,
        *,
        intent: str | None = None,
        image_base64: str | None = None,
        lat: float | None = None,
        lng: float | None = None,
        matched_segment_id: str | None = None,
    ) -> SessionData:
        """Partial-update a session's fields."""
        session = self.get_or_create(session_id)

        if intent is not None:
            session.intent = intent
        if image_base64 is not None:
            session.image_base64 = image_base64
        if lat is not None:
            session.lat = lat
        if lng is not None:
            session.lng = lng
        if matched_segment_id is not None:
            session.matched_segment_id = matched_segment_id

        session.touch()
        logger.debug(
            "session_updated",
            extra={"session_id": session_id, "fields": list(locals().keys())},
        )
        return session

    def get(self, session_id: str) -> Optional[SessionData]:
        """Return session if it exists and hasn't expired."""
        self._purge_expired()
        return self._store.get(session_id)

    def delete(self, session_id: str) -> None:
        with self._lock:
            self._store.pop(session_id, None)

    def active_count(self) -> int:
        self._purge_expired()
        return len(self._store)

    # ── Internal ───────────────────────────────────────────────

    def _purge_expired(self) -> None:
        """Remove all sessions older than TTL."""
        now = datetime.now(timezone.utc)
        expired_ids = [
            sid
            for sid, session in self._store.items()
            if session.is_expired(self._ttl)
        ]
        if expired_ids:
            with self._lock:
                for sid in expired_ids:
                    self._store.pop(sid, None)
            logger.debug(
                "sessions_purged", extra={"count": len(expired_ids)}
            )


# ── Singleton accessor ─────────────────────────────────────────
# Import `get_session_store` wherever you need the store.

_session_store: SessionStore | None = None


def get_session_store() -> SessionStore:
    """Lazy singleton — created once, reused everywhere."""
    global _session_store
    if _session_store is None:
        _session_store = SessionStore()
    return _session_store