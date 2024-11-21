"""Gherkin steps for downloading files."""
from __future__ import unicode_literals

from aloe import step
from aloe_webdriver_extra.util import CAPTURE_STRING, NUMBER
from .util import wait_for_file


@step(
    r'file {STRING} should be downloaded'
    r'(?: within ({NUMBER}) seconds)?$'.format(
        STRING=CAPTURE_STRING,
        NUMBER=NUMBER,
    ))
def file_should_download(self, filename, seconds):
    """
    Wait for the file to be downloaded.

    :param self: Object reference to aloe. [Not used].
    :param filename: Filename of the file to check.
    :param seconds: Number of seconds to wait for the file to be downloaded.
        [Optional]
    :return: None.
    """

    wait_for_file(filename, seconds)
