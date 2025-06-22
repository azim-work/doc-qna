from fastapi import APIRouter, File, UploadFile
from app.models.upload import UploadResponse
from app.core.pdf_extractor import extract_text_from_pdf

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)):
    """
    Upload a document (PDF or text) and return filename and character count.
    """
    text = ""
    # Check if the file is a PDF
    if file.filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file.file)

    else:
        # Read the file content
        content = await file.read()
        # Decode bytes to string
        text = content.decode("utf-8", errors="ignore")

    # Return the filename and number of characters
    return UploadResponse(filename=file.filename, num_chars=len(text))
