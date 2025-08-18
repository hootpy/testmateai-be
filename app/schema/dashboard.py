import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UserStats(BaseModel):
    totalTestsTaken: int
    averageScore: float
    bestScore: float
    studyStreak: int
    totalStudyTime: str  # formatted string like "45 hours"
    completedLessons: int
    currentStreak: int


class RecentActivity(BaseModel):
    id: uuid.UUID
    type: str
    title: str
    score: Optional[float]
    date: str  # ISO date
    time: str
    details: str


class DashboardResponse(BaseModel):
    userStats: UserStats
    recentActivity: List[RecentActivity]
