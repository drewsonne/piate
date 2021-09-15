import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="piate",
    version="0.1.6",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    url="https://www.github.com/drewsonne/piate",
    license="Apache",
    author="Drew J. Sonne",
    author_email="drew.sonne@gmail.com",
    description="Python Library to interact with the IATE database",
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=["requests", "dataclasses-json", "click"],
    entry_points={"console_scripts": ["iate=piate.cli:run"]},
)
