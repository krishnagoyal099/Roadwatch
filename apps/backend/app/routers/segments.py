"""
RoadWatch — Segments Router (admin/debug)
"""
from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import get_db

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/segments")
async def list_segments(
    district: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db=Depends(get_db),
):
    """List all road segments with optional district filter."""
    logger.info("list_segments_endpoint_called", extra={"district": district})
    try:
        query = db.table("road_segments").select("*")
        if district:
            query = query.eq("district", district)
        query = query.order("road_name")
        response = query.execute()
        all_rows = response.data or []
        page = all_rows[offset: offset + limit]
        return {"total": len(all_rows), "segments": page}
    except Exception as e:
        logger.exception("list_segments_failed")
        raise HTTPException(status_code=500, detail=str(e))
