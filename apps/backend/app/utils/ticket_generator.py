"""
RoadWatch — Ticket Number Generator
Format: RW-XXXX (uniqueness enforced by DB UNIQUE constraint)
"""
from __future__ import annotations

import logging
import random

logger = logging.getLogger(__name__)


def generate_ticket_number() -> str:
    number = random.randint(1000, 9999)
    ticket = f"RW-{number}"
    logger.debug("ticket_generated", extra={"ticket": ticket})
    return ticket
