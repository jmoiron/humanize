#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for filesize humanizing."""

from humanize import filesize
from .base import HumanizeTestCase

class FilesizeTestCase(HumanizeTestCase):
    def test_naturalsize(self):
        tests = (300, 3000, 3000000, 3000000000, 3000000000000, (300, True),
            (3000, True), (3000000, True), (300, False, True), (3000, False, True),
            (3000000, False, True), (1024, False, True), (10**26 * 30, False, True),
            (10**26 * 30, True), 10**26 * 30)
        results = ('300 Bytes', '3.0 kB', '3.0 MB', '3.0 GB', '3.0 TB',
            '300 Bytes', '2.9 KiB', '2.9 MiB', '300B', '2.9K', '2.9M', '1.0K', '2481.5Y',
            '2481.5 YiB', '3000.0 YB')
        self.assertManyResults(filesize.naturalsize, tests, results)

