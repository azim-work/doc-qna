import openai
import os
from dotenv import load_dotenv
from fastapi import HTTPException


# Load environment variables from .env file
load_dotenv()

# Set the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Default embedding model to use
EMBEDDING_MODEL = "text-embedding-3-small"


def get_embedding(chunk: str, model: str = EMBEDDING_MODEL) -> list[float]:
    """
    Get the embedding for a text chunk using the specified model.

    Args:
        chunk (str): The text chunk to embed.
        model (str): The model to use for embedding. Default is EMBEDDING_MODEL's value.

    Returns:
        list[float]: The embedding vector for the text chunk.
    """
    if not chunk.strip():
        raise ValueError("Input chunk is empty.")

    try:
        response = openai.embeddings.create(input=chunk, model=model)
        return response.data[0].embedding
    except openai.OpenAIError:
        raise HTTPException(status_code=503, detail="Embedding API error")
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected server error")
