# RoadWatch API Flow

The RoadWatch API is built with FastAPI and follows a modular router structure. The core interaction happens through a conversational interface (Chatbot) that orchestrates other services.

## Base URL
All API routes are prefixed with `/api`.

## 1. Chatbot API
The core entry point for citizen interactions.

### `POST /api/chat`
Handles natural language queries, image uploads for defects, and intent classification.

**Request Payload:**
```json
{
  "session_id": "uuid-string",
  "message": "There is a massive pothole here",
  "image_base64": "data:image/jpeg;base64,...", // Optional
  "lat": 22.5726, // Optional
  "lng": 88.3639  // Optional
}
```

**Flow:**
1. **Context Update**: Saves the user's location and any uploaded image to the current session.
2. **Intent Classification**: Uses LLM (Groq) to classify the intent (`report_defect`, `query_spending`, `check_quality`). If an image is attached, it forces `report_defect`.
3. **Routing**:
   - **Defects**: Forwards base64 image to the ML microservice for YOLOv8 inference. Saves the `Complaint` to Supabase.
   - **Spending/Quality**: Queries Supabase via H3 spatial indices to fetch regional road data.
4. **Response**: Returns a natural language reply and an optional `TicketConfirmation` object to render a UI card.

## 2. ML Microservice
A standalone FastAPI service running on port 8001 dedicated to heavy ML inference.

### `POST /analyse-image`
Runs YOLOv8 object detection on a road image.

**Request Payload:**
```json
{
  "image_base64": "data:image/jpeg;base64,..."
}
```
**Response:**
Returns `defect_type`, `severity_score` (1-5), and `confidence_pct`.
