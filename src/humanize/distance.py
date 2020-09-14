#!/usr/bin/env python

"""Distance humanizing functions for Django's GIS Distance."""

from django.contrib.gis.measure import Distance


class DistanceRounding:
    """Defines constants related to distance rounding."""

    QUARTER = 0.25
    HALF = 0.5

    ROUNDING_OPTIONS = [QUARTER, HALF]


class DistanceConfig:
    """Defines constants useful for unit conversion and formatting."""

    # Approximate metric to imperial equivalence for granularity
    IMPERIAL = {"mm": "inch", "cm": "inch", "m": "ft", "km": "mi"}

    # Singular and plural format of each unit
    LONG_NAMES = {
        # TODO: translate per locale
        "mm": ["milimiter", "milimeters"],
        "cm": ["centimiter", "centimeters"],
        "m": ["meter", "meters"],
        "km": ["kilometer", "kilometers"],
        "inch": ["inch", "inches"],
        "ft": ["foot", "feet"],
        "mi": ["mile", "miles"],
    }


class DistanceTranslation:
    """Defines dictionaries that can be used as custom translations of units."""

    # can be imported as custom translation
    COMMONWEALTH = {
        "milimiter": "milimitre",
        "milimiters": "milimitres",
        "centimeter": "centimetre",
        "centimeters": "centimetres",
        "meter": "metre",
        "meters": "metres",
        "kilometer": "kilometre",
        "kilometers": "kilometres",
    }


def _round_base(value, base):
    return round(value * base) / base


def _perform_rounding(value, rounding):
    """Rounds distances to closest 0.25 or 0.5."""
    if not value.is_integer():
        base = 4 if rounding == DistanceRounding.QUARTER else 2

        return _round_base(value, base)

    if value > 100:
        base = 25 if rounding == DistanceRounding.QUARTER else 50

        return _round_base(value, base)

    return value


def get_unit(d, imperial):
    """Gets unit most representative for granularity."""
    if d.m < 0.01:
        return "mm"
    if d.m < 1:
        return "cm"
    if imperial and d.mi > 0.1:
        # avoid thousands of feet, go to miles representation
        return "km"
    if d.m < 1000:
        return "m"
    if d.m < 10_000:
        return "km"


def _get_formatted_unit(value, unit, long_names, custom_translation):
    """Performs singular/plural, translation adjustments to unit."""
    if long_names:
        singular, plural = DistanceConfig.LONG_NAMES[unit]
        formatted_unit = singular if value == float(1) else plural
    else:
        formatted_unit = unit

    if formatted_unit not in custom_translation:
        # TODO: add locale-based translation
        return formatted_unit

    return custom_translation[formatted_unit]


def humanize_distance(
    d: Distance,
    imperial=False,
    long_names=False,
    precision=2,
    rounding=None,
    custom_translation={},
):
    """Return a natural representation of Django GIS Distance objects.

    Args:
        d (Distance): Distance object to be humanized
        imperial (bool): Specifies whether to use imperial measurements
            (inches, feet, miles). Defaults to `False`.
        long_names (bool): If `True`, long unit names will be used of
            abbreviations (e.g. kilometer instead of km). Defaults to `False`
        precision (int): Specifies how many decimals after the floating point
            should be used when formatting distances. Defaults to 2.
        rounding (None, humanize.distance.DistanceRounding): Enables rounding to
            nearest 0.25 or 0.5 for floating values, nearest 25 or 50 for
            values larger than 100, respectively. Good for larger distances,
            where approximation is needed. Defaults to `None`.
        custom_translation (dict): Specifies any custom translations of the
            units, e.g. `{'kilometers': 'Kilometer'}`. If a key is not found,
            it will not be translated. Use
            humanize.distance.DistanceTranslation.COMMONWEALTH for
            commonwealth spelling (e.g. 'metre' instead of 'meter').
            Defaults to empty dictionary.
    """
    unit = get_unit(d, imperial)

    if rounding and rounding not in DistanceRounding.ROUNDING_OPTIONS:
        rounding = DistanceRounding.QUARTER

    if imperial:
        unit = DistanceConfig.IMPERIAL[unit]

    value = getattr(d, unit)
    if rounding:
        value = _perform_rounding(value, rounding)

    formatted_unit = _get_formatted_unit(value, unit, long_names, custom_translation)

    # TODO: add human numerals and fractions, e.g. two kilometers, half a mile
    return "{} {}".format(
        round(value, precision) if not value.is_integer() else int(value),
        formatted_unit,
    )
