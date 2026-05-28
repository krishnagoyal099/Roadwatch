"""
RoadWatch — Chatbot Router
Module-level service instances make them patchable in tests.
DI is used only for stateful/DB resources (session store, db).
"""
from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, Depends

from app.core.session_store import SessionStore
from app.dependencies import get_sessions, get_db
from app.models.chat import ChatContext
from app.schemas.chat_schema import ChatRequest, ChatResponse, TicketConfirmation
from app.schemas.complaint_schema import ComplaintCreate
from app.services.complaint_service import ComplaintService
from app.services.cv_service import CVService
from app.services.geocoding_service import GeocodingService
from app.services.llm_service import LLMService
from app.services.quality_service import QualityService
from app.services.spending_service import SpendingService
from app.utils.response_formatter import format_ticket_confirmation

router = APIRouter()
logger = logging.getLogger(__name__)

# Module-level instances — patchable in tests via unittest.mock.patch
llm_service = LLMService()
cv_service = CVService()
geocoding_service = GeocodingService()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    sessions: SessionStore = Depends(get_sessions),
    db=Depends(get_db),
) -> ChatResponse:
    """
    Main chatbot endpoint.
    1. Updates session state with any new image/coordinates.
    2. Classifies intent via LLM.
    3. Routes to the appropriate handler.
    """
    session = sessions.get_or_create(request.session_id)

    update_kwargs: dict = {}
    if request.image_base64:
        update_kwargs["image_base64"] = request.image_base64
    if request.lat is not None and request.lng is not None:
        update_kwargs["lat"] = request.lat
        update_kwargs["lng"] = request.lng
    if update_kwargs:
        session = sessions.update(session.session_id, **update_kwargs)

    try:
        intent = llm_service.classify_intent(request.message)
    except Exception as e:
        logger.error("intent_classification_error", extra={"error": str(e)})
        intent = "unclear"

    sessions.update(session.session_id, intent=intent)
    logger.info("chat_intent_classified", extra={"session_id": session.session_id, "intent": intent})

    reply_text = ""
    ticket_data: Optional[TicketConfirmation] = None

    if intent == "report_defect":
        reply_text, ticket_data = await _handle_report_defect(request.message, session, sessions, db)
    elif intent == "query_spending":
        reply_text = await _handle_query_spending(request.message, db)
    elif intent == "check_quality":
        reply_text = await _handle_check_quality(request.message, session, sessions, db)
    else:
        reply_text = llm_service.generate_unclear_response(request.message)

    return ChatResponse(session_id=session.session_id, reply=reply_text, intent=intent, ticket=ticket_data)


async def _handle_report_defect(
    message: str, session, sessions: SessionStore, db
) -> tuple[str, Optional[TicketConfirmation]]:
    if not session.image_base64:
        return "I can help with that! Please upload a clear photo of the road defect so I can analyze it.", None

    if session.lat is None or session.lng is None:
        return (
            "Thanks for the photo! To pinpoint the exact road segment, please share your location "
            "using the 📍 button or type the address.",
            None,
        )

    try:
        cv_result = await cv_service.analyse(session.image_base64)
    except Exception as e:
        logger.error("cv_analysis_failed_in_chat", extra={"error": str(e)})
        return "I couldn't analyze the image right now. Please try again later.", None

    complaint_data = ComplaintCreate(
        h3_index="",
        defect_type=cv_result["defect_type"],
        severity_score=cv_result["severity_score"],
        confidence_pct=cv_result["confidence_pct"],
        image_base64=session.image_base64,
        citizen_lat=session.lat,
        citizen_lng=session.lng,
        citizen_description=message,
    )
    try:
        complaint_row = ComplaintService(db).create_complaint(
            data=complaint_data, session_id=session.session_id
        )
    except Exception as e:
        logger.error("complaint_creation_failed_in_chat", extra={"error": str(e)})
        return "I detected the issue but couldn't file the ticket due to a database error. Please try again.", None

    sessions.update(session.session_id, image_base64=None, lat=None, lng=None, intent=None)

    ctx = ChatContext(
        intent="report_defect",
        citizen_message=message,
        defect_type=complaint_row.get("defect_type"),
        severity_score=complaint_row.get("severity_score"),
        road_name=complaint_row.get("road_name"),
        district=complaint_row.get("district"),
        engineer_name=complaint_row.get("executive_engineer_name"),
        engineer_contact=complaint_row.get("executive_engineer_contact"),
        ticket_number=complaint_row.get("ticket_number"),
    )
    try:
        reply_text = llm_service.generate_defect_confirmation(ctx)
    except Exception:
        reply_text = (
            f"✅ Complaint filed!\n"
            f"• Ticket: {ctx.ticket_number}\n"
            f"• Defect: {ctx.defect_type} (Severity: {ctx.severity_score}/5)\n"
            f"• Road: {ctx.road_name}\n"
            f"• Engineer: {ctx.engineer_name}"
        )

    ticket = TicketConfirmation(**format_ticket_confirmation(complaint_row, complaint_row))
    return reply_text, ticket


