"""
Medical Report Parser
Converts OCR output into structured JSON.
"""
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from app.core.config import settings

class MarkerSchema(BaseModel):
    name: str = Field(description="Name of the marker, e.g., Hemoglobin")
    value: float | str = Field(description="The numeric or string value")
    unit: str = Field(description="Unit of measurement, e.g., g/dL")
    reference_range: str = Field(description="Normal reference range")

class PatientSchema(BaseModel):
    name: str = Field(description="Patient's full name, if available. Defaults to Unknown.")
    age: int | None = Field(description="Patient's age, if available.")
    gender: str = Field(description="Patient's gender, if available.")

class ParserSchema(BaseModel):
    patient: PatientSchema
    markers: list[MarkerSchema]

class ParserService:
    def parse(self, text: str) -> dict:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        prompt = f"Extract patient information and medical markers from the medical report text. Return ONLY valid JSON matching the schema.\nText:\n{text[:8000]}"
        
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ParserSchema,
            ),
        )
        return json.loads(response.text.strip())

parser_service = ParserService()
