"""
RoadWatch — Geocoding Service
Converts location text (e.g., "MG Road, Bengaluru") to lat/lng
using the OpenStreetMap Nominatim API.
"""
from __future__ import annotations

import logging
from typing import Optional

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class GeocodingService:
    """Handles forward geocoding (text → coordinates)."""

    async def geocode(self, location_text: str) -> Optional[tuple[float, float]]:
        """Convert a location string to (lat, lng). Returns None if not found."""
        settings = get_settings()
        params = {"q": location_text, "format": "json", "limit": 1}
        headers = {"User-Agent": settings.nominatim_user_agent}

        logger.info("geocoding_location", extra={"location": location_text})

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(settings.nominatim_url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()

                if not data:
                    logger.warning("geocoding_no_result", extra={"location": location_text})
                    return None

                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                logger.info("geocoding_success", extra={"location": location_text, "lat": lat, "lon": lon})
                return lat, lon

            except (httpx.HTTPStatusError, httpx.RequestError, KeyError, ValueError) as e:
                logger.error("geocoding_failed", extra={"location": location_text, "error": str(e)})
                return None
