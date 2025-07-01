import os
from dotenv import load_dotenv
import logging
import openai

# Load .env
load_dotenv()

# Get and validate the API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set.")

# Set OpenAI global client config
openai.api_key = OPENAI_API_KEY

# Configure logging globally
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
