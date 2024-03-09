import pytest_asyncio
import tempfile

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from typing import AsyncGenerator, Callable

from src.database.sqlite.handler import SQLiteHandler
from src.models.package_models import Dependency, Package


@pytest_asyncio.fixture
async def override_get_database_dependency() -> Callable:
    async def _override_get_database_dependency():
        db_handler = SQLiteHandler(database="test_dpkg_profiles")
        await db_handler.initialize()
        return db_handler

    return _override_get_database_dependency


@pytest_asyncio.fixture
async def app(override_get_database_dependency: Callable) -> AsyncGenerator:
    from src.api.common.dependencies import get_database_dependency
    from src.main import app

    app.dependency_overrides[get_database_dependency] = override_get_database_dependency
    yield app


@pytest_asyncio.fixture
async def async_client_v1(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore[arg-type]
        base_url="http://testserver/api/v1",
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture
async def sqlite():
    db_handler = SQLiteHandler(database="test_dpkg_profiles")
    await db_handler.initialize()

    yield db_handler

    # Perform cleanup after all tests are done
    await db_handler.drop_tables()
    await db_handler.engine.dispose()


@pytest_asyncio.fixture
def package_item():
    package_data = {
        "name": "dpkg",
        "version": "1.19.7ubuntu3.2",
        "description": "Debian package management system",
    }
    package_instance = Package.create_instance(package_data)

    dependency_data = {
        "dependent_package": "dpkg",
        "dependency_package": "libacl1 (= 2.2.53-6)",
    }
    package_instance.dependencies.append(Dependency(**dependency_data))
    dependency_data = {
        "dependent_package": "dpkg",
        "dependency_package": "libc6 (>= 2.14)",
    }
    package_instance.dependencies.append(Dependency(**dependency_data))

    return package_instance


@pytest_asyncio.fixture
async def created_package(sqlite, package_item):
    created_package = await sqlite.create_package(package_item)
    yield created_package


@pytest_asyncio.fixture
async def package_text():
    return """
Package: dpkg
Version: 1.19.7ubuntu3.2
Depends: libacl1 (= 2.2.53-6), libc6 (>= 2.14)
Description: Debian package management system
    """


@pytest_asyncio.fixture
async def package_json():
    return {
        "package": "dpkg",
        "version": "1.19.7ubuntu3.2",
        "description": "Debian package management system",
        "depends": "libacl1 (= 2.2.53-6), libc6 (>= 2.14)",
    }


@pytest_asyncio.fixture
async def package_file(package_text):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(package_text)
        file_name = temp_file.name
    return file_name
