from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="toml-lib",
    version="1.1.0",
    description="Allows for simple disk writing to keep persistent data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adu224256/tomllib",
    author="Sauce",
    author_email="saucejullyfish@gmail.com",
    license="GNU",
    packages=["tomllib"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["tomlkit"],
)