"""Main package for humanize."""
import pkg_resources

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

__version__ = VERSION = pkg_resources.get_distribution(__name__).version


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
