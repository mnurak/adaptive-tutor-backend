from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.core import security
from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.schemas.token import TokenData
from app.crud.crud_user import user as crud_user

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/api/v1/login/access-token"
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(
    # FIXED: Removed 'deps.' prefix. It's calling get_db from the same file.
    db: AsyncSession = Depends(get_db), 
    token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenData(email=payload.get("sub"))
    except (JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    query = (
        select(User)
        .options(selectinload(User.cognitive_profile))
        .filter(User.email == token_data.email)
    )
    result = await db.execute(query)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user