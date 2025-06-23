from datetime import datetime, timezone
from http.client import HTTPException
from app.models.query import QueryRequest, QueryResponse
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
    uploaded_at = datetime.now(timezone.utc).isoformat()

    document = {
        "filename": filename,
        "num_chars": num_chars,
        "uploaded_at": uploaded_at,
    }

    # Store the document in the document store
    document_store[doc_id] = document

    # Return the filename and number of characters
    return UploadResponse(
        doc_id=doc_id,
        filename=filename,
        num_chars=num_chars,
        uploaded_at=uploaded_at,
    )


@router.get("/list_documents")
def list_documents():
    """
    List all uploaded documents with their metadata.
    """
    documents = []
    for doc_id, doc in document_store.items():
        documents.append(
            {
                "doc_id": doc_id,
                "filename": doc["filename"],
                "num_chars": doc["num_chars"],
                "uploaded_at": doc["uploaded_at"],
            }
        )
    return documents


@router.post("/query", response_model=QueryResponse)
def query_document(query_request: QueryRequest):
    """
    Query a document and return an answer (MVP placeholder).
    """
    document: dict = document_store.get(query_request.document_id)
    if not document:
        # raise ValueError(f"Document with ID {query_request.document_id} not found.")
        raise HTTPException(
            status_code=404,
            detail=f"Document with ID {query_request.document_id} not found.",
        )

    answer = f'This is a placeholder answer for query "{query_request.question}" in document "{document["filename"]}".'

    return QueryResponse(
        answer=answer,
        source_document_id=query_request.document_id,
        source_document_name=document["filename"],
    )
