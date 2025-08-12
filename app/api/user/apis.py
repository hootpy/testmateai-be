from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.depends.get_session import get_session
from app.crud.user import UserCrud
from app.model.model import User
from app.schema.user import UserGet, UserCreate

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/", response_model=list[UserGet])
async def get_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)) -> Sequence[User]:
    """
    The endpoint to get list of user
    """

    return await UserCrud.get_users(db, skip, limit)


@router.post("/", response_model=UserGet)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_session),
) -> User:
    """
    The endpoint to create a user
    """

    return await UserCrud.create_user(db, user)
