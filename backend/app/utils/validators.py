"""
File validation utilities.
"""

import os
from pathlib import Path

from app.core.config import settings
from app.core.constants import ALLOWED_MIME_TYPES
from app.core.exceptions import FileTooLargeException, InvalidFileTypeException


def validate_file_extension(filename: str) -> None:
    """Raise InvalidFileTypeException if the file extension is not allowed."""
    ext = Path(filename).suffix.lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise InvalidFileTypeException(filename)


def validate_file_size(size_bytes: int) -> None:
    """Raise FileTooLargeException if the file exceeds the configured limit."""
    if size_bytes > settings.max_upload_bytes:
        raise FileTooLargeException(settings.MAX_UPLOAD_SIZE_MB)


def sanitize_filename(filename: str) -> str:
    """Return a safe version of a filename (no path traversal)."""
    return os.path.basename(filename).replace(" ", "_")
