
CREATE TABLE road_segments (
    id UUID PRIMARY KEY,
    road_name TEXT,
    district TEXT,
    road_type TEXT,
    h3_index TEXT,
    executive_engineer_name TEXT,
    executive_engineer_contact TEXT,
    contractor_name TEXT,
    budget_sanctioned_lakhs NUMERIC,
    last_maintenance_date TIMESTAMP,
    latitude NUMERIC,
    longitude NUMERIC,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE complaints (
    id UUID PRIMARY KEY,
    ticket_number TEXT UNIQUE,
    road_segment_id UUID REFERENCES road_segments(id),
    defect_type TEXT,
    severity_score INTEGER,
    confidence_pct NUMERIC,
    image_url TEXT,
    latitude NUMERIC,
    longitude NUMERIC,
    status TEXT,
    reported_by_session TEXT,
    escalated_at TIMESTAMP,
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE complaint_events (
    id UUID PRIMARY KEY,
    complaint_id UUID REFERENCES complaints(id),
    event_type TEXT,
    event_note TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
