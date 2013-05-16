# -*- coding: utf-8 -*-
import gettext as gettext_module
from threading import local
import os.path

__all__ = ['activate', 'deactivate', 'gettext', 'ngettext']

_TRANSLATIONS = {None: gettext_module.NullTranslations()}
_CURRENT = local()

_DEFAULT_LOCALE_PATH = os.path.join(os.path.dirname(__file__), 'locale')


def get_translation():
    try:
        return _TRANSLATIONS[_CURRENT.locale]
    except (AttributeError, KeyError):
        return _TRANSLATIONS[None]


def activate(locale, path=None):
    """Set 'locale' as current locale. Search for locale in directory 'path'
    @param locale: language name, eg 'en_GB'"""
    if path is None:
        path = _DEFAULT_LOCALE_PATH
    translation = gettext_module.translation('humanize', path, [locale])
    _TRANSLATIONS[locale] = translation
    _CURRENT.locale = locale
    return translation


def deactivate():
    _CURRENT.locale = None


def gettext(message):
    return get_translation().gettext(message)


def ngettext(message, plural, num):
    return get_translation().ngettext(message, plural, num)


def gettext_noop(message):
    """Example usage:
    CONSTANTS = [gettext_noop('first'), gettext_noop('second')]
    def num_name(n):
        return gettext(CONSTANTS[n])"""
    return message
