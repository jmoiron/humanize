from setuptools import find_packages, setup

with open("README.md", encoding="UTF-8") as f:
    long_description = f.read()


def local_scheme(version):
    """Skip the local version (eg. +xyz of 0.6.1.dev4+gdf99fe2)
    to be able to upload to Test PyPI"""
    return ""


setup(
    name="humanize",
    description="Python humanize utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jason Moiron",
    author_email="jmoiron@jmoiron.net",
    maintainer="Hugo van Kemenade",
    url="https://github.com/jmoiron/humanize",
    license="MIT",
    keywords="humanize time size",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    use_scm_version={"local_scheme": local_scheme},
    setup_requires=["setuptools_scm"],
    extras_require={"tests": ["freezegun", "pytest", "pytest-cov"]},
    python_requires=">=3.5",
    # Get strings from https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: General",
    ],
)
