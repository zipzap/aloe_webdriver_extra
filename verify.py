"""Gherkin steps to verify elements are present."""
from __future__ import unicode_literals

from aloe import step, world
from nose.tools import assert_equal
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.alert import Alert

from aloe_webdriver_extra.util import (
    CAPTURE_STRING,
    CAPTURE_STRING_INSIDE_SINGLE_QUOTE,
    NUMBER,
    wait_for,
)


@step(r'I should see page title {STRING}$'.format(
    STRING=CAPTURE_STRING,
))
@wait_for
def should_see_title(self, title):
    """
    Check that the given title is displayed on the page.

    :param self: Object reference to aloe. [Not used].
    :param title: Text displayed as title.
    :return: None.
    """

    elems = world.browser.find_elements_by_xpath(
        r'//h1[contains(normalize-space(.), "{}")]'.format(title)
    )

    assert elems, u"Couldn't find title: '{}'".format(title)


@step(r"I should see an alert containing text {STRING}$".format(
    STRING=CAPTURE_STRING,
))
def check_alert(self, text):
    """
    Assert an alert is showing and contains the given text.

    :param self: Object reference to aloe. [Not used].
    :param text: Text that should be displayed on the Alert box.
    :return: None
    """

    alert = Alert(world.browser)
    assert text in alert.text, "Alert doesn't contain text: {}".format(text)


@step(r'I should see {STRING} ({NUMBER}) times?$'.format(
    NUMBER=NUMBER,
    STRING=CAPTURE_STRING,
))
@step(r"I should see {STRING} ({NUMBER}) times?$".format(
    NUMBER=NUMBER,
    STRING=CAPTURE_STRING_INSIDE_SINGLE_QUOTE,
))
@wait_for
def multiple_should_see(self, text, repetitions):
    """
    Check that a text is displayed the given number of times.

    :param self: Object reference to aloe. [Not used].
    :param text: Text to look for in the page.
    :param repetitions: Number of times the `text` should appear in the page.
    :return: None.

    It searches for elements that contain the whole of the text we're looking
    for in themselves or subelements, but whose children do NOT contain that
    text - otherwise it matches <body> or <html> or other similarly useless
    things.
    """
    try:
        elements = [
            elem
            for elem in world.browser.find_elements_by_xpath(
                r'//*[contains(normalize-space(.),"{content}") '
                r'and not(./*[contains(normalize-space(.),"{content}")])]'
                .format(content=text))
            if elem.is_displayed()
        ]
    except NoSuchElementException:
        raise AssertionError("Text '{text}' not found.".format(
            text=text,
        ))

    assert_equal(
        len(elements), int(repetitions),
        "Found text '{0}' {1} times, expecting it {2} times".format(
            text, len(elements), int(repetitions)
        )
    )


@step(r'page source should( not)? contain {STRING}$'.format(
    STRING=CAPTURE_STRING,
))
@wait_for
def source_content(self, not_in, text):
    """
    Check that the source code contains or not a specific text.

    :param self: Object reference to aloe. [Not used].
    :param not_in: When set, it indicates the source code of the page should
        not contain the given `text`.
    :param text: Text to look for in the source code of the page.
    :return: None.

    Useful for verifying code that is not visible to the user is present or not
    in the page.
    """
    expected = True
    if not_in:
        expected = False

    contains = text in world.browser.page_source

    assert_equal(contains, expected)


@step(r'I should see {STRING} as the value for {STRING}$'.format(
    STRING=CAPTURE_STRING,
))
@wait_for
def verify_value_for_description_list(self, value, description_text):
    """
    Verify the value is next to the description term in a description list.

    :param self: Object reference to aloe. [Not used].
    :param value: The value to check i.e. the text in the <dd></dd> tag.
    :param description_text: The descriptive text adjacent to the value
        i.e. the text in the <dt></dt> tag.
    :return: None.

    Used to test that the value is in the correct position in the info table
    for a registration.

    Expects the table to have values in <dt></dt><dd></dd> pairs.
    """

    value_field = world.browser.find_element_by_xpath(
        r'//dt[text()[normalize-space()="{description_text}"]]'
        r'/following-sibling::dd[1]'.format(
            description_text=description_text,
        )
    )

    actual_value = value_field.text

    assert_equal(
        actual_value,
        value,
        'The value next to "{description_text}": "{actual_value}", did not '
        'match the expected value: "{expected_value}"'.format(
            description_text=description_text,
            actual_value=actual_value,
            expected_value=value,
        )
    )