async def _handle_query_spending(message: str, db) -> str:
    district = llm_service.extract_location(message)
    if not district:
        return "Which district's road spending would you like to know about? Please specify the district name."

    try:
        spending_data = SpendingService(db).get_spending(district=district)
    except Exception as e:
        logger.error("spending_query_failed", extra={"error": str(e)})
        return "I couldn't fetch the spending data right now. Please try again later."

    if not spending_data["segments"]:
        return f"I couldn't find any road spending data for '{district}'. Please check the district name."

    top = spending_data["segments"][0]
    ctx = ChatContext(
        intent="query_spending",
        citizen_message=message,
        district=district,
        budget_sanctioned_lakhs=spending_data.get("total_budget_sanctioned_lakhs"),
        contractor_name=top.get("contractor_name"),
        last_maintenance_date=str(top.get("last_maintenance_date", "")),
        open_complaints=top.get("open_complaints"),
    )
    try:
        return llm_service.generate_spending_summary(ctx)
    except Exception:
        return (
            f"Public spending for {district}:\n"
            f"• Total Budget: ₹{ctx.budget_sanctioned_lakhs} lakhs\n"
            f"• Active Contractors: {spending_data.get('total_contractors')}\n"
            f"• Road Segments: {spending_data.get('total_road_segments')}"
        )


async def _handle_check_quality(message: str, session, sessions: SessionStore, db) -> str:
    if session.lat is None or session.lng is None:
        location = llm_service.extract_location(message)
        if location:
            coords = await geocoding_service.geocode(location)
            if coords:
                sessions.update(session.session_id, lat=coords[0], lng=coords[1])
                session = sessions.get_or_create(session.session_id)
            else:
                return "I couldn't find the location you mentioned. Could you share your GPS location or be more specific?"
        else:
            return "To check the road quality, please share your location or tell me the specific road name and area."

    try:
        quality_data = QualityService(db).get_road_quality(session.lat, session.lng)
    except Exception as e:
        logger.error("quality_check_failed", extra={"error": str(e)})
        return "I couldn't check the road quality right now. Please try again later."

    if quality_data.get("quality_label") == "Unknown":
        return quality_data.get("error", "No road segment found near the provided location.")

    ctx = ChatContext(
        intent="check_quality",
        citizen_message=message,
        road_name=quality_data.get("road_name"),
        district=quality_data.get("district"),
        quality_label=quality_data.get("quality_label"),
        open_complaints=quality_data.get("open_complaints"),
        average_severity=quality_data.get("average_severity"),
        contractor_name=quality_data.get("contractor_name"),
        last_maintenance_date=str(quality_data.get("last_maintenance_date", "")),
    )
    try:
        return llm_service.generate_quality_assessment(ctx)
    except Exception:
        return (
            f"Road quality at {ctx.road_name}:\n"
            f"• Status: {ctx.quality_label}\n"
            f"• Open Complaints: {ctx.open_complaints}\n"
            f"• Avg Severity: {ctx.average_severity}/5\n"
            f"• Contractor: {ctx.contractor_name}"
        )


@router.post("/analyse-image", summary="Analyse a road defect image")
async def analyse_image(
    body: dict,
    sessions: SessionStore = Depends(get_sessions),
):
    """Direct endpoint for CV pipeline testing."""
    import base64 as _b64
    from fastapi import HTTPException

    session_id = body.get("session_id")
    image_base64 = body.get("image_base64")

    if not image_base64:
        raise HTTPException(status_code=422, detail="image_base64 is required.")
    try:
        _b64.b64decode(image_base64, validate=True)
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid base64 image data.")

    session = sessions.get_or_create(session_id)
    result = await cv_service.analyse(image_base64)
    sessions.update(session.session_id, image_base64=image_base64, intent="report_defect")

    return {
        "session_id": session.session_id,
        "defect_type": result["defect_type"],
        "severity_score": result["severity_score"],
        "confidence_pct": result["confidence_pct"],
        "message": (
            f"Detected a **{result['defect_type']}** with severity "
            f"{result['severity_score']}/5 ({result['confidence_pct']}% confidence). "
            "Please confirm your location to file a complaint."
        ),
    }
