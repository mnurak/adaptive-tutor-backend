from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core import security
from app.crud.crud_user import user as crud_user
from app.schemas.user import UserCreate, User
from app.schemas.token import Token

router = APIRouter()

@router.post("/register", response_model=User)
async def register_new_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserCreate,
) -> User:
    """
    Create a new student with their cognitive profile.
    """
    user = await crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    # Step 1: Create the user (Write operation)
    await crud_user.create(db, obj_in=user_in)
    
    # Step 2: Fetch the complete user data for the response (Read operation)
    new_user = await crud_user.get_by_email(db, email=user_in.email)
    
    return new_user

@router.post("/access-token", response_model=Token)
async def login_for_access_token(
    db: AsyncSession = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = await crud_user.get_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}