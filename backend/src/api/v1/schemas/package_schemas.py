from pydantic import BaseModel, ConfigDict, computed_field, Field
from typing import List, Optional

from src.config.base import settings


class DependencySchema(BaseModel):
    dependency_package: str

    model_config = ConfigDict(from_attributes=True)

    @computed_field(return_type=str)
    def url(self):
        package_name = self.dependency_package.split(" (")[0]
        return f"http://{settings.server_address}/api/v1/packages/{package_name}"


class ReverseDependencySchema(BaseModel):
    package_id: int = Field(exclude=True)
    dependent_package: str

    model_config = ConfigDict(from_attributes=True)

    @computed_field(return_type=str)
    def url(self):
        return f"http://{settings.server_address}/api/v1/packages/{self.package_id}"


class PackageSchema(BaseModel):
    id: int
    name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    dependencies: List[DependencySchema] = []
    reverse_dependencies: List[ReverseDependencySchema] = []

    model_config = ConfigDict(from_attributes=True)
