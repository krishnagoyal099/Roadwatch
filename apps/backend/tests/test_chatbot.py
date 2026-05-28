"""
RoadWatch — Chatbot Router Tests
"""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_chat_unclear_intent(client):
    response = await client.post(
        "/api/chat",
        json={"session_id": "s1", "message": "hello"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "unclear"
    assert "help with" in data["reply"].lower()


@pytest.mark.asyncio
async def test_chat_report_defect_missing_image(client):
    response = await client.post(
        "/api/chat",
        json={"session_id": "s2", "message": "report a pothole"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "report_defect"
    assert "photo" in data["reply"].lower() or "upload" in data["reply"].lower()
    assert data["ticket"] is None


@pytest.mark.asyncio
async def test_chat_report_defect_missing_location(client):
    response = await client.post(
        "/api/chat",
        json={
            "session_id": "s3",
            "message": "report a pothole",
            "image_base64": "data:image/jpeg;base64,FAKEIMAGEDATA",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "report_defect"
    assert "location" in data["reply"].lower() or "share" in data["reply"].lower()
    assert data["ticket"] is None


@pytest.mark.asyncio
async def test_chat_report_defect_complete(client):
    response = await client.post(
        "/api/chat",
        json={
            "session_id": "s4",
            "message": "report a pothole",
            "image_base64": "data:image/jpeg;base64,FAKEIMAGEDATA",
            "lat": 12.9716,
            "lng": 77.5946,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "report_defect"
    assert data["ticket"] is not None
    assert "ticket_number" in data["ticket"]


@pytest.mark.asyncio
async def test_chat_query_spending(client):
    response = await client.post(
        "/api/chat",
        json={"session_id": "s5", "message": "how much was spent"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "query_spending"
    assert "250" in data["reply"] or "budget" in data["reply"].lower()


@pytest.mark.asyncio
async def test_chat_check_quality_with_coords(client):
    response = await client.post(
        "/api/chat",
        json={
            "session_id": "s6",
            "message": "road quality",
            "lat": 12.9716,
            "lng": 77.5946,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "check_quality"
    assert "mg road" in data["reply"].lower() or "deteriorating" in data["reply"].lower()


@pytest.mark.asyncio
async def test_chat_check_quality_needs_location(client):
    """extract_location returns 'Bengaluru', geocoding returns (12.9716, 77.5946)."""
    response = await client.post(
        "/api/chat",
        json={"session_id": "s7", "message": "road quality"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "check_quality"
    assert "mg road" in data["reply"].lower() or "bengaluru" in data["reply"].lower()


@pytest.mark.asyncio
async def test_chat_missing_session_id(client):
    response = await client.post("/api/chat", json={"message": "hello"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_missing_message(client):
    response = await client.post("/api/chat", json={"session_id": "s8"})
    assert response.status_code == 422
