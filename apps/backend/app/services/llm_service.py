"""
RoadWatch — LLM Service
Wraps the Groq SDK for intent classification, entity extraction,
and natural language response generation.
Falls back to keyword matching when GROQ_API_KEY is not set (dev/test).
"""
from __future__ import annotations

import json
import logging
from typing import Optional

from app.core.config import get_settings
from app.models.chat import ChatContext

logger = logging.getLogger(__name__)

SYSTEM_PROMPT_CLASSIFY = """You are an AI assistant for RoadWatch, a civic road safety platform.
Your job is to classify the user's message into one of these intents:
- "report_defect": User wants to report a road issue like a pothole, crack, or damaged sign.
- "query_spending": User is asking about road budgets, contractors, or maintenance spending.
- "check_quality": User wants to know the condition or quality of a road/area.
- "unclear": The intent doesn't match the above.

Respond ONLY with a JSON object: {"intent": "one_of_the_above"}"""

SYSTEM_PROMPT_EXTRACT_LOCATION = """Extract the location or district name from the user's message.
If no specific location is mentioned, respond with null.
Respond ONLY with a JSON object: {"location": "extracted_location_or_null"}"""

SYSTEM_PROMPT_REPLY = """You are the friendly AI assistant for RoadWatch.
Generate a concise, helpful, and natural-sounding response based on the provided context.
Do not make up data. Use only the information given in the context."""

# ── Keyword fallback (used when no API key) ────────────────────
_KEYWORD_INTENTS = {
    "report_defect": ["report", "pothole", "crack", "damage", "broken", "defect", "problem", "issue"],
    "query_spending": ["spending", "budget", "money", "cost", "fund", "allocated", "contractor"],
    "check_quality": ["quality", "condition", "rating", "score", "road quality"],
}

_FALLBACK_REPLIES = {
    "report_defect": (
        "I can help you report a road defect. Please share your location (tap 📍) "
        "and upload a photo — I'll file a complaint ticket for you."
    ),
    "query_spending": (
        "You can view public road spending data on the Spending Dashboard. "
        "Would you like me to summarise the latest budget allocations?"
    ),
    "check_quality": (
        "I can pull up the latest road quality scores for your area. "
        "Please share your location or district name."
    ),
    "unclear": (
        "Hello! I'm the RoadWatch assistant. I can help you:\n"
        "• 📸 Report road defects (potholes, cracks, etc.)\n"
        "• 💰 View road spending data\n"
        "• 🛣️ Check road quality scores\n\n"
        "What would you like to do?"
    ),
}


def _keyword_classify(message: str) -> str:
    msg = message.lower()
    for intent, keywords in _KEYWORD_INTENTS.items():
        if any(kw in msg for kw in keywords):
            return intent
    return "unclear"


