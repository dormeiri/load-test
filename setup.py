import re

from setuptools import setup, find_packages


def find_version(filename):
    with open(filename) as f:
        pattern = r'__version__ = "(.*)"'
        m = next(re.match(pattern, line) for line in f)
        return m.group(1)


def read(filename):
    with open(filename) as f:
        return f.read()


setup(
    name="load_test",
    version=find_version("load_test/__init__.py"),
    description="Abstraction for load testing",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Dor Meiri",
    author_email="dormeiri@gmail.com",
    url="https://github.com/dormeiri/load-test",
    packages=find_packages("load_test"),
    package_dir={"": "load_test"},
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    project_urls={
        "Issues": "https://github.com/dormeiri/load-test/issues",
    },
)
