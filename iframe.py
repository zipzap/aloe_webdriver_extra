"""Gherkin steps related to HTML IFrames."""
from __future__ import unicode_literals

from aloe import step, world
from selenium.common.exceptions import NoSuchElementException
from .util import CAPTURE_OPTIONAL_POSITION, NUMBER

from aloe_webdriver_extra.util import wait_for


@wait_for
def wait_for_frame(position, **kwargs):
    """
    Wait for an iframe to appear.

    :param position: Position of the iframe among the others. The first element
        is in position 1.
    :return: None.
    """
    try:
        elem = world.browser.find_elements_by_xpath(r'//iframe')[position - 1]
        world.browser.switch_to.frame(elem)
    except (IndexError, NoSuchElementException):
        raise AssertionError("Frame {} not found.".format(position))


@step(r'I switch to {POSITION}frame(?: within ({NUMBER}) seconds)?$'.format(
    NUMBER=NUMBER,
    POSITION=CAPTURE_OPTIONAL_POSITION,
))
def switch_to_frame(self, position, seconds):
    """
    Switch to an iframe given its position.

    :param self: Object reference to aloe. [Not used].
    :param position: Position of the iframe among the others. The first element
        is in position 1.
    :param seconds: When set, it specifies the time in seconds to wait for the
        iframe to be visible before timing out. Default is 5 seconds.
    :return: None.

    When an iframe doesn't have a fixed id, this step helps to select it.
    """
    if position is None:
        position = 1
    if seconds is None:
        seconds = 5

    wait_for_frame(int(position), timeout=int(seconds))
