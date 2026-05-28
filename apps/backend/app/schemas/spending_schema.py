"""
RoadWatch — Spending API Schemas
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SegmentSpending(BaseModel):
    road_name: Optional[str] = None
    road_type: Optional[str] = None
    contractor_name: Optional[str] = None
    budget_sanctioned_lakhs: float
    last_maintenance_date: Optional[datetime] = None
    open_complaints: int = 0


class SpendingResponse(BaseModel):
    total_budget_sanctioned_lakhs: float
    total_road_segments: int
    total_contractors: int
    segments: list[SegmentSpending]
