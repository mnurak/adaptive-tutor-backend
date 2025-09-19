from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.schemas.chat import ConversationRequest, ConversationResponse
from app.services.chat_service import ConversationalChainService

router = APIRouter()

@router.post("/conversation", response_model=ConversationResponse)
async def handle_conversation(
    request: ConversationRequest,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Handles a single turn in a student's conversation, providing a
    context-aware, personalized response.
    """
    chat_service = ConversationalChainService(db, current_user)
    response_content = await chat_service.generate_response(request)
    return {"generated_response": response_content}