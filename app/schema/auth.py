from datetime import date

from pydantic import BaseModel, EmailStr, Field, field_validator


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


class LoginRequest(BaseModel):
    email: EmailStr


class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str


class UpdateProfileRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr | None = None
    targetScore: float | None = Field(default=None, ge=0.0, le=9.0)
    testDate: date | None = Field(default=None)
    hasPreviousTest: bool | None = None
    lastTestScore: float | None = Field(default=None, ge=0.0, le=9.0)
