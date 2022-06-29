#!/usr/bin/env python3

from setuptools import setup, find_packages


setup(
    packages=find_packages(where="native") +
    find_packages(),
    package_dir={
        "": "native",
        "demos": "demos"

    }
)
