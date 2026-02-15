"""
Configuration module for the Todo List API.
Loads environment variables and provides configuration settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Server Configuration
    PORT: int = int(os.getenv("PORT", "8000"))

    # OpenAI/OpenRouter Configuration (Phase III - AI Chatbot)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("baseURL", "")
    OPENAI_MODEL: str = os.getenv("model", "gpt-4o-mini")

    # Chatbot Session Configuration
    CHATBOT_SESSION_TTL: int = int(os.getenv("CHATBOT_SESSION_TTL", "1800"))  # 30 minutes
    CHATBOT_MAX_CONTEXT_MESSAGES: int = int(os.getenv("CHATBOT_MAX_CONTEXT_MESSAGES", "10"))
    CHATBOT_INTENT_CONFIDENCE_THRESHOLD: float = float(os.getenv("CHATBOT_INTENT_CONFIDENCE_THRESHOLD", "0.7"))

    @property
    def openai_configured(self) -> bool:
        """Check if OpenAI/OpenRouter API key is configured."""
        api_key = self.OPENROUTER_API_KEY or self.OPENAI_API_KEY
        return bool(api_key and api_key not in ["your-openai-api-key-here", ""])

    @property
    def api_key(self) -> str:
        """Get the appropriate API key (OpenRouter or OpenAI)."""
        return self.OPENROUTER_API_KEY or self.OPENAI_API_KEY


# Create a global settings instance
settings = Settings()
