humanize
-----------

This modest package contains various common humanization utilities, like turning
a number into a fuzzy human readable duration ('3 minutes ago') or into a human
readable size or throughput.

usage
-----

Integer humanization::

    >>> import humanize
    >>> humanize.intcomma(12345)
    '12,345'
    >>> humanize.intword(123455913)
    '123.5 million'
    >>> humanize.intword(12345591313)
    '12.3 billion'
    >>> humanize.apnumber(4)
    'four'
    >>> humanize.apnumber(41)
    '41'

Date & time humanization::

    >>> import datetime
    >>> humanize.naturalday(datetime.datetime.now())
    'today'
    >>> humanize.naturalday(datetime.datetime.now() - datetime.timedelta(days=1))
    'yesterday'
    >>> humanize.naturaltime(datetime.datetime.now() - datetime.timedelta(seconds=1))
    'a second ago'
    >>> humanize.naturaltime(datetime.datetime.now() - datetime.timedelta(seconds=3600))
    'an hour ago'

Filesize humanization::

    >>> humanize.naturalsize(1000000)
    '1.0 MB'
    >>> humanize.naturalsize(1000000, binary=True)
    '976.6 KiB'
    >>> humanize.naturalsize(1000000, gnu=True)
    '976.6K'


Human readable floating point numbers::

    >>> humanize.fractional(1/3)
    '1/3'
    >>> humanize.fractional(1.5)
    '1 1/2'
    >>> humanize.fractional(0.3)
    '3/10'
    >>> humanize.fractional(0.333)
    '1/3'
    >>> humanize.fractional(1)
    '1'
