import pytest

from sqlalchemy import select

from src.models.package_models import Package


@pytest.mark.asyncio(scope="session")
async def test_package_create(sqlite, package_item):
    async with sqlite.session_factory() as session:
        session.add(package_item)
        await session.commit()

        query_all = (await session.execute(select(Package))).scalars().all()
        assert len(query_all) == 1


@pytest.mark.asyncio(scope="session")
async def test_create_tables(sqlite):
    async with sqlite.session_factory() as session:
        async with session.bind.connect() as connection:
            table_names = await connection.run_sync(
                session.bind.dialect.get_table_names
            )
            assert table_names == ["dependencies", "packages"]


@pytest.mark.asyncio(scope="session")
async def test_health_check(sqlite):
    result = await sqlite.health_check()
    assert result is True
