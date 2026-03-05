from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""
    CLAUDE_API_KEY: str = ""
    WHISPER_API_KEY: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()