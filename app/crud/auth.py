from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.core.config import SETTINGS
from app.crud.user import UserCrud
from app.model.model import OtpCode, User


class AuthCrud:
    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)

    @classmethod
    async def issue_otp(cls, db: AsyncSession, email: str) -> OtpCode:
        # Ensure user exists (get_or_create strategy)
        await UserCrud.get_or_create_user_by_email(db, email=email)

        # Rate limit based on latest OTP for this email
        result = await db.execute(select(OtpCode).where(OtpCode.email == email).order_by(OtpCode.created_at.desc()))
        existing: Optional[OtpCode] = result.scalar_one_or_none()
        now = cls._now()
        if existing and (now - existing.created_at).total_seconds() < SETTINGS.OTP_RATE_LIMIT_SECONDS:
            return existing

        # Create new OTP record
        import random

        digits = "0123456789"
        code = "".join(random.choice(digits) for _ in range(SETTINGS.OTP_LENGTH))
        expires_at = now + timedelta(seconds=SETTINGS.OTP_TTL_SECONDS)
        otp = OtpCode(email=email, otp_code=code, expires_at=expires_at, created_at=now)
        db.add(otp)
        await db.commit()
        await db.refresh(otp)
        return otp

    @classmethod
    async def verify_otp(cls, db: AsyncSession, email: str, code: str) -> Optional[User]:
        result = await db.execute(
            select(OtpCode).where(OtpCode.email == email).order_by(OtpCode.created_at.desc()).limit(1)
        )
        otp: Optional[OtpCode] = result.scalar_one_or_none()
        if otp is None:
            return None
        now = cls._now()
        if otp.expires_at <= now:
            return None
        if otp.otp_code != code:
            return None
        user = await UserCrud.get_or_create_user_by_email(db, email=email)
        return user
