"""
Gemma 4 Service
"""
from google import genai
from app.core.config import settings

class GemmaService:
    def generate_summary(self, prompt: str) -> str:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt
        )
        return response.text.strip()

gemma_service = GemmaService()
