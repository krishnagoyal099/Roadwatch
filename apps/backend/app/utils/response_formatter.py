"""
RoadWatch — Response Formatting Utilities
"""
from __future__ import annotations

from typing import Optional


def format_complaint_summary(complaint: dict, segment: Optional[dict] = None) -> dict:
    return {
        "id": complaint.get("id"),
        "ticket_number": complaint.get("ticket_number"),
        "defect_type": complaint.get("defect_type"),
        "severity_score": complaint.get("severity_score"),
        "road_name": segment.get("road_name") if segment else None,
        "district": segment.get("district") if segment else None,
        "assigned_engineer": segment.get("executive_engineer_name") if segment else None,
        "status": complaint.get("status"),
        "created_at": complaint.get("created_at"),
    }


def format_ticket_confirmation(complaint: dict, segment: Optional[dict] = None) -> dict:
    return {
        "id": str(complaint.get("id")),
        "ticket_number": complaint.get("ticket_number"),
        "road_segment_id": str(complaint.get("road_segment_id", "")) or None,
        "defect_type": complaint.get("defect_type"),
        "severity_score": complaint.get("severity_score"),
        "confidence_pct": complaint.get("confidence_pct"),
        "image_url": complaint.get("image_url"),
        "latitude": complaint.get("latitude"),
        "longitude": complaint.get("longitude"),
        "status": complaint.get("status"),
        "road_name": segment.get("road_name") if segment else None,
        "district": segment.get("district") if segment else None,
        "executive_engineer_name": segment.get("executive_engineer_name") if segment else None,
        "executive_engineer_contact": segment.get("executive_engineer_contact") if segment else None,
    }
