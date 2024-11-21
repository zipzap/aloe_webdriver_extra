"""Gherkin steps to modify time/date in tests."""
from __future__ import absolute_import, print_function, unicode_literals

from datetime import datetime
from mock import patch
from time import sleep

from freezegun import freeze_time

from aloe import after, step, world


@step(r'I wait for (\d+) seconds?$')
def sleep_seconds(self, seconds):
    """
    Simple sleep function to wait for a number of seconds.

    :param self: Object reference to aloe. [Not used].
    :param seconds: Number of seconds to wait.
    :return: None.
    """

    sleep(int(seconds))


def unmock_time():
    """
    Stop mocking date, if active.

    :return: None.
    """

    try:
        world.freezer.stop()
        delattr(world, 'freezer')
    except AttributeError:
        pass


@step(r'Today\'s date is (\d{4}-\d{2}-\d{2})'
      r'(?: and time is (\d{,2}):(\d{2})h)?'
      r'(?: in timezone "([^"]*)")?$')
def mock_time(self, datestr, hour, minute, tzname):
    """
    Mock today's date.

    :param self: Object reference to aloe. [Not used].
    :param datestr: String representing the new date in the format YYYY-MM-DD.
    :param hour: Number representing the new time in 24h format. [Optional]
    :param minute: Number representing the new time. Between 0 and 59.
        [Optional, but required if the `hour` is specified.
    :param tzname: String representing the new timezone. [Optional].
    :return: None.
    """

    unmock_time()

    current_timezone = 'UTC'

    # Check if Django is installed.
    try:
        from django.conf import settings

        if settings.configured:
            current_timezone = settings.TIME_ZONE
    except ImportError:
        pass

    if not tzname:
        tzname = current_timezone

    mocked_time = datetime.strptime(datestr, '%Y-%m-%d')

    if hour and minute:
        mocked_time = mocked_time.replace(hour=int(hour), minute=int(minute))

    try:
        import pytz

        # Localize datetime to current timezone.
        mocked_time = (
            pytz.timezone(tzname).localize(mocked_time)
        )

    except ImportError:
        print("Install `pytz` in order to set the timezone.")

    world.freezer = freeze_time(mocked_time, ignore=[
        'aloe_webdriver',
        'aloe_webdriver_extra',
    ])
    world.freezer.start()


def remove_patches(*args):
    """
    Remove running patches.

    :return: None.
    """
    patch.stopall()

    unmock_time()


after.each_example(function=remove_patches, name='remove_patches')
