"""
RoadWatch — Chat API Schemas
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Payload for POST /api/chat."""
    session_id: str
    message: str = Field(..., min_length=1)
    image_base64: Optional[str] = None
    lat: Optional[float] = Field(None, ge=-90, le=90)
    lng: Optional[float] = Field(None, ge=-180, le=180)


class TicketConfirmation(BaseModel):
    """Ticket card returned when a defect is filed."""
    id: str
    ticket_number: str
    road_segment_id: Optional[str] = None
    defect_type: str
    severity_score: int
    confidence_pct: float
    image_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: str
    road_name: Optional[str] = None
    district: Optional[str] = None
    executive_engineer_name: Optional[str] = None
    executive_engineer_contact: Optional[str] = None


class ChatResponse(BaseModel):
    """Response for POST /api/chat."""
    session_id: str
    reply: str
    intent: Optional[str] = None
    ticket: Optional[TicketConfirmation] = None
