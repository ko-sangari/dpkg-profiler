from src.models.package_models import Package
from src.utils.parser import parse_package_info, file_parser


def test_parse_package_info(package_text, package_json):
    parsed_data = parse_package_info(package_text)
    assert parsed_data == package_json


def test_file_parser(package_text, package_file):
    packages = list(file_parser(package_file))
    assert len(packages) == 1

    package = packages[0]
    assert isinstance(package, Package)
    assert package.name == "dpkg"
    assert package.version == "1.19.7ubuntu3.2"
    assert package.description == "Debian package management system"
    assert len(package.dependencies) == 2
    dependency_names = [dep.dependency_package for dep in package.dependencies]
    assert "libacl1 (= 2.2.53-6)" in dependency_names
    assert "libc6 (>= 2.14)" in dependency_names
