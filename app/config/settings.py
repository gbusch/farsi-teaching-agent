"""
Application configuration and settings.
"""
import os

# Google Cloud Storage Configuration
GCS_BUCKET_NAME = "farsi-sentences"
SENTENCES_PREFIX = "sentences/"
ADMIN_PREFIX = "admin/"
ALLOWED_USERS_FILE = "allowed_users"

# AI Model Configuration
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_TEMPERATURE = 1.4
GEMINI_THINKING_BUDGET = -1
RESPONSE_MIME_TYPE = "application/json"

# Session Keys
def get_messages_key(sentence: str) -> str:
    """Generate session key for chat messages."""
    return f"messages_{sentence}"

def get_sentences_key(unit: str) -> str:
    """Generate session key for cached sentences."""
    return f"sentences_{unit}"

def get_sentence_index_key(unit: str) -> str:
    """Generate session key for selected sentence index."""
    return f"selected_sentence_index_{unit}"

# Environment Variables
def get_gemini_api_key() -> str:
    """Get Gemini API key from environment."""
    return os.environ.get("GEMINI_API_KEY", "")

def validate_environment():
    """Validate required environment variables."""
    if not get_gemini_api_key():
        raise ValueError("GEMINI_API_KEY environment variable is required")