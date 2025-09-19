from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.cognitive_profile import CognitiveProfileCreate, CognitiveProfile

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    cognitive_profile: CognitiveProfileCreate

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class User(BaseModel):
    id: int
    email: EmailStr
    cognitive_profile: CognitiveProfile

    class Config:
        from_attributes = True