from app.core.chunker import chunk_text
import tiktoken

tokenizer = tiktoken.encoding_for_model("text-embedding-3-small")

# Example test text
text = """Paragraph 1. Some short text.

Paragraph 2. Some longer text. Sentence two. Sentence three.

Paragraph 3. Another paragraph with multiple sentences. Sentence two. Sentence three. Sentence four."""

chunks = chunk_text(text, tokenizer, target_chunk_size=300)

# Print results
for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i+1} ---")
    print(chunk)
    print(f"Tokens: {len(tokenizer.encode(chunk))}")

print(f"\nTotal chunks: {len(chunks)}")
