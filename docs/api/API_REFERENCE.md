# RoadWatch API Reference

**Base URL (local):** `http://localhost:8000`
**Base URL (production):** `https://roadwatch-backend.up.railway.app`

All endpoints accept and return `application/json` unless noted.

---

## Health

### `GET /health`

Liveness check for Railway / uptime monitoring.

**Response 200:**
```json
{
  "status": "ok",
  "service": "roadwatch-api"
}
```

**cURL:**
```bash
curl http://localhost:8000/health
```

---

## Chatbot

### `POST /api/chat`

Primary conversational endpoint. The frontend sends every citizen message here.
The chatbot detects intent and responds with either a clarification request or a completed ticket.

**Request Body:**
```json
{
  "session_id": "uuid-string",
  "message": "I want to report a pothole on MG Road",
  "lat": 12.9716,
  "lng": 77.5946
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `session_id` | string | No | UUID for the conversation session. Omit to start a new session. |
| `message` | string | Yes | Citizen's text message |
| `lat` | float | No | Citizen's latitude |
| `lng` | float | No | Citizen's longitude |

**Intent values returned:**

| Intent | Triggered by |
|---|---|
| `report_defect` | "pothole", "crack", "damage", "broken", "defect" |
| `check_status` | "status", "ticket", "TCK-", "update" |
| `spending_query` | "spending", "budget", "money", "cost" |
| `quality_query` | "quality", "condition", "rating", "score" |
| `general` | Anything else |

**Response 200 (ticket filed):**
```json
{
  "session_id": "uuid-string",
  "reply": "I've filed your complaint. Here are the details:\n• Defect: Pothole\n• Severity: 4/5\n• Confidence: 92%\n• Ticket: TCK-42701",
  "intent": "report_defect",
  "ticket_number": "TCK-42701"
}
```

**Response 200 (needs more info):**
```json
{
  "session_id": "uuid-string",
  "reply": "I can help you report a road defect. Please share your location (tap the 📍 button) and upload a photo of the issue, and I'll file a complaint ticket for you.",
  "intent": "report_defect",
  "ticket_number": null
}
```

**cURL:**
```bash
# PowerShell — use curl.exe and a body file
echo '{"session_id":"test-001","message":"I want to report a pothole"}' | Out-File -Encoding utf8 body.json
curl.exe -s -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d "@body.json"

