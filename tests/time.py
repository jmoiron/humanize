#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for time humanizing."""

from mock import patch, Mock
from itertools import izip, chain

from humanize import time
from datetime import date, datetime, timedelta
from base import HumanizeTestCase

today = date.today()
one_day = timedelta(days=1)

class TimeUtilitiesTestCase(HumanizeTestCase):
    """These are not considered "public" interfaces, but require tests anyway."""
    def test_date_and_delta(self):
        now = datetime.now()
        td = timedelta
        int_tests = (3, 29, 86399, 86400, 86401*30)
        date_tests = [now - td(seconds=x) for x in int_tests]
        td_tests = [td(seconds=x) for x in int_tests]
        results = [(now - td(seconds=x), td(seconds=x)) for x in int_tests]
        for t in (int_tests, date_tests, td_tests):
            for arg, result in izip(t, results):
                dt, d = time.date_and_delta(arg)
                self.assertEqualDatetime(dt, result[0])
                self.assertEqualTimedelta(d, result[1])

class TimeTestCase(HumanizeTestCase):
    """Tests for the public interface of humanize.time"""

    def test_naturaltime(self):
        now = datetime.now()
        test_list = [
            now,
            now - timedelta(seconds=1),
            now - timedelta(seconds=30),
            now - timedelta(minutes=1, seconds=30),
            now - timedelta(minutes=2),
            now - timedelta(hours=1, minutes=30, seconds=30),
            now - timedelta(hours=23, minutes=50, seconds=50),
            now - timedelta(days=1),
            now - timedelta(days=500),
            now - timedelta(days=365*2 + 35),
            now + timedelta(seconds=1),
            now + timedelta(seconds=30),
            now + timedelta(minutes=1, seconds=30),
            now + timedelta(minutes=2),
            now + timedelta(hours=1, minutes=30, seconds=30),
            now + timedelta(hours=23, minutes=50, seconds=50),
            now + timedelta(days=1),
            now + timedelta(days=500),
            now + timedelta(days=365*2 + 35),
        ]
        result_list = [
            'now',
            'a second ago',
            '30 seconds ago',
            'a minute ago',
            '2 minutes ago',
            'an hour ago',
            '23 hours ago',
            'a day ago',
            '1 year, 4 months ago',
            '2 years, 1 month ago',
            'a second from now',
            '30 seconds from now',
            'a minute from now',
            '2 minutes from now',
            'an hour from now',
            '23 hours from now',
            'a day from now',
            '1 year, 4 months from now',
            '2 years, 1 month from now',
        ]
        with patch('humanize.time._now') as mocked:
            mocked.return_value = now
            self.assertManyResults(time.naturaltime, test_list, result_list)

    def test_naturalday(self):
        tomorrow = today + one_day
        yesterday = today - one_day
        someday = today - timedelta(10)
        test_list = (today, tomorrow, yesterday, someday, '02/26/1984',
            (date(1982, 6, 27), '%Y.%M.%D'), None, "Not a date at all.")
        result_list = ('today', 'tomorrow', 'yesterday', 'Sep 29', '02/26/1984',
            date(1982, 6, 27).strftime('%Y.%M.%D'), None, "Not a date at all.")
        self.assertManyResults(time.naturalday, test_list, result_list)

