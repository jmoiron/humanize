humanize
--------

.. image:: https://secure.travis-ci.org/jmoiron/humanize.png?branch=master
  :target: http://travis-ci.org/jmoiron/humanize

This modest package contains various common humanization utilities, like turning
a number into a fuzzy human readable duration ('3 minutes ago') or into a human
readable size or throughput.  It works with python 2.7 and 3.3 and is localized
to Russian, French, Korean and Slovak.

usage
-----

Integer humanization::

    >>> import humanize
    >>> humanize.intcomma(12345)
    '12,345'
    >>> humanize.intword(123455913)
    '123.5 million'
    >>> humanize.intword(12345591313)
    '12.3 billion'
    >>> humanize.apnumber(4)
    'four'
    >>> humanize.apnumber(41)
    '41'

Date & time humanization::

    >>> import datetime
    >>> humanize.naturalday(datetime.datetime.now())
    'today'
    >>> humanize.naturaldelta(datetime.timedelta(seconds=1001))
    '16 minutes'
    >>> humanize.naturalday(datetime.datetime.now() - datetime.timedelta(days=1))
    'yesterday'
    >>> humanize.naturalday(datetime.date(2007, 6, 5))
    'Jun 05'
    >>> humanize.naturaldate(datetime.date(2007, 6, 5))
    'Jun 05 2007'
    >>> humanize.naturaltime(datetime.datetime.now() - datetime.timedelta(seconds=1))
    'a second ago'
    >>> humanize.naturaltime(datetime.datetime.now() - datetime.timedelta(seconds=3600))
    'an hour ago'
    >>> humanize.naturaltime(datetime.datetime.now() - datetime.timedelta(seconds=7000))
    'an hour ago'
    >>> humanize.naturaltime(datetime.datetime.now() - datetime.timedelta(seconds=7000), precise=True)
    '1.9 hours ago'

Filesize humanization::

    >>> humanize.naturalsize(1000000)
    '1.0 MB'
    >>> humanize.naturalsize(1000000, binary=True)
    '976.6 KiB'
    >>> humanize.naturalsize(1000000, gnu=True)
    '976.6K'


Human readable floating point numbers::

    >>> humanize.fractional(1/3)
    '1/3'
    >>> humanize.fractional(1.5)
    '1 1/2'
    >>> humanize.fractional(0.3)
    '3/10'
    >>> humanize.fractional(0.333)
    '1/3'
    >>> humanize.fractional(1)
    '1'

Localization
------------

How to change locale in runtime ::

    >>> print humanize.naturaltime(datetime.timedelta(seconds=3))
    3 seconds ago
    >>> _t = humanize.i18n.activate('ru_RU')
    >>> print humanize.naturaltime(datetime.timedelta(seconds=3))
    3 секунды назад
    >>> humanize.i18n.deactivate()
    >>> print humanize.naturaltime(datetime.timedelta(seconds=3))
    3 seconds ago

You can pass additional parameter *path* to :func:`activate` to specify a path to
search locales in. ::

    >>> humanize.i18n.activate('pt_BR')
    IOError: [Errno 2] No translation file found for domain: 'humanize'
    >>> humanize.i18n.activate('pt_BR', path='path/to/my/portuguese/translation/')
    <gettext.GNUTranslations instance ...>

How to add new phrases to existing locale files ::

    $ xgettext -o humanize.pot -k'_' -k'N_' -k'P_:1c,2' -l python humanize/*.py  # extract new phrases
    $ msgmerge -U humanize/locale/ru_RU/LC_MESSAGES/humanize.po humanize.pot # add them to locale files
    $ msgfmt --check -o humanize/locale/ru_RU/LC_MESSAGES/humanize{.mo,.po} # compile to binary .mo

How to add new locale ::

    $ msginit -i humanize.pot -o humanize/locale/<locale name>/LC_MESSAGES/humanize.po --locale <locale name>

Where <locale name> is locale abbreviation, eg 'en_GB', 'pt_BR' or just 'ru', 'fr' etc.
