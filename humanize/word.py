#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Humanizing functions for numbers."""

import pronouncing


def pronounce(word):
    """
    Uses pronouncing library to give pronounciation of any word (English
    and non-English). "Pronunciations are given using a special
    phonetic alphabet known as ARPAbet."

    Parameters
    ----------
    word:       str

    Retruns
    -------
    pronounced_raw_string:  str
                            pronounciation for word ("The number 1
                            indicates primary stress; 2 indicates
                            secondary stress; and 0 indicates unstressed")
    """
    pronounced_raw = pronouncing.phones_for_word(word)
    pronounced_raw_string = pronounced_raw[0].encode('ascii')
    return pronounced_raw_string
