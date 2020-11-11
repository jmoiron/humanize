"""Main package for humanize."""
import sys

from humanize.filesize import naturalsize
from humanize.i18n import activate, deactivate
from humanize.number import apnumber, fractional, intcomma, intword, ordinal, scientific
from humanize.time import (
    naturaldate,
    naturalday,
    naturaldelta,
    naturaltime,
    precisedelta,
)

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata

__version__ = VERSION = importlib_metadata.version(__package__)


__all__ = [
    "__version__",
    "activate",
    "apnumber",
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
    "VERSION",
]
