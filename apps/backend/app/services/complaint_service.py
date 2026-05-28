"""
RoadWatch — Complaint Service
Business logic for creating, querying, and updating complaints.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from app.schemas.complaint_schema import ComplaintCreate, StatusUpdate
from app.utils.image_upload import upload_image
from app.utils.ticket_generator import generate_ticket_number

logger = logging.getLogger(__name__)


class ComplaintService:
    """Handles all database operations for complaints."""

    def __init__(self, supabase: Any) -> None:
        self.db = supabase

    def create_complaint(self, data: ComplaintCreate, session_id: str) -> dict:
        """
        1. Resolve road segment via H3 / lat+lng
        2. Generate ticket with retry on collision
        3. Upload image to Supabase Storage (if provided)
        4. Insert complaint row
        5. Insert 'Filed' event
        6. Return merged complaint + segment data
        """
        # 1. Resolve segment
        segment = None
        from app.utils.h3_utils import match_road_segment
        if data.citizen_lat is not None and data.citizen_lng is not None:
            segment = match_road_segment(data.citizen_lat, data.citizen_lng, self.db)
        else:
            seg_resp = self.db.table("road_segments").select("*").eq("h3_index", data.h3_index).execute()
            if seg_resp.data:
                segment = seg_resp.data[0]

        # 2. Ticket + insert with retry
        complaint_row = None
        for attempt in range(5):
            ticket_number = generate_ticket_number()
            image_url = None

            # 3. Upload image
            if data.image_base64:
                try:
                    image_url = upload_image(data.image_base64, ticket_number, self.db)
                except Exception as e:
                    logger.error("image_upload_failed", extra={"error": str(e)})

            insert_data = {
                "id": str(uuid.uuid4()),
                "ticket_number": ticket_number,
                "road_segment_id": segment["id"] if segment else None,
                "defect_type": data.defect_type,
                "severity_score": data.severity_score,
                "confidence_pct": data.confidence_pct,
                "image_url": image_url,
                "latitude": data.citizen_lat,
                "longitude": data.citizen_lng,
                "status": "Filed",
                "reported_by_session": session_id,
            }

            try:
                response = self.db.table("complaints").insert(insert_data).execute()
                complaint_row = response.data[0]
                logger.info("complaint_created", extra={"ticket": ticket_number, "attempt": attempt + 1})
                break
            except Exception as e:
                if "duplicate key" in str(e) and "ticket_number" in str(e):
                    logger.warning("ticket_collision_retrying", extra={"ticket": ticket_number})
                    continue
                logger.exception("complaint_insert_failed")
                raise RuntimeError(f"Failed to create complaint: {e}") from e

        if not complaint_row:
            raise RuntimeError("Failed to generate unique ticket number after 5 attempts.")

        # 4. Insert Filed event
        try:
            self.db.table("complaint_events").insert({
                "id": str(uuid.uuid4()),
                "complaint_id": complaint_row["id"],
                "event_type": "Filed",
                "event_note": "Auto-filed via RoadWatch chatbot",
            }).execute()
        except Exception as e:
            logger.error("filed_event_insert_failed", extra={"error": str(e)})

        # 5. Merge segment data for response
        complaint_row["road_name"] = segment.get("road_name") if segment else None
        complaint_row["district"] = segment.get("district") if segment else None
        complaint_row["executive_engineer_name"] = segment.get("executive_engineer_name") if segment else None
        complaint_row["executive_engineer_contact"] = segment.get("executive_engineer_contact") if segment else None
        return complaint_row

    def get_complaints(
        self,
        status: Optional[str] = None,
        defect_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        """Fetch a paginated, filterable list of complaints."""
        query = self.db.table("complaints").select(
            "id, ticket_number, defect_type, severity_score, status, created_at, "
            "road_segments(road_name, district, executive_engineer_name)"
        )
        if status:
            query = query.eq("status", status)
        if defect_type:
            query = query.eq("defect_type", defect_type)
        query = query.order("created_at", desc=True)

        response = query.execute()
        rows = response.data or []
        total = len(rows)
        page = rows[offset: offset + limit]

        complaints = []
        for row in page:
            seg = row.pop("road_segments", None) or {}
            row["road_name"] = seg.get("road_name")
            row["district"] = seg.get("district")
            row["assigned_engineer"] = seg.get("executive_engineer_name")
            complaints.append(row)

        return {"total": total, "complaints": complaints}

    def get_complaint_detail(self, complaint_id: str) -> Optional[dict]:
        """Fetch full complaint detail with timeline events."""
        result = (
            self.db.table("complaints")
            .select("*, road_segments(road_name, district, road_type, contractor_name, "
                    "executive_engineer_name, executive_engineer_contact)")
            .eq("id", str(complaint_id))
            .single()
            .execute()
        )
        complaint = result.data
        if not complaint:
            return None

        seg = complaint.pop("road_segments", None) or {}
        for key in ["road_name", "district", "road_type", "contractor_name",
                    "executive_engineer_name", "executive_engineer_contact"]:
            complaint[key] = seg.get(key)

        events_result = (
            self.db.table("complaint_events")
            .select("id, event_type, event_note, created_at")
            .eq("complaint_id", str(complaint_id))
            .order("created_at", desc=False)
            .execute()
        )
        complaint["events"] = events_result.data or []
        return complaint

    def update_complaint_status(self, complaint_id: str, update: StatusUpdate) -> Optional[dict]:
        """Update a complaint's status and append an event."""
        update_data: dict = {"status": update.new_status}
        now = datetime.now(timezone.utc).isoformat()
        if update.new_status == "Escalated":
            update_data["escalated_at"] = now
        elif update.new_status == "Resolved":
            update_data["resolved_at"] = now

        result = (
            self.db.table("complaints")
            .update(update_data)
            .eq("id", str(complaint_id))
            .execute()
        )
        data = result.data[0] if result.data else None
        if data:
            try:
                self.db.table("complaint_events").insert({
                    "id": str(uuid.uuid4()),
                    "complaint_id": str(complaint_id),
                    "event_type": update.new_status,
                    "event_note": update.event_note,
                }).execute()
            except Exception as e:
                logger.warning("status_event_insert_failed", extra={"error": str(e)})
            logger.info("complaint_status_updated", extra={"id": complaint_id, "status": update.new_status})
        return data
