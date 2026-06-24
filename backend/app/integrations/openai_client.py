"""
OpenAI client wrapper (thin integration layer).
"""

from app.core.config import settings


def get_openai_client():
    """Return a configured OpenAI client."""
    try:
        from openai import OpenAI
        return OpenAI(api_key=settings.OPENAI_API_KEY, timeout=settings.AI_REQUEST_TIMEOUT)
    except ImportError:
        raise ImportError("openai package not installed")
