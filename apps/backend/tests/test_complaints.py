"""
RoadWatch — Complaints Router Tests
"""
from __future__ import annotations

import pytest

from tests.conftest import MOCK_COMPLAINT_ID


_PAYLOAD = {
    "h3_index": "891e2659c2bffff",
    "defect_type": "Surface Crack",
    "severity_score": 3,
    "confidence_pct": 90.0,
    "citizen_lat": 12.9716,
    "citizen_lng": 77.5946,
}


@pytest.mark.asyncio
async def test_create_complaint(client):
    response = await client.post("/api/complaints?session_id=test-api", json=_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data["defect_type"] == "Surface Crack"
    assert data["status"] == "Filed"
    assert data["ticket_number"].startswith("RW-")


@pytest.mark.asyncio
async def test_list_complaints(client):
    response = await client.get("/api/complaints")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "complaints" in data
    assert isinstance(data["complaints"], list)


@pytest.mark.asyncio
async def test_list_complaints_seeded(client):
    """Pre-seeded MOCK_COMPLAINT is visible in the list."""
    response = await client.get("/api/complaints")
    data = response.json()
    assert data["total"] >= 1


@pytest.mark.asyncio
async def test_list_complaints_filter_status(client):
    response = await client.get("/api/complaints?status=Filed")
    assert response.status_code == 200
    data = response.json()
    assert all(c["status"] == "Filed" for c in data["complaints"])


@pytest.mark.asyncio
async def test_get_complaint_detail(client):
    create_resp = await client.post("/api/complaints?session_id=test-detail", json=_PAYLOAD)
    complaint_id = create_resp.json()["id"]

    response = await client.get(f"/api/complaints/{complaint_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == complaint_id
    assert "events" in data
    assert len(data["events"]) > 0
    assert data["events"][0]["event_type"] == "Filed"


@pytest.mark.asyncio
async def test_get_complaint_not_found(client):
    response = await client.get("/api/complaints/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_complaint_status(client):
    # Get the real seeded complaint ID from the list (fresh fixture generates a new UUID each run)
    list_resp = await client.get("/api/complaints")
    complaints = list_resp.json()["complaints"]
    assert complaints, "Expected at least one pre-seeded complaint"
    complaint_id = complaints[0]["id"]

    response = await client.patch(
        f"/api/complaints/{complaint_id}/status",
        json={"new_status": "Escalated", "event_note": "No action taken"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Escalated"


@pytest.mark.asyncio
async def test_update_complaint_invalid_status(client):
    response = await client.patch(
        f"/api/complaints/{MOCK_COMPLAINT_ID}/status",
        json={"new_status": "Flying"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_severity_out_of_range(client):
    bad = {**_PAYLOAD, "severity_score": 10}
    assert (await client.post("/api/complaints?session_id=test-api", json=bad)).status_code == 422
