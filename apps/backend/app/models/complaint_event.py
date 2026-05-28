"""
RoadWatch — Complaint Event Database Model
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ComplaintEventDB(BaseModel):
    """Mirrors the Supabase `complaint_events` table schema."""

    id: uuid.UUID
    complaint_id: uuid.UUID
    event_type: str
    event_note: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
