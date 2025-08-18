from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.utils.level import calculate_level_progress
from app.common.utils.user_activity import convert_user_activity_to_response, convert_user_activity_to_submit_response
from app.common.utils.user_analytics import convert_analytics_to_response
from app.core.depends.get_current_user import get_current_user
from app.core.depends.get_session import get_session
from app.crud.user import UserCrud
from app.crud.user_activity import UserActivityCrud
from app.crud.user_analytics import UserAnalyticsCrud
from app.model.model import User
from app.schema.user import AddXpRequest, AddXpResponse, ProgressResponse
from app.schema.user_activity import SubmitActivityRequest

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


@router.post("/activities")
async def submit_practice_session(
    payload: SubmitActivityRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Submit practice session results
    """
    # Validate activity type
    valid_types = ["listening", "reading", "writing", "speaking"]
    if payload.type not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid type. Must be one of: {', '.join(valid_types)}",
        )

    # Validate practice type
    valid_practice_types = ["mockTest", "practice"]
    if payload.practiceType not in valid_practice_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid practiceType. Must be one of: {', '.join(valid_practice_types)}",
        )

    # Create user activity
    user_activity = await UserActivityCrud.create_user_activity(
        db=db,
        user_id=current_user.id,
        activity_type=payload.type,
        practice_type=payload.practiceType,
        score=payload.score,
        band=payload.band,
        details=payload.details,
        xp_earned=payload.xpEarned,
        time_spent=payload.timeSpent,
    )

    # Convert to response format
    activity_response = convert_user_activity_to_submit_response(user_activity)

    return {"success": True, "data": activity_response, "message": "Practice session submitted successfully"}


@router.get("/activities")
async def get_user_activities(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
):
    """
    Get user's activities
    """
    # Get user activities
    user_activities = await UserActivityCrud.get_user_activities(db, current_user.id, limit=limit)

    # Convert to response format
    activity_responses = [convert_user_activity_to_response(activity) for activity in user_activities]

    return {"success": True, "data": activity_responses}


@router.get("/analytics")
async def get_user_analytics(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    time_range: Annotated[str, Query(description="Time range: all, 7d, 30d, 90d")] = "all",
    practice_type: Annotated[str, Query(description="Practice type: both, mockTest, practice")] = "both",
):
    """
    Get user's performance analytics
    """
    # Validate time range
    valid_time_ranges = ["all", "7d", "30d", "90d"]
    if time_range not in valid_time_ranges:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid timeRange. Must be one of: {', '.join(valid_time_ranges)}",
        )

    # Validate practice type
    valid_practice_types = ["both", "mockTest", "practice"]
    if practice_type not in valid_practice_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid practiceType. Must be one of: {', '.join(valid_practice_types)}",
        )

    # Get analytics data
    analytics_data = await UserAnalyticsCrud.get_user_analytics(
        db=db,
        user_id=current_user.id,
        time_range=time_range,
        practice_type=practice_type,
    )

    # Convert to response format
    analytics_response = convert_analytics_to_response(analytics_data)

    return {"success": True, "data": analytics_response}
