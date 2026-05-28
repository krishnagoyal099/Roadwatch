"""
RoadWatch — Input Validators
"""
from __future__ import annotations

import re


def is_valid_base64_image(value: str) -> bool:
    if not value:
        return False
    if value.startswith("data:image/"):
        return True
    if len(value) < 100:
        return False
    return bool(re.match(r"^[A-Za-z0-9+/=\s]+$", value[:200]))


def sanitize_string(value: str, max_length: int = 500) -> str:
    if not value:
        return ""
    return value.strip()[:max_length]
