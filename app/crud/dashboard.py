from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from sqlalchemy import and_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.model.model import User, UserActivity


class DashboardCrud:
    @classmethod
    async def get_dashboard_data(cls, db: AsyncSession, user_id: uuid.UUID) -> Dict:
        """
        Get comprehensive dashboard data for a user
        """
        # Get user activities
        activities_result = await db.execute(
            select(UserActivity).where(UserActivity.user_id == user_id).order_by(desc(UserActivity.created_at))
        )
        activities = activities_result.scalars().all()

        # Get user info
        user_result = await db.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one_or_none()

        if not user:
            return cls._get_empty_dashboard()

        # Calculate user stats
        user_stats = cls._calculate_user_stats(activities, user)

        # Get recent activity (last 3)
        recent_activity = cls._get_recent_activity(activities[:3])

        return {
            "userStats": user_stats,
            "recentActivity": recent_activity,
        }

    @classmethod
    def _get_empty_dashboard(cls) -> Dict:
        """Return empty dashboard structure"""
        return {
            "userStats": {
                "totalTestsTaken": 0,
                "averageScore": 0.0,
                "bestScore": 0.0,
                "studyStreak": 0,
                "totalStudyTime": "0 hours",
                "completedLessons": 0,
                "currentStreak": 0,
            },
            "recentActivity": [],
        }

    @classmethod
    def _calculate_user_stats(cls, activities: List[UserActivity], user: User) -> Dict:
        """Calculate comprehensive user statistics"""
        if not activities:
            return {
                "totalTestsTaken": 0,
                "averageScore": 0.0,
                "bestScore": 0.0,
                "studyStreak": 0,
                "totalStudyTime": "0 hours",
                "completedLessons": 0,
                "currentStreak": 0,
            }

        # Calculate basic stats
        total_tests_taken = len([a for a in activities if a.practice_type == "mockTest"])
        completed_lessons = len([a for a in activities if a.practice_type == "practice"])

        # Calculate scores
        scores = [a.score for a in activities if a.score is not None]
        average_score = sum(scores) / len(scores) if scores else 0.0
        best_score = max(scores) if scores else 0.0

        # Calculate study time
        total_time_minutes = sum(a.time_spent or 0 for a in activities)
        total_study_time = cls._format_study_time(total_time_minutes)

        # Calculate streaks
        study_streak = cls._calculate_study_streak(activities)
        current_streak = cls._calculate_current_streak(activities)

        return {
            "totalTestsTaken": total_tests_taken,
            "averageScore": round(average_score, 1),
            "bestScore": round(best_score, 1),
            "studyStreak": study_streak,
            "totalStudyTime": total_study_time,
            "completedLessons": completed_lessons,
            "currentStreak": current_streak,
        }

    @classmethod
    def _format_study_time(cls, minutes: int) -> str:
        """Format study time in hours"""
        if minutes < 60:
            return f"{minutes} minutes"
        hours = minutes // 60
        remaining_minutes = minutes % 60
        if remaining_minutes == 0:
            return f"{hours} hours"
        return f"{hours} hours {remaining_minutes} minutes"

    @classmethod
    def _calculate_study_streak(cls, activities: List[UserActivity]) -> int:
        """Calculate longest study streak"""
        if not activities:
            return 0

        # Group activities by date
        date_activities = {}
        for activity in activities:
            date = activity.created_at.date()
            if date not in date_activities:
                date_activities[date] = []
            date_activities[date].append(activity)

        # Sort dates
        sorted_dates = sorted(date_activities.keys(), reverse=True)

        # Find longest consecutive streak
        max_streak = 0
        current_streak = 0
        current_date = datetime.utcnow().date()

        for date in sorted_dates:
            days_diff = (current_date - date).days
            if days_diff == current_streak:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                break

        return max_streak

    @classmethod
    def _calculate_current_streak(cls, activities: List[UserActivity]) -> int:
        """Calculate current study streak"""
        if not activities:
            return 0

        # Sort activities by date (newest first)
        sorted_activities = sorted(activities, key=lambda x: x.created_at.date(), reverse=True)

        streak = 0
        current_date = datetime.utcnow().date()

        for activity in sorted_activities:
            activity_date = activity.created_at.date()
            days_diff = (current_date - activity_date).days

            if days_diff == streak:
                streak += 1
            else:
                break

        return streak

    @classmethod
    def _get_recent_activity(cls, activities: List[UserActivity]) -> List[Dict]:
        """Get recent activity data (last 3)"""
        recent = []
        for activity in activities:
            # Determine activity type and title
            activity_type = activity.practice_type or "practice"
            title = f"{activity.type.title()} {activity_type.title()}"

            # Format details
            details = f"{activity.type.title()} practice"
            if activity.score is not None:
                details += f" - Score: {activity.score}"
            if activity.time_spent:
                details += f" - Time: {activity.time_spent} minutes"

            recent.append(
                {
                    "id": activity.id,
                    "type": activity_type,
                    "title": title,
                    "score": float(activity.score) if activity.score else None,
                    "date": activity.created_at.date().isoformat(),
                    "time": activity.created_at.strftime("%H:%M"),
                    "details": details,
                }
            )
        return recent
