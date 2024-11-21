"""Miscellaneous Gherkin steps."""
from __future__ import print_function, unicode_literals

import logging

from aloe import step, world
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from aloe_webdriver_extra.util import (
    CAPTURE_NUMBER,
    CAPTURE_STRING,
    wait_for,
)


logger = logging.getLogger(__name__)


@step(r'I refresh the page$')
def refresh_page(self):
    """
    Refresh the current page.

    :param self: Object reference to aloe.
    :return: None.
    """

    # Don't use world.browser.refresh, as this seems that it may deadlock?
    # Unconfirmed because it was a heisenbug, but something to think about if
    # changing this.
    self.given('I visit "%s"' % (world.browser.current_url))


@step(r'I click away$')
def click_away(self):
    """
    Click outside of any element, to remove focus from the current element.

    :param self: Object reference to aloe. [Not used].
    :return: None.
    """

    body = world.browser.find_elements_by_xpath(r'//body')[0]
    body.click()


@step(r'I wait for animations to finish$')
@wait_for
def wait_for_animations(self):
    """
    Wait for all the animations on the page to end.

    :param self: Object reference to aloe. [Not used].
    :return: None.
    """

    assert world.browser.execute_script('return $(":animated").length == 0')


@step(r'I click (?:link|button|element) with id {STRING}$'.format(
    STRING=CAPTURE_STRING,
))
@wait_for
def click_by_id(self, element_id):
    """
    This help to click on links that doesn't have any text. i.e. image links.

    :param self: Object reference to aloe. [Not used].
    :param element_id: HTML ID of the element to click.
    :return: None.
    """
    try:
        elem = world.browser.find_element_by_id(element_id)
    except NoSuchElementException:
        raise AssertionError(
            "Link|button|element with id '{id}' not found.".format(
                id=element_id,
            ))

    elem.click()


@step(r'I hover over element with id {STRING}$'.format(
    STRING=CAPTURE_STRING,
))
@wait_for
def hover_on_element(self, element_id):
    """
    Hover over the given element.

    :param self: Object reference to aloe. [Not used].
    :param element_id: HTML ID of the element to hover.
    :return: None.

    Useful when wanting to initiate on_mouseover events.
    """
    element = world.browser.find_element_by_id(element_id)
    hover = ActionChains(world.browser).move_to_element(element)
    hover.perform()


@step(
    r'I scroll element with id {STRING} into view'
    r'(?: with offset {NUMBER}, {NUMBER})?$'.format(
        STRING=CAPTURE_STRING,
        NUMBER=CAPTURE_NUMBER,
    ),
)
def scroll_element_into_view(self, element_id, offset_x, offset_y):
    """
    Scroll the page to bring the specified element into view.

    :param element_id: String representing the desired element's id.
    :param offset_x: the specified offset (in pixels) to apply along the x axis.
        Supports negative and positive numbers.
    :param offset_y: the specified offset (in pixels) to apply along the y axis.
        Supports negative and positive numbers.
    :return: None.
    """

    element = world.browser.find_element_by_id(element_id)

    # Scroll the element to the top of the view.
    action = ActionChains(world.browser).move_to_element(element)
    action.perform()

    # If an offset is desired (i.e. the element is obscured and must be
    # visible for Selenium to perform an action) then scroll by the specified
    # offset amount along the x and y axis to bring the element out from under
    # any nav menus or elements.
    if offset_x and offset_y:
        world.browser.execute_script(
            'window.scrollBy({offset_x}, {offset_y});'.format(
                offset_x=offset_x,
                offset_y=offset_y,
            ))
