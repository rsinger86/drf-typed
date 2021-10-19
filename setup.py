#!/usr/bin/env python
from codecs import open

from setuptools import find_packages, setup


def readme():
    with open("README.md", "r") as infile:
        return infile.read()


classifiers = [
    # Pick your license as you wish (should match "license" above)
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.6",
]
setup(
    name="drf-typed",
    version="0.1.1",
    description="Use type annotations for request validation and serializer fields in Django REST Framework",
    author="Robert Singer",
    author_email="robertgsinger@gmail.com",
    packages=["rest_typed", "rest_framework-stubs"],
    url="https://github.com/rsinger86/drf-typed",
    license="MIT",
    keywords="django rest type annotations automatic validation validate",
    long_description=readme(),
    classifiers=classifiers,
    long_description_content_type="text/markdown",
)
