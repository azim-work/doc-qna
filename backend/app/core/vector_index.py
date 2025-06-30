from typing import Dict, List

"""
Vector index to store indexed chunks from all documents.
Each entry in the list is a dictionary containing:
- document_id: The ID of the document the chunk belongs to.
- chunk_id: The ID of the chunk within the document.
- text: The text of the chunk.
- embedding: The embedding vector for the chunk. 
"""
vector_index: List[Dict] = []
