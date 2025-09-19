from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create the asynchronous engine for connecting to the database
engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)

# --- CORRECTED ---
# This is the single, authoritative session factory for the entire application.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)