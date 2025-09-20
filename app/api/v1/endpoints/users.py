from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel # Import BaseModel

from app.api import deps
from app.models.user import User
from app.schemas.user import User as UserSchema
from app.schemas.cognitive_profile import CognitiveProfileUpdate
from app.crud.crud_cognitive_profile import profile as crud_profile
# Import the new ML-based analyzer service
from app.services.cognitive_analyzer import ml_cognitive_analyzer_service

# Define the request model for the new endpoint
class AnalysisRequest(BaseModel):
    prompt: str

router = APIRouter()

@router.get("/me", response_model=UserSchema)
async def read_current_user(current_user: User = Depends(deps.get_current_user)):
    """
    Get the profile and details for the currently authenticated student.
    """
    return current_user

@router.put("/me/profile", response_model=UserSchema)
async def update_current_user_profile(
    profile_in: CognitiveProfileUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Manually update the currently authenticated student's cognitive profile.
    """
    await crud_profile.update(
        db, 
        db_obj=current_user.cognitive_profile, 
        obj_in=profile_in
    )
    await db.refresh(current_user, attribute_names=['cognitive_profile'])
    return current_user

# --- NEW ENDPOINT ---
@router.post("/me/analyze/preview", response_model=CognitiveProfileUpdate)
async def preview_prompt_analysis(
    request: AnalysisRequest,
    current_user: User = Depends(deps.get_current_user),
):
    """
    Analyzes a student's prompt and returns the inferred cognitive
    profile changes WITHOUT saving them to the database.
    """
    # Run the prompt through the ML analyzer using the user's current profile
    inferred_profile_update, confidence = ml_cognitive_analyzer_service.analyze_prompt(
        request.prompt, 
        current_profile=current_user.cognitive_profile
    )
    
    # Return the inferred changes directly
    return inferred_profile_update