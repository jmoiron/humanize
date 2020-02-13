#!/usr/bin/env python

"""Tests for time humanizing."""

import datetime as dt
from unittest.mock import patch

import pytest
from freezegun import freeze_time
from humanize import time

from .base import HumanizeTestCase

ONE_DAY_DELTA = dt.timedelta(days=1)

# In seconds
ONE_MICROSECOND = 1 / 1000000
FOUR_MICROSECONDS = 4 / 1000000
ONE_MILLISECOND = 1 / 1000
FOUR_MILLISECONDS = 4 / 1000
ONE_HOUR = 3600
ONE_DAY = 24 * ONE_HOUR
ONE_YEAR = 365.25 * ONE_DAY

with freeze_time("2020-02-02"):
    TODAY = dt.date.today()
    TOMORROW = TODAY + ONE_DAY_DELTA
    YESTERDAY = TODAY - ONE_DAY_DELTA


class FakeDate:
    def __init__(self, year, month, day):
        self.year, self.month, self.day = year, month, day


VALUE_ERROR_TEST = FakeDate(290149024, 2, 2)
OVERFLOW_ERROR_TEST = FakeDate(120390192341, 2, 2)


class TimeUtilitiesTestCase(HumanizeTestCase):
    """These are not considered "public" interfaces, but require tests anyway."""

    def test_date_and_delta(self):
        now = dt.datetime.now()
        td = dt.timedelta
        int_tests = (3, 29, 86399, 86400, 86401 * 30)
        date_tests = [now - td(seconds=x) for x in int_tests]
        td_tests = [td(seconds=x) for x in int_tests]
        results = [(now - td(seconds=x), td(seconds=x)) for x in int_tests]
        for t in (int_tests, date_tests, td_tests):
            for arg, result in zip(t, results):
                date, d = time.date_and_delta(arg)
                self.assertEqualDatetime(date, result[0])
                self.assertEqualTimedelta(d, result[1])
        self.assertEqual(time.date_and_delta("NaN"), (None, "NaN"))


class TimeTestCase(HumanizeTestCase):
    """Tests for the public interface of humanize.time"""

    def test_naturaldelta_nomonths(self):
        now = dt.datetime.now()
        test_list = [
            dt.timedelta(days=7),
            dt.timedelta(days=31),
            dt.timedelta(days=230),
            dt.timedelta(days=400),
        ]
        result_list = [
            "7 days",
            "31 days",
            "230 days",
            "1 year, 35 days",
        ]
        with patch("humanize.time._now") as mocked:
            mocked.return_value = now

            def nd_nomonths(d):
                return time.naturaldelta(d, months=False)

            self.assertManyResults(nd_nomonths, test_list, result_list)

    def test_naturaldelta(self):
        now = dt.datetime.now()
        test_list = [
            0,
            1,
            30,
            dt.timedelta(minutes=1, seconds=30),
            dt.timedelta(minutes=2),
            dt.timedelta(hours=1, minutes=30, seconds=30),
            dt.timedelta(hours=23, minutes=50, seconds=50),
            dt.timedelta(days=1),
            dt.timedelta(days=500),
            dt.timedelta(days=365 * 2 + 35),
            dt.timedelta(seconds=1),
            dt.timedelta(seconds=30),
            dt.timedelta(minutes=1, seconds=30),
            dt.timedelta(minutes=2),
            dt.timedelta(hours=1, minutes=30, seconds=30),
            dt.timedelta(hours=23, minutes=50, seconds=50),
            dt.timedelta(days=1),
            dt.timedelta(days=500),
            dt.timedelta(days=365 * 2 + 35),
            # regression tests for bugs in post-release humanize
            dt.timedelta(days=10000),
            dt.timedelta(days=365 + 35),
            30,
            dt.timedelta(days=365 * 2 + 65),
            dt.timedelta(days=365 + 4),
            dt.timedelta(days=35),
            dt.timedelta(days=65),
            dt.timedelta(days=9),
            dt.timedelta(days=365),
            "NaN",
        ]
        result_list = [
            "a moment",
            "a second",
            "30 seconds",
            "a minute",
            "2 minutes",
            "an hour",
            "23 hours",
            "a day",
            "1 year, 4 months",
            "2 years",
            "a second",
            "30 seconds",
            "a minute",
            "2 minutes",
            "an hour",
            "23 hours",
            "a day",
            "1 year, 4 months",
            "2 years",
            "27 years",
            "1 year, 1 month",
            "30 seconds",
            "2 years",
            "1 year, 4 days",
            "a month",
            "2 months",
            "9 days",
            "a year",
            "NaN",
        ]
        with patch("humanize.time._now") as mocked:
            mocked.return_value = now
            self.assertManyResults(time.naturaldelta, test_list, result_list)

    def test_naturaltime(self):
        now = dt.datetime.now()
        test_list = [
            now,
            now - dt.timedelta(seconds=1),
            now - dt.timedelta(seconds=30),
            now - dt.timedelta(minutes=1, seconds=30),
            now - dt.timedelta(minutes=2),
            now - dt.timedelta(hours=1, minutes=30, seconds=30),
            now - dt.timedelta(hours=23, minutes=50, seconds=50),
            now - dt.timedelta(days=1),
            now - dt.timedelta(days=500),
            now - dt.timedelta(days=365 * 2 + 35),
            now + dt.timedelta(seconds=1),
            now + dt.timedelta(seconds=30),
            now + dt.timedelta(minutes=1, seconds=30),
            now + dt.timedelta(minutes=2),
            now + dt.timedelta(hours=1, minutes=30, seconds=30),
            now + dt.timedelta(hours=23, minutes=50, seconds=50),
            now + dt.timedelta(days=1),
            now + dt.timedelta(days=500),
            now + dt.timedelta(days=365 * 2 + 35),
            # regression tests for bugs in post-release humanize
            now + dt.timedelta(days=10000),
            now - dt.timedelta(days=365 + 35),
            30,
            now - dt.timedelta(days=365 * 2 + 65),
            now - dt.timedelta(days=365 + 4),
            "NaN",
        ]
        result_list = [
            "now",
            "a second ago",
            "30 seconds ago",
            "a minute ago",
            "2 minutes ago",
            "an hour ago",
            "23 hours ago",
            "a day ago",
            "1 year, 4 months ago",
            "2 years ago",
            "a second from now",
            "30 seconds from now",
            "a minute from now",
            "2 minutes from now",
            "an hour from now",
            "23 hours from now",
            "a day from now",
            "1 year, 4 months from now",
            "2 years from now",
            "27 years from now",
            "1 year, 1 month ago",
            "30 seconds ago",
            "2 years ago",
            "1 year, 4 days ago",
            "NaN",
        ]
        with patch("humanize.time._now") as mocked:
            mocked.return_value = now
            self.assertManyResults(time.naturaltime, test_list, result_list)

    def test_naturaltime_nomonths(self):
        now = dt.datetime.now()
        test_list = [
            now,
            now - dt.timedelta(seconds=1),
            now - dt.timedelta(seconds=30),
            now - dt.timedelta(minutes=1, seconds=30),
            now - dt.timedelta(minutes=2),
            now - dt.timedelta(hours=1, minutes=30, seconds=30),
            now - dt.timedelta(hours=23, minutes=50, seconds=50),
            now - dt.timedelta(days=1),
            now - dt.timedelta(days=17),
            now - dt.timedelta(days=47),
            now - dt.timedelta(days=500),
            now - dt.timedelta(days=365 * 2 + 35),
            now + dt.timedelta(seconds=1),
            now + dt.timedelta(seconds=30),
            now + dt.timedelta(minutes=1, seconds=30),
            now + dt.timedelta(minutes=2),
            now + dt.timedelta(hours=1, minutes=30, seconds=30),
            now + dt.timedelta(hours=23, minutes=50, seconds=50),
            now + dt.timedelta(days=1),
            now + dt.timedelta(days=500),
            now + dt.timedelta(days=365 * 2 + 35),
            # regression tests for bugs in post-release humanize
            now + dt.timedelta(days=10000),
            now - dt.timedelta(days=365 + 35),
            30,
            now - dt.timedelta(days=365 * 2 + 65),
            now - dt.timedelta(days=365 + 4),
            "NaN",
        ]
        result_list = [
            "now",
            "a second ago",
            "30 seconds ago",
            "a minute ago",
            "2 minutes ago",
            "an hour ago",
            "23 hours ago",
            "a day ago",
            "17 days ago",
            "47 days ago",
            "1 year, 135 days ago",
            "2 years ago",
            "a second from now",
            "30 seconds from now",
            "a minute from now",
            "2 minutes from now",
            "an hour from now",
            "23 hours from now",
            "a day from now",
            "1 year, 135 days from now",
            "2 years from now",
            "27 years from now",
            "1 year, 35 days ago",
            "30 seconds ago",
            "2 years ago",
            "1 year, 4 days ago",
            "NaN",
        ]
        with patch("humanize.time._now") as mocked:
            mocked.return_value = now

            def nt_nomonths(d):
                return time.naturaltime(d, months=False)

            self.assertManyResults(nt_nomonths, test_list, result_list)


