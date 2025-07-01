from typing import List, Dict
from app.core.embedder import get_embedding
from app.core.vector_index import vector_index


def cosine_similarity(vec1, vec2) -> float:
    """
    Compute cosine similarity between two ALREADY normalized vectors.

    Args:
        vec1 (List[float]): First vector.
        vec2 (List[float]): Second vector.

    Returns:
        float: Cosine similarity between the two vectors.
    """
    return sum(a * b for a, b in zip(vec1, vec2))


def search_document(document_id: str, question: str, k: int = 3) -> List[Dict]:
    """
    Search for the top k similar chunks in a document based on a question.

    Args:
        document_id (str): ID of the document to search.
        question (str): The question to find relevant chunks for.
        k (int): Number of top similar chunks to return.

    Returns:
        List[Dict]: List of dictionaries containing:
            - document_id: The ID of the document the chunk belongs to.
            - chunk_id: The ID of the chunk within the document.
            - text: The text of the chunk.
            - score (float): Cosine similarity score (higher is more relevant)

    """

    # Get embedding for the question
    question_embedding = get_embedding(question)

    # Filter chunks for this document
    filtered_chunks = [
        chunk for chunk in vector_index if chunk["document_id"] == document_id
    ]

    # If no chunks found for the document, return empty list
    if not filtered_chunks:
        return []

    # Compute each chunk's cosine similarity with the question
    scored_chunks = []
    for chunk in filtered_chunks:
        score = cosine_similarity(question_embedding, chunk["embedding"])
        scored_chunks.append(
            {
                "document_id": chunk["document_id"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "score": score,
            }
        )

    # Sort by scores descending
    scored_chunks.sort(key=lambda x: x["score"], reverse=True)

    # Return the top k chunks
    return scored_chunks[:k]
