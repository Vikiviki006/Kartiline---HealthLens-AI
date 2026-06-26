"""
Retrieval Layer (RAG)
Retrieves medical knowledge from PostgreSQL.
"""
from sqlalchemy.orm import Session
from app.models.medical_marker_model import MedicalMarker

class RetrievalService:
    def retrieve_knowledge(self, db: Session, marker_name: str) -> MedicalMarker | None:
        return db.query(MedicalMarker).filter(MedicalMarker.marker_name.ilike(f"%{marker_name}%")).first()

retrieval_service = RetrievalService()
