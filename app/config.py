import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env if present (without overwriting existing system environment variables)
load_dotenv(dotenv_path=BASE_DIR / ".env", override=False)

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DEFAULT_DB_PATH = DATA_DIR / "kaamsaathi.db"

class Settings:
    PROJECT_NAME: str = "KaamSaathi AI"
    VERSION: str = "1.0.0"
    
    # Centralized single Gemini model configuration
    # Default is strictly gemini-3.8-flash as required
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    
    # Environment and test controls
    @property
    def ENVIRONMENT(self) -> str:
        return os.getenv("ENVIRONMENT", "production")

    @property
    def ALLOW_TEST_SESSION_HEADER(self) -> bool:
        return os.getenv("ALLOW_TEST_SESSION_HEADER", "false").lower() in ("true", "1")
    
    # Session cookie configuration for safe user isolation
    SESSION_COOKIE_NAME: str = "kaamsaathi_session"
    
    # Maximum upload size in bytes (5 MB limit)
    MAX_UPLOAD_BYTES: int = 5 * 1024 * 1024
    
    # Upstream AI timeout (in milliseconds for Google GenAI SDK) and rate limit settings
    AI_TIMEOUT_MS: int = int(os.getenv("AI_TIMEOUT_MS", "30000"))
    AI_RATE_LIMIT_PER_MINUTE: int = int(os.getenv("AI_RATE_LIMIT_PER_MINUTE", "20"))

    @property
    def DB_PATH(self) -> Path:
        custom_path = os.getenv("DATABASE_PATH")
        if custom_path:
            return Path(custom_path)
        return DEFAULT_DB_PATH

    @classmethod
    def get_api_key(cls) -> str | None:
        """Reads Gemini API key strictly from environment variables without writing secrets to disk."""
        key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if key:
            key = key.strip()
            # Basic sanity check
            if len(key) > 5 and not key.startswith("your_"):
                return key
        return None

settings = Settings()
