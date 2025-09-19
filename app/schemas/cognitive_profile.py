from pydantic import BaseModel
from enum import Enum

class InstructionFlow(str, Enum):
    sequential = "sequential"
    global_ = "global"

class InputPreference(str, Enum):
    visual = "visual"
    verbal = "verbal"

class EngagementStyle(str, Enum):
    active = "active"
    reflective = "reflective"

class ConceptType(str, Enum):
    sensing = "sensing"
    intuitive = "intuitive"

class LearningAutonomy(str, Enum):
    guided = "guided"
    independent = "independent"

class MotivationType(str, Enum):
    intrinsic = "intrinsic"
    extrinsic = "extrinsic"

class FeedbackPreference(str, Enum):
    immediate = "immediate"
    delayed = "delayed"

class ComplexityTolerance(str, Enum):
    high = "high"
    low = "low"


class CognitiveProfileBase(BaseModel):
    instruction_flow: InstructionFlow = InstructionFlow.sequential
    input_preference: InputPreference = InputPreference.verbal
    engagement_style: EngagementStyle = EngagementStyle.reflective
    concept_type: ConceptType = ConceptType.intuitive
    learning_autonomy: LearningAutonomy = LearningAutonomy.guided
    motivation_type: MotivationType = MotivationType.intrinsic
    feedback_preference: FeedbackPreference = FeedbackPreference.delayed
    complexity_tolerance: ComplexityTolerance = ComplexityTolerance.high

class CognitiveProfileCreate(CognitiveProfileBase):
    pass

class CognitiveProfileUpdate(CognitiveProfileBase):
    pass

class CognitiveProfile(CognitiveProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True