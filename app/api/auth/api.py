from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.utils.email import send_email
from app.core.config import SETTINGS
from app.core.depends.get_current_user import get_current_user
from app.core.depends.get_session import get_session
from app.crud.auth import AuthCrud
from app.crud.user import UserCrud
from app.model.model import OtpCode, User
from app.schema.auth import LoginRequest, RegisterRequest, UpdateProfileRequest, VerifyOtpRequest

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
async def login(payload: LoginRequest, db: Annotated[AsyncSession, Depends(get_session)]):
    # Issue OTP using AuthCrud
    otp = await AuthCrud.issue_otp(db, str(payload.email))

    # Send OTP email
    await send_email(str(payload.email), subject="Your login code", body=f"Your OTP is {otp.otp_code}")

    return {
        "success": True,
        "data": {"email": payload.email, "otpExpiry": otp.expires_at.isoformat()},
        "message": "OTP sent to your email. Please check your inbox.",
    }


@router.post("/register")
async def register(payload: RegisterRequest, db: Annotated[AsyncSession, Depends(get_session)]):
    email = str(payload.email)

    # Get or create user using UserCrud
    user = await UserCrud.get_or_create_user_by_email(db, email=email)

    # Extract user data before any operations that might expire the session
    user_id = str(user.id)
    user_name = user.name
    user_target_score = user.target_score
    user_test_date = user.test_date
    user_level = user.level
    user_xp = user.xp
    user_created_at = user.created_at

    # Update user with registration data if it's a new user or if data is provided
    if payload.name or payload.targetScore is not None or payload.testDate is not None:
        await UserCrud.update_user_profile(
            db,
            user_id=user.id,
            name=payload.name,
            target_score=payload.targetScore,
            test_date=payload.testDate,
        )
        # Refresh user data and update our variables
        user = await UserCrud.get_user_by_id(db, user.id)
        if user:
            user_name = user.name
            user_target_score = user.target_score
            user_test_date = user.test_date

    # Create OTP manually to avoid double user creation in AuthCrud
    now = datetime.now(timezone.utc)
    import random

    digits = "0123456789"
    otp_code = "".join(random.choice(digits) for _ in range(6))
    expires_at = now + timedelta(minutes=5)

    otp = OtpCode(email=email, otp_code=otp_code, expires_at=expires_at, created_at=now)
    db.add(otp)
    await db.commit()
    await db.refresh(otp)

    # Send OTP to user's email
    await send_email(email, subject="Your login code", body=f"Your OTP is {otp.otp_code}")

    # Response per spec using stored data
    user_payload = {
        "id": user_id,
        "name": user_name,
        "email": email,
        "targetScore": float(user_target_score) if user_target_score is not None else None,
        "testDate": user_test_date.isoformat() if user_test_date else None,
        "level": user_level,
        "xp": user_xp,
        "createdAt": user_created_at.isoformat() if user_created_at else None,
    }
    return {
        "success": True,
        "data": {
            "user": user_payload,
            "message": "Registration successful. Please check your email for OTP.",
        },
    }


@router.post("/verify-otp")
async def verify_otp(payload: VerifyOtpRequest, db: Annotated[AsyncSession, Depends(get_session)]):
    # Verify OTP using AuthCrud
    user = await AuthCrud.verify_otp(db, str(payload.email), payload.otp)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")

    # Issue JWT
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=SETTINGS.JWT_EXPIRE_MINUTES)
    claims = {
        "sub": str(user.id),
        "email": user.email,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    token = jwt.encode(claims, SETTINGS.JWT_SECRET, algorithm=SETTINGS.JWT_ALGORITHM)

    user_payload = {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "currentScore": float(user.current_score) if getattr(user, "current_score", None) is not None else 0.0,
        "targetScore": float(user.target_score) if getattr(user, "target_score", None) is not None else None,
        "testDate": user.test_date.isoformat() if getattr(user, "test_date", None) else None,
        "hasPreviousTest": bool(getattr(user, "has_previous_test", False)),
        "lastTestScore": float(user.last_test_score) if getattr(user, "last_test_score", None) is not None else None,
        "level": user.level,
        "xp": user.xp,
    }

    return {"success": True, "data": {"user": user_payload, "token": token}, "message": "Login successful"}


@router.get("/profile")
async def get_profile(
    current_user: Annotated[User, Depends(get_current_user)],
):
    profile = {
        "id": str(current_user.id),
        "name": current_user.name,
        "email": current_user.email,
        "currentScore": float(current_user.current_score)
        if getattr(current_user, "current_score", None) is not None
        else 0.0,
        "targetScore": float(current_user.target_score)
        if getattr(current_user, "target_score", None) is not None
        else None,
        "testDate": current_user.test_date.isoformat() if getattr(current_user, "test_date", None) else None,
        "hasPreviousTest": bool(getattr(current_user, "has_previous_test", False)),
        "lastTestScore": float(current_user.last_test_score)
        if getattr(current_user, "last_test_score", None) is not None
        else None,
        "level": current_user.level,
        "xp": current_user.xp,
        "createdAt": current_user.created_at.isoformat() if current_user.created_at else None,
        "updatedAt": current_user.updated_at.isoformat() if current_user.updated_at else None,
    }

    return {"success": True, "data": profile}


@router.put("/profile")
async def update_profile(
    payload: UpdateProfileRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    # Update user profile using UserCrud
    updated_user = await UserCrud.update_user_profile(
        db,
        user_id=current_user.id,
        name=payload.name,
        email=payload.email,
        target_score=payload.targetScore,
        test_date=payload.testDate,
        has_previous_test=payload.hasPreviousTest,
        last_test_score=payload.lastTestScore,
    )

    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    response = {
        "id": str(updated_user.id),
        "name": updated_user.name,
        "email": updated_user.email,
        "currentScore": float(updated_user.current_score)
        if getattr(updated_user, "current_score", None) is not None
        else 0.0,
        "targetScore": float(updated_user.target_score)
        if getattr(updated_user, "target_score", None) is not None
        else None,
        "testDate": updated_user.test_date.isoformat() if getattr(updated_user, "test_date", None) else None,
        "hasPreviousTest": bool(getattr(updated_user, "has_previous_test", False)),
        "lastTestScore": float(updated_user.last_test_score)
        if getattr(updated_user, "last_test_score", None) is not None
        else None,
        "level": updated_user.level,
        "xp": updated_user.xp,
        "updatedAt": updated_user.updated_at.isoformat() if updated_user.updated_at else None,
    }

    return {"success": True, "data": response, "message": "Profile updated successfully"}
