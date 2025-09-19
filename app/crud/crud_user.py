from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload # Make sure this is imported

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from app.models.cognitive_profile import CognitiveProfile

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> User | None:
        # UPDATED: Always load the cognitive profile when getting a user by email
        result = await db.execute(
            select(User)
            .options(selectinload(User.cognitive_profile))
            .filter(User.email == email)
        )
        return result.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        # UPDATED: This function now ONLY creates the user.
        # The problematic 'db.refresh' call is removed.
        cognitive_profile_data = obj_in.cognitive_profile.model_dump()
        
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            cognitive_profile=CognitiveProfile(**cognitive_profile_data)
        )
        db.add(db_obj)
        await db.commit()
        return db_obj

user = CRUDUser(User)