"""
RoadWatch — Image Upload Utility
"""
from __future__ import annotations

import base64
import logging
import uuid

from app.core.config import get_settings

logger = logging.getLogger(__name__)


def _strip_data_uri(base64_str: str) -> tuple[str, str]:
    if base64_str.startswith("data:"):
        header, data = base64_str.split(",", 1)
        mime_part = header.split(";")[0]
        mime_type = mime_part.split(":")[1]
        ext_map = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/gif": ".gif"}
        return data.strip(), ext_map.get(mime_type, ".jpg")
    return base64_str.strip(), ".jpg"


def upload_image(base64_str: str, ticket_number: str, supabase_client) -> str:
    settings = get_settings()
    bucket = settings.supabase_storage_bucket
    raw_data, ext = _strip_data_uri(base64_str)

    try:
        image_bytes = base64.b64decode(raw_data)
    except Exception as exc:
        raise ValueError("Invalid base64 image data") from exc

    path = f"complaints/{ticket_number}/{uuid.uuid4().hex}{ext}"
    logger.info("uploading_image", extra={"ticket": ticket_number, "path": path})

    try:
        supabase_client.storage.from_(bucket).upload(
            path=path,
            file=image_bytes,
            file_options={"content-type": f"image/{ext.lstrip('.')}", "upsert": "true"},
        )
    except Exception as exc:
        raise RuntimeError(f"Image upload failed: {exc}") from exc

    public_url = supabase_client.storage.from_(bucket).get_public_url(path)
    logger.info("image_uploaded", extra={"url": public_url})
    return public_url
