#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for humanize."""

from setuptools import setup, find_packages
import io

version = '0.5.1'

setup(
    name='humanize',
    version=version,
    description="python humanize utilities",
    long_description=io.open('README.rst', 'r', encoding="UTF-8").read(),
    extras_require = {
        "tests": ["pytest", "pytest-cov"],
        "tests:python_version < '3.4'": ["mock"],
    },
    # Get strings from https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    keywords='humanize time size',
    author='Jason Moiron',
    author_email='jmoiron@jmoiron.net',

    url='https://github.com/jmoiron/humanize',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
      # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
