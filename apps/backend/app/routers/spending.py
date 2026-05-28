"""
RoadWatch — Spending Router
"""
from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import get_db
from app.schemas.spending_schema import SpendingResponse
from app.services.spending_service import SpendingService

router = APIRouter()
logger = logging.getLogger(__name__)


def _get_svc(db=Depends(get_db)) -> SpendingService:
    return SpendingService(db)


@router.get("/spending", response_model=SpendingResponse)
async def get_spending(
    district: Optional[str] = Query(None),
    road_type: Optional[str] = Query(None),
    service: SpendingService = Depends(_get_svc),
):
    logger.info("get_spending_endpoint_called", extra={"district": district, "road_type": road_type})
    try:
        result = service.get_spending(district=district, road_type=road_type)
        return result
    except Exception as e:
        logger.exception("get_spending_failed")
        raise HTTPException(status_code=500, detail=str(e))