class LLMService:
    """Handles all interactions with the Large Language Model."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        settings = get_settings()
        key = api_key or settings.groq_api_key
        self.model = settings.groq_model
        self.max_tokens = settings.groq_max_tokens
        self.temperature = settings.groq_temperature
        self.client = None

        if key:
            try:
                from groq import Groq
                self.client = Groq(api_key=key)
                logger.info("llm_service_groq_initialized", extra={"model": self.model})
            except Exception as e:
                logger.warning("llm_groq_init_failed", extra={"error": str(e)})

    def _chat(self, system_prompt: str, user_message: str, json_mode: bool = True) -> str:
        if not self.client:
            raise RuntimeError("Groq client not initialized (no API key).")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                response_format={"type": "json_object"} if json_mode else {"type": "text"},
            )
            content = response.choices[0].message.content
            logger.debug("llm_response", extra={"prompt": system_prompt[:50], "response": content})
            return content
        except Exception as e:
            logger.exception("llm_call_failed")
            raise RuntimeError(f"LLM call failed: {e}") from e

    def classify_intent(self, message: str) -> str:
        if not self.client:
            return _keyword_classify(message)
        try:
            raw = self._chat(SYSTEM_PROMPT_CLASSIFY, message)
            data = json.loads(raw)
            intent = data.get("intent", "unclear").lower()
            valid = {"report_defect", "query_spending", "check_quality", "unclear"}
            if intent not in valid:
                logger.warning("invalid_intent_classified", extra={"raw_intent": intent})
                return "unclear"
            logger.info("intent_classified", extra={"intent": intent})
            return intent
        except (json.JSONDecodeError, KeyError, RuntimeError):
            logger.error("intent_classification_failed", exc_info=True)
            return _keyword_classify(message)

    def extract_location(self, message: str) -> Optional[str]:
        if not self.client:
            return None
        try:
            raw = self._chat(SYSTEM_PROMPT_EXTRACT_LOCATION, message)
            data = json.loads(raw)
            location = data.get("location")
            logger.info("location_extracted", extra={"location": location})
            return location
        except (json.JSONDecodeError, KeyError, RuntimeError):
            logger.error("location_extraction_failed", exc_info=True)
            return None

    def generate_reply(self, intent: str, message: str, context: Optional[str] = None) -> str:
        """Backwards-compatible single reply generator (used by chatbot router)."""
        if not self.client:
            return _FALLBACK_REPLIES.get(intent, _FALLBACK_REPLIES["unclear"])
        prompt = f"The citizen said: '{message}'\nIntent: {intent}\n"
        if context:
            prompt += f"Context: {context}\n"
        prompt += "Generate a short, helpful reply."
        try:
            return self._chat(SYSTEM_PROMPT_REPLY, prompt, json_mode=False)
        except RuntimeError:
            return _FALLBACK_REPLIES.get(intent, _FALLBACK_REPLIES["unclear"])

    def generate_defect_confirmation(self, ctx: ChatContext) -> str:
        prompt = (
            f"Context: A citizen just reported a defect.\n"
            f"Defect: {ctx.defect_type}, Severity: {ctx.severity_score}/5\n"
            f"Road: {ctx.road_name}, {ctx.district}\n"
            f"Engineer: {ctx.engineer_name} ({ctx.engineer_contact})\n"
            f"Ticket: {ctx.ticket_number}\n"
            "Task: Write a brief, polite confirmation summarising these details."
        )
        return self._chat(SYSTEM_PROMPT_REPLY, prompt, json_mode=False)

    def generate_spending_summary(self, ctx: ChatContext) -> str:
        prompt = (
            f"Context: A citizen asked about road spending in {ctx.district or 'their area'}.\n"
            f"Total Budget: ₹{ctx.budget_sanctioned_lakhs} lakhs\n"
            f"Contractor: {ctx.contractor_name}\n"
            f"Last Maintenance: {ctx.last_maintenance_date or 'Unknown'}\n"
            f"Open Complaints: {ctx.open_complaints}\n"
            "Task: Write a clear, accessible summary for a regular citizen."
        )
        return self._chat(SYSTEM_PROMPT_REPLY, prompt, json_mode=False)

    def generate_quality_assessment(self, ctx: ChatContext) -> str:
        prompt = (
            f"Context: A citizen asked about road quality at {ctx.road_name or 'a location'}, {ctx.district or ''}.\n"
            f"Quality Label: {ctx.quality_label}\n"
            f"Open Complaints: {ctx.open_complaints}, Avg Severity: {ctx.average_severity}\n"
            f"Contractor: {ctx.contractor_name}\n"
            f"Last Maintenance: {ctx.last_maintenance_date or 'Unknown'}\n"
            "Task: Explain the road quality to the citizen in simple terms."
        )
        return self._chat(SYSTEM_PROMPT_REPLY, prompt, json_mode=False)

    def generate_unclear_response(self, message: str) -> str:
        if not self.client:
            return _FALLBACK_REPLIES["unclear"]
        prompt = (
            f"The citizen said: '{message}'\n"
            "Couldn't determine intent. Politely explain you can help with:\n"
            "1. Reporting a road defect\n"
            "2. Checking public spending on roads\n"
            "3. Checking road quality\n"
            "Ask them to choose one."
        )
        try:
            return self._chat(SYSTEM_PROMPT_REPLY, prompt, json_mode=False)
        except RuntimeError:
            return _FALLBACK_REPLIES["unclear"]
