#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for humanize."""

import io

from setuptools import find_packages, setup

with io.open("README.md", encoding="UTF-8") as f:
    long_description = f.read()


version = "0.5.1"


setup(
    name="humanize",
    version=version,
    description="Python humanize utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jason Moiron",
    author_email="jmoiron@jmoiron.net",
    url="https://github.com/jmoiron/humanize",
    license="MIT",
    keywords="humanize time size",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    entry_points="""
    # -*- Entry points: -*-
    """,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    extras_require={
        "tests": ["freezegun", "pytest", "pytest-cov"],
        "tests:python_version < '3.4'": ["mock"],
    },
    # Get strings from https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
