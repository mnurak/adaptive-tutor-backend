from pydantic import BaseModel, Field

class ProgressBase(BaseModel):
    mastery_level: int = Field(..., ge=0, le=100)

class ProgressCreate(ProgressBase):
    concept_id: int

class ProgressUpdate(ProgressBase):
    pass

class Progress(ProgressBase):
    id: int
    user_id: int
    concept_id: int

    class Config:
        from_attributes = True

class ConceptProgress(BaseModel):
    concept: str
    concept_id: int
    mastery_level: int