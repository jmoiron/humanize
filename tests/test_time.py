#!/usr/bin/env python

"""Tests for time humanizing."""

import datetime as dt
from unittest.mock import patch

from freezegun import freeze_time
from humanize import time

from .base import HumanizeTestCase

ONE_DAY = dt.timedelta(days=1)


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
    def test_naturalday(self):
        # Arrange
        today = dt.date.today()
        tomorrow = today + ONE_DAY
        yesterday = today - ONE_DAY

        someday = dt.date(today.year, 3, 5)
        someday_result = "Mar 05"

        valerrtest = FakeDate(290149024, 2, 2)
        overflowtest = FakeDate(120390192341, 2, 2)

        test_list = (
            today,
            tomorrow,
            yesterday,
            someday,
            "02/26/1984",
            (dt.date(1982, 6, 27), "%Y.%m.%d"),
            None,
            "Not a date at all.",
            valerrtest,
            overflowtest,
        )
        result_list = (
            "today",
            "tomorrow",
            "yesterday",
            someday_result,
            "02/26/1984",
            "1982.06.27",
            None,
            "Not a date at all.",
            valerrtest,
            overflowtest,
        )

        # Act / Assert
        self.assertManyResults(time.naturalday, test_list, result_list)

    @freeze_time("2020-02-02")
    def test_naturaldate(self):
        # Arrange
        today = dt.date.today()
        tomorrow = today + ONE_DAY
        yesterday = today - ONE_DAY

        someday = dt.date(today.year, 3, 5)
        someday_result = "Mar 05"

        test_list = (
            today,
            tomorrow,
            yesterday,
            someday,
            dt.date(1982, 6, 27),
            None,
            "Not a date at all.",
            VALUE_ERROR_TEST,
            OVERFLOW_ERROR_TEST,
        )
        result_list = (
            "today",
            "tomorrow",
            "yesterday",
            someday_result,
            "Jun 27 1982",
            None,
            "Not a date at all.",
            VALUE_ERROR_TEST,
            OVERFLOW_ERROR_TEST,
        )

        # Act / Assert
        self.assertManyResults(time.naturaldate, test_list, result_list)
