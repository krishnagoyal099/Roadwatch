"""
RoadWatch — Road Quality Router Tests
Uses pre-seeded MOCK_ROAD_SEGMENT (h3_index="891e2659c2bffff", coords 12.9716, 77.5946).
The H3 index for (12.9716, 77.5946) at resolution 9 must match to hit the segment.
Coordinates (0.0, 0.0) produce a different H3 cell → returns Unknown.
"""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_get_road_quality_valid_coords(client):
    """Coordinates match the pre-seeded MG Road segment."""
    response = await client.get("/api/road-quality?lat=12.9716&lng=77.5946")
    assert response.status_code == 200
    data = response.json()
    assert data["road_name"] == "MG Road"
    assert data["quality_label"] in ["Good", "Deteriorating", "Critical"]
    assert "open_complaints" in data


@pytest.mark.asyncio
async def test_get_road_quality_invalid_coords(client):
    """Coords with no matching segment → quality_label = Unknown."""
    response = await client.get("/api/road-quality?lat=0.0&lng=0.0")
    assert response.status_code == 200
    data = response.json()
    assert data["quality_label"] == "Unknown"
    assert "error" in data


@pytest.mark.asyncio
async def test_get_road_quality_missing_params(client):
    response = await client.get("/api/road-quality")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_road_quality_missing_lat(client):
    response = await client.get("/api/road-quality?lng=77.5946")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_road_quality_has_recent_complaints(client):
    response = await client.get("/api/road-quality?lat=12.9716&lng=77.5946")
    data = response.json()
    assert "recent_complaints" in data


@pytest.mark.asyncio
async def test_get_road_quality_contractor_field(client):
    response = await client.get("/api/road-quality?lat=12.9716&lng=77.5946")
    data = response.json()
    if data["quality_label"] != "Unknown":
        assert data["contractor_name"] == "L&T Construction"
