from setuptools import Command, find_packages, setup
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="productdata",  # Required
    version="1.0.0",  # Required
    description="product crawler",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    author="Justin Kwok",  # Optional
    author_email="bluetinkwok@gmail.com",  # Optional
    classifiers=[  # Optional
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="product comparsion, python",  # Optional
    packages=find_packages(exclude=["importlib", "pymysql", "pandas"]),
)