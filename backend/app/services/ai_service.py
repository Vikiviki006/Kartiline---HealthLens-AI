"""
AI Service — provider-agnostic health analysis using Gemini or OpenAI.

Prompt templates are loaded from constants. Structured JSON output is parsed
and validated. Retries and timeout handling are built-in.
"""

import json
import time
from typing import Any

import httpx

from app.core.config import settings
from app.core.exceptions import AIServiceException, AITimeoutException
from app.utils.logger import logger

# ── Prompt templates ──────────────────────────────────────────────────────────

_ANALYSIS_PROMPT = """
You are a board-certified medical AI assistant. Analyze the following extracted medical report text and return a valid JSON object only (no markdown, no extra text).

Medical Report Text:
---
{report_text}
---

Return JSON with exactly this structure:
{{
  "health_summary": "A patient-friendly plain-English summary (2-4 sentences)",
  "abnormal_markers": [
    {{
      "name": "marker name",
      "value": "patient's value",
      "unit": "unit",
      "reference_range": "normal range",
      "severity": "borderline|abnormal|critical",
      "explanation": "simple explanation for the patient"
    }}
  ],
  "recommendations": [
    {{
      "category": "diet|lifestyle|medication|followup",
      "recommendation": "specific, actionable recommendation"
    }}
  ],
  "doctor_questions": [
    "Question 1 the patient should ask their doctor",
    "Question 2",
    "Question 3"
  ],
  "overall_risk": "low|moderate|high"
}}
"""

_TREND_PROMPT = """
You are a medical AI assistant. Given the following series of values for the health marker '{marker_name}' across multiple dates, identify the trend and provide a brief analysis.

Data points (date → value):
{data_points}

Return JSON only:
{{
  "trend": "improving|stable|worsening|fluctuating",
  "analysis": "Brief plain-English trend analysis",
  "recommendation": "Action recommendation based on trend"
}}
"""


# ── Provider clients ──────────────────────────────────────────────────────────

def _call_gemini(prompt: str) -> str:
    """Call Google Gemini API and return raw text response."""
    import google.generativeai as genai

    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel(settings.GEMINI_MODEL)
    response = model.generate_content(prompt)
    return response.text


def _call_openai(prompt: str) -> str:
    """Call OpenAI Chat Completions API and return raw text response."""
    from openai import OpenAI

    client = OpenAI(api_key=settings.OPENAI_API_KEY, timeout=settings.AI_REQUEST_TIMEOUT)
    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


# ── AI Service ────────────────────────────────────────────────────────────────

class AIService:
    """Orchestrates AI calls with retry logic and JSON parsing."""

    def _call_provider(self, prompt: str) -> str:
        provider = settings.AI_PROVIDER
        if provider == "gemini":
            return _call_gemini(prompt)
        elif provider == "openai":
            return _call_openai(prompt)
        raise AIServiceException(f"Unknown AI provider: {provider}")

    def _call_with_retry(self, prompt: str) -> str:
        """Call the AI provider with exponential backoff retries."""
        last_exc: Exception | None = None
        for attempt in range(1, settings.AI_MAX_RETRIES + 1):
            try:
                logger.info(
                    f"AI call attempt {attempt}/{settings.AI_MAX_RETRIES} "
                    f"[provider={settings.AI_PROVIDER}]"
                )
                return self._call_provider(prompt)
            except httpx.TimeoutException:
                raise AITimeoutException()
            except Exception as exc:
                last_exc = exc
                wait = 2 ** attempt
                logger.warning(f"AI call failed (attempt {attempt}): {exc}. Retrying in {wait}s…")
                time.sleep(wait)
        raise AIServiceException(str(last_exc))

    @staticmethod
    def _parse_json(raw: str) -> dict[str, Any]:
        """Extract and parse JSON from AI raw response."""
        # Strip markdown code blocks if present
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            cleaned = "\n".join(lines[1:-1])
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise AIServiceException(f"Failed to parse AI JSON response: {exc}") from exc

    def analyze_report(self, report_text: str) -> dict[str, Any]:
        """
        Run full health analysis on extracted OCR text.

        Returns:
            Parsed structured dict with summary, abnormal markers,
            recommendations, and doctor questions.
        """
        start = time.monotonic()
        prompt = _ANALYSIS_PROMPT.format(report_text=report_text[:8000])  # trim to fit context
        raw = self._call_with_retry(prompt)
        elapsed_ms = int((time.monotonic() - start) * 1000)
        result = self._parse_json(raw)
        result["processing_time_ms"] = elapsed_ms
        result["ai_provider"] = settings.AI_PROVIDER
        result["model_used"] = (
            settings.GEMINI_MODEL if settings.AI_PROVIDER == "gemini" else settings.OPENAI_MODEL
        )
        logger.info(f"AI analysis complete in {elapsed_ms}ms")
        return result

    def analyze_trend(self, marker_name: str, data_points: list[dict]) -> dict[str, Any]:
        """Analyze the trend for a specific health marker over time."""
        formatted = "\n".join(f"  {dp['date']}: {dp['value']}" for dp in data_points)
        prompt = _TREND_PROMPT.format(marker_name=marker_name, data_points=formatted)
        raw = self._call_with_retry(prompt)
        return self._parse_json(raw)


# Singleton
ai_service = AIService()
