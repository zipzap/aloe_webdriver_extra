"""Gherkin steps that can be used to test WCAG 2.0 compliance."""
from __future__ import unicode_literals

from aloe import step, world
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from aloe_webdriver_extra.util import wait_for


@step(r'an image with id "(.*?)" '
      r'should contain alternative text "(.*?)"$')
@wait_for
def verify_alt_text_for_image_id(self, image_id, alt_text):
    """
    Verify alternative text of image element based on its id.

    :param self: Object reference to aloe.
    :param image_id: ID value of the image element to look for.
    :param alt_text: Value we expect the alternative text to contain.
    :return: True iff image element contains the given alternative text.
    """

    element = world.browser.find_element_by_id(image_id)
    returned_alt = element.get_attribute('alt')

    assert alt_text in returned_alt, (
        "Image with id {id} "
        "has alternative text '{result}'. "
        "Expected '{expected}'".format(
            id=image_id,
            result=returned_alt,
            expected=alt_text,
        ))


@step(r'images containing source url "(.*?)" '
      r'should contain alternative text "(.*?)"$')
@wait_for
def verify_alt_text_for_image_source(self, source_url, expected_alt_text):
    """
    Verify alternative text of image element based on its source URL.

    :param self: Object reference to aloe.
    :param source_url: Value contained in target element's source URL.
    :param expected_alt_text: Value we expect the alternative text to contain.
    :return: True iff image element contains the given alternative text.
    """

    try:
        elements = world.browser.find_elements_by_xpath(
            '//img[contains(@src, "{}")]'.format(source_url))
    except NoSuchElementException:
        raise AssertionError("Image '{url}' not found.".format(
            url=source_url,
        ))

    assert elements, "Expected image can't be found on page"

    for idx, element in enumerate(elements):
        returned_alt = element.get_attribute('alt')
        assert expected_alt_text in returned_alt, (
            "[index = {index}] "
            "Image containing source url {source_url} "
            "has alternative text '{result}'. "
            "Expected '{expected}'".format(
                index=idx,
                source_url=source_url,
                result=returned_alt,
                expected=expected_alt_text,
            ))


@step(r'the text "(.*?)" should be visible to screen reader$')
@wait_for
def verify_element_attribute_value(self, expected_sr_text):
    """
    Verify the given text is visible to screen reader.

    :param self: Object reference to aloe.
    :param expected_sr_text: Value expected to be visible to screen reader.
    :return: True iff the given text is found as attribute value of any HTML
        element used for accessibility.
    """

    attribute_names = [
        'aria-label',
    ]

    screen_readable_text_found = False
    for name in attribute_names:
        try:
            elements = world.browser.find_elements_by_xpath(
                '//*[@{}]'.format(name))
        except NoSuchElementException:
            raise AssertionError(
                "Text '{text}' not part of an aria-label attribute.".format(
                    text=expected_sr_text,
                ))

        if any(
                expected_sr_text in element.get_attribute(name)
                for element in elements):
            screen_readable_text_found = True
            break

    assert screen_readable_text_found, (
        "The text '{txt}' was not found to be screen readable.".format(
            txt=expected_sr_text
        )
    )


@step(r'the element with id "(.*?)" has a valid aria-describedby attribute$')
def verify_describedby_object_exists(self, object_id):
    """
    Verify the aria-described referenced by the element with object_id exists.

    :param self: Object reference to aloe. [Not used].
    :param object_id: The id of the object with the aria-describedby attribute.
    :return: None.
    """

    obj = world.browser.find_element_by_id(object_id)

    referenced_id = obj.get_attribute('aria-describedby')

    assert referenced_id, (
        "No aria-describedby attribute found for the element with id "
        "{object_id}".format(
            object_id=object_id,
        )
    )

    assert world.browser.find_element_by_id(referenced_id), (
        "Unable to find element with id {referenced_id}, referenced in the "
        "aria-describedby attribute of the element with id {object_id}".format(
            referenced_id=referenced_id,
            object_id=object_id,
        )
    )


@step(r'I press the special key "(.*?)"$')
def special_key_press(self, key_name):
    """
    Simulate pressing a special key.

    :param self: Object reference to aloe. [Not used].
    :param key_name: Name of the key to press. Currently supported keys are:
        TAB
        ENTER
    :return: None.
    """

    key_map = {
        'TAB': Keys.TAB,
        'ENTER': Keys.ENTER,
    }

    key = key_map.get(key_name)

    assert key, (
        "Special key {key_name} is not configured.".format(
            key_name=key_name,
        )
    )

    ActionChains(world.browser).send_keys(key).perform()
