import contextlib
from typing import AsyncIterator, LiteralString

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, declared_attr

from app.common.exceptions.db_session import DatabaseSessionManagerInitializeError


class BaseTableName:
    """
    Base class for SQLAlchemy models that automatically generates a table name based on the class name.
    """

    @declared_attr
    def __tablename__(cls) -> LiteralString:
        """
        Returns the table name for the SQLAlchemy model.

        :return: The table name as a string.
        """
        return "".join([f"_{c.lower()}" if c.isupper() else c for c in cls.__name__]).lstrip("_")


Base = declarative_base(cls=BaseTableName)


class DatabaseSessionManager:
    """
    A class to manage database sessions and connections.

    ...

    Attributes
    ----------
    _engine : AsyncEngine
        the async engine used to connect to the database
    _sessionmaker : async_sessionmaker[AsyncSession]
        the async sessionmaker used to create sessions

    Methods
    -------
    init(database_url: str) -> None:
        Initializes the database session manager with the given database URL.

    close() -> None:
        Closes the database session manager.

    connect() -> AsyncIterator[AsyncConnection]:
        Connects to the database and returns an async connection.

    session() -> AsyncIterator[AsyncSession]:
        Creates a new async session and returns it.

    create_all(connection: AsyncConnection) -> None:
        Creates all tables in the database.

    drop_all(connection: AsyncConnection) -> None:
        Drops all tables in the database.
    """

    def __init__(self) -> None:
        """
        Constructs all the necessary attributes for the DatabaseSessionManager object.
        """
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = None

    def init(self, database_url: str) -> None:
        """
        Initializes the database session manager with the given database URL.

        Parameters
        ----------
        database_url : str
            The URL of the database to connect to.
        """
        self._engine = create_async_engine(database_url, future=True)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self) -> None:
        """
        Closes the database session manager.
        """
        if self._engine is None:
            raise DatabaseSessionManagerInitializeError
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """
        Connects to the database and returns an async connection.
        """
        if self._engine is None:
            raise DatabaseSessionManagerInitializeError

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """
        Creates a new async session and returns it.
        """
        if self._sessionmaker is None:
            raise DatabaseSessionManagerInitializeError

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    @staticmethod
    async def create_all(connection: AsyncConnection) -> None:
        """
        Creates all tables in the database.

        Parameters
        ----------
        connection : AsyncConnection
            The async connection to the database.
        """
        await connection.run_sync(Base.metadata.create_all)

    @staticmethod
    async def drop_all(connection: AsyncConnection) -> None:
        """
        Drops all tables in the database.

        Parameters
        ----------
        connection : AsyncConnection
            The async connection to the database.
        """
        await connection.run_sync(Base.metadata.drop_all)


sessionmanager = DatabaseSessionManager()
