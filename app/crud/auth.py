from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.core.config import SETTINGS
from app.model.model import OtpCode, User
from app.crud.user import UserCrud


class AuthCrud:
    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)

    @classmethod
    async def issue_otp(cls, db: AsyncSession, email: str) -> OtpCode:
        # Ensure user exists (get_or_create strategy)
        await UserCrud.get_or_create_user_by_email(db, email)

        # Rate limit based on latest OTP for this email
        query = await db.execute(select(OtpCode).where(OtpCode.email == email).order_by(OtpCode.created_at.desc()))
        existing: Optional[OtpCode] = query.scalar_one_or_none()
        now = cls._now()
        if existing and (now - existing.created_at).total_seconds() < SETTINGS.OTP_RATE_LIMIT_SECONDS:
            return existing

        # Create new OTP record
        code = cls._generate_otp_code()
        expires_at = now + timedelta(seconds=SETTINGS.OTP_TTL_SECONDS)
        otp = OtpCode(email=email, otp=code, expires_at=expires_at, created_at=now)
        db.add(otp)
        await db.commit()
        await db.refresh(otp)
        return otp

    @staticmethod
    def _generate_otp_code() -> str:
        import random

        digits = "0123456789"
        return "".join(random.choice(digits) for _ in range(SETTINGS.OTP_LENGTH))

    @classmethod
    async def verify_otp(cls, db: AsyncSession, email: str, code: str) -> Optional[User]:
        query = await db.execute(select(OtpCode).where(OtpCode.email == email).order_by(OtpCode.created_at.desc()))
        otp: Optional[OtpCode] = query.scalar_one_or_none()
        if otp is None:
            return None
        now = cls._now()
        if otp.expires_at <= now:
            return None
        if otp.otp != code:
            return None
        # Ensure user exists and return it
        user = await UserCrud.get_or_create_user_by_email(db, email)
        return user
