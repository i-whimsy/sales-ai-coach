"""Configuration module for AI Sales Coaching System"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Sales Coaching System"
    VERSION: str = "1.0.0"
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./sales_coach.db"
    
    # API Key settings (from environment variables or .env file)
    OPENAI_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None
    CLAUDE_API_KEY: Optional[str] = None
    WHISPER_API_KEY: Optional[str] = None
    
    class Config:
        """Pydantic config"""
        env_file = ".env"
        case_sensitive = True


settings = Settings()
