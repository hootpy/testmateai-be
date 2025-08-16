from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.depends.get_current_user import get_current_user
from app.core.depends.get_session import get_session
from app.crud.user import UserCrud
from app.model.model import User
from app.schema.user import UserDetail, UserProfileResponse, UserUpdate

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/me", response_model=UserDetail)
async def get_user_detail(current_user: User = Depends(get_current_user)) -> User:
    """
    Get current user's detail
    """
    return current_user


@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user's profile
    """
    return UserProfileResponse(user=current_user)


@router.put("/profile", response_model=UserProfileResponse)
async def update_user_profile(
    payload: UserUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)
):
    """
    Update current user's profile
    """
    updated = await UserCrud.update_user_profile(
        db,
        user_id=current_user.id,
        name=payload.name,
        target_score=payload.targetScore,
        test_date=payload.testDate,
        preferences=payload.preferences,
    )

    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserProfileResponse(user=updated)


@router.patch("/me", response_model=UserDetail)
async def update_user_detail(
    payload: UserUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)
) -> User:
    """
    Update current user's profile
    """
    name = payload.name if payload.name is not None else current_user.name
    target_score = payload.targetScore if payload.targetScore is not None else current_user.target_score
    test_date = payload.testDate if payload.testDate is not None else current_user.test_date
    preferences = payload.preferences if payload.preferences is not None else current_user.preferences

    user = await UserCrud.update_user_profile(
        db, user_id=current_user.id, name=name, target_score=target_score, test_date=test_date, preferences=preferences
    )
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/account")
async def delete_user_account(db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    """
    Delete current user's account
    """
    success = await UserCrud.delete_user_account(db, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete account")

    return {"message": "Account deleted successfully"}
