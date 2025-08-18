from app.model.model import UserActivity
from app.schema.user_activity import ActivityResponse


def convert_user_activity_to_response(user_activity: UserActivity) -> ActivityResponse:
    """Convert a UserActivity model to ActivityResponse"""
    return ActivityResponse(
        id=user_activity.id,
        type=user_activity.type,
        practiceType=user_activity.practice_type or "",
        score=float(user_activity.score) if user_activity.score is not None else 0.0,
        band=float(user_activity.band) if user_activity.band is not None else 0.0,
        details=user_activity.details,
        xpEarned=user_activity.xp_earned,
        timeSpent=user_activity.time_spent,
        createdAt=user_activity.created_at,
    )


def convert_user_activity_to_submit_response(user_activity: UserActivity) -> dict:
    """Convert a UserActivity model to submit response format"""
    from app.schema.user_activity import SubmitActivityResponse

    return {
        "activityId": user_activity.id,
        "type": user_activity.type,
        "practiceType": user_activity.practice_type or "",
        "score": float(user_activity.score) if user_activity.score is not None else 0.0,
        "band": float(user_activity.band) if user_activity.band is not None else 0.0,
        "xpEarned": user_activity.xp_earned,
        "timeSpent": user_activity.time_spent or 0,
        "createdAt": user_activity.created_at,
    }
