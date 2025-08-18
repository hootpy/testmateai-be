from __future__ import annotations

import uuid
from datetime import date, datetime, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.model.model import User


class UserCrud:
    @classmethod
    async def get_user_by_id(cls, db: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id).limit(1))
        return result.scalar_one_or_none()

    @classmethod
    async def get_user_by_email(cls, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email).limit(1))
        return result.scalar_one_or_none()

    @classmethod
    async def create_user(
        cls,
        db: AsyncSession,
        *,
        name: str,
        email: str,
        target_score: float | None = None,
        test_date: date | None = None,
    ) -> User:
        now = datetime.now(timezone.utc)
        user = User(
            name=name,
            email=email,
            target_score=target_score,
            test_date=test_date,
            created_at=now,
            updated_at=now,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @classmethod
    async def get_or_create_user_by_email(
        cls, db: AsyncSession, *, email: str, default_name: Optional[str] = None
    ) -> User:
        existing = await cls.get_user_by_email(db, email)
        if existing is not None:
            return existing
        name_value = default_name or email.split("@", 1)[0]
        return await cls.create_user(db, name=name_value, email=email)

    @classmethod
    async def update_user_profile(
        cls,
        db: AsyncSession,
        *,
        user_id: uuid.UUID,
        name: Optional[str] = None,
        email: Optional[str] = None,
        target_score: Optional[float] = None,
        test_date: Optional[date] = None,
        has_previous_test: Optional[bool] = None,
        last_test_score: Optional[float] = None,
    ) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id).limit(1))
        user = result.scalar_one_or_none()
        if user is None:
            return None
        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if target_score is not None:
            user.target_score = target_score
        if test_date is not None:
            user.test_date = test_date
        if has_previous_test is not None:
            user.has_previous_test = has_previous_test
        if last_test_score is not None:
            user.last_test_score = last_test_score
        user.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(user)
        return user

    @classmethod
    async def get_user_progress(cls, db: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
        """
        Get user with all progress-related fields for the progress endpoint.
        This method ensures we get fresh data from the database.
        """
        result = await db.execute(select(User).where(User.id == user_id).limit(1))
        return result.scalar_one_or_none()

    @classmethod
    async def add_xp_to_user(cls, db: AsyncSession, user_id: uuid.UUID, xp_amount: int) -> Optional[User]:
        """
        Add XP to user and handle level progression.
        Returns the updated user or None if user not found.
        """
        result = await db.execute(select(User).where(User.id == user_id).limit(1))
        user = result.scalar_one_or_none()
        if user is None:
            return None

        # Store previous values for response
        previous_xp = user.xp
        previous_level = user.level

        # Add XP
        user.xp += xp_amount

        # Calculate new level based on XP
        new_level = cls._calculate_level_from_xp(user.xp)
        user.level = new_level

        # Update timestamp
        user.updated_at = datetime.now(timezone.utc)

        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    def _calculate_level_from_xp(xp: int) -> int:
        """
        Calculate level based on total XP.

        Level progression formula:
        - Level 1: 0-99 XP
        - Level 2: 100-299 XP (200 XP needed)
        - Level 3: 300-599 XP (300 XP needed)
        - Level 4: 600-999 XP (400 XP needed)
        - And so on...
        """
        if xp < 100:
            return 1

        # For level 2 and above, calculate based on cumulative XP needed
        level = 1
        cumulative_xp_needed = 0

        while True:
            level += 1
            cumulative_xp_needed += level * 100

            if xp < cumulative_xp_needed:
                return level - 1

        return 1  # Fallback
