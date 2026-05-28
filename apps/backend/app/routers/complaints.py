"""
RoadWatch — Complaints Router
"""
from __future__ import annotations

import logging
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import get_db
from app.schemas.complaint_schema import (
    ComplaintCreate, ComplaintDetail, ComplaintListResponse, ComplaintSummary, StatusUpdate,
)
from app.services.complaint_service import ComplaintService

router = APIRouter()
logger = logging.getLogger(__name__)


def _get_svc(db=Depends(get_db)) -> ComplaintService:
    return ComplaintService(db)


@router.post("/complaints", status_code=201)
async def create_complaint(
    data: ComplaintCreate,
    session_id: str = Query("api-direct"),
    service: ComplaintService = Depends(_get_svc),
):
    logger.info("create_complaint_endpoint_called")
    try:
        return service.create_complaint(data=data, session_id=session_id)
    except Exception as e:
        logger.exception("create_complaint_failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/complaints", response_model=ComplaintListResponse)
async def list_complaints(
    status: Optional[str] = Query(None),
    defect_type: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    service: ComplaintService = Depends(_get_svc),
) -> ComplaintListResponse:
    logger.info("list_complaints_endpoint_called", extra={"status": status})
    try:
        result = service.get_complaints(status=status, defect_type=defect_type, limit=limit, offset=offset)
        complaints = []
        for r in result["complaints"]:
            if not r.get("created_at"):
                r["created_at"] = None
            complaints.append(ComplaintSummary(**r))
        return ComplaintListResponse(total=result["total"], complaints=complaints)
    except Exception as e:
        logger.exception("list_complaints_failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/complaints/{complaint_id}", response_model=ComplaintDetail)
async def get_complaint_detail(
    complaint_id: uuid.UUID,
    service: ComplaintService = Depends(_get_svc),
) -> ComplaintDetail:
    logger.info("get_complaint_detail_endpoint_called", extra={"id": str(complaint_id)})
    try:
        result = service.get_complaint_detail(str(complaint_id))
        if not result:
            raise HTTPException(status_code=404, detail="Complaint not found")
        return ComplaintDetail(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("get_complaint_detail_failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/complaints/{complaint_id}/status")
async def update_complaint_status(
    complaint_id: uuid.UUID,
    update: StatusUpdate,
    service: ComplaintService = Depends(_get_svc),
):
    logger.info("update_status_endpoint_called", extra={"id": str(complaint_id), "status": update.new_status})
    try:
        result = service.update_complaint_status(str(complaint_id), update)
        if not result:
            raise HTTPException(status_code=404, detail="Complaint not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("update_status_failed")
        raise HTTPException(status_code=500, detail=str(e))
