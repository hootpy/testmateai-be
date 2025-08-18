from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.utils.level import calculate_level_progress
from app.core.depends.get_current_user import get_current_user
from app.core.depends.get_session import get_session
from app.crud.user import UserCrud
from app.model.model import User
from app.schema.user import AddXpRequest, AddXpResponse, ProgressResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/progress", response_model=ProgressResponse)
async def get_user_progress(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Get user's current progress and stats
    """
    # Get fresh user data from database
    user = await UserCrud.get_user_progress(db, current_user.id)
    if user is None:
        # Fallback to current_user if database query fails
        user = current_user

    # Calculate level progression
    xp_to_next_level, level_progress = calculate_level_progress(user.xp, user.level)

    return ProgressResponse(
        level=user.level,
        xp=user.xp,
        currentScore=float(user.current_score) if user.current_score is not None else 0.0,
        targetScore=float(user.target_score) if user.target_score is not None else None,
        testDate=user.test_date.isoformat() if user.test_date else None,
        hasPreviousTest=user.has_previous_test,
        lastTestScore=float(user.last_test_score) if user.last_test_score is not None else None,
        xpToNextLevel=xp_to_next_level,
        levelProgress=level_progress,
    )


@router.post("/xp/add")
async def add_xp_to_user(
    payload: AddXpRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Add XP to user account
    """
    # Validate source
    valid_sources = ["practice", "mock_test", "streak"]
    if payload.source not in valid_sources:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid source. Must be one of: {', '.join(valid_sources)}",
        )

    # Store previous values for response
    previous_level = current_user.level
    previous_xp = current_user.xp

    # Add XP to user
    updated_user = await UserCrud.add_xp_to_user(db, current_user.id, payload.amount)
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Determine if user leveled up
    leveled_up = updated_user.level > previous_level

    response_data = AddXpResponse(
        previousLevel=previous_level,
        newLevel=updated_user.level,
        previousXp=previous_xp,
        newXp=updated_user.xp,
        xpGained=payload.amount,
        leveledUp=leveled_up,
    )

    return {"success": True, "data": response_data, "message": "XP added successfully"}
