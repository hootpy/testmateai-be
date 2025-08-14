from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.depends.get_session import get_session
from app.core.depends.get_current_user import get_current_user
from app.crud.user import UserCrud
from app.model.model import User
from app.schema.user import UserGet, UserUpdateName

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/me", response_model=UserGet)
async def get_user_detail(current_user: User = Depends(get_current_user)) -> User:
    """
    Get current user's detail
    """
    return current_user


@router.patch("/me", response_model=UserGet)
async def change_user_name(
    payload: UserUpdateName, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)
) -> User:
    """
    Update current user's name
    """
    user = await UserCrud.update_user_name(db, current_user.id, payload.name)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
