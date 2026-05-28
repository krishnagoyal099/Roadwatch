"""
RoadWatch — Spending Service
Business logic for querying public spending on road segments.
"""
from __future__ import annotations

import logging
from typing import Any, Optional

from app.schemas.spending_schema import SegmentSpending

logger = logging.getLogger(__name__)


class SpendingService:
    """Handles aggregation of spending and complaint data."""

    def __init__(self, supabase: Any) -> None:
        self.db = supabase

    def get_spending(self, district: Optional[str] = None, road_type: Optional[str] = None) -> dict:
        """
        Get spending overview with per-segment breakdown.
        Two-step fetch (segments + open complaints) merged in-memory.
        """
        # 1. Fetch segments
        seg_query = self.db.table("road_segments").select("*")
        if district:
            seg_query = seg_query.eq("district", district)
        if road_type:
            seg_query = seg_query.eq("road_type", road_type)

        segments = seg_query.execute().data or []

        if not segments:
            return {
                "total_budget_sanctioned_lakhs": 0.0,
                "total_road_segments": 0,
                "total_contractors": 0,
                "segments": [],
            }

        segment_ids = [s["id"] for s in segments]

        # 2. Fetch open complaints for these segments
        comp_resp = (
            self.db.table("complaints")
            .select("road_segment_id, status")
            .in_("road_segment_id", segment_ids)
            .execute()
        )
        open_counts: dict[str, int] = {}
        for c in comp_resp.data or []:
            if c["status"] != "Resolved":
                sid = c["road_segment_id"]
                open_counts[sid] = open_counts.get(sid, 0) + 1

        # 3. Aggregate
        total_budget = 0.0
        contractors: set = set()
        segment_list = []

        for s in segments:
            budget = float(s.get("budget_sanctioned_lakhs", 0))
            total_budget += budget
            if s.get("contractor_name"):
                contractors.add(s["contractor_name"])

            segment_list.append(
                SegmentSpending(
                    road_name=s.get("road_name"),
                    road_type=s.get("road_type"),
                    contractor_name=s.get("contractor_name"),
                    budget_sanctioned_lakhs=budget,
                    last_maintenance_date=s.get("last_maintenance_date"),
                    open_complaints=open_counts.get(s["id"], 0),
                ).model_dump()
            )

        return {
            "total_budget_sanctioned_lakhs": round(total_budget, 2),
            "total_road_segments": len(segments),
            "total_contractors": len(contractors),
            "segments": segment_list,
        }
