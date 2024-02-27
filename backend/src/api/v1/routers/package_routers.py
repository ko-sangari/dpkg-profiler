from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from typing import Union

from src.api.common.dependencies import get_database_dependency
from src.api.v1.schemas.package_schemas import PackageSchema
from src.database.sqlite.handler import SQLiteHandler

router = APIRouter(
    prefix="/packages",
    tags=["packages"],
)


@router.get("/", response_model=Page[PackageSchema])
async def get_all_packages(
    name: str = None,
    database: SQLiteHandler = Depends(get_database_dependency),
) -> Page[PackageSchema]:
    """
    Retrieves a list of all packages and their associated dependencies.

    Args:
        name (str): Optional search text for filtering packages by name.

    Returns:
        Page[PackageSchema]: A page of packages with their details and dependencies.
    """
    return await database.get_all_packages(search_text=name)  # type: ignore


@router.get("/{package_lookup}", response_model=PackageSchema)
async def get_package_by_lookup(
    package_lookup: Union[int, str],
    database: SQLiteHandler = Depends(get_database_dependency),
) -> PackageSchema:
    """
    Retrieves package details by package ID or name.

    Args:
        package_lookup (Union[int, str]): ID or name of the package to retrieve.

    Returns:
        PackageSchema: Details of the specified package.

    Raises:
        HTTPException: If the package is not found.
    """
    if package_lookup.isdigit():  # type: ignore[union-attr]
        package = await database.get_package(package_id=int(package_lookup))
    else:
        package = await database.get_package(package_name=str(package_lookup))

    if package:
        return package  # type: ignore[return-value]
    raise HTTPException(status_code=404, detail="Package not found!")
