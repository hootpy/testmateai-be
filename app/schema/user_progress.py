from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Achievement(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    earned: bool
    date: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserSkills(BaseModel):
    speaking: float
    listening: float
    reading: float
    writing: float


class Activity(BaseModel):
    type: str
    action: str
    score: Optional[float] = None
    timestamp: datetime
    details: Optional[dict] = None

    class Config:
        from_attributes = True


class UserProgressResponse(BaseModel):
    level: int
    xp: int
    totalXP: int = Field(..., validation_alias="total_xp", serialization_alias="totalXP")
    skills: UserSkills
    achievements: List[Achievement] = []
    recentActivity: List[Activity] = Field(
        default_factory=list, validation_alias="recent_activity", serialization_alias="recentActivity"
    )

    class Config:
        populate_by_name = True


class UserAchievementsResponse(BaseModel):
    achievements: List[Achievement] = []


class UserActivityResponse(BaseModel):
    activities: List[Activity] = []
