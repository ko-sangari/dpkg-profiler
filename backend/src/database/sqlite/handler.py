import logging

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import List, Optional

from src.database.sqlite.core import SQLiteCore
from src.models.package_models import Package

logger = logging.getLogger(__name__)


class SQLiteHandler(SQLiteCore):
    """
    A subclass of SQLiteCore that handles database queries for SQLite databases.

    This class provides methods for interacting with the SQLite database,
    including querying, inserting, updating, and deleting records.
    """

    def __init__(self, db_url: URL = None, database: str = None) -> None:
        """
        Initializes the SQLiteCore with a database URL and connects to it.

        Args:
            db_url (str, optional): The database URL. Defaults to None.
            database (str, optional): The name of the database to connect to. Defaults to None.
        """
        super().__init__(db_url, database)

    async def create_package(self, package: Package) -> Optional[Package]:
        """
        Creates a new package record in the database.

        Args:
            package (Package): The package object to be created.

        Returns:
            Optional[Package]: The created package object if successful, None otherwise.
        """
        async with self.session_factory() as session:
            try:
                session.add(package)
                await session.commit()
                await session.refresh(package, attribute_names=["dependencies"])
                return package
            except IntegrityError:
                await session.rollback()  # Rollback the transaction
                logger.error(f"Package {package.name} already exists.")
        return None

    async def get_all_packages(self, search_text: str = None) -> List[Package]:
        """
        Retrieves a list of all packages from the database.

        Args:
            search_text (str, optional): A search text to filter packages by name.

        Returns:
            List[Package]: A list of package objects matching the search criteria.
        """
        async with self.session_factory() as session:
            query = select(Package).options(joinedload(Package.dependencies))
            if search_text:
                query = query.filter(Package.name.ilike(f"%{search_text}%"))
            return await paginate(session, query)  # type: ignore[no-any-return]

    async def get_package(
        self, package_id: Optional[int] = None, package_name: Optional[str] = None
    ) -> Optional[Package]:
        """
        Retrieves a package from the database by its ID or name.

        Args:
            package_id (Optional[int]): The ID of the package to retrieve.
            package_name (Optional[str]): The name of the package to retrieve.

        Returns:
            Optional[Package]: The retrieved package object if found, None otherwise.
        """
        query = select(Package).options(
            joinedload(Package.dependencies),
            joinedload(Package.reverse_dependencies),
        )
        if package_id:
            query = query.filter(Package.id == package_id)
        elif package_name:
            query = query.filter(Package.name == package_name)

        async with self.session_factory() as session:
            package = (await session.execute(query)).scalar()

        return package
