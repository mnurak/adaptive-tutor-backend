from fastapi import APIRouter, Depends, HTTPException
from neo4j import AsyncSession as Neo4jAsyncSession

from app.db.neo4j_driver import get_neo4j_session
from app.services.knowledge_graph import Neo4jKnowledgeGraphService

router = APIRouter()

# ... (existing /context, /next, and /learning-path endpoints remain the same)
@router.get("/{concept_name}/context")
async def get_concept_context(
    concept_name: str,
    neo4j_session: Neo4jAsyncSession = Depends(get_neo4j_session),
):
    kg_service = Neo4jKnowledgeGraphService(neo4j_session)
    context = await kg_service.get_learning_context(concept_name=concept_name)
    if not context:
        raise HTTPException(status_code=404, detail="Concept not found in the Knowledge Graph")
    return context

@router.get("/{concept_name}/next")
async def recommend_next_concept(
    concept_name: str,
    neo4j_session: Neo4jAsyncSession = Depends(get_neo4j_session),
):
    kg_service = Neo4jKnowledgeGraphService(neo4j_session)
    recommendations = await kg_service.recommend_next_concept(concept_name=concept_name)
    return {"recommendations": recommendations}

@router.get("/{concept_name}/learning-path")
async def get_full_learning_path(
    concept_name: str,
    neo4j_session: Neo4jAsyncSession = Depends(get_neo4j_session),
):
    kg_service = Neo4jKnowledgeGraphService(neo4j_session)
    path = await kg_service.get_learning_path(concept_name=concept_name)
    if not path:
        return {"learning_path": [], "target_concept": concept_name}
    return {"learning_path": path, "target_concept": concept_name}

# ------------------ NEW ENDPOINT ------------------
@router.get("/{concept_name}/analysis")
async def get_concept_analysis(
    concept_name: str,
    neo4j_session: Neo4jAsyncSession = Depends(get_neo4j_session),
):
    """
    Get a comprehensive analysis of a concept, including its various relationships.
    """
    kg_service = Neo4jKnowledgeGraphService(neo4j_session)
    analysis = await kg_service.get_comprehensive_analysis(concept_name=concept_name)
    if not analysis:
        raise HTTPException(status_code=404, detail="Concept not found for analysis.")
    
    return analysis