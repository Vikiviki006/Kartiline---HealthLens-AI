"""
Upload router — POST /api/v1/upload
"""

from fastapi import APIRouter, Depends, File, Request, UploadFile
from sqlalchemy.orm import Session

from app.controllers.upload_controller import UploadController
from app.core.security import get_subject_from_token
from app.database.session import get_db

router = APIRouter(prefix="/upload", tags=["Upload"])


def _get_current_user_id(request: Request) -> str:
    """Extract user ID from Bearer token. Returns placeholder for unauthenticated dev mode."""
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return get_subject_from_token(auth[7:])
    # DEV ONLY: hardcoded UUID so uploads work without auth during development
    return "00000000-0000-0000-0000-000000000001"


@router.post("", summary="Upload a medical report PDF or image")
async def upload_report(
    request: Request,
    file: UploadFile = File(..., description="PDF or image medical report"),
    db: Session = Depends(get_db),
):
    """
    Upload a medical report file.

    - Validates file type (PDF / image) and size.
    - Stores the file locally (or S3 if configured).
    - Runs OCR text extraction.
    - Returns the created report record with a text preview.
    """
    import uuid
    user_id_str = _get_current_user_id(request)
    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        # If it's an email (demo mode), generate a consistent UUID from it
        user_id = uuid.uuid5(uuid.NAMESPACE_DNS, user_id_str)
    ctrl = UploadController(db)
    return await ctrl.handle_upload(file=file, user_id=user_id, request=request)
