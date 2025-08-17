from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.depends.get_current_user import get_current_user
from app.core.depends.get_session import get_session
from app.crud.user import UserCrud
from app.crud.user_progress import UserProgressCrud
from app.model.model import User
from app.schema.user import UserDetail, UserProfileResponse, UserUpdate
from app.schema.user_progress import UserAchievementsResponse, UserActivityResponse, UserProgressResponse, UserSkills

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

    user = await UserCrud.update_user_profile(
        db, user_id=current_user.id, name=name, target_score=target_score, test_date=test_date
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


@router.get("/progress", response_model=UserProgressResponse)
async def get_user_progress(db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    """
    Get current user's progress, skills, achievements, and recent activity
    """
    # Get user skills (speaking, listening, reading, writing)
    skills_data = await UserProgressCrud.get_user_skills(db, current_user.id)
    skills = UserSkills(**skills_data)

    # Get user's total XP
    total_xp = await UserProgressCrud.get_user_total_xp(db, current_user.id)

    # Get user's achievements
    achievements = await UserProgressCrud.get_user_achievements(db, current_user.id)

    # Get user's recent activity (limit to 5 most recent activities)
    recent_activity = await UserProgressCrud.get_user_activities(db, current_user.id, limit=5)

    return UserProgressResponse(
        level=current_user.level,
        xp=current_user.xp,
        total_xp=total_xp,
        skills=skills,
        achievements=achievements,
        recent_activity=recent_activity,
    )


@router.get("/achievements", response_model=UserAchievementsResponse)
async def get_user_achievements(
    db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)
):
    """
    Get all achievements with their earned status for the current user
    """
    achievements = await UserProgressCrud.get_all_achievements(db, current_user.id)
    return UserAchievementsResponse(achievements=achievements)


@router.get("/activity", response_model=UserActivityResponse)
async def get_user_activity(
    limit: int = Query(10, gt=0, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Get current user's activity history with pagination
    """
    activities = await UserProgressCrud.get_user_activities(db, current_user.id, limit=limit, offset=offset)
    return UserActivityResponse(activities=activities)
