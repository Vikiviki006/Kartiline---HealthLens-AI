from fastapi import APIRouter, UploadFile, File, HTTPException
from ocr.pdf_parser import extract_text_from_pdf
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_report(file: UploadFile = File(...)):

    try:
        # Validate file type
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported currently."
            )

        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Extract text from PDF
        extracted_text = extract_text_from_pdf(file_path)

        return {
            "success": True,
            "filename": file.filename,
            "file_path": file_path,
            "extracted_text": extracted_text
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )