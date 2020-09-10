#!/usr/bin/env python

"""Tests for time humanizing."""

import datetime as dt

import humanize
import pytest
from freezegun import freeze_time
from humanize import time

ONE_DAY_DELTA = dt.timedelta(days=1)

# In seconds
ONE_MICROSECOND = 1 / 1000000
FOUR_MICROSECONDS = 4 / 1000000
ONE_MILLISECOND = 1 / 1000
FOUR_MILLISECONDS = 4 / 1000
MICROSECONDS_101_943 = 101943 / 1000000  # 101.94 milliseconds
MILLISECONDS_1_337 = 1337 / 1000  # 1.337 seconds
ONE_HOUR = 3600
ONE_DAY = 24 * ONE_HOUR
ONE_YEAR = 365.25 * ONE_DAY

with freeze_time("2020-02-02"):
    NOW = dt.datetime.now()
    TODAY = dt.date.today()
    TOMORROW = TODAY + ONE_DAY_DELTA
    YESTERDAY = TODAY - ONE_DAY_DELTA


class FakeDate:
    def __init__(self, year, month, day):
        self.year, self.month, self.day = year, month, day


VALUE_ERROR_TEST = FakeDate(290149024, 2, 2)
OVERFLOW_ERROR_TEST = FakeDate(120390192341, 2, 2)


def assertEqualDatetime(dt1, dt2):
    assert (dt1 - dt2).seconds == 0


def assertEqualTimedelta(td1, td2):
    assert td1.days == td2.days
    assert td1.seconds == td2.seconds


# These are not considered "public" interfaces, but require tests anyway.


def test_date_and_delta():
    now = dt.datetime.now()
    td = dt.timedelta
    int_tests = (3, 29, 86399, 86400, 86401 * 30)
    date_tests = [now - td(seconds=x) for x in int_tests]
    td_tests = [td(seconds=x) for x in int_tests]
    results = [(now - td(seconds=x), td(seconds=x)) for x in int_tests]
    for t in (int_tests, date_tests, td_tests):
        for arg, result in zip(t, results):
            date, d = time.date_and_delta(arg)
            assertEqualDatetime(date, result[0])
            assertEqualTimedelta(d, result[1])
    assert time.date_and_delta("NaN") == (None, "NaN")


# Tests for the public interface of humanize.time


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (dt.timedelta(days=7), "7 days"),
        (dt.timedelta(days=31), "31 days"),
        (dt.timedelta(days=230), "230 days"),
        (dt.timedelta(days=400), "1 year, 35 days"),
    ],
)
def test_naturaldelta_nomonths(test_input, expected):
    assert humanize.naturaldelta(test_input, months=False) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (0, "a moment"),
        (1, "a second"),
        (dt.timedelta(seconds=1), "a second"),
        (30, "30 seconds"),
        (dt.timedelta(seconds=30), "30 seconds"),
        (dt.timedelta(seconds=59), "59 seconds"),
        (dt.timedelta(minutes=1, seconds=0), "a minute"),
        (dt.timedelta(minutes=1, seconds=1), "a minute"),
        (dt.timedelta(minutes=1, seconds=29), "a minute"),
        (dt.timedelta(minutes=1, seconds=30), "2 minutes"),
        (dt.timedelta(minutes=1, seconds=59), "2 minutes"),
        (dt.timedelta(minutes=2, seconds=0), "2 minutes"),
        (dt.timedelta(minutes=2, seconds=1), "2 minutes"),
        (dt.timedelta(minutes=2, seconds=59), "3 minutes"),
        (dt.timedelta(minutes=3, seconds=10), "3 minutes"),
        (dt.timedelta(hours=1, minutes=25, seconds=30), "an hour"),
        (dt.timedelta(hours=1, minutes=30, seconds=30), "2 hours"),
        (2 * 60 * 60 - 1, "2 hours"),  # 2 hours minus 1 second
        (2 * 60 * 60 + 1, "2 hours"),  # 2 hours plus 1 second
        (dt.timedelta(hours=22, minutes=50, seconds=50), "23 hours"),
        (dt.timedelta(hours=23, minutes=10, seconds=10), "23 hours"),
        (dt.timedelta(hours=23, minutes=50, seconds=50), "a day"),
        (dt.timedelta(hours=24, minutes=10, seconds=10), "a day"),
        (dt.timedelta(days=1), "a day"),
        (dt.timedelta(days=9), "9 days"),
        (dt.timedelta(days=25), "a month"),
        (dt.timedelta(days=35), "a month"),
        (dt.timedelta(days=65), "2 months"),
        (dt.timedelta(days=170), "6 months"),  # ~5.6 months
        (dt.timedelta(days=365), "a year"),
        (dt.timedelta(days=365 + 4), "1 year, 4 days"),
        (dt.timedelta(days=365 + 35), "1 year, 1 month"),
        (dt.timedelta(days=500), "1 year, 4 months"),
        (2 * 365 * 24 * 60 * 60 - 1, "2 years"),  # 2 years minus 1 second
        (2 * 365 * 24 * 60 * 60 + 1, "2 years"),  # 2 years plus 1 second
        (dt.timedelta(days=365 * 2 + 35), "2 years"),
        (dt.timedelta(days=365 * 2 + 65), "2 years"),
        (dt.timedelta(days=10000), "27 years"),
        ("NaN", "NaN"),
    ],
)
def test_naturaldelta(test_input, expected):
    assert humanize.naturaldelta(test_input) == expected


@freeze_time("2020-02-02")
@pytest.mark.parametrize(
    "test_input, expected",
    [
        (NOW, "now"),
        (NOW - dt.timedelta(seconds=1), "a second ago"),
        (NOW - dt.timedelta(seconds=30), "30 seconds ago"),
        (NOW - dt.timedelta(minutes=1, seconds=30), "a minute ago"),
        (NOW - dt.timedelta(minutes=2), "2 minutes ago"),
        (NOW - dt.timedelta(hours=1, minutes=30, seconds=30), "an hour ago"),
        (NOW - dt.timedelta(hours=23, minutes=50, seconds=50), "23 hours ago"),
        (NOW - dt.timedelta(days=1), "a day ago"),
        (NOW - dt.timedelta(days=500), "1 year, 4 months ago"),
        (NOW - dt.timedelta(days=365 * 2 + 35), "2 years ago"),
        (NOW + dt.timedelta(seconds=1), "a second from now"),
        (NOW + dt.timedelta(seconds=30), "30 seconds from now"),
        (NOW + dt.timedelta(minutes=1, seconds=30), "a minute from now"),
        (NOW + dt.timedelta(minutes=2), "2 minutes from now"),
        (NOW + dt.timedelta(hours=1, minutes=30, seconds=30), "an hour from now"),
        (NOW + dt.timedelta(hours=23, minutes=50, seconds=50), "23 hours from now"),
        (NOW + dt.timedelta(days=1), "a day from now"),
        (NOW + dt.timedelta(days=500), "1 year, 4 months from now"),
        (NOW + dt.timedelta(days=365 * 2 + 35), "2 years from now"),
        # regression tests for bugs in post-release humanize
        (NOW + dt.timedelta(days=10000), "27 years from now"),
        (NOW - dt.timedelta(days=365 + 35), "1 year, 1 month ago"),
        (30, "30 seconds ago"),
        (NOW - dt.timedelta(days=365 * 2 + 65), "2 years ago"),
        (NOW - dt.timedelta(days=365 + 4), "1 year, 4 days ago"),
        ("NaN", "NaN"),
    ],
)
def test_naturaltime(test_input, expected):
    assert humanize.naturaltime(test_input) == expected


@freeze_time("2020-02-02")
@pytest.mark.parametrize(
    "test_input, expected",
    [
        (NOW, "now"),
        (NOW - dt.timedelta(seconds=1), "a second ago"),
        (NOW - dt.timedelta(seconds=30), "30 seconds ago"),
        (NOW - dt.timedelta(minutes=1, seconds=30), "a minute ago"),
        (NOW - dt.timedelta(minutes=2), "2 minutes ago"),
        (NOW - dt.timedelta(hours=1, minutes=30, seconds=30), "an hour ago"),
        (NOW - dt.timedelta(hours=23, minutes=50, seconds=50), "23 hours ago"),
        (NOW - dt.timedelta(days=1), "a day ago"),
        (NOW - dt.timedelta(days=17), "17 days ago"),
        (NOW - dt.timedelta(days=47), "47 days ago"),
        (NOW - dt.timedelta(days=500), "1 year, 135 days ago"),
        (NOW - dt.timedelta(days=365 * 2 + 35), "2 years ago"),
        (NOW + dt.timedelta(seconds=1), "a second from now"),
        (NOW + dt.timedelta(seconds=30), "30 seconds from now"),
        (NOW + dt.timedelta(minutes=1, seconds=30), "a minute from now"),
        (NOW + dt.timedelta(minutes=2), "2 minutes from now"),
        (NOW + dt.timedelta(hours=1, minutes=30, seconds=30), "an hour from now"),
        (NOW + dt.timedelta(hours=23, minutes=50, seconds=50), "23 hours from now"),
        (NOW + dt.timedelta(days=1), "a day from now"),
        (NOW + dt.timedelta(days=500), "1 year, 135 days from now"),
        (NOW + dt.timedelta(days=365 * 2 + 35), "2 years from now"),
        # regression tests for bugs in post-release humanize
        (NOW + dt.timedelta(days=10000), "27 years from now"),
        (NOW - dt.timedelta(days=365 + 35), "1 year, 35 days ago"),
        (30, "30 seconds ago"),
        (NOW - dt.timedelta(days=365 * 2 + 65), "2 years ago"),
        (NOW - dt.timedelta(days=365 + 4), "1 year, 4 days ago"),
        ("NaN", "NaN"),
    ],
)
def test_naturaltime_nomonths(test_input, expected):
    assert humanize.naturaltime(test_input, months=False) == expected


@freeze_time("2020-02-02")
@pytest.mark.parametrize(
    "test_args, expected",
    [
        ([TODAY], "today"),
        ([TOMORROW], "tomorrow"),
        ([YESTERDAY], "yesterday"),
        ([dt.date(TODAY.year, 3, 5)], "Mar 05"),
        (["02/26/1984"], "02/26/1984"),
        ([dt.date(1982, 6, 27), "%Y.%m.%d"], "1982.06.27"),
        ([None], None),
        (["Not a date at all."], "Not a date at all."),
        ([VALUE_ERROR_TEST], VALUE_ERROR_TEST),
        ([OVERFLOW_ERROR_TEST], OVERFLOW_ERROR_TEST),
    ],
)
def test_naturalday(test_args, expected):
    assert humanize.naturalday(*test_args) == expected


@freeze_time("2020-02-02")
@pytest.mark.parametrize(
    "test_input, expected",
    [
        (TODAY, "today"),
        (TOMORROW, "tomorrow"),
        (YESTERDAY, "yesterday"),
        (dt.date(TODAY.year, 3, 5), "Mar 05"),
        (dt.date(1982, 6, 27), "Jun 27 1982"),
        (None, None),
        ("Not a date at all.", "Not a date at all."),
        (VALUE_ERROR_TEST, VALUE_ERROR_TEST),
        (OVERFLOW_ERROR_TEST, OVERFLOW_ERROR_TEST),
        (dt.date(2019, 2, 2), "Feb 02 2019"),
        (dt.date(2019, 3, 2), "Mar 02 2019"),
        (dt.date(2019, 4, 2), "Apr 02 2019"),
        (dt.date(2019, 5, 2), "May 02 2019"),
        (dt.date(2019, 6, 2), "Jun 02 2019"),
        (dt.date(2019, 7, 2), "Jul 02 2019"),
        (dt.date(2019, 8, 2), "Aug 02 2019"),
        (dt.date(2019, 9, 2), "Sep 02 2019"),
        (dt.date(2019, 10, 2), "Oct 02"),
        (dt.date(2019, 11, 2), "Nov 02"),
        (dt.date(2019, 12, 2), "Dec 02"),
        (dt.date(2020, 1, 2), "Jan 02"),
        (dt.date(2020, 2, 2), "today"),
        (dt.date(2020, 3, 2), "Mar 02"),
        (dt.date(2020, 4, 2), "Apr 02"),
        (dt.date(2020, 5, 2), "May 02"),
        (dt.date(2020, 6, 2), "Jun 02"),
        (dt.date(2020, 7, 2), "Jul 02"),
        (dt.date(2020, 8, 2), "Aug 02 2020"),
        (dt.date(2020, 9, 2), "Sep 02 2020"),
        (dt.date(2020, 10, 2), "Oct 02 2020"),
        (dt.date(2020, 11, 2), "Nov 02 2020"),
        (dt.date(2020, 12, 2), "Dec 02 2020"),
        (dt.date(2021, 1, 2), "Jan 02 2021"),
        (dt.date(2021, 2, 2), "Feb 02 2021"),
    ],
)
def test_naturaldate(test_input, expected):
    assert humanize.naturaldate(test_input) == expected


@pytest.mark.parametrize(
    "seconds, expected",
    [
        (ONE_MICROSECOND, "a moment"),
        (FOUR_MICROSECONDS, "a moment"),
        (ONE_MILLISECOND, "a moment"),
        (FOUR_MILLISECONDS, "a moment"),
        (2, "2 seconds"),
        (4, "4 seconds"),
        (ONE_HOUR + FOUR_MILLISECONDS, "an hour"),
        (ONE_DAY + FOUR_MILLISECONDS, "a day"),
        (ONE_YEAR + FOUR_MICROSECONDS, "a year"),
    ],
)
def test_naturaldelta_minimum_unit_default(seconds, expected):
    # Arrange
    delta = dt.timedelta(seconds=seconds)

    # Act / Assert
    assert humanize.naturaldelta(delta) == expected


@pytest.mark.parametrize(
    "minimum_unit, seconds, expected",
    [
        ("seconds", ONE_MICROSECOND, "a moment"),
        ("seconds", FOUR_MICROSECONDS, "a moment"),
        ("seconds", ONE_MILLISECOND, "a moment"),
        ("seconds", FOUR_MILLISECONDS, "a moment"),
        ("seconds", MICROSECONDS_101_943, "a moment"),  # 0.10194 s
        ("seconds", MILLISECONDS_1_337, "a second"),  # 1.337 s
        ("seconds", 2, "2 seconds"),
        ("seconds", 4, "4 seconds"),
        ("seconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour"),
        ("seconds", ONE_DAY + FOUR_MILLISECONDS, "a day"),
        ("seconds", ONE_YEAR + FOUR_MICROSECONDS, "a year"),
        ("microseconds", ONE_MICROSECOND, "1 microsecond"),
        ("microseconds", FOUR_MICROSECONDS, "4 microseconds"),
        ("microseconds", FOUR_MILLISECONDS, "4 milliseconds"),
        ("microseconds", MICROSECONDS_101_943, "102 milliseconds"),  # 101,940 µs
        ("microseconds", MILLISECONDS_1_337, "a second"),  # 1,337,000 µs
        ("microseconds", 2, "2 seconds"),
        ("microseconds", 4, "4 seconds"),
        ("microseconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour"),
        ("microseconds", ONE_DAY + FOUR_MILLISECONDS, "a day"),
        ("microseconds", ONE_YEAR + FOUR_MICROSECONDS, "a year"),
        ("milliseconds", FOUR_MICROSECONDS, "0 milliseconds"),
        ("milliseconds", ONE_MILLISECOND, "1 millisecond"),
        ("milliseconds", FOUR_MILLISECONDS, "4 milliseconds"),
        ("milliseconds", MICROSECONDS_101_943, "102 milliseconds"),
        ("milliseconds", MILLISECONDS_1_337, "a second"),
        ("milliseconds", 2, "2 seconds"),
        ("milliseconds", 4, "4 seconds"),
        ("milliseconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour"),
        ("milliseconds", ONE_YEAR + FOUR_MICROSECONDS, "a year"),
        # Seconds are rounded to nearest
        ("seconds", 0.1, "a moment"),
        ("seconds", 0.4, "a moment"),
        ("seconds", 0.6, "a second"),
        ("seconds", 0.9, "a second"),
        ("seconds", 1.1, "a second"),
        ("seconds", 1.4, "a second"),
        ("seconds", 1.6, "2 seconds"),
        ("seconds", 1.9, "2 seconds"),
        # Milliseconds are rounded to nearest
        ("milliseconds", 0.1 * ONE_MILLISECOND, "0 milliseconds"),
        ("milliseconds", 0.4 * ONE_MILLISECOND, "0 milliseconds"),
        ("milliseconds", 0.6 * ONE_MILLISECOND, "1 millisecond"),
        ("milliseconds", 0.9 * ONE_MILLISECOND, "1 millisecond"),
        ("milliseconds", 1.1 * ONE_MILLISECOND, "1 millisecond"),
        ("milliseconds", 1.4 * ONE_MILLISECOND, "1 millisecond"),
        ("milliseconds", 1.6 * ONE_MILLISECOND, "2 milliseconds"),
        ("milliseconds", 1.9 * ONE_MILLISECOND, "2 milliseconds"),
        # Microseconds are rounded to nearest
        ("microseconds", 0.1 * ONE_MICROSECOND, "0 microseconds"),
        ("microseconds", 0.4 * ONE_MICROSECOND, "0 microseconds"),
        ("microseconds", 0.6 * ONE_MICROSECOND, "1 microsecond"),
        ("microseconds", 0.9 * ONE_MICROSECOND, "1 microsecond"),
        ("microseconds", 1.1 * ONE_MICROSECOND, "1 microsecond"),
        ("microseconds", 1.4 * ONE_MICROSECOND, "1 microsecond"),
        ("microseconds", 1.6 * ONE_MICROSECOND, "2 microseconds"),
        ("microseconds", 1.9 * ONE_MICROSECOND, "2 microseconds"),
    ],
)
def test_naturaldelta_minimum_unit_explicit(minimum_unit, seconds, expected):
    # Arrange
    delta = dt.timedelta(seconds=seconds)

    # Act / Assert
    assert humanize.naturaldelta(delta, minimum_unit=minimum_unit) == expected


@pytest.mark.parametrize(
    "seconds, expected",
    [
        (ONE_MICROSECOND, "now"),
        (FOUR_MICROSECONDS, "now"),
        (ONE_MILLISECOND, "now"),
        (FOUR_MILLISECONDS, "now"),
        (2, "2 seconds ago"),
        (4, "4 seconds ago"),
        (ONE_HOUR + FOUR_MILLISECONDS, "an hour ago"),
        (ONE_DAY + FOUR_MILLISECONDS, "a day ago"),
        (ONE_YEAR + FOUR_MICROSECONDS, "a year ago"),
    ],
)
def test_naturaltime_minimum_unit_default(seconds, expected):
    # Arrange
    delta = dt.timedelta(seconds=seconds)

    # Act / Assert
    assert humanize.naturaltime(delta) == expected


@pytest.mark.parametrize(
    "minimum_unit, seconds, expected",
    [
        ("seconds", ONE_MICROSECOND, "now"),
        ("seconds", FOUR_MICROSECONDS, "now"),
        ("seconds", ONE_MILLISECOND, "now"),
        ("seconds", FOUR_MILLISECONDS, "now"),
        ("seconds", MICROSECONDS_101_943, "now"),  # 0.10194 s
        ("seconds", MILLISECONDS_1_337, "a second ago"),  # 1.337 s
        ("seconds", 2, "2 seconds ago"),
        ("seconds", 4, "4 seconds ago"),
        ("seconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour ago"),
        ("seconds", ONE_DAY + FOUR_MILLISECONDS, "a day ago"),
        ("seconds", ONE_YEAR + FOUR_MICROSECONDS, "a year ago"),
        ("milliseconds", FOUR_MICROSECONDS, "0 milliseconds ago"),
        ("milliseconds", ONE_MILLISECOND, "1 millisecond ago"),
        ("milliseconds", FOUR_MILLISECONDS, "4 milliseconds ago"),
        ("milliseconds", MICROSECONDS_101_943, "101 milliseconds ago"),  # 101.94 ms
        ("milliseconds", MILLISECONDS_1_337, "a second ago"),  # 1,337 ms
        ("milliseconds", 2, "2 seconds ago"),
        ("milliseconds", 4, "4 seconds ago"),
        ("milliseconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour ago"),
        ("milliseconds", ONE_YEAR + FOUR_MICROSECONDS, "a year ago"),
        ("microseconds", ONE_MICROSECOND, "1 microsecond ago"),
        ("microseconds", FOUR_MICROSECONDS, "4 microseconds ago"),
        ("microseconds", FOUR_MILLISECONDS, "4 milliseconds ago"),
        ("microseconds", MICROSECONDS_101_943, "101 milliseconds ago"),  # 101,940 µs
        ("microseconds", MILLISECONDS_1_337, "a second ago"),  # 1,337,000 µs
        ("microseconds", 2, "2 seconds ago"),
        ("microseconds", 4, "4 seconds ago"),
        ("microseconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour ago"),
        ("microseconds", ONE_DAY + FOUR_MILLISECONDS, "a day ago"),
        ("microseconds", ONE_YEAR + FOUR_MICROSECONDS, "a year ago"),
    ],
)
def test_naturaltime_minimum_unit_explicit(minimum_unit, seconds, expected):
    # Arrange
    delta = dt.timedelta(seconds=seconds)

    # Act / Assert
    assert humanize.naturaltime(delta, minimum_unit=minimum_unit) == expected


@pytest.mark.parametrize(
    "val, min_unit, expected",
    [
        (dt.timedelta(microseconds=1), "microseconds", "1 microsecond"),
        (dt.timedelta(microseconds=2), "microseconds", "2 microseconds"),
        (dt.timedelta(microseconds=1000), "microseconds", "1 millisecond"),
        (dt.timedelta(microseconds=2000), "microseconds", "2 milliseconds"),
        (dt.timedelta(seconds=1), "seconds", "1 second"),
        (1, "seconds", "1 second"),
        (2, "seconds", "2 seconds"),
        (60, "seconds", "1 minute"),
        (120, "seconds", "2 minutes"),
        (3600, "seconds", "1 hour"),
        (3600 * 2, "seconds", "2 hours"),
        (3600 * 24, "seconds", "1 day"),
        (3600 * 24 * 2, "seconds", "2 days"),
        (3600 * 24 * 365, "seconds", "1 year"),
        (3600 * 24 * 365 * 2, "seconds", "2 years"),
    ],
)
def test_precisedelta_one_unit_enough(val, min_unit, expected):
    assert humanize.precisedelta(val, minimum_unit=min_unit) == expected


@pytest.mark.parametrize(
    "val, min_unit, expected",
    [
        (
            dt.timedelta(microseconds=1001),
            "microseconds",
            "1 millisecond and 1 microsecond",
        ),
        (
            dt.timedelta(microseconds=2002),
            "microseconds",
            "2 milliseconds and 2 microseconds",
        ),
        (
            dt.timedelta(seconds=1, microseconds=2),
            "microseconds",
            "1 second and 2 microseconds",
        ),
        (
            dt.timedelta(hours=4, seconds=3, microseconds=2),
            "microseconds",
            "4 hours, 3 seconds and 2 microseconds",
        ),
        (
            dt.timedelta(days=5, hours=4, seconds=3, microseconds=2),
            "microseconds",
            "5 days, 4 hours, 3 seconds and 2 microseconds",
        ),
        (
            dt.timedelta(days=370, hours=4, seconds=3, microseconds=2),
            "microseconds",
            "1 year, 5 days, 4 hours, 3 seconds and 2 microseconds",
        ),
        (
            dt.timedelta(days=370, microseconds=2),
            "microseconds",
            "1 year, 5 days and 2 microseconds",
        ),
        (
            dt.timedelta(days=370, seconds=2),
            "microseconds",
            "1 year, 5 days and 2 seconds",
        ),
    ],
)
def test_precisedelta_multiple_units(val, min_unit, expected):
    assert humanize.precisedelta(val, minimum_unit=min_unit) == expected


