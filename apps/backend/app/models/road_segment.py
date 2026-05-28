"""
RoadWatch — Road Segment Database Model
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RoadSegmentDB(BaseModel):
    """Mirrors the Supabase `road_segments` table schema."""

    id: uuid.UUID
    road_name: str
    district: str
    road_type: str
    h3_index: str
    executive_engineer_name: str
    executive_engineer_contact: str
    contractor_name: str
    budget_sanctioned_lakhs: float = Field(ge=0)
    last_maintenance_date: Optional[datetime] = None
    latitude: float
    longitude: float
    created_at: datetime

    model_config = {"from_attributes": True}
