"""
Seed script for Medical Markers Knowledge Base.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.medical_marker_model import MedicalMarker

INITIAL_MARKERS = [
    {
        "marker_name": "Hemoglobin",
        "category": "Complete Blood Count",
        "description": "Hemoglobin is the protein in red blood cells that carries oxygen.",
        "normal_description": "Normal hemoglobin levels indicate adequate oxygen transport in the body.",
        "low_meaning": "Low hemoglobin levels may indicate anemia.",
        "high_meaning": "High hemoglobin levels may indicate polycythemia or dehydration.",
        "lifestyle_recommendations": "Maintain a balanced diet rich in iron and vitamins.",
        "doctor_advice": "Consult a doctor if hemoglobin levels are persistently low or high."
    },
    {
        "marker_name": "Vitamin D",
        "category": "Vitamins",
        "description": "Vitamin D is essential for bone health and immune function.",
        "normal_description": "Normal Vitamin D levels support bone density and immune response.",
        "low_meaning": "Low Vitamin D can lead to bone weakness and increased susceptibility to infections.",
        "high_meaning": "Very high Vitamin D levels can cause toxicity, leading to hypercalcemia.",
        "lifestyle_recommendations": "Get adequate sun exposure and consume Vitamin D fortified foods.",
        "doctor_advice": "Discuss Vitamin D supplementation with your doctor if levels are low."
    }
]

def seed_medical_markers():
    db: Session = SessionLocal()
    try:
        for marker_data in INITIAL_MARKERS:
            existing = db.query(MedicalMarker).filter_by(marker_name=marker_data["marker_name"]).first()
            if not existing:
                marker = MedicalMarker(**marker_data)
                db.add(marker)
        db.commit()
        print("Medical markers seeded successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding medical markers: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_medical_markers()
