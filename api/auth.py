from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_session
from db.models import User
from schemas.auth import UserCreateResponse, TokenInfo
from utils import hash_password, verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/token/")
async def get_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> TokenInfo:

    db_user: User = (
        await session.execute(
            select(User).filter(User.email==form_data.username)
        )
    ).scalar()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email.'
        )

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid password.'
        )

    access_token = create_access_token(db_user.id)
    return TokenInfo(
        access_token=access_token
    )


@router.post("/register/")
async def create_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> UserCreateResponse:
    email = form_data.username
    password = form_data.password

    db_user: User = (
        await session.execute(
            select(User).filter(User.email == email)
        )
    ).scalar()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already exists.'
        )

    hashed_password = hash_password(password)
    new_user = User(
        email=email,
        password=hashed_password
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return UserCreateResponse(
        id=new_user.id,
        email=new_user.email
    )
