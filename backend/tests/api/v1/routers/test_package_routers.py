import pytest

from fastapi import status


@pytest.mark.asyncio(scope="session")
async def test_response_structure(async_client_v1):
    response = await async_client_v1.get("/packages/")
    assert response.status_code == status.HTTP_200_OK
    assert "items" in response.json()
    assert "total" in response.json()
    assert "page" in response.json()
    assert "size" in response.json()
    assert "pages" in response.json()


@pytest.mark.asyncio(scope="session")
async def test_get_all_packages(async_client_v1, created_package):
    response = await async_client_v1.get("/packages/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["items"]) == 1


@pytest.mark.asyncio(scope="session")
async def test_get_package_by_id(async_client_v1, created_package):
    response = await async_client_v1.get(f"/packages/{created_package.id}")
    assert response.status_code == status.HTTP_200_OK
    api_response = response.json()
    assert api_response["name"] == created_package.name
    assert len(api_response["dependencies"]) == len(created_package.dependencies)

    response = await async_client_v1.get("/packages/10")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    api_response = response.json()
    assert api_response["detail"] == "Package not found!"


@pytest.mark.asyncio(scope="session")
async def test_get_package_by_name(async_client_v1, created_package):
    response = await async_client_v1.get(f"/packages/{created_package.name}")
    assert response.status_code == status.HTTP_200_OK
    api_response = response.json()
    assert api_response["name"] == created_package.name
    assert len(api_response["dependencies"]) == len(created_package.dependencies)

    response = await async_client_v1.get("/packages/dpkg-pro")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    api_response = response.json()
    assert api_response["detail"] == "Package not found!"
