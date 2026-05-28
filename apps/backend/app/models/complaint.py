"""
RoadWatch — Complaint Database Model
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ComplaintDB(BaseModel):
    """Mirrors the Supabase `complaints` table schema."""

    id: uuid.UUID
    ticket_number: str
    road_segment_id: Optional[uuid.UUID] = None
    defect_type: str
    severity_score: int = Field(ge=1, le=5)
    confidence_pct: float
    image_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: str = "Filed"
    reported_by_session: Optional[str] = None
    escalated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}
