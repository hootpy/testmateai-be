import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class ProgressResponse(BaseModel):
    level: int
    xp: int
    currentScore: float
    targetScore: Optional[float]
    testDate: Optional[str]
    hasPreviousTest: bool
    lastTestScore: Optional[float]
    xpToNextLevel: int
    levelProgress: float


class AddXpRequest(BaseModel):
    amount: int = Field(..., gt=0, description="Amount of XP to add (positive integer)")
    source: str = Field(..., description="Source of XP: practice, mock_test, or streak")
    activityId: Optional[uuid.UUID] = Field(None, description="Optional UUID of the activity")


class AddXpResponse(BaseModel):
    previousLevel: int
    newLevel: int
    previousXp: int
    newXp: int
    xpGained: int
    leveledUp: bool
