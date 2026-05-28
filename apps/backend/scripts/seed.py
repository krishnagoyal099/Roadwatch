"""
RoadWatch — Database Seeder
Populates Supabase with realistic Bengaluru demo data.
Run: python scripts/seed.py
"""
from __future__ import annotations

import os
import uuid
from datetime import datetime, timedelta, timezone
from random import choice, randint

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env")

db: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── Demo Data ──────────────────────────────────────────────────

ENGINEERS = [
    {"name": "R. Kumar",   "contact": "99001-23456"},
    {"name": "A. Singh",   "contact": "99002-34567"},
    {"name": "P. Sharma",  "contact": "99003-45678"},
    {"name": "V. Rao",     "contact": "99004-56789"},
]

CONTRACTORS = ["L&T Construction", "NCC Ltd", "Dilip Buildcon", "Afcons Infrastructure"]

# (seq_id, road_name, district, road_type, h3_index, eng_idx, cont_idx, budget_lakhs, maint_days_ago)
ROAD_SEGMENTS = [
    (1, "MG Road",           "Bengaluru", "NH",       "8960145b483ffff", 0, 0, 250.0, 60),
    (2, "Brigade Road",      "Bengaluru", "SH",       "891e2659c4bffff", 1, 1, 120.0, 90),
    (3, "Church Street",     "Bengaluru", "District", "891e2659c6bffff", 2, 2,  80.0, 120),
    (4, "Residency Road",    "Bengaluru", "SH",       "891e2659c8bffff", 3, 3, 150.0,  45),
    (5, "Infantry Road",     "Bengaluru", "District", "891e2659cabffff", 0, 1,  60.0, 200),
    (6, "Cubbon Road",       "Bengaluru", "NH",       "891e2659ccbffff", 1, 0, 300.0,  30),
    (7, "Lavelle Road",      "Bengaluru", "District", "891e2659cebffff", 2, 3,  90.0, 150),
    (8, "Vittal Mallya Road","Bengaluru", "SH",       "891e2659d0bffff", 3, 2, 110.0,  80),
]

DEFECT_TYPES = ["Pothole", "Surface Crack", "Missing Signage", "Faded Lane Marking", "Damaged Guardrail"]


def _rand_coords():
    return round(12.97 + randint(0, 100) / 10000, 6), round(77.59 + randint(0, 100) / 10000, 6)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def seed_segments():
    print("Seeding road_segments...")
    for seg in ROAD_SEGMENTS:
        lat, lng = _rand_coords()
        last_maint = (_now() - timedelta(days=seg[8])).isoformat()
        row = {
            "id": str(uuid.UUID(int=seg[0])),
            "road_name": seg[1],
            "district": seg[2],
            "road_type": seg[3],
            "h3_index": seg[4],
            "executive_engineer_name": ENGINEERS[seg[5]]["name"],
            "executive_engineer_contact": ENGINEERS[seg[5]]["contact"],
            "contractor_name": CONTRACTORS[seg[6]],
            "budget_sanctioned_lakhs": seg[7],
            "last_maintenance_date": last_maint,
            "latitude": lat,
            "longitude": lng,
        }
        db.table("road_segments").upsert(row, on_conflict="id").execute()
    print(f"  ✓ {len(ROAD_SEGMENTS)} road segments")


def seed_complaints():
    print("Seeding complaints and events...")
    statuses = ["Resolved"] * 4 + ["Escalated"] * 5 + ["Filed"] * 11

    for i, status in enumerate(statuses):
        seg = ROAD_SEGMENTS[i % len(ROAD_SEGMENTS)]
        segment_id = str(uuid.UUID(int=seg[0]))
        ticket_number = f"RW-{1000 + i:04d}"
        lat, lng = _rand_coords()
        filed_at = (_now() - timedelta(days=randint(1, 30))).isoformat()

        row = {
            "id": str(uuid.uuid4()),
            "ticket_number": ticket_number,
            "road_segment_id": segment_id,
            "defect_type": choice(DEFECT_TYPES),
            "severity_score": randint(1, 5),
            "confidence_pct": round(randint(7500, 9900) / 100, 1),
            "image_url": f"https://supabase.co/storage/v1/object/public/complaint-images/mock_{i}.jpg",
            "latitude": lat,
            "longitude": lng,
            "status": status,
            "reported_by_session": "seed-script",
            "created_at": filed_at,
        }

        if status in ("Escalated", "Resolved"):
            row["escalated_at"] = (datetime.fromisoformat(filed_at) + timedelta(days=2)).isoformat()
        if status == "Resolved":
            row["resolved_at"] = (datetime.fromisoformat(filed_at) + timedelta(days=7)).isoformat()

        try:
            resp = db.table("complaints").insert(row).execute()
            cid = resp.data[0]["id"]

            events = [
                {"id": str(uuid.uuid4()), "complaint_id": cid, "event_type": "Filed",
                 "event_note": "Auto-filed via chatbot", "created_at": filed_at},
            ]
            if status in ("Escalated", "Resolved"):
                events.append({
                    "id": str(uuid.uuid4()), "complaint_id": cid, "event_type": "Escalated",
                    "event_note": "Severity high, no action in 48h", "created_at": row["escalated_at"],
                })
            if status == "Resolved":
                events.append({
                    "id": str(uuid.uuid4()), "complaint_id": cid, "event_type": "Resolved",
                    "event_note": "Defect repaired by contractor", "created_at": row["resolved_at"],
                })
            for ev in events:
                db.table("complaint_events").insert(ev).execute()

        except Exception as e:
            print(f"  ⚠ Failed {ticket_number}: {e}")

    print(f"  ✓ {len(statuses)} complaints with events")


def main():
    print("=== RoadWatch Database Seeder ===")
    seed_segments()
    seed_complaints()
    print("=== Seeding complete! ===")


if __name__ == "__main__":
    main()
