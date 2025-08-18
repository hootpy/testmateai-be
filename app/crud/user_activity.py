from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.model.model import UserActivity


class UserActivityCrud:
    @classmethod
    async def create_user_activity(
        cls,
        db: AsyncSession,
        user_id: uuid.UUID,
        activity_type: str,
        practice_type: str,
        score: float,
        band: float,
        details: Optional[dict] = None,
        xp_earned: int = 0,
        time_spent: Optional[int] = None,
    ) -> UserActivity:
        """
        Create a new user activity record
        """
        user_activity = UserActivity(
            user_id=user_id,
            type=activity_type,
            practice_type=practice_type,
            score=score,
            band=band,
            details=details,
            xp_earned=xp_earned,
            time_spent=time_spent,
        )

        db.add(user_activity)
        await db.commit()
        await db.refresh(user_activity)

        return user_activity

    @classmethod
    async def get_user_activity_by_id(cls, db: AsyncSession, activity_id: uuid.UUID) -> Optional[UserActivity]:
        """Get a single user activity by ID"""
        result = await db.execute(select(UserActivity).where(UserActivity.id == activity_id).limit(1))
        return result.scalar_one_or_none()

    @classmethod
    async def get_user_activities(cls, db: AsyncSession, user_id: uuid.UUID, limit: int = 50) -> list[UserActivity]:
        """Get all activities for a specific user"""
        result = await db.execute(
            select(UserActivity)
            .where(UserActivity.user_id == user_id)
            .order_by(UserActivity.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
