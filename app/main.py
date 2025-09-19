import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_router
from app.db.session import engine
from app.db.base_class import Base
from app.db.init_db import init_db
from app.db.neo4j_driver import neo4j_driver

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles application startup and shutdown events."""
    print("--- Application Starting Up ---")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_db()
    neo4j_driver.get_driver()
    
    yield
    
    print("--- Application Shutting Down ---")
    await neo4j_driver.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    openapi_url="/api/v1/openapi.json"
)

# ----------------- FINAL CORS FIX -----------------
# This allows all origins, methods, and headers.
# It's the most open configuration possible for development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods
    allow_headers=["*"], # Allow all headers
)
# ----------------------------------------------------

app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME}!"}