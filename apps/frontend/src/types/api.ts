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
  road_type?: string | null;
  contractor_name?: string | null;
  executive_engineer_name?: string | null;
  executive_engineer_contact?: string | null;
  budget_sanctioned?: number | null;
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