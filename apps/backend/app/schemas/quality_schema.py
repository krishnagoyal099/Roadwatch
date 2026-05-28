"""
RoadWatch — Road Quality API Schemas
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RecentComplaint(BaseModel):
    ticket_number: str
    defect_type: str
    severity_score: int
    status: str
    created_at: Optional[datetime] = None


# ── List mode (GET /api/road-quality) ──────────────────────────

class RoadQualityRecord(BaseModel):
    """One segment's quality summary — used in list mode."""
    road_segment_id: str
    road_name: Optional[str] = None
    district: Optional[str] = None
    road_type: Optional[str] = None
    contractor_name: Optional[str] = None
    h3_index: Optional[str] = None
    last_maintenance_date: Optional[str] = None
    avg_severity: float
    open_complaint_count: int
    quality_label: str        # Good | Deteriorating | Critical
    last_complaint_date: Optional[str] = None
    recent_complaints: list[RecentComplaint] = []


class RoadQualityListResponse(BaseModel):
    data: list[RoadQualityRecord]
    count: int


# ── Point-lookup mode (GET /api/road-quality?lat=&lng=) ────────

class RoadQualityPointResponse(BaseModel):
    """Response when querying by lat/lng — matches API spec."""
    road_name: Optional[str] = None
    district: Optional[str] = None
    road_type: Optional[str] = None
    contractor_name: Optional[str] = None
    last_maintenance_date: Optional[datetime] = None
    open_complaints: int = 0
    average_severity: float = 0.0
    quality_label: str = "Unknown"
    recent_complaints: list[RecentComplaint] = []
    error: Optional[str] = None
