#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for time humanizing."""

from humanize import time
from base import HumanizeTestCase

class TimeTestCase(HumanizeTestCase):

    def ordinal_test(self):
        test_list = ('1', '2', '3', '4', '11', '12', '13', '101', '102', '103',
            '111', 'something else', None)
        result_list = ('1st', '2nd', '3rd', '4th', '11th', '12th', '13th',
            '101st', '102nd', '103rd', '111th', 'something else', None)
        self.assertManyResults(time.ordinal, test_list, result_list)

