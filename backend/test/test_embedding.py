from app.core.embedder import get_embedding

chunk = "This is a test chunk for embedding."
vector = get_embedding(chunk)
print("Length of embedding vector:", len(vector))
print("First 5 elements of the embedding vector:", vector[:5])
assert isinstance(vector, list), "Embedding should be a list."
assert all(
    isinstance(x, float) for x in vector
), "All elements in the embedding vector should be floats."
