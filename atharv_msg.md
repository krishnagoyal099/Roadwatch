hey mongrels

## 1. Base URL & CORS
The backend runs on `http://localhost:8000` (or our Railway URL for production). CORS is fully configured to allow requests from your Vite frontend at `http://localhost:5173`.

## 2. Page 1: Chatbot (`POST /api/chat`)
**CRITICAL:** You MUST generate a UUID `session_id` on page load and persist it in React state for the duration of the conversation.

**Request Body Schema:**
```json
{
  "session_id": "string",
  "message": "string",
  "image_base64": "string | null",
  "lat": "float | null",
  "lng": "float | null"
}
```

**Response Body Schema:**
```json
{
  "session_id": "string",
  "reply": "string",
  "intent": "string | null",
  "ticket": { ...TicketConfirmation } // null unless a ticket is created
}
```

**Multi-turn Logic:**
If `ticket` is null and `reply` asks for an image or location, you must prompt the user in the UI. When sending their next message (or image/location), include the same `session_id` so the backend remembers the conversation state.

**Image Base64 Flow:**
Use the JavaScript `FileReader` API to convert the uploaded image to a base64 string. Send the entire string including the `data:image/...;base64,` prefix in the `image_base64` field.

## 3. Page 2: Dashboard (`GET /api/complaints` & `GET /api/complaints/:id`)
**List Endpoint (`GET /api/complaints`):**
- **Query Parameters:** `status` (string, optional), `defect_type` (string, optional), `limit` (integer, default 50, max 500), `offset` (integer, default 0).
- **Valid Status Strings:** "Filed", "Escalated", "Resolved"
- **Response Schema:**
```json
{
  "total": "integer",
  "complaints": [ ...ComplaintSummary ]
}
```

**Detail Endpoint (`GET /api/complaints/:id`):**
Returns the full `ComplaintDetail` object. Pay special attention to the `events` array, which contains the timeline of the complaint (e.g., Filed -> Escalated) for you to render the timeline UI.

## 4. Page 3: Spending Tracker (`GET /api/spending`)
**Query Parameters:**
- `district` (string, optional)
- `road_type` (string, optional)

**Response Schema:**
```json
{
  "total_budget_sanctioned_lakhs": "float",
  "total_road_segments": "integer",
  "total_contractors": "integer",
  "segments": [ ...SegmentSpending ]
}
```

## 5. Demo Prep Endpoint (`PATCH /api/complaints/:id/status`)
You can use this endpoint during demo prep to move complaints through their lifecycle ("Filed" -> "Escalated" -> "Resolved") to populate the dashboard and timeline.
**Request Body:**
```json
{
  "new_status": "string (Filed|Escalated|Resolved)",
  "event_note": "string | null"
}
```

## 6. TypeScript Interfaces
Copy-paste these exact interfaces into your React project to match the backend Pydantic schemas:

```typescript
// --- Chat ---
export interface ChatRequest {
  session_id: string;
  message: string;
  image_base64?: string | null;
  lat?: number | null;
  lng?: number | null;
}

export interface TicketConfirmation {
  id: string;
  ticket_number: string;
  road_segment_id?: string | null;
  defect_type: string;
  severity_score: number;
  confidence_pct: number;
  image_url?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  status: string;
  road_name?: string | null;
  district?: string | null;
  executive_engineer_name?: string | null;
  executive_engineer_contact?: string | null;
}

export interface ChatResponse {
  session_id: string;
  reply: string;
  intent?: string | null;
  ticket?: TicketConfirmation | null;
}

// --- Complaints ---
export interface ComplaintCreate {
  h3_index: string;
  defect_type: string;
  severity_score: number;
  confidence_pct: number;
  image_base64?: string | null;
  citizen_lat?: number | null;
  citizen_lng?: number | null;
  citizen_description?: string | null;
}

export interface StatusUpdate {
  new_status: 'Filed' | 'Escalated' | 'Resolved';
  event_note?: string | null;
}

export interface ComplaintSummary {
  id: string;
  ticket_number: string;
  defect_type: string;
  severity_score: number;
  road_name?: string | null;
  district?: string | null;
  assigned_engineer?: string | null;
  status: string;
  created_at?: string | null;
}

export interface ComplaintListResponse {
  total: number;
  complaints: ComplaintSummary[];
}

export interface EventTimeline {
  id: string;
  event_type: string;
  event_note?: string | null;
  created_at?: string | null;
}

export interface ComplaintDetail {
  id: string;
  ticket_number: string;
  road_segment_id?: string | null;
  defect_type: string;
  severity_score: number;
  confidence_pct: number;
  image_url?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  status: string;
  escalated_at?: string | null;
  resolved_at?: string | null;
  created_at?: string | null;
  road_name?: string | null;
  district?: string | null;
  events: EventTimeline[];
}

// --- Spending ---
export interface SegmentSpending {
  road_name?: string | null;
  road_type?: string | null;
  contractor_name?: string | null;
  budget_sanctioned_lakhs: number;
  last_maintenance_date?: string | null;
  open_complaints: number;
}

export interface SpendingResponse {
  total_budget_sanctioned_lakhs: number;
  total_road_segments: number;
  total_contractors: number;
  segments: SegmentSpending[];
}
```
