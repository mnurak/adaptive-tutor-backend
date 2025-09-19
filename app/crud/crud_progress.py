from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.crud.base import CRUDBase
from app.models.progress import Progress
from app.schemas.progress import ProgressCreate, ProgressUpdate

class CRUDProgress(CRUDBase[Progress, ProgressCreate, ProgressUpdate]):
    async def get_by_user_and_concept(
        self, db: AsyncSession, *, user_id: int, concept_id: int
    ) -> Progress | None:
        result = await db.execute(
            select(Progress).filter(
                and_(Progress.user_id == user_id, Progress.concept_id == concept_id)
            )
        )
        return result.scalars().first()

progress = CRUDProgress(Progress)