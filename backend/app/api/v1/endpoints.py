from datetime import datetime, timezone
from fastapi import HTTPException
from app.models.query import QueryRequest, QueryResponse
from fastapi import APIRouter, File, UploadFile
from app.models.upload import UploadResponse
from app.core.pdf_extractor import extract_text_from_pdf
from app.core.document_store import document_store
from app.core.indexer import index_document
from app.core.vector_index import vector_index
from app.core.retriever import search_document
from app.core.llm import generate_answer
import tiktoken
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

    document_id = str(uuid.uuid4())
    num_chars = len(text)
    filename = file.filename
    uploaded_at = datetime.now(timezone.utc).isoformat()

    document = {
        "filename": filename,
        "num_chars": num_chars,
        "uploaded_at": uploaded_at,
    }

    # Store the document in the document store
    document_store[document_id] = document

    # Index the document
    tokenizer = tiktoken.encoding_for_model("text-embedding-3-small")
    indexes = index_document(
        document_id=document_id, text=text, tokenizer=tokenizer, chunk_size=50
    )
    # Add the indexed chunks to the vector index
    vector_index.extend(indexes)

    # Return the filename and number of characters
    return UploadResponse(
        document_id=document_id,
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
    # alises for cleaner code
    question, document_id = query_request.question, query_request.document_id

    # Validate document
    document: dict = document_store.get(document_id)
    if not document:
        raise HTTPException(
            status_code=404,
            detail=f"Document with ID {document_id} not found.",
        )
    top_chunks = search_document(document_id=document_id, question=question, k=3)

    if not top_chunks:
        raise HTTPException(
            status_code=404, detail="No relevant chunks found in the document."
        )

    # Extract only the chunks' text
    chunk_texts = [chunk["text"] for chunk in top_chunks]

    # Generate answer from the LLM
    answer = generate_answer(chunks=chunk_texts, question=question)

    # Return as API response
    return QueryResponse(
        answer=answer,
        source_document_id=document_id,
        source_document_name=document["filename"],
    )
