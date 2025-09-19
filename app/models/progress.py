from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    mastery_level = Column(Integer, default=0) # Scale of 0-100

    user = relationship("User", back_populates="progress")
    concept = relationship("Concept")

    __table_args__ = (UniqueConstraint('user_id', 'concept_id', name='_user_concept_uc'),)