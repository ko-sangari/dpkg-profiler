import re

import asyncio
from typing import Generator

from src.models.package_models import Dependency, Package
from src.database.sqlite.handler import SQLiteHandler


def parse_package_info(package_info: str) -> dict:
    """
    Parse individual package information from a string into a dictionary.

    Args:
        package_info (str): The package information as a string.

    Returns:
        dict: A dictionary containing parsed package information.
    """
    package_data = {}
    current_key = None
    current_value = []

    for line in package_info.split("\n"):
        if ":" in line and not line.startswith(" "):
            # If there is an ongoing key, save it before starting a new one
            if current_key is not None:
                package_data[current_key] = "\n".join(current_value).strip()
            try:
                key, value = line.split(":", 1)
                value = value.strip()
            except ValueError:
                key = line.replace(":", "")
                value = ""
            current_key = key.replace("-", "_").lower()
            current_value = [value]
        elif current_key and line.strip():
            # In case it's a multiline value.
            current_value.append(line.strip())
        else:
            # Empty line, potentially end of current key
            if current_key is not None:
                package_data[current_key] = " ".join(current_value).strip()
                current_key = None
                current_value = []

    return package_data


def file_parser(filename: str) -> Generator[Package, None, None]:
    """
    Parse a dpkg status file and yield Package objects.

    Args:
        filename (str): Path to the dpkg status file.

    Yields:
        Generator[Package, None, None]: A generator of Package objects.
    """
    with open(filename, "r") as file:
        content = file.read()

    packages = re.split(r"\n\n+", content)

    for package_info in packages:
        package_data = parse_package_info(package_info)
        package = Package.create_instance(package_data)

        if "depends" in package_data:
            for depend in package_data["depends"].split(","):
                if " | " in depend:
                    for part in depend.split(" | "):
                        package.dependencies.append(
                            Dependency(
                                dependent_package=package.name,
                                dependency_package=part.strip(),
                            )
                        )
                else:
                    package.dependencies.append(
                        Dependency(
                            dependent_package=package.name,
                            dependency_package=depend.strip(),
                        )
                    )
        yield package


async def parse_dpkg():
    db = SQLiteHandler()
    await db.drop_tables()
    await db.create_tables()
    for package in file_parser("/var/lib/dpkg/status"):
        await db.create_package(package)


if __name__ == "__main__":
    asyncio.run(parse_dpkg())
