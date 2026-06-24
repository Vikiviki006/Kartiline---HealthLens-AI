"""OCR client wrapper — thin integration layer."""

from app.core.config import settings
from app.utils.logger import logger


def get_ocr_engine_name() -> str:
    """Return the configured OCR engine name."""
    return settings.OCR_ENGINE


def is_tesseract_available() -> bool:
    """Check whether Tesseract is installed and reachable."""
    try:
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
        pytesseract.get_tesseract_version()
        return True
    except Exception as exc:
        logger.warning(f"Tesseract not available: {exc}")
        return False
