from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.setup.database import sessionmanager


async def get_session() -> AsyncIterator[AsyncSession]:
    """Get a session from the session manager"""
    async with sessionmanager.session() as session:
        yield session
