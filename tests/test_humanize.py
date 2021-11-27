"""Other tests."""
import sys

import pytest

import humanize


def test_version():
    if sys.version_info >= (3, 7):
        with pytest.warns(DeprecationWarning):
            VERSION = humanize.VERSION
    else:
        VERSION = humanize.VERSION

    assert VERSION == humanize.__version__
