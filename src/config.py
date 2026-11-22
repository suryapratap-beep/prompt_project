import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env if present
load_dotenv(BASE_DIR / ".env")

# API Keys & Model configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
DEFAULT_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

DATA_PATH = BASE_DIR / "data" / "products.csv"
BENCHMARK_PATH = BASE_DIR / "data" / "test_queries.json"

def get_genai_client(api_key: str = None):
    """
    Returns a configured google-genai Client if an API key is available,
    otherwise returns None.
    """
    key = api_key or GEMINI_API_KEY
    if not key:
        return None
    try:
        from google import genai
        return genai.Client(api_key=key)
    except Exception as e:
        print(f"Warning: Could not initialize google.genai Client: {e}")
        return None
