"""Main package for humanize."""

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
]
