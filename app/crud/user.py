from datetime import date, datetime, timezone
from typing import Optional, Sequence

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
        now = datetime.now(timezone.utc)
        new_user = User(
            email=user.email,
            name=user.name,
            level=0,
            xp=0,
            target_score=None,
            test_date=None,
            created_at=now,
            updated_at=now,
        )
        db.add(new_user)
        try:
            await db.commit()
        except IntegrityError as e:
            raise UniqueViolationField from e
        await db.refresh(new_user)
        return new_user

    @classmethod
    async def get_user_by_id(cls, db: AsyncSession, user_id: int) -> User | None:
        """
        Get a single user by id.

        :param db: AsyncSession: Async SQLAlchemy session.
        :param user_id: int: The user id to lookup.
        :return: User | None: The user if found, otherwise None.
        """
        query = await db.execute(select(User).where(User.id == user_id))
        return query.scalar_one_or_none()

    @classmethod
    async def get_user_by_email(cls, db: AsyncSession, email: str) -> Optional[User]:
        query = await db.execute(select(User).where(User.email == email))
        return query.scalar_one_or_none()

    @classmethod
    async def update_user_name(cls, db: AsyncSession, user_id: int, new_name: str) -> User | None:
        """
        Update an existing user's name.

        :param db: AsyncSession: Async SQLAlchemy session.
        :param user_id: int: The user id to update.
        :param new_name: str: The new name to set.
        :return: User | None: The updated user if found, otherwise None.
        """
        query = await db.execute(select(User).where(User.id == user_id))
        user = query.scalar_one_or_none()
        if user is None:
            return None
        user.name = new_name
        user.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(user)
        return user

    @classmethod
    async def get_or_create_user_by_email(cls, db: AsyncSession, email: str) -> User:
        user = await cls.get_user_by_email(db, email)
        if user is not None:
            return user
        # Use local-part as fallback name
        local_part = email.split("@", 1)[0]
        create_payload = UserCreate(name=local_part, email=email)
        return await cls.create_user(db, create_payload)

    @classmethod
    async def update_user_profile(
        cls,
        db: AsyncSession,
        user_id: int,
        name: str,
        target_score: Optional[float],
        test_date: Optional[date],
    ) -> Optional[User]:
        query = await db.execute(select(User).where(User.id == user_id))
        user = query.scalar_one_or_none()
        if user is None:
            return None
        user.name = name
        user.target_score = target_score
        user.test_date = test_date
        user.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(user)
        return user

    @classmethod
    async def delete_user_account(cls, db: AsyncSession, user_id: int) -> bool:
        """
        Delete a user account by ID.

        :param db: AsyncSession: Async SQLAlchemy session.
        :param user_id: int: The user id to delete.
        :return: bool: True if user was deleted, False if user was not found.
        """
        query = await db.execute(select(User).where(User.id == user_id))
        user = query.scalar_one_or_none()
        if user is None:
            return False
        await db.delete(user)
        await db.commit()
        return True
