import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.api import api_router
from app.db.session import engine
from app.db.base_class import Base
from app.db.init_db import init_db
from app.db.neo4j_driver import neo4j_driver

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """
    # Startup logic
    print("--- Application Starting Up ---")
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Optional: drop tables for a clean start
        await conn.run_sync(Base.metadata.create_all)
    await init_db()
    neo4j_driver.get_driver() # Initialize the driver
    
    yield # The application is now running
    
    # Shutdown logic
    print("--- Application Shutting Down ---")
    await neo4j_driver.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan, # Use the new lifespan manager
    openapi_url="/api/v1/openapi.json"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME}!"}

# This is a simple mock for the GORQ API for demonstration purposes
@app.post("/mock-gorq/generate", tags=["Mock"])
async def mock_gorq_api(request_body: dict):
    """A mock endpoint to simulate the GORQ LLM API."""
    await asyncio.sleep(1) # Simulate network latency
    prompt = request_body.get("prompt", "")
    return {"instruction": f"🎨 **Visually Engaging Instruction** 🎨\n\nHere is a personalized lesson based on your profile:\n\n{prompt}\n\n*This was a mock response generated for demonstration.*"}