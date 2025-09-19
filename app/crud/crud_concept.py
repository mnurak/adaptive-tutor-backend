from app.crud.base import CRUDBase
from app.models.concept import Concept
from app.schemas.concept import ConceptCreate, ConceptCreate # Using same for update

class CRUDConcept(CRUDBase[Concept, ConceptCreate, ConceptCreate]):
    pass

concept = CRUDConcept(Concept)