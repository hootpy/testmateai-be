from datetime import datetime, timezone
from typing import Any, Dict

from app.schema.user_analytics import SkillAnalytics, UserAnalyticsResponse


def convert_analytics_to_response(analytics_data: Dict[str, Any]) -> UserAnalyticsResponse:
    """Convert analytics data to response format"""
    # Convert skill breakdown
    skill_breakdown = {}
    for skill, data in analytics_data["skillBreakdown"].items():
        skill_breakdown[skill] = SkillAnalytics(
            totalSessions=data["totalSessions"],
            averageScore=data["averageScore"],
            bestScore=data["bestScore"],
            totalTimeSpent=data["totalTimeSpent"],
            improvementTrend=data["improvementTrend"],
        )

    return UserAnalyticsResponse(
        overallStats=analytics_data["overallStats"],
        skillBreakdown=skill_breakdown,
        recentActivity=analytics_data["recentActivity"],
        studyStreak=analytics_data["studyStreak"],
        createdAt=datetime.now(timezone.utc),
    )
