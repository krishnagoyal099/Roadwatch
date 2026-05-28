"""
RoadWatch — H3 Spatial Utilities
"""
from __future__ import annotations

import logging
from typing import Any, Optional

import h3

from app.core.config import get_settings

logger = logging.getLogger(__name__)


def lat_lng_to_h3(lat: float, lng: float, resolution: int | None = None) -> str:
    settings = get_settings()
    res = resolution or settings.h3_resolution
    h3_index = h3.latlng_to_cell(lat, lng, res)
    logger.debug("h3_conversion", extra={"lat": lat, "lng": lng, "res": res, "h3_index": h3_index})
    return h3_index


def get_k_ring(h3_index: str, k: int | None = None) -> list[str]:
    settings = get_settings()
    ring_distance = k or settings.h3_k_ring_distance
    return list(h3.grid_disk(h3_index, ring_distance))


def match_road_segment(lat: float, lng: float, supabase_client: Any) -> Optional[dict]:
    """
    Find the road segment for the given coordinates.
    1. Try exact H3 match.
    2. Expand to k-ring and return closest.
    """
    h3_index = lat_lng_to_h3(lat, lng)

    response = (
        supabase_client.table("road_segments")
        .select("*")
        .eq("h3_index", h3_index)
        .execute()
    )
    if response.data:
        logger.info("h3_exact_match", extra={"h3_index": h3_index, "segment_id": response.data[0]["id"]})
        return response.data[0]

    neighbours = [n for n in get_k_ring(h3_index) if n != h3_index]
    if not neighbours:
        return None

    response = (
        supabase_client.table("road_segments")
        .select("*")
        .in_("h3_index", neighbours)
        .execute()
    )
    if not response.data:
        logger.info("h3_no_segment_found", extra={"h3_index": h3_index})
        return None

    closest_segment = min(
        response.data,
        key=lambda seg: h3.grid_distance(h3_index, seg["h3_index"])
    )
    logger.info("h3_k_ring_match", extra={"h3_index": h3_index, "segment_id": closest_segment["id"]})
    return closest_segment
