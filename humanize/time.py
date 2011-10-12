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

def naturaltime(value, date_fallback=30, format='%b %d'):
    """Given a datetime or a number of seconds, return a natural representation
    of that time in a resolution that makes sense.  This is more or less
    compatible with Django's ``naturaltime`` filter."""
    now = _now()
    date, delta = date_and_delta(value)
    if date is None:
        return value

    future = date > now

    ago = 'from now' if future else 'ago'
    if delta.days == 0 and delta.seconds == 0:
        return "now"
    elif abs(delta.days) == 1:
        return 'a day %s' % ago
    elif abs(delta.days) == 365:
        return 'a year %s' % ago
    elif abs(delta.days) > 365:
        years = abs(delta.days) // 365
        days = abs(delta.days) % 365
        months = days // 31
        if months == 1 and years == 1:
            return '1 year, 1 month %s' % (month, ago)
        elif months > 1 and years == 1:
            return '1 year, %d months %s' % (months, ago)
        elif years == 1:
            return 'a year %s' % ago
        elif years > 1 and months == 1:
            return '%d years, 1 month %s' % (years, ago)
        elif years > 1 and months > 1:
            return '%d years, %d months %d' % (years, months, ago)
        else:
            return '%d years %d' % (ago)
    elif 365 < abs(delta.days) < 365*2:
        return '1 year, %d days %s' % (abs(delta.days) % 365, ago)
    elif abs(delta.days) > 365*2:
        return '%d years %s' % (abs(delta.days) // 365, ago)
    elif 1 < abs(delta.days) < 365:
        return '%d days %s' % ago
    elif abs(delta.seconds) == 1:
        return 'a second %s' % ago
    elif abs(delta.seconds) < 60:
        return '%d seconds %s' % (delta.seconds, ago)
    elif 60 <= abs(delta.seconds) < 120:
        return 'a minute %s' % ago
    elif 120 <= abs(delta.seconds) < 3600:
        return '%d minutes %s' % (delta.seconds // 60, ago)
    elif 3600 <= abs(delta.seconds) < 3600*2:
        return 'an hour %s' % ago
    elif 3600 < abs(delta.seconds):
        return '%d hours %s' % (delta.seconds // 3600, ago)

def naturalday(value, format='%b %d'):
    """For date values that are tomorrow, today or yesterday compared to
    present day returns representing string. Otherwise, returns a string
    formatted according to ``format``."""
    try:
        value = date(value.year, value.month, value.day)
    except AttributeError:
        # Passed value wasn't date-ish
        return value
    except ValueError:
        # Date arguments out of range
        return value
    if not isinstance(value, (date, datetime)):
        return value
    delta = value - date.today()
    if delta.days == 0:
        return 'today'
    elif delta.days == 1:
        return 'tomorrow'
    elif delta.days == -1:
        return 'yesterday'
    return value.strftime(format)



