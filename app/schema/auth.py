from datetime import date
from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic.config import ConfigDict


class LoginRequest(BaseModel):
    email: EmailStr


class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    email: EmailStr
    name: str | None = None
    targetScore: float | None = Field(default=None)
    testDate: date | None = Field(default=None)

    @field_validator("targetScore")
    @classmethod
    def validate_target_score(cls, value: float | None) -> float | None:
        if value is None:
            return value
        doubled = value * 2
        if abs(doubled - round(doubled)) > 1e-9:
            raise ValueError("targetScore must be in 0.5 increments (e.g., 7.0, 7.5)")
        return value


class CompleteRegistrationRequest(BaseModel):
    email: EmailStr
    otp: str
    name: str
    targetScore: float | None = Field(default=None)
    testDate: date | None = Field(default=None)

    @field_validator("targetScore")
    @classmethod
    def validate_target_score(cls, value: float | None) -> float | None:
        if value is None:
            return value
        doubled = value * 2
        if abs(doubled - round(doubled)) > 1e-9:
            raise ValueError("targetScore must be in 0.5 increments (e.g., 7.0, 7.5)")
        return value


class AuthUser(BaseModel):
    id: int
    email: EmailStr
    name: str
    level: int
    xp: int
    targetScore: float | None = Field(default=None, validation_alias="target_score", serialization_alias="targetScore")
    testDate: date | None = Field(default=None, validation_alias="test_date", serialization_alias="testDate")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class RegistrationCompleteResponse(BaseModel):
    token: str
    user: AuthUser
