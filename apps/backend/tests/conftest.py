"""
RoadWatch — Pytest Fixtures & Mocks
Async AsyncClient with mocked Supabase, LLM, CV, and Geocoding services.
"""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timezone
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.core.session_store import SessionStore
from app.main import app
from app.dependencies import get_db, get_sessions


# ── Mock Constants ─────────────────────────────────────────────

MOCK_SEGMENT_ID = str(uuid.uuid4())
MOCK_COMPLAINT_ID = str(uuid.uuid4())
MOCK_SESSION_ID = "test-session-123"

MOCK_ROAD_SEGMENT = {
    "id": MOCK_SEGMENT_ID,
    "road_name": "MG Road",
    "district": "Bengaluru",
    "road_type": "NH",
    "h3_index": "8960145b483ffff",  # h3.latlng_to_cell(12.9716, 77.5946, 9)
    "executive_engineer_name": "R. Kumar",
    "executive_engineer_contact": "99001-23456",
    "contractor_name": "L&T Construction",
    "budget_sanctioned_lakhs": 250.0,
    "last_maintenance_date": "2023-11-01T00:00:00Z",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "created_at": datetime.now(timezone.utc).isoformat(),
}

MOCK_COMPLAINT = {
    "id": MOCK_COMPLAINT_ID,
    "ticket_number": "RW-0001",
    "road_segment_id": MOCK_SEGMENT_ID,
    "defect_type": "Pothole",
    "severity_score": 4,
    "confidence_pct": 87.5,
    "image_url": "https://supabase.co/storage/v1/.../RW-0001.jpg",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "status": "Filed",
    "reported_by_session": MOCK_SESSION_ID,
    "escalated_at": None,
    "resolved_at": None,
    "created_at": datetime.now(timezone.utc).isoformat(),
}


# ── Fake Supabase ──────────────────────────────────────────────

class _FakeQB:
    """Chainable Postgrest-like query builder backed by an in-memory store."""

    def __init__(self, table_name: str, store: dict) -> None:
        self._name = table_name
        self._store = store
        self._filters: dict = {}
        self._pending_insert: Any = None
        self._pending_update: dict | None = None
        self._single = False

    def select(self, *args, **kwargs) -> "_FakeQB":
        return self

    def insert(self, data: Any) -> "_FakeQB":
        self._pending_insert = data
        return self

    def update(self, data: dict) -> "_FakeQB":
        self._pending_update = data
        return self

    def eq(self, col: str, val: Any) -> "_FakeQB":
        self._filters[col] = val
        return self

    def in_(self, col: str, vals: list) -> "_FakeQB":
        self._filters[col] = vals
        return self

    def order(self, *args, **kwargs) -> "_FakeQB":
        return self

    def range(self, *args, **kwargs) -> "_FakeQB":
        return self

    def single(self) -> "_FakeQB":
        self._single = True
        return self

    def execute(self):
        table = self._store.setdefault(self._name, [])

        # INSERT
        if self._pending_insert is not None:
            rows = self._pending_insert if isinstance(self._pending_insert, list) else [self._pending_insert]
            inserted = []
            for r in rows:
                r = dict(r)
                if "id" not in r:
                    r["id"] = str(uuid.uuid4())
                table.append(r)
                inserted.append(r)
            return MagicMock(data=inserted, count=len(inserted))

        # Filter — match against the live store list so updates mutate in-place
        def _matches(r):
            for col, val in self._filters.items():
                if isinstance(val, list):
                    if r.get(col) not in val:
                        return False
                else:
                    if r.get(col) != val:
                        return False
            return True

        results = [r for r in table if _matches(r)]

        # UPDATE — mutate the actual store objects
        if self._pending_update is not None:
            for r in results:
                r.update(self._pending_update)
            return MagicMock(data=results, count=len(results))

        # SELECT
        if self._single:
            return MagicMock(data=results[0] if results else None)
        return MagicMock(data=results, count=len(results))


class FakeSupabaseClient:
    """In-memory Supabase with pre-seeded demo data."""

    def __init__(self) -> None:
        self._store: dict = {
            "road_segments": [MOCK_ROAD_SEGMENT.copy()],
            "complaints": [MOCK_COMPLAINT.copy()],
            "complaint_events": [],
        }

    def table(self, name: str) -> _FakeQB:
        return _FakeQB(name, self._store)

    def seed_table(self, name: str, rows: list) -> None:
        self._store[name] = list(rows)

    def get_table(self, name: str) -> list:
        return list(self._store.get(name, []))

    def storage(self):
        mock_storage = MagicMock()
        mock_bucket = MagicMock()
        mock_storage.from_.return_value = mock_bucket
        mock_bucket.upload.return_value = None
        mock_bucket.get_public_url.return_value = "https://supabase.co/storage/v1/mock-image.jpg"
        return mock_storage


# ── Fixtures ───────────────────────────────────────────────────

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client():
    """Async HTTP client with all external deps mocked."""
    fake_db = FakeSupabaseClient()
    fresh_sessions = SessionStore(ttl_minutes=30)

    app.dependency_overrides[get_db] = lambda: fake_db
    app.dependency_overrides[get_sessions] = lambda: fresh_sessions

    with (
        patch("app.routers.chatbot.llm_service") as mock_llm,
        patch("app.routers.chatbot.cv_service") as mock_cv,
        patch("app.routers.chatbot.geocoding_service") as mock_geo,
    ):
        # LLM: intent classification
        mock_llm.classify_intent.side_effect = lambda msg: {
            "report a pothole": "report_defect",
            "how much was spent": "query_spending",
            "road quality": "check_quality",
            "hello": "unclear",
        }.get(msg, "unclear")

        mock_llm.extract_location.return_value = "Bengaluru"
        mock_llm.generate_defect_confirmation.return_value = "Complaint filed! Ticket RW-0001."
        mock_llm.generate_spending_summary.return_value = "Total budget for Bengaluru is 250 lakhs."
        mock_llm.generate_quality_assessment.return_value = (
            "MG Road is Deteriorating with 1 open complaint."
        )
        mock_llm.generate_unclear_response.return_value = (
            "I can help with reporting, spending, or quality."
        )

        # CV: async method
        mock_cv.analyse = AsyncMock(return_value={
            "defect_type": "Pothole",
            "severity_score": 4,
            "confidence_pct": 87.5,
        })

        # Geocoding: async method
        mock_geo.geocode = AsyncMock(return_value=(12.9716, 77.5946))

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

    app.dependency_overrides.clear()


# ── Legacy sync fixture (kept for backwards compat) ─────────────

@pytest.fixture
def mock_db() -> FakeSupabaseClient:
    return FakeSupabaseClient()
