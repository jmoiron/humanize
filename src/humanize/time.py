#!/usr/bin/env python

"""Time humanizing functions.  These are largely borrowed from Django's
``contrib.humanize``."""

import datetime as dt
from enum import Enum

from .i18n import gettext as _
from .i18n import ngettext

__all__ = ["naturaldelta", "naturaltime", "naturalday", "naturaldate"]


class Unit(Enum):
    MILLISECONDS = 0
    MICROSECONDS = 1
    SECONDS = 2


def _now():
    return dt.datetime.now()


def abs_timedelta(delta):
    """Returns an "absolute" value for a timedelta, always representing a
    time distance."""
    if delta.days < 0:
        now = _now()
        return now - (now + delta)
    return delta


def date_and_delta(value, *, now=None):
    """Turn a value into a date and a timedelta which represents how long ago
    it was.  If that's not possible, return (None, value)."""
    if not now:
        now = _now()
    if isinstance(value, dt.datetime):
        date = value
        delta = now - value
    elif isinstance(value, dt.timedelta):
        date = now - value
        delta = value
    else:
        try:
            value = int(value)
            delta = dt.timedelta(seconds=value)
            date = now - delta
        except (ValueError, TypeError):
            return None, value
    return date, abs_timedelta(delta)


def naturaldelta(value, months=True, minimum_unit="seconds"):
    """Return a natural representation of a timedelta or number of seconds.

    This is similar to naturaltime, but does not add tense to the result.

    Args:
        value: A timedelta or a number of seconds.
        months: If True, then a number of months (based on 30.5 days) will be used for
            fuzziness between years.
        minimum_unit: If microseconds or milliseconds, use those units for subsecond
            deltas.

    Returns:
        str: A natural representation of the amount of time elapsed.
    """
    minimum_unit = Unit[minimum_unit.upper()]
    date, delta = date_and_delta(value)
    if date is None:
        return value

    use_months = months

    seconds = abs(delta.seconds)
    days = abs(delta.days)
    years = days // 365
    days = days % 365
    months = int(days // 30.5)

    if not years and days < 1:
        if seconds == 0:
            if minimum_unit == Unit.MICROSECONDS:
                return (
                    ngettext("%d microsecond", "%d microseconds", delta.microseconds)
                    % delta.microseconds
                )
            elif minimum_unit == Unit.MILLISECONDS:
                milliseconds = delta.microseconds / 1000
                return (
                    ngettext("%d millisecond", "%d milliseconds", milliseconds)
                    % milliseconds
                )
            return _("a moment")
        elif seconds == 1:
            return _("a second")
        elif seconds < 60:
            return ngettext("%d second", "%d seconds", seconds) % seconds
        elif 60 <= seconds < 120:
            return _("a minute")
        elif 120 <= seconds < 3600:
            minutes = seconds // 60
            return ngettext("%d minute", "%d minutes", minutes) % minutes
        elif 3600 <= seconds < 3600 * 2:
            return _("an hour")
        elif 3600 < seconds:
            hours = seconds // 3600
            return ngettext("%d hour", "%d hours", hours) % hours
    elif years == 0:
        if days == 1:
            return _("a day")
        if not use_months:
            return ngettext("%d day", "%d days", days) % days
        else:
            if not months:
                return ngettext("%d day", "%d days", days) % days
            elif months == 1:
                return _("a month")
            else:
                return ngettext("%d month", "%d months", months) % months
    elif years == 1:
        if not months and not days:
            return _("a year")
        elif not months:
            return ngettext("1 year, %d day", "1 year, %d days", days) % days
        elif use_months:
            if months == 1:
                return _("1 year, 1 month")
            else:
                return (
                    ngettext("1 year, %d month", "1 year, %d months", months) % months
                )
        else:
            return ngettext("1 year, %d day", "1 year, %d days", days) % days
    else:
        return ngettext("%d year", "%d years", years) % years


def naturaltime(value, future=False, months=True, minimum_unit="seconds"):
    """Return a natural representation of a time in a resolution that makes sense.

    This is more or less compatible with Django's naturaltime filter.

    Args:
        value: A timedate or a number of seconds.
        future: Ignored for datetimes, where the tense is always figured out based on
            the current time. For integers, the return value will be past tense by
            default, unless future is True.
        months: If True, then a number of months (based on 30.5 days) will be used for
            fuzziness between years.
        minimum_unit: If microseconds or milliseconds, use those units for subsecond
            times.

    Returns:
        str: A natural representation of the input in a resolution that makes sense.
    """
    now = _now()
    date, delta = date_and_delta(value, now=now)
    if date is None:
        return value
    # determine tense by value only if datetime/timedelta were passed
    if isinstance(value, (dt.datetime, dt.timedelta)):
        future = date > now

    ago = _("%s from now") if future else _("%s ago")
    delta = naturaldelta(delta, months, minimum_unit)

    if delta == _("a moment"):
        return _("now")

    return ago % delta


def naturalday(value, format="%b %d"):
    """For date values that are tomorrow, today or yesterday compared to
    present day returns representing string. Otherwise, returns a string
    formatted according to ``format``."""
    try:
        value = dt.date(value.year, value.month, value.day)
    except AttributeError:
        # Passed value wasn't date-ish
        return value
    except (OverflowError, ValueError):
        # Date arguments out of range
        return value
    delta = value - dt.date.today()
    if delta.days == 0:
        return _("today")
    elif delta.days == 1:
        return _("tomorrow")
    elif delta.days == -1:
        return _("yesterday")
    return value.strftime(format)


def naturaldate(value):
    """Like naturalday, but append a year for dates more than about five months away.
    """
    try:
        value = dt.date(value.year, value.month, value.day)
    except AttributeError:
        # Passed value wasn't date-ish
        return value
    except (OverflowError, ValueError):
        # Date arguments out of range
        return value
    delta = abs_timedelta(value - dt.date.today())
    if delta.days >= 5 * 365 / 12:
        return naturalday(value, "%b %d %Y")
    return naturalday(value)
