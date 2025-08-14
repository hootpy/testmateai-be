from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt  # type: ignore[import-not-found]
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import SETTINGS
from app.core.depends.get_session import get_session
from app.schema.auth import LoginRequest, VerifyOtpRequest, TokenResponse
from app.common.utils.email import send_email
from app.crud.auth import AuthCrud

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
