"""
RoadWatch — YOLOv8 Predictor
Loads trained model and runs inference on a PIL image.
"""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Optional
import numpy as np
from PIL import Image
import torch


logger = logging.getLogger(__name__)

CLASS_NAMES = [
    "Pothole",
    "Surface Crack",
    "Missing Signage",
    "Faded Lane Marking",
    "Damaged Guardrail",
]

CONF_THRESHOLD = 0.25
_model = None


def load_model(weights_path: Optional[Path] = None):
    global _model
    if _model is not None:
        return _model

    from ultralytics import YOLO

    if weights_path is None:
        weights_path = Path(__file__).parent.parent / "models" / "best.pt"
    if not weights_path.exists():
        raise FileNotFoundError(f"Model weights not found at {weights_path}")

    logger.info(f"Loading YOLOv8 model from {weights_path}")
    _model = YOLO(str(weights_path))
    logger.info("YOLOv8 model loaded successfully")
    return _model


def predict(image: Image.Image) -> dict:
    """
    Run inference on a PIL image.
    Returns best detection as dict with cls_id, confidence, box.
    """
    model = load_model()
    results = model(image, conf=CONF_THRESHOLD, verbose=False)

    if not results or len(results[0].boxes) == 0:
        return {"cls_id": 1, "confidence": 0.0, "box": None,
                "img_w": image.width, "img_h": image.height}

    boxes = results[0].boxes
    best_idx = int(boxes.conf.argmax())
    cls_id = int(boxes.cls[best_idx].item())
    conf = float(boxes.conf[best_idx].item())
    box = boxes.xyxy[best_idx].cpu().numpy().tolist()

    # Prefer Pothole if detected anywhere with decent confidence
    if len(boxes) > 1:
        for i in range(len(boxes)):
            if int(boxes.cls[i].item()) == 0 and float(boxes.conf[i].item()) > 0.3:
                cls_id = 0
                conf = float(boxes.conf[i].item())
                box = boxes.xyxy[i].cpu().numpy().tolist()
                break

    if cls_id >= len(CLASS_NAMES):
        cls_id = 0

    return {
        "cls_id": cls_id,
        "confidence": conf,
        "box": box,
        "img_w": image.width,
        "img_h": image.height,
    }