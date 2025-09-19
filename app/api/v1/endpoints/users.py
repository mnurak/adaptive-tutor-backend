from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models.user import User
from app.schemas.user import User as UserSchema
from app.schemas.cognitive_profile import CognitiveProfile, CognitiveProfileUpdate
from app.crud.base import CRUDBase
from app.models.cognitive_profile import CognitiveProfile as CognitiveProfileModel
from app.schemas.cognitive_profile import CognitiveProfile, CognitiveProfileUpdate
from app.services.cognitive_analyzer import cognitive_analyzer_service
from pydantic import BaseModel

class CognitiveAnalysisRequest(BaseModel):
    prompt: str

router = APIRouter()
crud_profile = CRUDBase(CognitiveProfileModel)

@router.get("/me", response_model=UserSchema)
def read_user_me(current_user: User = Depends(deps.get_current_user)):
    """Get current user."""
    return current_user

@router.get("/{user_id}/profile", response_model=CognitiveProfile)
async def get_student_profile(
    user_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """Get a student's cognitive profile."""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this profile")
    
    return current_user.cognitive_profile

@router.put("/{user_id}/profile", response_model=CognitiveProfile)
async def update_student_profile(
    user_id: int,
    profile_in: CognitiveProfileUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """Update a student's cognitive profile."""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this profile")
    
    profile = await crud_profile.update(db, db_obj=current_user.cognitive_profile, obj_in=profile_in)
    return profile

@router.post("/me/analyze", response_model=CognitiveProfile)
async def analyze_student_prompt(
    analysis_request: CognitiveAnalysisRequest,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Analyzes a student's prompt and updates their cognitive profile.
    """
    # 1. Analyze the prompt to get the suggested profile changes
    inferred_profile_update, confidence = cognitive_analyzer_service.analyze_prompt(
        analysis_request.prompt
    )

    if not inferred_profile_update.model_dump(exclude_unset=True):
        # If no traits were inferred, just return the current profile
        return current_user.cognitive_profile

    # 2. Get the current profile as a dictionary
    current_profile_dict = CognitiveProfile.model_validate(current_user.cognitive_profile).model_dump()
    
    # 3. Merge the inferred changes into the current profile
    # The 'exclude_unset=True' is crucial to only update fields that were detected
    update_data = inferred_profile_update.model_dump(exclude_unset=True)
    current_profile_dict.update(update_data)

    # 4. Create a final, validated update object
    final_profile_update = CognitiveProfileUpdate(**current_profile_dict)

    # 5. Save the updated profile to the database
    updated_profile = await crud_profile.update(
        db, db_obj=current_user.cognitive_profile, obj_in=final_profile_update
    )
    
    # Note: The 'confidence' score is not stored in the DB in this design,
    # but it could be returned or logged if needed.
    
    return updated_profile