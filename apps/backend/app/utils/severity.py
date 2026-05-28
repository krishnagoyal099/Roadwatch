"""
RoadWatch — Severity Utilities
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class SeverityInfo(BaseModel):
    label: str
    colour: str


SEVERITY_MAP: dict[int, SeverityInfo] = {
    1: SeverityInfo(label="Low",      colour="#22c55e"),
    2: SeverityInfo(label="Minor",    colour="#84cc16"),
    3: SeverityInfo(label="Moderate", colour="#f59e0b"),
    4: SeverityInfo(label="Major",    colour="#f97316"),
    5: SeverityInfo(label="Critical", colour="#ef4444"),
}


def get_severity_info(score: int) -> SeverityInfo:
    return SEVERITY_MAP.get(score, SeverityInfo(label="Unknown", colour="#9ca3af"))


def compute_quality_label(avg_severity: Optional[float], open_complaints: int) -> str:
    if avg_severity is None and open_complaints == 0:
        return "Good"
    if open_complaints > 5 or (avg_severity is not None and avg_severity > 3.5):
        return "Critical"
    if avg_severity is not None and avg_severity < 2 and open_complaints < 3:
        return "Good"
    return "Deteriorating"
