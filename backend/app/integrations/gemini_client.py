"""
Gemini AI client wrapper (thin integration layer).
Detailed logic stays in ai_service.py.
"""

from app.core.config import settings
from app.utils.logger import logger


def get_gemini_client():
    """Return a configured Gemini GenerativeModel instance."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        return genai.GenerativeModel(settings.GEMINI_MODEL)
    except ImportError:
        logger.error("google-generativeai package not installed")
        raise
