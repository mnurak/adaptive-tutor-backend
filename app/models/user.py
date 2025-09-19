from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    cognitive_profile = relationship("CognitiveProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    progress = relationship("Progress", back_populates="user", cascade="all, delete-orphan")