#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for humanize."""

from setuptools import setup, find_packages
import sys, os

version = '0.3'

# some trove classifiers:


setup(
    name='humanize',
    version=version,
    description="python humanize utilities",
    long_description=open('README.rst').read(),
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
    ],
    keywords='humanize time size',
    author='Jason Moiron',
    author_email='jmoiron@jmoiron.net',

    url='http://github.com/jmoiron/humanize',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite="tests",
    install_requires=[
      # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
