"""
File system helper utilities.
"""

import os
import shutil
import uuid
from pathlib import Path
from datetime import datetime

from app.core.config import settings
from app.utils.logger import logger


def ensure_upload_dir() -> Path:
    """Ensure the upload directory exists and return its Path."""
    upload_path = Path(settings.UPLOAD_DIR)
    try:
        upload_path.mkdir(parents=True, exist_ok=True)
    except OSError:
        # Fallback to /tmp directory for serverless environments (e.g., Vercel)
        upload_path = Path("/tmp") / settings.UPLOAD_DIR
        upload_path.mkdir(parents=True, exist_ok=True)
    return upload_path


def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename preserving the original extension."""
    ext = Path(original_filename).suffix.lower()
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    return f"{timestamp}_{unique_id}{ext}"


def save_upload_file(file_bytes: bytes, original_filename: str) -> str:
    """
    Persist uploaded bytes to the local upload directory.

    Returns:
        Relative file path string.
    """
    upload_dir = ensure_upload_dir()
    unique_name = generate_unique_filename(original_filename)
    file_path = upload_dir / unique_name

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    logger.info(f"File saved: {file_path}")
    return str(file_path)


def delete_file(file_path: str) -> bool:
    """Delete a file from the filesystem. Returns True on success."""
    try:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            logger.info(f"File deleted: {file_path}")
            return True
        return False
    except OSError as exc:
        logger.error(f"Failed to delete file {file_path}: {exc}")
        return False


def get_file_size(file_path: str) -> int:
    """Return the file size in bytes. Returns 0 if file doesn't exist."""
    try:
        return os.path.getsize(file_path)
    except OSError:
        return 0
