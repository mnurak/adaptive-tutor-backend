from pydantic import BaseModel, Field
from typing import Optional, Any, List

class Neo4jConcept(BaseModel):
    """
    Represents a rich concept (Topic or Subtopic) fetched from Neo4j,
    matching the user's specific DSA graph structure.
    """
    # Core properties present in most nodes
    name: str
    id: str
    
    # Detailed properties that may or may not be present
    description: Optional[str] = None
    complexity: Optional[str] = None
    level: Optional[int] = None
    estimated_hours: Optional[int] = None
    practical_applications: Optional[List[str]] = []
    type: Optional[str] = None
    key_concepts: Optional[List[str]] = []
    
    # Custom validator to handle the Neo4j object structure
    @classmethod
    def model_validate(cls, obj: Any, **kwargs):
        # The data from the neo4j driver is a dict-like object (a Node)
        # We convert it to a standard dictionary to be safe.
        properties = dict(obj)
        return super().model_validate(properties, **kwargs)

    class Config:
        from_attributes = True