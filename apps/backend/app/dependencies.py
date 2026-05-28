"""
RoadWatch — Shared FastAPI Dependencies
All service getters use Depends(get_db) so FastAPI resolves them correctly.
Tests override at the service level directly.
"""
from __future__ import annotations

from fastapi import Depends
from supabase import Client

from app.core.database import get_supabase
from app.core.session_store import SessionStore, get_session_store
from app.services.llm_service import LLMService
from app.services.cv_service import CVService
from app.services.complaint_service import ComplaintService
from app.services.spending_service import SpendingService
from app.services.quality_service import QualityService


def get_db() -> Client:
    return get_supabase()


def get_sessions() -> SessionStore:
    return get_session_store()


def get_llm() -> LLMService:
    return LLMService()


def get_cv() -> CVService:
    return CVService()


def get_complaint_service(db: Client = Depends(get_db)) -> ComplaintService:
    return ComplaintService(db)


def get_spending_service(db: Client = Depends(get_db)) -> SpendingService:
    return SpendingService(db)


def get_quality_service(db: Client = Depends(get_db)) -> QualityService:
    return QualityService(db)