from datetime import datetime
from fastapi import APIRouter, File, UploadFile
from app.models.upload import UploadResponse
from app.core.pdf_extractor import extract_text_from_pdf
from app.core.doc_store import document_store
import uuid

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)):
    """
    Upload a document (PDF or text) and return filename and character count.
    """
    # Check if the file is a PDF
    if file.filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file.file)

    else:
        # Read the file content
        content = await file.read()
        # Decode bytes to string
        text = content.decode("utf-8", errors="ignore")

    doc_id = str(uuid.uuid4())
    num_chars = len(text)
    filename = file.filename

    document = {
        "filename": filename,
        "num_chars": num_chars,
        "uploaded_at": datetime.utcnow(),
    }

    # Store the document in the document store
    document_store[doc_id] = document

    # Return the filename and number of characters
    return UploadResponse(doc_id=doc_id, filename=filename, num_chars=num_chars)
