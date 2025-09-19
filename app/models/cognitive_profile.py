from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.schemas.cognitive_profile import (
    InstructionFlow, InputPreference, EngagementStyle, ConceptType,
    LearningAutonomy, MotivationType, FeedbackPreference, ComplexityTolerance
)

class CognitiveProfile(Base):
    __tablename__ = "cognitive_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    instruction_flow = Column(Enum(InstructionFlow), default=InstructionFlow.sequential)
    input_preference = Column(Enum(InputPreference), default=InputPreference.verbal)
    engagement_style = Column(Enum(EngagementStyle), default=EngagementStyle.reflective)
    concept_type = Column(Enum(ConceptType), default=ConceptType.intuitive)
    learning_autonomy = Column(Enum(LearningAutonomy), default=LearningAutonomy.guided)
    motivation_type = Column(Enum(MotivationType), default=MotivationType.intrinsic)
    feedback_preference = Column(Enum(FeedbackPreference), default=FeedbackPreference.delayed)
    complexity_tolerance = Column(Enum(ComplexityTolerance), default=ComplexityTolerance.high)

    user = relationship("User", back_populates="cognitive_profile")