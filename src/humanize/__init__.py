"""Main package for humanize."""

import sys
import warnings

from humanize.filesize import naturalsize
from humanize.i18n import activate, deactivate, thousands_separator
from humanize.number import (
    apnumber,
    clamp,
    fractional,
    intcomma,
    intword,
    ordinal,
    scientific,
)
from humanize.time import (
    naturaldate,
    naturalday,
    naturaldelta,
    naturaltime,
    precisedelta,
)

try:
    # Python 3.8+
    import importlib.metadata as importlib_metadata
except ImportError:
    # <Python 3.7 and lower
    import importlib_metadata

__version__ = importlib_metadata.version(__name__)


if sys.version_info >= (3, 7):
    # This technique isn't available for 3.6 but we don't need to warn for 3.6
    # because we'll drop 3.6 at the same time as removing this
    def __getattr__(name):
        if name == "VERSION":
            warnings.warn(
                "VERSION is deprecated and will be removed in humanize 4.0. "
                "Use __version__ instead, available since humanize 1.0 (Feb 2020).",
                DeprecationWarning,
                stacklevel=2,
            )
            return __version__
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


else:
    VERSION = __version__


__all__ = [
    "__version__",
    "activate",
    "apnumber",
    "clamp",
    "deactivate",
    "fractional",
    "intcomma",
    "intword",
    "naturaldate",
    "naturalday",
    "naturaldelta",
    "naturalsize",
    "naturaltime",
    "ordinal",
    "precisedelta",
    "scientific",
    "thousands_separator",
    "VERSION",
]
