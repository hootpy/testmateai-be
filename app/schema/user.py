from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic.config import ConfigDict


class UserGet(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserUpdateName(BaseModel):
    name: str


class StudyPlanFocusArea(BaseModel):
    skill: str
    reason: str


class StudyPlanWeeklySchedule(BaseModel):
    week: int
    focus: str
    tasks: List[str]


class StudyPlan(BaseModel):
    summary: str
    weeks: int
    recommendations: List[str]
    focus_areas: List[StudyPlanFocusArea]
    weekly_schedule: List[StudyPlanWeeklySchedule]


class UserDetail(BaseModel):
    id: int
    email: EmailStr
    name: str
    level: int
    xp: int
    currentScore: float = 0.0
    targetScore: float | None = Field(default=None, validation_alias="target_score", serialization_alias="targetScore")
    testDate: date | None = Field(default=None, validation_alias="test_date", serialization_alias="testDate")
    hasPreviousTest: bool = False
    lastTestScore: float | None = None
    studyPlan: Optional[StudyPlan] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UserUpdate(BaseModel):
    name: str | None = None
    targetScore: float | None = None
    testDate: date | None = None

    @field_validator("targetScore")
    @classmethod
    def validate_target_score(cls, value: float | None) -> float | None:
        if value is None:
            return None
        doubled = value * 2
        if abs(doubled - round(doubled)) > 1e-9:
            raise ValueError("targetScore must be in 0.5 increments (e.g., 7.0, 7.5)")
        return value


class UserUpdateResponse(BaseModel):
    user: UserDetail


class UserProfileResponse(BaseModel):
    user: UserDetail

    class Config:
        from_attributes = True
        json_encoders = {date: lambda v: v.isoformat() if v else None}
