from typing import Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

from app.common.exceptions.common import UniqueViolationField
from app.model.model import User
from app.schema.user import UserCreate


class UserCrud:
    """
    This class contains methods to perform CRUD operations on the User model.
    """

    @classmethod
    async def get_users(cls, db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[User]:
        """
        Get a list of users from the database.

        :param db: AsyncSession: Async SQLAlchemy session.
        :param skip: int: The number of users to skip.
        :param limit: int: The maximum number of users to return.
        :return: Sequence[User]: A sequence of User objects.
        """
        query = await db.execute(select(User).offset(skip).limit(limit))
        return query.scalars().all()

    @classmethod
    async def create_user(cls, db: AsyncSession, user: UserCreate) -> User:
        """
        Create a new user in the database.

        :param db: AsyncSession: Async SQLAlchemy session.
        :param user: UserCreate: The user object to create.
        :return: User: The created user object.
        """
        new_user = User(**user.model_dump())
        db.add(new_user)
        try:
            await db.commit()
        except IntegrityError as e:
            raise UniqueViolationField from e
        await db.refresh(new_user)
        return new_user
