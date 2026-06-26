from fastapi import HTTPException
from sqlalchemy.orm import Session
import uuid
from app.services.chat_service import ChatService
from app.core.exceptions import ReportNotFoundException

class ChatController:
    def __init__(self, db: Session):
        self._chat_service = ChatService(db)

    def handle_question(self, report_id: uuid.UUID, user_id: uuid.UUID, question: str) -> dict:
        try:
            answer = self._chat_service.ask_question(report_id, user_id, question)
            return {
                "report_id": str(report_id),
                "question": question,
                "answer": answer
            }
        except ReportNotFoundException as e:
            raise HTTPException(status_code=404, detail=f"Report not found: {e.report_id}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
