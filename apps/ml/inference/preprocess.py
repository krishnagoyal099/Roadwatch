"""
RoadWatch — Image Preprocessor
Decodes base64 image string to PIL Image.
"""
from __future__ import annotations
import base64
import io
from PIL import Image


def decode_base64_image(image_base64: str) -> Image.Image:
    """
    Decode a base64 string (with or without data URI prefix) to PIL Image.
    """
    if "," in image_base64:
        image_base64 = image_base64.split(",", 1)[1]
    image_bytes = base64.b64decode(image_base64)
    return Image.open(io.BytesIO(image_bytes)).convert("RGB")