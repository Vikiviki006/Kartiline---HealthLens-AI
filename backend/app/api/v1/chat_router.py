from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from app.database.session import get_db
from app.controllers.chat_controller import ChatController
from app.core.security import get_subject_from_token

router = APIRouter(prefix="/reports/{report_id}/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    question: str

def _get_current_user_id(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return get_subject_from_token(auth[7:])
    return "00000000-0000-0000-0000-000000000001"

@router.post("", summary="Ask a question about a medical report")
def ask_question(
    report_id: uuid.UUID,
    payload: ChatRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    user_id_str = _get_current_user_id(request)
    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        # If it's an email (demo mode), generate a consistent UUID from it
        user_id = uuid.uuid5(uuid.NAMESPACE_DNS, user_id_str)
    
    ctrl = ChatController(db)
    return ctrl.handle_question(report_id=report_id, user_id=user_id, question=payload.question)
