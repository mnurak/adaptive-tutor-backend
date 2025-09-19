from pydantic import BaseModel
from typing import Optional, Any, List

# --- SCHEMA FOR POSTGRESQL CONCEPTS ---
# This is the schema used by init_db.py to create the initial
# concepts in your relational database.
class ConceptBase(BaseModel):
    name: str
    description: Optional[str] = None

class ConceptCreate(ConceptBase):
    pass

# --- SCHEMA FOR NEO4J CONCEPTS ---
# This is the rich schema used by the knowledge graph services.
class Neo4jConcept(BaseModel):
    """
    Represents a rich concept (Topic or Subtopic) fetched from Neo4j,
    matching your specific DSA graph structure.
    """
    name: str
    id: str
    description: Optional[str] = None
    complexity: Optional[str] = None
    level: Optional[int] = None
    estimated_hours: Optional[int] = None
    practical_applications: Optional[List[str]] = []
    type: Optional[str] = None
    key_concepts: Optional[List[str]] = []
    
    @classmethod
    def model_validate(cls, obj: Any, **kwargs):
        properties = dict(obj)
        return super().model_validate(properties, **kwargs)

    class Config:
        from_attributes = True