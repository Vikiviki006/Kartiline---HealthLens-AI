"""
OCR Service — multi-engine text extraction with fallback strategy.

Priority: pdfplumber → PyMuPDF → Tesseract (image OCR)
"""

from pathlib import Path
from typing import Optional

from app.core.config import settings
from app.core.exceptions import OCRFailedException
from app.utils.logger import logger


# ── Engine implementations ────────────────────────────────────────────────────

def _extract_with_pdfplumber(file_path: str) -> str:
    """Extract text from PDF using pdfplumber."""
    import pdfplumber

    text_parts: list[str] = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def _extract_with_pymupdf(file_path: str) -> str:
    """Extract text from PDF using PyMuPDF (fitz)."""
    import fitz  # PyMuPDF

    text_parts: list[str] = []
    with fitz.open(file_path) as doc:
        for page in doc:
            text_parts.append(page.get_text("text"))
    return "\n".join(text_parts)


def _extract_with_tesseract(file_path: str) -> str:
    """Extract text from an image file using pytesseract."""
    import pytesseract
    from PIL import Image

    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
    img = Image.open(file_path)
    return pytesseract.image_to_string(img)


# ── Public interface ──────────────────────────────────────────────────────────

class OCRService:
    """
    Extracts raw text from uploaded medical report files.
    Tries configured primary engine first, falls back if enabled.
    """

    _ENGINE_MAP = {
        "pdfplumber": _extract_with_pdfplumber,
        "pymupdf": _extract_with_pymupdf,
        "tesseract": _extract_with_tesseract,
    }
    _PDF_ENGINES = ["pdfplumber", "pymupdf"]
    _IMAGE_ENGINES = ["tesseract"]

    def extract_text(self, file_path: str) -> tuple[str, str]:
        """
        Extract text from file_path.

        Returns:
            (extracted_text, engine_used)

        Raises:
            OCRFailedException: if all engines fail.
        """
        path = Path(file_path)
        is_pdf = path.suffix.lower() == ".pdf"

        engines_to_try = self._determine_engine_order(is_pdf)
        last_error: Exception | None = None

        for engine_name in engines_to_try:
            try:
                logger.info(f"Attempting OCR with engine: {engine_name}")
                func = self._ENGINE_MAP[engine_name]
                text = func(file_path)
                if text and text.strip():
                    logger.info(
                        f"OCR succeeded with engine={engine_name}, "
                        f"chars={len(text)}"
                    )
                    return text.strip(), engine_name
                logger.warning(f"Engine {engine_name} returned empty text, trying fallback")
            except Exception as exc:
                last_error = exc
                logger.warning(f"Engine {engine_name} failed: {exc}")
                if not settings.OCR_FALLBACK_ENABLED:
                    break

        raise OCRFailedException(str(last_error) if last_error else "All OCR engines returned empty output")

    def _determine_engine_order(self, is_pdf: bool) -> list[str]:
        """Return ordered list of engines to attempt."""
        primary = settings.OCR_ENGINE
        if is_pdf:
            fallbacks = [e for e in self._PDF_ENGINES if e != primary]
        else:
            fallbacks = [e for e in self._IMAGE_ENGINES if e != primary]

        engines = [primary]
        if settings.OCR_FALLBACK_ENABLED:
            engines += fallbacks
        return engines


# Singleton
ocr_service = OCRService()
