"""
RoadWatch — Computer Vision Service
Analyses road damage images.
Uses a mock implementation by default, or calls a real CV backend if configured.
"""
from __future__ import annotations

import logging
import random
from typing import Any

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)

MOCK_DEFECT_TYPES = ["Pothole", "Surface Crack", "Missing Signage", "Faded Lane Marking", "Damaged Guardrail"]


class CVService:
    """Handles image analysis for road defects."""

    def __init__(self) -> None:
        self.settings = get_settings()

    async def analyse(self, image_base64: str) -> dict[str, Any]:
        """
        Analyse a base64 encoded image.
        Returns: {"defect_type": str, "severity_score": int, "confidence_pct": float}
        """
        if self.settings.cv_use_mock:
            return self._mock_analysis()
        return await self._real_analysis(image_base64)

    def _mock_analysis(self) -> dict[str, Any]:
        defect = random.choice(MOCK_DEFECT_TYPES)
        severity = random.randint(2, 5)
        confidence = round(random.uniform(75.0, 98.0), 1)
        logger.info("cv_mock_analysis", extra={"defect": defect, "severity": severity})
        return {"defect_type": defect, "severity_score": severity, "confidence_pct": confidence}

    async def _real_analysis(self, image_base64: str) -> dict[str, Any]:
        cv_url = f"{self.settings.cv_service_url}/analyse-image"
        logger.info("calling_external_cv", extra={"url": cv_url})
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(cv_url, json={"image_base64": image_base64})
                response.raise_for_status()
                data = response.json()
                logger.info("cv_external_success", extra={"defect": data.get("defect_type")})
                return data
            except httpx.HTTPStatusError as e:
                logger.error("cv_service_http_error", extra={"status": e.response.status_code})
                raise RuntimeError(f"CV Service error: {e.response.status_code}") from e
            except httpx.RequestError as e:
                logger.error("cv_service_unreachable", extra={"error": str(e)})
                raise RuntimeError("CV Service unreachable") from e
