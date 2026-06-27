from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from app.database.session import get_db
from app.controllers.chat_controller import ChatController
from app.api.deps import get_current_user_id

router = APIRouter(prefix="/reports/{report_id}/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    question: str

@router.post("", summary="Ask a question about a medical report")
def ask_question(
    report_id: uuid.UUID,
    payload: ChatRequest,
    request: Request,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id)
):
    ctrl = ChatController(db)
    return ctrl.handle_question(report_id=report_id, user_id=user_id, question=payload.question)
