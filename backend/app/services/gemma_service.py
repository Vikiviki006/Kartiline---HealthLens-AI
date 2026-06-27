"""
Gemma 4 Service
"""
from google import genai
from app.core.config import settings

class GemmaService:
    def generate_summary(self, prompt: str) -> str:
        if not settings.GEMINI_API_KEY:
            # Return a demo response if API key is not configured
            return (
                "This is a demo response. To enable AI-powered responses, please configure "
                "your GEMINI_API_KEY in the .env file with a valid Google Generative AI API key. "
                "Your question was: " + prompt[:100]
            )
        
        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"

gemma_service = GemmaService()
