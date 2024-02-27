import logging

from typing import Optional

from sqlalchemy import text
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    close_all_sessions,
    create_async_engine,
)

from src.config.base import settings
from src.database.common.dependencies import BaseSQL

logger = logging.getLogger(__name__)


class SQLiteCore:
    """
    A class to handle core SQLite operations using SQLAlchemy.

    Attributes:
        db_url (str): The database URL.
        engine: The SQLAlchemy engine.
        session_factory: A SQLAlchemy session factory.
    """

    def __init__(
        self, db_url: Optional[URL] = None, database: Optional[str] = None
    ) -> None:
        """
        Initializes the SQLiteCore with a database URL and connects to it.

        Args:
            db_url (str, optional): The database URL. Defaults to None.
            database (str, optional): The name of the database to connect to. Defaults to None.
        """
        self.db_url = (
            db_url
            if db_url
            else f"sqlite+aiosqlite:///.database/{database if database else settings.sqlite_database}.db"
        )
        self.base_model = BaseSQL
        self.engine = create_async_engine(self.db_url)  # type: ignore[arg-type]
        self.session_factory = async_sessionmaker(
            bind=self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def initialize(self) -> None:
        await self.create_tables()

    async def create_tables(self) -> None:
        """
        Creates all tables in the database based on the SQLAlchemy models.
        """
        async with self.engine.begin() as connection:
            await connection.run_sync(self.base_model.metadata.create_all)

    async def drop_tables(self) -> None:
        """
        Drops all tables in the database based on the SQLAlchemy models.
        """
        await close_all_sessions()
        async with self.engine.begin() as connection:
            await connection.run_sync(self.base_model.metadata.drop_all)

    async def health_check(self) -> bool:
        """
        Performs a health check on the database.

        Returns:
            bool: True if the database is accessible and operational, False otherwise.
        """
        try:
            async with self.engine.connect() as connection:
                result = await connection.execute(text("SELECT 1"))
                return bool(result.scalar())
        except SQLAlchemyError as e:
            logger.error(f"Database health check failed: {e}")
            return False
