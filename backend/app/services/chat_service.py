from sqlalchemy.orm import Session
import uuid
from app.repositories.report_repository import ReportRepository
from app.services.retrieval_service import retrieval_service
from app.services.gemma_service import gemma_service
from app.core.exceptions import ReportNotFoundException
from app.models.report_marker_model import ReportMarker
from app.models.medical_marker_model import MedicalMarker

class ChatService:
    def __init__(self, db: Session):
        self._db = db
        self._report_repo = ReportRepository(db)

    def ask_question(self, report_id: uuid.UUID, user_id: uuid.UUID, question: str) -> str:
        report = self._report_repo.get_by_id(report_id, user_id)
        if not report:
            raise ReportNotFoundException(str(report_id))
        
        # 1. Check with database: Fetch all markers for this report
        markers = self._db.query(ReportMarker).filter(ReportMarker.report_id == report_id).all()
        
        # 2. Retrieve document knowledge (RAG) for these markers
        knowledge_context = []
        marker_summaries = []
        for m in markers:
            marker_summaries.append(f"{m.marker_name}: {m.value} {m.unit} (Status: {m.status}, Ref: {m.reference_range})")
            k = retrieval_service.retrieve_knowledge(self._db, m.marker_name)
            if k:
                knowledge_context.append(f"Marker: {k.marker_name}\nDescription: {k.description}\nAbnormal Meaning: {k.high_meaning} / {k.low_meaning}\nAdvice: {k.doctor_advice}")

        # 3. Push to AI Model (Gemma4)
        context_str = "\n".join(knowledge_context)
        marker_str = "\n".join(marker_summaries)
        
        prompt = f"""
You are a specialized medical AI assistant. The user is asking a follow-up question about their medical report.
Do NOT invent new medical facts. Rely heavily on the provided RAG knowledge context.

--- PATIENT REPORT MARKERS ---
{marker_str}

--- MEDICAL KNOWLEDGE CONTEXT (RAG) ---
{context_str}

--- USER QUESTION ---
{question}

Answer the question professionally, directly addressing the user's data and the medical context provided above.
"""
        return gemma_service.generate_summary(prompt)