@freeze_time("2020-02-02")
@pytest.mark.parametrize(
    "test_input, expected",
    [
        (TODAY, "today"),
        (TOMORROW, "tomorrow"),
        (YESTERDAY, "yesterday"),
        (dt.date(TODAY.year, 3, 5), "Mar 05"),
        ("02/26/1984", "02/26/1984"),
        (None, None),
        ("Not a date at all.", "Not a date at all."),
        (VALUE_ERROR_TEST, VALUE_ERROR_TEST),
        (OVERFLOW_ERROR_TEST, OVERFLOW_ERROR_TEST),
    ],
)
def test_naturalday(test_input, expected):
    assert time.naturalday(test_input) == expected


@freeze_time("2020-02-02")
@pytest.mark.parametrize(
    "test_value, test_format, expected",
    [(dt.date(1982, 6, 27), "%Y.%m.%d", "1982.06.27")],
)
def test_naturalday_format(test_value, test_format, expected):
    assert time.naturalday(test_value, test_format) == expected


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
    ],
)
def test_naturaldate(test_input, expected):
    assert time.naturaldate(test_input) == expected


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
    assert time.naturaldelta(delta) == expected


@pytest.mark.parametrize(
    "minimum_unit, seconds, expected",
    [
        ("seconds", ONE_MICROSECOND, "a moment"),
        ("seconds", FOUR_MICROSECONDS, "a moment"),
        ("seconds", ONE_MILLISECOND, "a moment"),
        ("seconds", FOUR_MILLISECONDS, "a moment"),
        ("seconds", 2, "2 seconds"),
        ("seconds", 4, "4 seconds"),
        ("seconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour"),
        ("seconds", ONE_DAY + FOUR_MILLISECONDS, "a day"),
        ("seconds", ONE_YEAR + FOUR_MICROSECONDS, "a year"),
        ("microseconds", ONE_MICROSECOND, "1 microsecond"),
        ("microseconds", FOUR_MICROSECONDS, "4 microseconds"),
        ("microseconds", 2, "2 seconds"),
        ("microseconds", 4, "4 seconds"),
        ("microseconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour"),
        ("microseconds", ONE_DAY + FOUR_MILLISECONDS, "a day"),
        ("microseconds", ONE_YEAR + FOUR_MICROSECONDS, "a year"),
        ("milliseconds", ONE_MILLISECOND, "1 millisecond"),
        ("milliseconds", FOUR_MILLISECONDS, "4 milliseconds"),
        ("milliseconds", 2, "2 seconds"),
        ("milliseconds", 4, "4 seconds"),
        ("milliseconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour"),
        ("milliseconds", ONE_YEAR + FOUR_MICROSECONDS, "a year"),
    ],
)
def test_naturaldelta_minimum_unit_explicit(minimum_unit, seconds, expected):
    # Arrange
    delta = dt.timedelta(seconds=seconds)

    # Act / Assert
    assert time.naturaldelta(delta, minimum_unit=minimum_unit) == expected


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
    assert time.naturaltime(delta) == expected


@pytest.mark.parametrize(
    "minimum_unit, seconds, expected",
    [
        ("seconds", ONE_MICROSECOND, "now"),
        ("seconds", FOUR_MICROSECONDS, "now"),
        ("seconds", ONE_MILLISECOND, "now"),
        ("seconds", FOUR_MILLISECONDS, "now"),
        ("seconds", 2, "2 seconds ago"),
        ("seconds", 4, "4 seconds ago"),
        ("seconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour ago"),
        ("seconds", ONE_DAY + FOUR_MILLISECONDS, "a day ago"),
        ("seconds", ONE_YEAR + FOUR_MICROSECONDS, "a year ago"),
        ("microseconds", ONE_MICROSECOND, "1 microsecond ago"),
        ("microseconds", FOUR_MICROSECONDS, "4 microseconds ago"),
        ("microseconds", 2, "2 seconds ago"),
        ("microseconds", 4, "4 seconds ago"),
        ("microseconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour ago"),
        ("microseconds", ONE_DAY + FOUR_MILLISECONDS, "a day ago"),
        ("microseconds", ONE_YEAR + FOUR_MICROSECONDS, "a year ago"),
        ("milliseconds", ONE_MILLISECOND, "1 millisecond ago"),
        ("milliseconds", FOUR_MILLISECONDS, "4 milliseconds ago"),
        ("milliseconds", 2, "2 seconds ago"),
        ("milliseconds", 4, "4 seconds ago"),
        ("milliseconds", ONE_HOUR + FOUR_MILLISECONDS, "an hour ago"),
        ("milliseconds", ONE_YEAR + FOUR_MICROSECONDS, "a year ago"),
    ],
)
def test_naturaltime_minimum_unit_explicit(minimum_unit, seconds, expected):
    # Arrange
    delta = dt.timedelta(seconds=seconds)

    # Act / Assert
    assert time.naturaltime(delta, minimum_unit=minimum_unit) == expected
