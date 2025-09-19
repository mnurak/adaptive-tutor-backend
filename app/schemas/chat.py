from pydantic import BaseModel
from typing import List, Dict

class ChatMessage(BaseModel):
    role: str # "user" or "assistant"
    content: str

class ConversationRequest(BaseModel):
    prompt: str
    conversation_history: List[ChatMessage] = []

class ConversationResponse(BaseModel):
    generated_response: str