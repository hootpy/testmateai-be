from typing import Dict, List

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.model.model import Achievement, TestSession, User, UserAchievement, UserActivity
from app.schema.user_progress import Achievement as AchievementSchema
from app.schema.user_progress import Activity


class UserProgressCrud:
    """
    This class contains methods to handle user progress, achievements, and activity data.
    """

    @classmethod
    async def get_user_skills(cls, db: AsyncSession, user_id: int) -> Dict[str, float]:
        """
        Calculate user's skills (speaking, listening, reading, writing) based on test sessions.

        :param db: AsyncSession: Async SQLAlchemy session.
        :param user_id: int: The user ID.
        :return: Dict[str, float]: Dictionary containing skill scores.
        """
        # Default skill values
        skills = {"speaking": 0.0, "listening": 0.0, "reading": 0.0, "writing": 0.0}

        # Get latest test sessions for each skill type
        for skill_type in skills.keys():
            query = await db.execute(
                select(TestSession)
                .where(TestSession.user_id == user_id, TestSession.test_type == skill_type)
                .order_by(desc(TestSession.created_at))
                .limit(1)
            )

            session = query.scalar_one_or_none()
            if session and session.score is not None:
                skills[skill_type] = session.score

        return skills

    @classmethod
    async def get_user_achievements(cls, db: AsyncSession, user_id: int) -> List[AchievementSchema]:
        """
        Get achievements earned by a user.

        :param db: AsyncSession: Async SQLAlchemy session.
        :param user_id: int: The user ID.
        :return: List[Dict]: List of achievement details with earned status.
        """
        # Get user's achievements
        query = await db.execute(
            select(Achievement, UserAchievement.earned_at)
            .join(UserAchievement, UserAchievement.achievement_id == Achievement.id, isouter=True)
            .where(UserAchievement.user_id == user_id)
        )

        user_achievements = []
        for achievement, earned_at in query.all():
            user_achievements.append(
                AchievementSchema(
                    id=achievement.id,
                    name=achievement.name,
                    description=achievement.description,
                    icon=achievement.icon,
                    earned=earned_at is not None,
                    date=earned_at if earned_at else None,
                )
            )

        return user_achievements

    @classmethod
    async def get_all_achievements(cls, db: AsyncSession, user_id: int) -> List[AchievementSchema]:
        """
        Get all achievements with earned status for a user.

        :param db: AsyncSession: Async SQLAlchemy session.
        :param user_id: int: The user ID.
        :return: List[Dict]: List of all achievements with earned status.
        """
        # Get all achievements and check if user has earned them
        query = await db.execute(
            select(Achievement, UserAchievement.earned_at).outerjoin(
                UserAchievement,
                (UserAchievement.achievement_id == Achievement.id) & (UserAchievement.user_id == user_id),
            )
        )

        all_achievements = []
        for achievement, earned_at in query.all():
            all_achievements.append(
                AchievementSchema(
                    id=achievement.id,
                    name=achievement.name,
                    description=achievement.description,
                    icon=achievement.icon,
                    earned=earned_at is not None,
                    date=earned_at if earned_at else None,
                )
            )

        return all_achievements

    @classmethod
    async def get_user_activities(
        cls, db: AsyncSession, user_id: int, limit: int = 10, offset: int = 0
    ) -> List[Activity]:
        """
        Get user activities with pagination.

        :param db: AsyncSession: Async SQLAlchemy session.
        :param user_id: int: The user ID.
        :param limit: int: Maximum number of activities to return.
        :param offset: int: Number of activities to skip.
        :return: List[Dict]: List of user activities.
        """
        query = await db.execute(
            select(UserActivity)
            .where(UserActivity.user_id == user_id)
            .order_by(desc(UserActivity.timestamp))
            .offset(offset)
            .limit(limit)
        )

        activities = []
        for activity in query.scalars().all():
            # Extract score from details if available
            score = None
            if activity.details and "score" in activity.details:
                score = activity.details.get("score")

            # Determine activity type based on action
            activity_type = "test"  # Default type
            if "study" in activity.action.lower():
                activity_type = "study"
            elif "practice" in activity.action.lower():
                activity_type = "practice"

            activities.append(
                Activity(
                    type=activity_type,
                    action=activity.action,
                    score=score,
                    timestamp=activity.timestamp,
                    details=activity.details,
                )
            )

        return activities

    @classmethod
    async def get_user_total_xp(cls, db: AsyncSession, user_id: int) -> int:
        """
        Calculate total XP a user has earned (sum of current XP and XP for each level).

        :param db: AsyncSession: Async SQLAlchemy session.
        :param user_id: int: The user ID.
        :return: int: Total XP earned.
        """
        query = await db.execute(select(User).where(User.id == user_id))
        user = query.scalar_one_or_none()

        if not user:
            return 0

        # Calculate total XP (current XP + XP from previous levels)
        # Assuming each level requires 1000 XP
        level_xp = user.level * 1000
        return level_xp + user.xp
