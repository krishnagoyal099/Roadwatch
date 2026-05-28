"""
RoadWatch — Application Configuration
Single source of truth for every environment variable.
Uses pydantic-settings for validation and type coercion.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Immutable, validated application settings loaded from .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ────────────────────────────────────────────
    app_name: str = "RoadWatch"
    app_env: Literal["development", "staging", "production"] = "development"
    debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # ── Supabase ───────────────────────────────────────────────
    supabase_url: str
    supabase_key: str
    supabase_service_role_key: str
    supabase_storage_bucket: str = "complaint-images"

    # ── LLM (Groq) ────────────────────────────────────────────
    groq_api_key: str = ""
    groq_model: str = "llama3-70b-8192"
    groq_max_tokens: int = 512
    groq_temperature: float = 0.3

    # ── CV Service ─────────────────────────────────────────────
    cv_service_url: str = "http://localhost:8001"
    cv_use_mock: bool = True

    # ── Geocoding ──────────────────────────────────────────────
    nominatim_url: str = "https://nominatim.openstreetmap.org/search"
    nominatim_user_agent: str = "RoadWatch/1.0"

    # ── H3 Spatial ─────────────────────────────────────────────
    h3_resolution: int = Field(default=9, ge=0, le=15)
    h3_k_ring_distance: int = Field(default=1, ge=1, le=5)

    # ── Session Store ──────────────────────────────────────────
    session_ttl_minutes: int = Field(default=30, ge=1)

    # ── CORS ───────────────────────────────────────────────────
    frontend_url: str = "http://localhost:5173"

    # ── Server ─────────────────────────────────────────────────
    host: str = "0.0.0.0"
    port: int = 8000

    # ── Validators ─────────────────────────────────────────────
    @field_validator("app_env", mode="before")
    @classmethod
    def lower_case_env(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("groq_api_key", mode="before")
    @classmethod
    def strip_key(cls, v: str) -> str:
        return v.strip()

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached accessor — import and call this everywhere."""
    return Settings()