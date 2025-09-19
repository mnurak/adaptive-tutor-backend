# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Adaptive Tutoring System"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str
    
    GORQ_API_KEY: str
    GORQ_API_BASE_URL: str

    # Add these Neo4j settings
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str

    class Config:
        env_file = ".env"

settings = Settings()