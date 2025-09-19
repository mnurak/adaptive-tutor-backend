from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.crud.base import CRUDBase
from app.models.concept import Concept
from app.schemas.concept import ConceptCreate # <-- Corrected import

class CRUDConcept(CRUDBase[Concept, ConceptCreate, ConceptCreate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Concept | None:
        result = await db.execute(select(Concept).filter(Concept.name == name))
        return result.scalars().first()

concept = CRUDConcept(Concept)