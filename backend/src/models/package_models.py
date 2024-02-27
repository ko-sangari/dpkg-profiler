from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from src.database.common.dependencies import BaseSQL


class Package(BaseSQL):
    __tablename__ = "packages"

    name = Column(String, nullable=True, unique=True, index=True)
    version = Column(String, nullable=True)
    description = Column(String, nullable=True)

    dependencies = relationship("Dependency", backref="package")

    reverse_dependencies = relationship(
        "Dependency",
        primaryjoin="Package.name == foreign(Dependency.dependency_package)",
        backref="reverse_dependencies",
    )

    @classmethod
    def create_instance(cls, data):
        instance = cls()
        for key, value in data.items():
            if key == "package":
                setattr(instance, "name", value)
            elif hasattr(instance, key):
                setattr(instance, key, value)
        return instance


class Dependency(BaseSQL):
    __tablename__ = "dependencies"

    package_id = Column(Integer, ForeignKey("packages.id"))
    dependent_package = Column(String)
    dependency_package = Column(String)
