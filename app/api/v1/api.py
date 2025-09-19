# app/api/v1/api.py

from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, concepts, instructions, chat 

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/login", tags=["Authentication"])
api_router.include_router(users.router, prefix="/student", tags=["Student"])
api_router.include_router(concepts.router, prefix="/concept", tags=["Knowledge Graph"])
api_router.include_router(instructions.router, prefix="/instruction", tags=["Tutoring"])
api_router.include_router(chat.router, prefix="/chat", tags=["Conversational Chat"]) 