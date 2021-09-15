from setuptools import setup

setup(
    name="piate",
    version="0.1.1",
    packages=["piate"],
    url="https://www.github.com/drewsonne/piate",
    license="Apache",
    author="drew",
    author_email="drew.sonne@gmail.com",
    description="Python Library to interact with the IATE database",
    install_requires=["requests", "requests_oauthlib", "dataclasses-json", "click"],
    entry_points={"console_scripts": ["iate=piate.cli:run"]},
)
