"""
Upload router — POST /api/v1/upload
"""

import uuid
from fastapi import APIRouter, Depends, File, Request, UploadFile, BackgroundTasks
from sqlalchemy.orm import Session

from app.controllers.upload_controller import UploadController
from app.database.session import get_db
from app.services.email_service import send_notification_email
from app.api.deps import get_current_user_id

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("", summary="Upload a medical report PDF or image")
async def upload_report(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF or image medical report"),
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Upload a medical report file.

    - Validates file type (PDF / image) and size.
    - Stores the file locally (or S3 if configured).
    - Runs OCR text extraction.
    - Returns the created report record with a text preview.
    """
    # We could fetch user email from DB, but for now we assume placeholder/demo
    # Let's get the email from the user via DB
    from app.models.user_model import User
    user = db.query(User).filter(User.id == user_id).first()
    user_email = user.email if user else "demo@healthlens.ai"
    
    ctrl = UploadController(db)
    response = await ctrl.handle_upload(file=file, user_id=user_id, request=request)
    
    background_tasks.add_task(
        send_notification_email, 
        user_email, 
        "Report Uploaded Successfully", 
        f"Your report '{file.filename}' has been successfully uploaded and is ready for analysis."
    )
    
    return response
