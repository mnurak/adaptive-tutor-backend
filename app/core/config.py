from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # --- Application Settings ---
    PROJECT_NAME: str = "Adaptive Tutoring System"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- PostgreSQL Connection String ---
    # This is the primary variable the application code uses.
    DATABASE_URL: str

    # --- Variables for Docker Compose ---
    # These are needed so Pydantic doesn't raise an error.
    # The application itself doesn't use them directly.
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    
    # --- Neo4j Settings ---
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str

    # --- Groq API Key ---
    GORQ_API_KEY: str

    class Config:
        env_file = ".env"
        # This allows extra variables in the .env that are not defined in the model
        extra = "ignore" 

settings = Settings()