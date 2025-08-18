from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SkillAnalytics(BaseModel):
    totalSessions: int
    averageScore: float
    bestScore: float
    totalTimeSpent: int  # in minutes
    improvementTrend: float  # percentage improvement over time


class UserAnalyticsResponse(BaseModel):
    overallStats: Dict[str, int]  # total sessions, total time, etc.
    skillBreakdown: Dict[str, SkillAnalytics]  # listening, reading, writing, speaking
    recentActivity: List[Dict[str, Any]]  # last 5 activities
    studyStreak: int  # consecutive days of activity
    createdAt: datetime


class AnalyticsQueryParams(BaseModel):
    timeRange: str = Field("all", description="Time range: all, 7d, 30d, 90d")
    practiceType: str = Field("both", description="Practice type filter: both, mockTest, practice")
