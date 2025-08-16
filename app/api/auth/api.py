from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt  # type: ignore[import-not-found]
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import SETTINGS
from app.core.depends.get_current_user import get_current_user
from app.core.depends.get_session import get_session
from app.model.model import User
from app.schema.auth import (
    LoginRequest,
    VerifyOtpRequest,
    TokenResponse,
    RegisterRequest,
    CompleteRegistrationRequest,
    RegistrationCompleteResponse,
    AuthUser,
)
from app.common.utils.email import send_email
from app.crud.auth import AuthCrud
from app.crud.user import UserCrud
from app.schema.user import UserUpdateResponse, UserUpdate

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
async def login(payload: LoginRequest, db: Annotated[AsyncSession, Depends(get_session)]):
    otp = await AuthCrud.issue_otp(db, payload.email)
    # Email: "Your OTP is 123456"
    await send_email(payload.email, subject="Your login code", body=f"Your OTP is {otp.code}")
    return {"ok": True}


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(payload: VerifyOtpRequest, db: Annotated[AsyncSession, Depends(get_session)]):
    user = await AuthCrud.verify_otp(db, payload.email, payload.otp)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")

    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=SETTINGS.JWT_EXPIRE_MINUTES)
    payload_claims = {
        "sub": str(user.id),
        "email": user.email,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    token = jwt.encode(payload_claims, SETTINGS.JWT_SECRET, algorithm=SETTINGS.JWT_ALGORITHM)
    return TokenResponse(access_token=token)


@router.get("/logout")
async def logout():
    return {"ok": True}


@router.post("/register")
async def register(payload: RegisterRequest, db: Annotated[AsyncSession, Depends(get_session)]):
    otp = await AuthCrud.issue_otp(db, payload.email)
    await send_email(payload.email, subject="Your login code", body=f"Your OTP is {otp.otp}")
    return {"message": "OTP sent successfully"}


@router.post("/complete-registration", response_model=RegistrationCompleteResponse)
async def complete_registration(
    payload: CompleteRegistrationRequest, db: Annotated[AsyncSession, Depends(get_session)]
):
    user = await AuthCrud.verify_otp(db, payload.email, payload.otp)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")

    # Update profile with provided info
    updated = await UserCrud.update_user_profile(
        db,
        user_id=user.id,
        name=payload.name,
        target_score=payload.targetScore,
        test_date=payload.testDate,
    )
    assert updated is not None

    # Issue JWT
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=SETTINGS.JWT_EXPIRE_MINUTES)
    claims = {"sub": str(updated.id), "email": updated.email, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    token = jwt.encode(claims, SETTINGS.JWT_SECRET, algorithm=SETTINGS.JWT_ALGORITHM)
    return RegistrationCompleteResponse(token=token, user=AuthUser.model_validate(updated))


@router.put("/update-profile", response_model=UserUpdateResponse)
async def update_profile(
    payload: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_session)],
    user: User = Depends(get_current_user),
):
    updated = await UserCrud.update_user_profile(
        db,
        user_id=user.id,
        name=payload.name,
        target_score=payload.targetScore,
        test_date=payload.testDate,
    )
    if updated is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update profile")

    return UserUpdateResponse(user=updated)


@router.delete("/delete-account")
async def delete_account(
    db: Annotated[AsyncSession, Depends(get_session)],
    user: User = Depends(get_current_user),
):
    success = await UserCrud.delete_user_account(db, user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete account")

    return {"message": "Account deleted successfully"}
