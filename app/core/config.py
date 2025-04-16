import os
from functools import lru_cache
from typing import List

from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    """
    Application settings.
    
    This class uses Pydantic to validate and parse environment variables.
    Default values are provided for development, but should be overridden
    in production.
    """
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Security Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_secret_key")
    
    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./pastebin.db")
    
    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    PROJECT_NAME: str = "PasteShit API"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "A simple pastebin-like API for storing and retrieving text snippets"


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings.
    
    The function is cached so that settings are loaded only once.
    
    Returns:
        Settings: Application settings
    """
    return Settings() 