"""
RoadWatch — Spending Router Tests
Pre-seeded MOCK_ROAD_SEGMENT has district="Bengaluru" and budget=250 lakhs.
"""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_get_spending_overview(client):
    response = await client.get("/api/spending")
    assert response.status_code == 200
    data = response.json()
    assert "total_budget_sanctioned_lakhs" in data
    assert "total_road_segments" in data
    assert "total_contractors" in data
    assert "segments" in data
    assert isinstance(data["segments"], list)


@pytest.mark.asyncio
async def test_spending_seeded_data(client):
    """Pre-seeded segment is returned."""
    response = await client.get("/api/spending")
    data = response.json()
    assert data["total_road_segments"] >= 1
    assert data["total_budget_sanctioned_lakhs"] >= 250.0


@pytest.mark.asyncio
async def test_get_spending_by_district(client):
    response = await client.get("/api/spending?district=Bengaluru")
    assert response.status_code == 200
    data = response.json()
    assert data["total_road_segments"] > 0
    assert all(s["road_name"] == "MG Road" for s in data["segments"])


@pytest.mark.asyncio
async def test_get_spending_empty_district(client):
    response = await client.get("/api/spending?district=NonExistentDistrict")
    assert response.status_code == 200
    data = response.json()
    assert data["total_road_segments"] == 0
    assert data["total_budget_sanctioned_lakhs"] == 0.0


@pytest.mark.asyncio
async def test_spending_has_open_complaints_field(client):
    response = await client.get("/api/spending")
    data = response.json()
    assert all("open_complaints" in s for s in data["segments"])
