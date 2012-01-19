#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Time humanizing functions.  These are largely borrowed from Django's
``contrib.humanize``."""

import time
from datetime import datetime, timedelta, date

__all__ = ['naturaltime', 'naturalday']

def _now():
    return datetime.now()

def abs_timedelta(delta):
    """Returns an "absolute" value for a timedelta, always representing a
    time distance."""
    if delta.days < 0:
        now = _now()
        return now - (now + delta)
    return delta

def date_and_delta(value):
    """Turn a value into a date and a timedelta which represents how long ago
    it was.  If that's not possible, return (None, value)."""
    now = _now()
    if isinstance(value, datetime):
        date = value
        delta = now - value
    elif isinstance(value, timedelta):
        date = now - value
        delta = value
    else:
        try:
            value = int(value)
            delta = timedelta(seconds=value)
            date = now - delta
        except (ValueError, TypeError):
            return (None, value)
    return date, abs_timedelta(delta)

def naturaldelta(value, months=True):
    """Given a timedelta or a number of seconds, return a natural
    representation of the amount of time elapsed.  This is similar to
    ``naturaltime``, but does not add tense to the result.  If ``months``
    is True, then a number of months (based on 30.5 days) will be used
    for fuzziness between years."""
    now = _now()
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
            return "a moment"
        elif seconds == 1:
            return "a second"
        elif seconds < 60:
            return "%d seconds" % (seconds)
        elif 60 <= seconds < 120:
            return "a minute"
        elif 120 <= seconds < 3600:
            return "%d minutes" % (seconds // 60)
        elif 3600 <= seconds < 3600*2:
            return "an hour"
        elif 3600 < seconds:
            return "%d hours" % (seconds // 3600)
    elif years == 0:
        if days == 1:
            return "a day"
        if not use_months:
            return "%d days" % days
        else:
            if not months:
                return "%d days" % days
            elif months == 1:
                return "a month"
            else:
                return "%d months" % months
    elif years == 1:
        if not months and not days:
            return "a year"
        elif not months:
            return "1 year, %d days" % days
        elif use_months:
            if months == 1:
                return "1 year, 1 month"
            else:
                return "1 year, %d months" % months
        else:
            return "1 year, %d days" % days
    else:
        return "%d years" % years


def naturaltime(value, future=False, months=True):
    """Given a datetime or a number of seconds, return a natural representation
    of that time in a resolution that makes sense.  This is more or less
    compatible with Django's ``naturaltime`` filter.  ``future`` is ignored for
    datetimes, where the tense is always figured out based on the current time.
    If an integer is passed, the return value will be past tense by default,
    unless ``future`` is set to True."""
    now = _now()
    date, delta = date_and_delta(value)
    if date is None:
        return value
    # determine tense by value only if datetime/timedelta were passed
    if isinstance(value, (datetime, timedelta)):
        future = date > now

    ago = 'from now' if future else 'ago'
    delta = naturaldelta(delta)

    if delta == "a moment":
        return "now"

    return "%s %s" % (delta, ago)

def naturalday(value, format='%b %d'):
    """For date values that are tomorrow, today or yesterday compared to
    present day returns representing string. Otherwise, returns a string
    formatted according to ``format``."""
    try:
        value = date(value.year, value.month, value.day)
    except AttributeError:
        # Passed value wasn't date-ish
        return value
    except (OverflowError, ValueError):
        # Date arguments out of range
        return value
    delta = value - date.today()
    if delta.days == 0:
        return 'today'
    elif delta.days == 1:
        return 'tomorrow'
    elif delta.days == -1:
        return 'yesterday'
    return value.strftime(format)



