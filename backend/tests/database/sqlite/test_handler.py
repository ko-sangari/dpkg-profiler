import pytest


@pytest.mark.asyncio(scope="session")
async def test_create_package(sqlite, created_package, package_item):
    # Check if the package is created successfully
    retrieved_package = await sqlite.get_package(package_id=package_item.id)

    assert retrieved_package.name == package_item.name
    assert len(retrieved_package.dependencies) == 2


@pytest.mark.asyncio(scope="session")
async def test_get_package_by_name(sqlite, package_item):
    retrieved_package = await sqlite.get_package(package_name=package_item.name)
    assert retrieved_package.id == package_item.id
