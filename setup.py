#!/usr/bin/env python
from codecs import open

from setuptools import find_packages, setup
import os


def readme():
    with open("README.md", "r") as infile:
        return infile.read()


def find_stub_files(name):
    result = []
    for root, dirs, files in os.walk(name):
        for file in files:
            if file.endswith(".pyi"):
                if os.path.sep in root:
                    sub_root = root.split(os.path.sep, 1)[-1]
                    file = os.path.join(sub_root, file)
                result.append(file)
    return result


classifiers = [
    # Pick your license as you wish (should match "license" above)
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.6",
]
setup(
    name="drf-typed",
    version="0.1.3",
    description="Use type annotations for request validation and serializer fields in Django REST Framework",
    author="Robert Singer",
    author_email="robertgsinger@gmail.com",
    packages=find_packages(exclude=["test_project*"]) + ["rest_framework-stubs"],
    package_data={"rest_framework-stubs": find_stub_files("rest_framework-stubs")},
    url="https://github.com/rsinger86/drf-typed",
    license="MIT",
    keywords="django rest type annotations automatic validation validate",
    long_description=readme(),
    classifiers=classifiers,
    long_description_content_type="text/markdown",
)
