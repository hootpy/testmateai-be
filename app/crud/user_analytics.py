from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from sqlalchemy import and_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.common.utils.cache import analytics_cache
from app.model.model import UserActivity


class UserAnalyticsCrud:
    @classmethod
    async def get_user_analytics(
        cls,
        db: AsyncSession,
        user_id: uuid.UUID,
        time_range: str = "all",
        practice_type: str = "both",
    ) -> Dict:
        """
        Get comprehensive analytics for a user
        """
        # Generate cache key
        cache_key = f"analytics:{user_id}:{time_range}:{practice_type}"

        # Try to get from cache first
        cached_result = await analytics_cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        # Build base query
        base_query = select(UserActivity).where(UserActivity.user_id == user_id)

        # Apply time range filter
        if time_range != "all":
            days = cls._get_days_from_range(time_range)
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            base_query = base_query.where(UserActivity.created_at >= cutoff_date)

        # Apply practice type filter
        if practice_type != "both":
            base_query = base_query.where(UserActivity.practice_type == practice_type)

        # Get all activities for the user
        result = await db.execute(base_query.order_by(desc(UserActivity.created_at)))
        activities = result.scalars().all()

        if not activities:
            analytics_result = cls._get_empty_analytics()
        else:
            # Calculate analytics
            analytics_result = cls._calculate_analytics(activities)

        # Cache the result for 5 minutes
        await analytics_cache.set(cache_key, analytics_result, ttl_seconds=300)

        return analytics_result

    @classmethod
    def _get_days_from_range(cls, time_range: str) -> int:
        """Convert time range string to number of days"""
        range_map = {
            "7d": 7,
            "30d": 30,
            "90d": 90,
        }
        return range_map.get(time_range, 0)

    @classmethod
    def _get_empty_analytics(cls) -> Dict:
        """Return empty analytics structure"""
        empty_skill = {
            "totalSessions": 0,
            "averageScore": 0.0,
            "bestScore": 0.0,
            "totalTimeSpent": 0,
            "improvementTrend": 0.0,
        }

        return {
            "overallStats": {
                "totalSessions": 0,
                "totalTimeSpent": 0,
                "averageScore": 0.0,
                "bestScore": 0.0,
            },
            "skillBreakdown": {
                "listening": empty_skill,
                "reading": empty_skill,
                "writing": empty_skill,
                "speaking": empty_skill,
            },
            "recentActivity": [],
            "studyStreak": 0,
        }

    @classmethod
    def _calculate_analytics(cls, activities: List[UserActivity]) -> Dict:
        """Calculate analytics from user activities"""
        # Group activities by skill
        skill_activities = {
            "listening": [],
            "reading": [],
            "writing": [],
            "speaking": [],
        }

        total_sessions = len(activities)
        total_time_spent = 0
        all_scores = []

        for activity in activities:
            skill = activity.type.lower()
            if skill in skill_activities:
                skill_activities[skill].append(activity)

            if activity.score is not None:
                all_scores.append(activity.score)

            if activity.time_spent is not None:
                total_time_spent += activity.time_spent

        # Calculate overall stats
        overall_stats = {
            "totalSessions": total_sessions,
            "totalTimeSpent": total_time_spent,
            "averageScore": sum(all_scores) / len(all_scores) if all_scores else 0.0,
            "bestScore": max(all_scores) if all_scores else 0.0,
        }

        # Calculate skill breakdown
        skill_breakdown = {}
        for skill, skill_acts in skill_activities.items():
            skill_breakdown[skill] = cls._calculate_skill_analytics(skill_acts)

        # Get recent activity (last 5)
        recent_activity = cls._get_recent_activity(activities[:5])

        # Calculate study streak
        study_streak = cls._calculate_study_streak(activities)

        return {
            "overallStats": overall_stats,
            "skillBreakdown": skill_breakdown,
            "recentActivity": recent_activity,
            "studyStreak": study_streak,
        }

    @classmethod
    def _calculate_skill_analytics(cls, activities: List[UserActivity]) -> Dict:
        """Calculate analytics for a specific skill"""
        if not activities:
            return {
                "totalSessions": 0,
                "averageScore": 0.0,
                "bestScore": 0.0,
                "totalTimeSpent": 0,
                "improvementTrend": 0.0,
            }

        scores = [act.score for act in activities if act.score is not None]
        time_spent = sum(act.time_spent or 0 for act in activities)

        # Calculate improvement trend (simple: first vs last score)
        improvement_trend = 0.0
        if len(scores) >= 2:
            first_score = scores[0]
            last_score = scores[-1]
            if first_score > 0:
                improvement_trend = ((last_score - first_score) / first_score) * 100

        return {
            "totalSessions": len(activities),
            "averageScore": sum(scores) / len(scores) if scores else 0.0,
            "bestScore": max(scores) if scores else 0.0,
            "totalTimeSpent": time_spent,
            "improvementTrend": improvement_trend,
        }

    @classmethod
    def _get_recent_activity(cls, activities: List[UserActivity]) -> List[Dict]:
        """Get recent activity data"""
        recent = []
        for activity in activities:
            recent.append(
                {
                    "id": str(activity.id),
                    "type": activity.type,
                    "practiceType": activity.practice_type,
                    "score": float(activity.score) if activity.score else 0.0,
                    "timeSpent": activity.time_spent or 0,
                    "createdAt": activity.created_at.isoformat(),
                }
            )
        return recent

    @classmethod
    def _calculate_study_streak(cls, activities: List[UserActivity]) -> int:
        """Calculate consecutive days of study"""
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
