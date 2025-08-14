from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.core.config import SETTINGS
from app.model.model import Otp, User
from app.crud.user import UserCrud


class AuthCrud:
    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)

    @classmethod
    async def issue_otp(cls, db: AsyncSession, email: str) -> Otp:
        user: User = await UserCrud.get_or_create_user_by_email(db, email)

        # Rate limit based on last_sent_at
        query = await db.execute(select(Otp).where(Otp.user_id == user.id).order_by(Otp.created_at.desc()))
        existing: Optional[Otp] = query.scalar_one_or_none()
        now = cls._now()
        if (
            existing
            and existing.last_sent_at
            and (now - existing.last_sent_at).total_seconds() < SETTINGS.OTP_RATE_LIMIT_SECONDS
        ):
            return existing

        # Create or update OTP
        code = cls._generate_otp_code()
        expires_at = now + timedelta(seconds=SETTINGS.OTP_TTL_SECONDS)
        if existing:
            existing.code = code
            existing.expires_at = expires_at
            existing.last_sent_at = now
            db.add(existing)
            await db.commit()
            await db.refresh(existing)
            return existing

        otp = Otp(user_id=user.id, code=code, expires_at=expires_at, created_at=now, last_sent_at=now)
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
        query_user = await db.execute(select(User).where(User.email == email))
        user: Optional[User] = query_user.scalar_one_or_none()
        if user is None:
            return None
        query = await db.execute(select(Otp).where(Otp.user_id == user.id).order_by(Otp.created_at.desc()))
        otp: Optional[Otp] = query.scalar_one_or_none()
        if otp is None:
            return None
        now = cls._now()
        if otp.expires_at <= now:
            return None
        if otp.code != code:
            return None
        return user
