"""
RoadWatch — Complaint API Schemas
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ── Requests ────────────────────────────────────────────────────

class ComplaintCreate(BaseModel):
    """Payload for POST /api/complaints."""
    h3_index: str
    defect_type: str
    severity_score: int = Field(ge=1, le=5)
    confidence_pct: float = Field(ge=0, le=100)
    image_base64: Optional[str] = None
    citizen_lat: Optional[float] = Field(None, ge=-90, le=90)
    citizen_lng: Optional[float] = Field(None, ge=-180, le=180)
    citizen_description: Optional[str] = None


class StatusUpdate(BaseModel):
    """Payload for PATCH /api/complaints/:id/status."""
    new_status: str
    event_note: Optional[str] = None

    @field_validator("new_status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed = {"Filed", "Escalated", "Resolved"}
        if v not in allowed:
            raise ValueError(f"Status must be one of {allowed}")
        return v


# ── Responses ───────────────────────────────────────────────────

class ComplaintSummary(BaseModel):
    """Lightweight complaint for list views."""
    id: uuid.UUID
    ticket_number: str
    defect_type: str
    severity_score: int
    road_name: Optional[str] = None
    district: Optional[str] = None
    assigned_engineer: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None


class ComplaintListResponse(BaseModel):
    """Response for GET /api/complaints."""
    total: int
    complaints: list[ComplaintSummary]


class EventTimeline(BaseModel):
    """Single event in a complaint's lifecycle."""
    id: uuid.UUID
    event_type: str
    event_note: Optional[str] = None
    created_at: Optional[datetime] = None


class ComplaintDetail(BaseModel):
    """Full complaint detail for GET /api/complaints/:id."""
    id: uuid.UUID
    ticket_number: str
    road_segment_id: Optional[uuid.UUID] = None
    defect_type: str
    severity_score: int
    confidence_pct: float
    image_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: str
    escalated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    road_name: Optional[str] = None
    district: Optional[str] = None
    events: list[EventTimeline] = []
