"""
RoadWatch — Internal Chat State Model
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ChatContext(BaseModel):
    """Bundles all context needed by the LLM to generate a contextual response."""

    intent: str
    citizen_message: str
    defect_type: Optional[str] = None
    severity_score: Optional[int] = None
    confidence_pct: Optional[float] = None
    road_name: Optional[str] = None
    district: Optional[str] = None
    engineer_name: Optional[str] = None
    engineer_contact: Optional[str] = None
    contractor_name: Optional[str] = None
    budget_sanctioned_lakhs: Optional[float] = None
    last_maintenance_date: Optional[str] = None
    ticket_number: Optional[str] = None
    open_complaints: Optional[int] = None
    average_severity: Optional[float] = None
    quality_label: Optional[str] = None
