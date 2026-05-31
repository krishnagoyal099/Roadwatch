"""
RoadWatch — CV API Entry Point
FastAPI app exposing POST /analyse-image.
Run with: uvicorn apps.ml.api.analyse_image:app --port 8001
"""
from __future__ import annotations
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

from inference.predictor import CLASS_NAMES, predict
from inference.preprocess import decode_base64_image
from inference.severity_engine import compute_severity

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s — %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="RoadWatch CV Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyseRequest(BaseModel):
    image_base64: str


class AnalyseResponse(BaseModel):
    defect_type: str
    severity_score: int
    confidence_pct: float


@app.post("/analyse-image", response_model=AnalyseResponse)
async def analyse_image(req: AnalyseRequest) -> AnalyseResponse:
    try:
        image = decode_base64_image(req.image_base64)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid image: {exc}")

    result = predict(image)
    severity = compute_severity(
        result["box"], result["img_w"], result["img_h"], result["confidence"]
    )

    defect_type = CLASS_NAMES[result["cls_id"]]
    confidence_pct = round(result["confidence"] * 100, 2)

    logger.info(f"Detection: {defect_type}, severity={severity}, conf={confidence_pct}%")

    return AnalyseResponse(
        defect_type=defect_type,
        severity_score=severity,
        confidence_pct=confidence_pct,
    )


@app.get("/health")
def health():
    model_path = Path(__file__).parent.parent / "models" / "best.pt"
    return {"status": "ok", "model_loaded": model_path.exists()}