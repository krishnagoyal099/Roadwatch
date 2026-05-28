"""
RoadWatch — Road Quality Router
lat and lng are required — calls get_road_quality(lat, lng) from service.
"""
from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import get_db
from app.schemas.quality_schema import RoadQualityPointResponse
from app.services.quality_service import QualityService

router = APIRouter()
logger = logging.getLogger(__name__)


def _get_svc(db=Depends(get_db)) -> QualityService:
    return QualityService(db)


@router.get("/road-quality", response_model=RoadQualityPointResponse)
async def get_road_quality(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    service: QualityService = Depends(_get_svc),
):
    """Check road quality at specific coordinates via H3 matching."""
    logger.info("get_road_quality_endpoint_called", extra={"lat": lat, "lng": lng})
    try:
        result = service.get_road_quality(lat=lat, lng=lng)
        return result
    except Exception as e:
        logger.exception("get_road_quality_failed")
        raise HTTPException(status_code=500, detail=str(e))
