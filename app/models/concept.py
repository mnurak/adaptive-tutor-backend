from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

concept_prerequisite_association = Table(
    "concept_prerequisite",
    Base.metadata,
    Column("concept_id", Integer, ForeignKey("concepts.id"), primary_key=True),
    Column("prerequisite_id", Integer, ForeignKey("concepts.id"), primary_key=True),
)

class Concept(Base):
    __tablename__ = "concepts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, unique=True)
    description = Column(String)

    prerequisites = relationship(
        "Concept",
        secondary=concept_prerequisite_association,
        primaryjoin=id == concept_prerequisite_association.c.concept_id,
        secondaryjoin=id == concept_prerequisite_association.c.prerequisite_id,
        backref="required_for"
    )