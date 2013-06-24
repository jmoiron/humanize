# -*- coding: utf-8 -*-
import logging
import gettext as gettext_module
from threading import local
import os.path

try:
    from django.utils import translation as django_translation

except ImportError:
    django_translation = None # NOQA

LOGGER = logging.getLogger(__name__)

__all__ = ['activate', 'deactivate', 'gettext', 'ngettext', 'django_language']

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


class django_language(object):
    """ a context manager for easy language switching in Django. Usage::

            with django_language():
                humanize.whatever(…)

        And that's all. It runs activate with the current django language
        in the current thread.

    """

    def __enter__(self):
        if django_translation is None:
            return

        current_lang = django_translation.get_language()

        if current_lang != 'en':
            try:
                # TODO: find a way to do this automatically, application-wide…
                activate(current_lang, path=os.path.join(
                         os.path.dirname(__file__), 'locale'))
            except:
                # Humanize will crash badly if it find no gettext message file.
                # But we shouldn't because it's harmless, in the end.
                LOGGER.warning(u'could not switch `humanize` i18n to %s, '
                               u'its translations will appear in english.',
                               current_lang)

    def __exit__(self, *args, **kwargs):
        try:
            deactivate()

        except:
            pass
