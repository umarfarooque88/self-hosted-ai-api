"""
Configuration management for Self-Hosted AI API
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""

    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Ollama settings
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "127.0.0.1")
    OLLAMA_PORT: int = int(os.getenv("OLLAMA_PORT", "11434"))
    OLLAMA_URL: str = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"

    # Model settings
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "qwen:1.8b")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "512"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))

    # ngrok settings
    NGROK_AUTH_TOKEN: Optional[str] = os.getenv("NGROK_AUTH_TOKEN")
    USE_NGROK: bool = os.getenv("USE_NGROK", "False").lower() == "true"

    # Security settings
    API_KEY: Optional[str] = os.getenv("API_KEY")
    REQUIRE_API_KEY: bool = os.getenv("REQUIRE_API_KEY", "False").lower() == "true"

    # Rate limiting
    RATE_LIMIT: str = os.getenv("RATE_LIMIT", "10/minute")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    def get_ollama_url(self) -> str:
        """Get full Ollama URL"""
        return self.OLLAMA_URL

    def is_auth_enabled(self) -> bool:
        """Check if API key authentication is enabled"""
        return self.REQUIRE_API_KEY and bool(self.API_KEY)


# Global settings instance
settings = Settings()
