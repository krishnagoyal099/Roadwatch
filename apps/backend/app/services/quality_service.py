"""
RoadWatch — Road Quality Service
Business logic for assessing road quality.
Supports both lat/lng point lookup and district-level listing.
"""
from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any, Optional

from app.schemas.quality_schema import RecentComplaint
from app.utils.h3_utils import match_road_segment
from app.utils.severity import compute_quality_label

logger = logging.getLogger(__name__)


class QualityService:
    """Handles road quality checks."""

    def __init__(self, supabase: Any) -> None:
        self.db = supabase

    # ── Point lookup (spec method) ──────────────────────────────

    def get_road_quality(self, lat: float, lng: float) -> dict:
        """
        1. Match coordinates to road segment via H3
        2. Fetch complaints for segment
        3. Calculate stats and quality label
        """
        segment = match_road_segment(lat, lng, self.db)

        if not segment:
            logger.info("no_segment_found_for_quality", extra={"lat": lat, "lng": lng})
            return {
                "quality_label": "Unknown",
                "error": "No road segment found near the provided location.",
                "open_complaints": 0,
                "average_severity": 0.0,
                "recent_complaints": [],
            }

        segment_id = segment["id"]
        comp_resp = (
            self.db.table("complaints")
            .select("ticket_number, defect_type, severity_score, status, created_at")
            .eq("road_segment_id", str(segment_id))
            .order("created_at", desc=True)
            .execute()
        )
        all_complaints = comp_resp.data or []

        open_list = [c for c in all_complaints if c.get("status") != "Resolved"]
        open_count = len(open_list)
        avg_severity = (
            round(sum(c["severity_score"] for c in open_list) / open_count, 2)
            if open_count else None
        )
        quality_label = compute_quality_label(avg_severity, open_count)
        recent = [RecentComplaint(**c).model_dump() for c in all_complaints[:5]]

        return {
            "road_name": segment.get("road_name"),
            "district": segment.get("district"),
            "road_type": segment.get("road_type"),
            "contractor_name": segment.get("contractor_name"),
            "last_maintenance_date": segment.get("last_maintenance_date"),
            "open_complaints": open_count,
            "average_severity": avg_severity or 0.0,
            "quality_label": quality_label,
            "recent_complaints": recent,
        }

    # ── List mode (district filter, used by router without lat/lng) ──

    def get_quality(self, district: Optional[str] = None) -> list[dict]:
        """Return quality records for all segments, optionally filtered by district."""
        seg_query = self.db.table("road_segments").select(
            "id, road_name, district, road_type, contractor_name, h3_index, last_maintenance_date"
        )
        if district:
            seg_query = seg_query.eq("district", district)
        segments = seg_query.execute().data or []

        if not segments:
            return []

        seg_ids = [s["id"] for s in segments]
        complaints = (
            self.db.table("complaints")
            .select("road_segment_id, severity_score, status, created_at, ticket_number, defect_type")
            .in_("road_segment_id", seg_ids)
            .execute()
            .data or []
        )

        grouped: dict[str, list[dict]] = defaultdict(list)
        for c in complaints:
            grouped[c["road_segment_id"]].append(c)

        results = []
        for seg in segments:
            seg_complaints = grouped.get(seg["id"], [])
            if not seg_complaints:
                continue

            scores = [c["severity_score"] for c in seg_complaints if c.get("severity_score")]
            open_count = sum(1 for c in seg_complaints if c.get("status") != "Resolved")
            avg_sev = round(sum(scores) / len(scores), 2) if scores else 0.0
            last_date = max((c.get("created_at", "") for c in seg_complaints), default=None)
            recent = sorted(seg_complaints, key=lambda c: c.get("created_at") or "", reverse=True)[:5]

            results.append({
                "road_segment_id": seg["id"],
                "road_name": seg.get("road_name"),
                "district": seg.get("district"),
                "road_type": seg.get("road_type"),
                "contractor_name": seg.get("contractor_name"),
                "h3_index": seg.get("h3_index"),
                "last_maintenance_date": seg.get("last_maintenance_date"),
                "avg_severity": avg_sev,
                "open_complaint_count": open_count,
                "quality_label": compute_quality_label(avg_sev, open_count),
                "last_complaint_date": last_date,
                "recent_complaints": [
                    {"ticket_number": c.get("ticket_number", ""), "defect_type": c.get("defect_type", ""),
                     "severity_score": c.get("severity_score", 0), "status": c.get("status", ""),
                     "created_at": c.get("created_at")}
                    for c in recent
                ],
            })

        results.sort(key=lambda r: r["avg_severity"], reverse=True)
        return results
