from app.core.chunker import chunk_text
from app.core.embedder import get_embedding
from typing import List, Dict


def index_document(
    document_id: str, text: str, tokenizer, chunk_size: int = 300
) -> List[Dict]:
    """
    Splits a document into chunks, generates embeddings for each chunk,
    and returns a list of indexed chunks.
    """

    # Create chunks from the text
    chunks = chunk_text(text, tokenizer, target_chunk_size=chunk_size)
    index = []

    for i, chunk in enumerate(chunks):
        # Generate the embedding for the chunk
        embedding = get_embedding(chunk)
        index.append(
            {
                "document_id": document_id,
                "chunk_id": i,
                "text": chunk,
                "embedding": embedding,
            }
        )

    return index
