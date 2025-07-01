from app import config
import logging
import openai
from typing import List

DEFAULT_MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.0


def generate_answer(
    chunks: List[str], question: str, model: str = DEFAULT_MODEL
) -> str:
    """
    Generate an answer from the given context chunks and user question using an LLM.

    Args:
        chunks (List[str]): List of context chunks to use for generating the answer.
        question (str): The user's question to answer.
        model (str): The LLM model to use for generating the answer (default: DEFAULT_MODEL).
    """

    # Join the chunks into a single context string with "---" as a separator
    context = "\n---\n".join(chunks)

    # System prompt for grounding
    system_prompt = (
        "You are a helpful assistant that answers questions based only on the provided context. "
        "If the answer cannot be found in the context, say 'I don't know'."
    )

    # User prompt with STUFFING pattern
    user_prompt = f"Context:\n{context}\n\n" f"Question: {question}\n" "Answer:"

    # Message list for ChatCompletion
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # Call OpenAI Chat API
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=TEMPERATURE,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error generating the answer: {e}")
        return "An error occurred while generating the answer."
