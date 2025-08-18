from typing import Any, Dict

from app.schema.dashboard import DashboardResponse, RecentActivity, UserStats


def convert_dashboard_to_response(dashboard_data: Dict[str, Any]) -> DashboardResponse:
    """Convert dashboard data to response format"""
    # Convert user stats
    user_stats = UserStats(
        totalTestsTaken=dashboard_data["userStats"]["totalTestsTaken"],
        averageScore=dashboard_data["userStats"]["averageScore"],
        bestScore=dashboard_data["userStats"]["bestScore"],
        studyStreak=dashboard_data["userStats"]["studyStreak"],
        totalStudyTime=dashboard_data["userStats"]["totalStudyTime"],
        completedLessons=dashboard_data["userStats"]["completedLessons"],
        currentStreak=dashboard_data["userStats"]["currentStreak"],
    )

    # Convert recent activity
    recent_activity = []
    for activity_data in dashboard_data["recentActivity"]:
        recent_activity.append(
            RecentActivity(
                id=activity_data["id"],
                type=activity_data["type"],
                title=activity_data["title"],
                score=activity_data["score"],
                date=activity_data["date"],
                time=activity_data["time"],
                details=activity_data["details"],
            )
        )

    return DashboardResponse(
        userStats=user_stats,
        recentActivity=recent_activity,
    )
