from __future__ import annotations

import uuid
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.model.model import MockTest


class MockTestCrud:
    @classmethod
    async def get_all_mock_tests(cls, db: AsyncSession, limit: int = 50) -> List[MockTest]:
        """
        Get all available mock tests.
        Returns tests ordered by creation date (newest first).
        """
        result = await db.execute(select(MockTest).order_by(MockTest.created_at.desc()).limit(limit))
        return result.scalars().all()

    @classmethod
    async def get_mock_test_by_id(cls, db: AsyncSession, test_id: uuid.UUID) -> MockTest | None:
        """Get a single mock test by ID"""
        result = await db.execute(select(MockTest).where(MockTest.id == test_id).limit(1))
        return result.scalar_one_or_none()