@pytest.mark.parametrize(
    "val, min_unit, fmt, expected",
    [
        (
            dt.timedelta(microseconds=1001),
            "milliseconds",
            "%0.4f",
            "1.0010 milliseconds",
        ),
        (
            dt.timedelta(microseconds=2002),
            "milliseconds",
            "%0.4f",
            "2.0020 milliseconds",
        ),
        (dt.timedelta(microseconds=2002), "milliseconds", "%0.2f", "2.00 milliseconds"),
        (
            dt.timedelta(seconds=1, microseconds=230000),
            "seconds",
            "%0.2f",
            "1.23 seconds",
        ),
        (
            dt.timedelta(hours=4, seconds=3, microseconds=200000),
            "seconds",
            "%0.2f",
            "4 hours and 3.20 seconds",
        ),
        (
            dt.timedelta(days=5, hours=4, seconds=30 * 60),
            "seconds",
            "%0.2f",
            "5 days, 4 hours and 30 minutes",
        ),
        (
            dt.timedelta(days=5, hours=4, seconds=30 * 60),
            "hours",
            "%0.2f",
            "5 days and 4.50 hours",
        ),
        (dt.timedelta(days=5, hours=4, seconds=30 * 60), "days", "%0.2f", "5.19 days"),
        (dt.timedelta(days=120), "months", "%0.2f", "3.93 months"),
        (dt.timedelta(days=183), "years", "%0.1f", "0.5 years"),
    ],
)
def test_precisedelta_custom_format(val, min_unit, fmt, expected):
    assert humanize.precisedelta(val, minimum_unit=min_unit, format=fmt) == expected


@pytest.mark.parametrize(
    "val, min_unit, suppress, expected",
    [
        (
            dt.timedelta(microseconds=1200),
            "microseconds",
            [],
            "1 millisecond and 200 microseconds",
        ),
        (
            dt.timedelta(microseconds=1200),
            "microseconds",
            ["milliseconds"],
            "1200 microseconds",
        ),
        (
            dt.timedelta(microseconds=1200),
            "microseconds",
            ["microseconds"],
            "1.20 milliseconds",
        ),
        (
            dt.timedelta(seconds=1, microseconds=200),
            "microseconds",
            ["seconds"],
            "1000 milliseconds and 200 microseconds",
        ),
        (
            dt.timedelta(seconds=1, microseconds=200000),
            "microseconds",
            ["milliseconds"],
            "1 second and 200000 microseconds",
        ),
        (
            dt.timedelta(seconds=1, microseconds=200000),
            "microseconds",
            ["milliseconds", "microseconds"],
            "1.20 seconds",
        ),
        (
            dt.timedelta(hours=4, seconds=30, microseconds=200),
            "microseconds",
            ["microseconds"],
            "4 hours, 30 seconds and 0.20 milliseconds",
        ),
        (
            dt.timedelta(hours=4, seconds=30, microseconds=200),
            "microseconds",
            ["seconds"],
            "4 hours, 30000 milliseconds and 200 microseconds",
        ),
        (
            dt.timedelta(hours=4, seconds=30, microseconds=200),
            "microseconds",
            ["seconds", "milliseconds"],
            "4 hours and 30000200 microseconds",
        ),
        (
            dt.timedelta(hours=4, seconds=30, microseconds=200),
            "microseconds",
            ["hours"],
            "240 minutes, 30 seconds and 200 microseconds",
        ),
        (
            dt.timedelta(hours=4, seconds=30, microseconds=200),
            "microseconds",
            ["hours", "seconds", "milliseconds", "microseconds"],
            "240.50 minutes",
        ),
    ],
)
def test_precisedelta_suppress_units(val, min_unit, suppress, expected):
    assert (
        humanize.precisedelta(val, minimum_unit=min_unit, suppress=suppress) == expected
    )


def test_precisedelta_bogus_call():
    assert humanize.precisedelta(None) is None

    with pytest.raises(ValueError):
        humanize.precisedelta(1, minimum_unit="years", suppress=["years"])

    with pytest.raises(ValueError):
        humanize.naturaldelta(1, minimum_unit="years")


def test_time_unit():
    years, minutes = time._Unit["YEARS"], time._Unit["MINUTES"]
    assert minutes < years
    assert years > minutes
    assert minutes == minutes

    with pytest.raises(TypeError):
        years < "foo"
