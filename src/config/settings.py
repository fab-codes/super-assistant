from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

class GeminiConfig:
    API_KEY = os.getenv("GOOGLE_API_KEY")
    MODEL_ID = os.getenv("GOOGLE_MODEL_ID", "gemini-2.5-flash")

class AppConfig:
    API_KEY = os.getenv("API_KEY")
    TIMEZONE = os.getenv("TIMEZONE")
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
def validate_config():
    missing = []
    if not GeminiConfig.API_KEY:
        missing.append("GOOGLE_API_KEY")
    if not AppConfig.API_KEY:
        missing.append("API_KEY")
    if not AppConfig.TIMEZONE:
        missing.append("TIMEZONE")
    
    if missing:
        raise ValueError(f"Missing environment variables: {missing}")
    
validate_config()