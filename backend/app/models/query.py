from pydantic import BaseModel


class QueryRequest(BaseModel):
    document_id: str
    question: str


class QueryResponse(BaseModel):
    answer: str
    source_document_id: str
    source_document_name: str
