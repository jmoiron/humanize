#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Humanizing functions for numbers."""

import re
from fractions import Fraction


def ordinal(value):
    """Converts an integer to its ordinal as a string. 1 is '1st', 2 is '2nd',
    3 is '3rd', etc. Works for any integer or anything int() will turn into an
    integer.  Anything other value will have nothing done to it."""
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value
    t = ('th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th')
    if value % 100 in (11, 12, 13):  # special case
        return u"%d%s" % (value, t[0])
    return u'%d%s' % (value, t[value % 10])


def intcomma(value):
    """Converts an integer to a string containing commas every three digits.
    For example, 3000 becomes '3,000' and 45000 becomes '45,000'.  To maintain
    some compatability with Django's intcomma, this function also accepts
    floats."""
    try:
        if isinstance(value, basestring):
            float(value.replace(',', ''))
        else:
            float(value)
    except (TypeError, ValueError):
        return value
    orig = str(value)
    new = re.sub("^(-?\d+)(\d{3})", '\g<1>,\g<2>', orig)
    if orig == new:
        return new
    else:
        return intcomma(new)

powers = [10 ** x for x in (6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 100)]
human_powers = ('million', 'billion', 'trillion', 'quadrillion', 'quintillion',
    'sextillion', 'septillion', 'octillion', 'nonillion', 'decillion', 'googol')


def intword(value, format='%.1f'):
    """Converts a large integer to a friendly text representation. Works best for
    numbers over 1 million. For example, 1000000 becomes '1.0 million', 1200000
    becomes '1.2 million' and '1200000000' becomes '1.2 billion'.  Supports up to
    decillion (33 digits) and googol (100 digits).  You can pass format to change
    the number of decimal or general format of the number portion.  This function
    returns a string unless the value passed was unable to be coaxed into an int."""
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    if value < powers[0]:
        return str(value)
    for ordinal, power in enumerate(powers[1:], 1):
        if value < power:
            chopped = value / float(powers[ordinal - 1])
            return (' '.join([format, human_powers[ordinal - 1]])) % chopped
    return str(value)


def apnumber(value):
    """For numbers 1-9, returns the number spelled out. Otherwise, returns the
    number. This follows Associated Press style.  This always returns a string
    unless the value was not int-able, unlike the Django filter."""
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value
    if not 0 < value < 10:
        return str(value)
    return ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')[value - 1]


def fractional(value):
    '''
    There will be some cases where one might not want to show
        ugly decimal places for floats and decimals.
    This function returns a human readable fractional number
        in form of fractions and mixed fractions.
    Pass in a string, or a number or a float, and this function returns
        a string representation of a fraction
        or whole number
        or a mixed fraction
    Examples:
        fractional(0.3) will return '1/3'
        fractional(1.3) will return '1 3/10'
        fractional(float(1/3)) will return '1/3'
        fractional(1) will return '1'
    This will always return a string.
    '''
    try:
        number = float(value)
    except (TypeError, ValueError):
        return value
    wholeNumber = int(number)
    frac = Fraction(number - wholeNumber).limit_denominator(1000)
    numerator = frac._numerator
    denominator = frac._denominator
    if wholeNumber and not numerator and denominator == 1:
        return '%.0f' % wholeNumber  # this means that an integer was passed in (or variants of that integer like 1.0000)
    elif not wholeNumber:
        return '%.0f/%.0f' % (numerator, denominator)
    else:
        return '%.0f %.0f/%.0f' % (wholeNumber, numerator, denominator)
