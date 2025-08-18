import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class SubmitActivityRequest(BaseModel):
    type: str = Field(..., description="Type of activity: listening|reading|writing|speaking")
    practiceType: str = Field(..., description="Type of practice: mockTest|practice")
    score: float = Field(..., ge=0.0, le=9.0, description="Score between 0.0 and 9.0")
    band: float = Field(..., ge=0.0, le=9.0, description="Band score between 0.0 and 9.0")
    details: Optional[Dict[str, Any]] = Field(None, description="Optional additional details")
    xpEarned: int = Field(0, ge=0, description="XP earned from this activity")
    timeSpent: int = Field(..., ge=0, description="Time spent in minutes")


class ActivityResponse(BaseModel):
    id: uuid.UUID
    type: str
    practiceType: str
    score: float
    band: float
    details: Optional[Dict[str, Any]]
    xpEarned: int
    timeSpent: Optional[int]
    createdAt: datetime


class SubmitActivityResponse(BaseModel):
    activityId: uuid.UUID
    type: str
    practiceType: str
    score: float
    band: float
    xpEarned: int
    timeSpent: int
    createdAt: datetime


class SubmitActivityResponse(BaseModel):
    success: bool
    data: ActivityResponse
    message: str
