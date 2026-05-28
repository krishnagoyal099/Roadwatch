hey mongrels

## 1. The Contract
The backend expects your CV model to return exactly the following JSON structure when analyzing an image:
```json
{
  "defect_type": "str",
  "severity_score": "int (1-5)",
  "confidence_pct": "float"
}
```

## 2. Valid Defect Types
The system expects exactly one of the following 5 classes for the `defect_type` string:
- `Pothole`
- `Surface Crack`
- `Missing Signage`
- `Faded Lane Marking`
- `Damaged Guardrail`

## 3. Integration Options
You have two ways to integrate your YOLOv8/RDD2022 model into the backend:
- **Option A (In-app update):** Update `app/services/cv_service.py` -> `_real_analysis()` to call your hosted Roboflow/YOLO endpoint directly. If you do this, tell me and make sure to set `CV_USE_MOCK=false` in the `.env` file.
- **Option B (Standalone API):** Deploy your own standalone FastAPI server with a `/analyse-image` endpoint. Give me the URL, and I will set it as `CV_SERVICE_URL` in the `.env` file.

## 4. Image Handling
The frontend sends the image as an `image_base64` string, which includes the data URI prefix (e.g., `data:image/jpeg;base64,...`). My `cv_service` will pass this exact string directly to you. You must handle the stripping of the data URI prefix and base64 decoding on your end before passing it to your model.

## 5. Severity Logic
Remember that the severity score (1-5) must be derived from the bounding box area and detection confidence. Ensure your pipeline calculates and returns this integer!
