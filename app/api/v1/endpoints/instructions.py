from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from neo4j import AsyncSession as Neo4jAsyncSession

from app.api import deps
from app.db.neo4j_driver import get_neo4j_session
from app.models.user import User
from app.crud.crud_progress import progress as crud_progress
from app.schemas.progress import ProgressCreate, Progress as ProgressSchema
from app.services.knowledge_graph import Neo4jKnowledgeGraphService
from app.services.prompt_generator import build_llm_prompt
# FIXED: Import the new function, not the old client object
from app.services.gpt_client import generate_instruction

router = APIRouter()

# This endpoint still uses PostgreSQL to track student-specific progress
@router.post("/progress/update", response_model=ProgressSchema)
async def update_student_progress(
    progress_in: ProgressCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Update a student's mastery of a concept (stored in PostgreSQL).
    """
    progress = await crud_progress.get_by_user_and_concept(
        db, user_id=current_user.id, concept_id=progress_in.concept_id
    )
    if progress:
        updated_progress = await crud_progress.update(db, db_obj=progress, obj_in=progress_in)
        return updated_progress
    else:
        new_progress_data = progress_in.model_dump()
        new_progress_data['user_id'] = current_user.id
        new_progress = await crud_progress.create(db, obj_in=new_progress_data)
        return new_progress

# This endpoint now uses Neo4j to get context and generate instructions
@router.post("/{concept_name}/generate")
async def generate_personalized_instruction(
    concept_name: str,
    neo4j_session: Neo4jAsyncSession = Depends(get_neo4j_session),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Generates a highly personalized lesson by performing a full concept analysis,
    then building a sophisticated prompt for the LLM.
    """
    # Step 1: Perform a comprehensive analysis of the concept using the knowledge graph
    kg_service = Neo4jKnowledgeGraphService(neo4j_session)
    analysis = await kg_service.get_comprehensive_analysis(concept_name=concept_name)

    if not analysis:
        raise HTTPException(status_code=404, detail="Concept not found in Knowledge Graph")
    
    # Step 2: Build the sophisticated prompt using the analysis and the student's profile
    prompt = build_llm_prompt(user=current_user, analysis=analysis)
    
    # Step 3: Send the prompt to the LLM and get the lesson
    # FIXED: Call the new function directly
    instruction = await generate_instruction(prompt)
    
    return {"generated_instruction": instruction, "prompt_sent": prompt}