# Linux/macOS
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test-001","message":"I want to report a pothole","lat":12.9716,"lng":77.5946}'
```

---

### `POST /api/analyse-image`

Analyse a road damage image using the CV service (mock in dev, YOLO in prod).
Called internally by the chatbot, but also directly callable.

**Request Body:**
```json
{
  "session_id": "uuid-string",
  "image_base64": "/9j/4AAQSkZJRgAB..."
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `session_id` | string | No | Conversation session to attach result to |
| `image_base64` | string | Yes | Raw base64-encoded image (no data URI prefix) |

**Response 200:**
```json
{
  "session_id": "uuid-string",
  "defect_type": "Pothole",
  "severity_score": 4,
  "confidence_pct": 87.5,
  "message": "Detected a **Pothole** with severity 4/5 (87.5% confidence). Please confirm your location to file a complaint."
}
```

**Severity scale:**

| Score | Meaning |
|---|---|
| 1 | Minor — cosmetic only |
| 2 | Low — monitor |
| 3 | Moderate — schedule repair |
| 4 | High — urgent repair |
| 5 | Critical — immediate action |

**cURL:**
```bash
# Linux/macOS — encode a real image file
IMAGE_B64=$(base64 -i pothole.jpg)
curl -X POST http://localhost:8000/api/analyse-image \
  -H "Content-Type: application/json" \
  -d "{\"image_base64\": \"$IMAGE_B64\"}"

# PowerShell
$b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes("pothole.jpg"))
echo "{`"image_base64`":`"$b64`"}" | Out-File -Encoding utf8 img.json
curl.exe -s -X POST http://localhost:8000/api/analyse-image -H "Content-Type: application/json" -d "@img.json"
```

---

## Complaints

### `POST /api/complaints`

File a new road defect complaint. Usually called by the chatbot handler after CV analysis.

**Request Body:**
```json
{
  "road_segment_id": "uuid",
  "defect_type": "Pothole",
  "severity_score": 4,
  "confidence_pct": 87.5,
  "image_url": "https://supabase.co/storage/v1/.../RW-0042.jpg",
  "latitude": 12.9716,
  "longitude": 77.5946,
  "reported_by_session": "uuid-string"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `defect_type` | string | Yes | One of: `Pothole`, `Cracks`, `Water Logging`, `Broken Streetlight`, `Faded Markings` |
| `severity_score` | int | Yes | 1–5 |
| `confidence_pct` | float | Yes | 0–100 |
| `latitude` | float | Yes | Location of defect |
| `longitude` | float | Yes | Location of defect |
| `reported_by_session` | string | Yes | Session UUID of reporter |
| `road_segment_id` | string | No | Matched road segment UUID |
| `image_url` | string | No | Public URL of uploaded image |

**Response 201:**
```json
{
  "id": "uuid",
  "ticket_number": "TCK-42701",
  "road_segment_id": "uuid",
  "defect_type": "Pothole",
  "severity_score": 4,
  "confidence_pct": 87.5,
  "image_url": "https://supabase.co/storage/v1/.../RW-0042.jpg",
  "latitude": 12.9716,
  "longitude": 77.5946,
  "status": "Filed",
  "reported_by_session": "uuid-string",
  "escalated_at": null,
  "resolved_at": null,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**cURL:**
```bash
curl -X POST http://localhost:8000/api/complaints \
  -H "Content-Type: application/json" \
  -d '{
    "defect_type": "Pothole",
    "severity_score": 4,
    "confidence_pct": 87.5,
    "latitude": 12.9716,
    "longitude": 77.5946,
    "reported_by_session": "test-session-001"
  }'
```

---

### `GET /api/complaints`

List all complaints with optional filters and pagination.

**Query Parameters:**

| Param | Type | Default | Description |
|---|---|---|---|
| `status` | string | — | `Filed`, `Under Review`, `In Progress`, `Resolved`, `Rejected` |
| `district` | string | — | Filter by district name |

**Response 200:**
```json
{
  "data": [
    {
      "id": "uuid",
      "ticket_number": "TCK-42701",
      "defect_type": "Pothole",
      "severity_score": 4,
      "confidence_pct": 87.5,
      "status": "Filed",
      "latitude": 12.9716,
      "longitude": 77.5946,
      "reported_by_session": "uuid",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "count": 1
}
```

**cURL:**
```bash
# All complaints
curl http://localhost:8000/api/complaints

# Filter by status
curl "http://localhost:8000/api/complaints?status=Filed"

# Filter by district
curl "http://localhost:8000/api/complaints?district=Central+Delhi"
```

---

### `GET /api/complaints/{id}`

Get a single complaint by UUID.

**Response 200:** Same shape as one item in `GET /api/complaints`.

**Response 404:**
```json
{ "detail": "Complaint not found." }
```

**cURL:**
```bash
curl http://localhost:8000/api/complaints/some-uuid-here
```

---

### `PATCH /api/complaints/{id}/status`

Update the status of a complaint. Setting `In Progress` automatically sets `escalated_at`;
`Resolved` sets `resolved_at`.

**Request Body:**
```json
{ "status": "In Progress" }
```

**Valid status transitions:**

```
Filed → Under Review → In Progress → Resolved
Filed → Rejected
```

**Response 200:** Updated complaint object.

**cURL:**
```bash
curl -X PATCH http://localhost:8000/api/complaints/some-uuid/status \
  -H "Content-Type: application/json" \
  -d '{"status": "In Progress"}'
```

---

## Spending

### `GET /api/spending`

Return road segment budget allocations with open complaint counts attached.

**Query Parameters:**

| Param | Type | Description |
|---|---|---|
| `district` | string | Filter by district name |
| `road_type` | string | `Arterial`, `Collector`, `Local`, `Highway` |

**Response 200:**
```json
{
  "data": [
    {
      "road_segment_id": "uuid",
      "road_name": "MG Road",
      "district": "Central Delhi",
      "road_type": "Arterial",
      "budget_sanctioned_lakhs": 250.0,
      "open_complaints": 3,
      "last_maintenance_date": "2024-03-01T00:00:00Z"
    }
  ],
  "total_budget_lakhs": 250.0,
  "count": 1
}
```

**cURL:**
```bash
curl http://localhost:8000/api/spending
curl "http://localhost:8000/api/spending?district=Central+Delhi&road_type=Arterial"
```

---

## Road Quality

### `GET /api/road-quality`

Return road quality assessments derived from complaint severity scores.
Segments with no complaints are excluded.

**Query Parameters:**

| Param | Type | Description |
|---|---|---|
| `district` | string | Filter by district name |

**Quality Labels:**

| Label | Condition |
|---|---|
| `Good` | avg severity ≤ 1.5 **and** open complaints < 3 |
| `Deteriorating` | avg severity ≤ 3 **or** open complaints < 5 |
| `Critical` | avg severity > 3 **and** open complaints ≥ 5 |

**Response 200:**
```json
{
  "data": [
    {
      "road_segment_id": "uuid",
      "road_name": "MG Road",
      "district": "Central Delhi",
      "h3_index": "8928308280fffff",
      "avg_severity": 3.7,
      "open_complaint_count": 6,
      "quality_label": "Critical",
      "last_complaint_date": "2024-05-01T10:00:00Z"
    }
  ],
  "count": 1
}
```

**cURL:**
```bash
curl http://localhost:8000/api/road-quality
curl "http://localhost:8000/api/road-quality?district=North+Delhi"
```

---

## Error Responses

All errors follow a consistent shape:

```json
{ "detail": "Human-readable error message", "error_id": "abc12345" }
```

| Code | Meaning |
|---|---|
| `400` | Bad request |
| `404` | Resource not found |
| `422` | Validation error (missing/invalid fields) |
| `500` | Internal server error (includes `error_id` for tracing) |

---

## Interactive Docs

When `APP_ENV=development`, Swagger UI is available at:
- **Swagger:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI JSON:** `http://localhost:8000/openapi.json`
