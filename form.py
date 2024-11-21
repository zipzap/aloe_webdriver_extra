"""
Gherkin steps to deal with multiple elements using the same labels/values.

Aloe Webdriver fails when trying to locate an element when there is more than
one of them using the same label/value.
"""
from __future__ import absolute_import, unicode_literals

import os

from aloe import step, world
from aloe_webdriver import (
    DATE_FIELDS,
    TEXT_FIELDS,
)
from aloe_webdriver.util import (
    find_any_field,
    find_field,
)
from nose.tools import assert_equal
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from aloe_webdriver_extra.util import (
    BUTTON_XPATH,
    CAPTURE_OPTIONAL_POSITION,
    CAPTURE_POSITION,
    CAPTURE_STRING,
    find_elements_by_label,
    find_option_in_select_element,
    find_select_element_by_label,
    nth_element,
    wait_for,
)


@step(
    r'option {STRING} should be (present|absent) in {POSITION}selector '
    r'{STRING}$'.format(
        POSITION=CAPTURE_OPTIONAL_POSITION,
        STRING=CAPTURE_STRING,
    ))
def selector_contains(self, option, status, position, selector_id):
    """
    Assert if an option is present or absent in a select box.

    :param self: Object reference to aloe. [Not used].
    :param option: Text to match against the options displayed in the select
        box.
    :param status: A string either 'present' or 'absent' to denote if the given
        option is listed or not in the select box.
    :param position: 1-based index of the desired select box. If not set, it
        defaults to 1.

        Note, can only match against the selector label when using position
        arguments, name and id are not supported.
    :param selector_id: ID, Name or Label to identify the select box.
    :return: None.
    """

    if position:
        # Find all select elements with matching labels, ignoring id/names,
        # it's not expected to have multiple select boxes with the same id/name.
        selector = find_select_element_by_label(selector_id, position)

    else:
        # No position, so only expect 1 field with the name, id or label.
        selector = find_field(world.browser, 'select', selector_id)

    desired_option = find_option_in_select_element(
        select_element=selector,
        label=option,
        raise_error=False,
    )

    option_found = False

    if desired_option is not None:
        option_found = True

    status_mapping = {
        'present': True,
        'absent': False,
    }

    assert option_found == status_mapping[status], (
        'The option "{option}" was not {status} in "{selector}"'.format(
            option=option,
            status=status,
            selector=selector_id,
        ))


@step(
    r'The (?:{POSITION} )?select box labelled {STRING} should have {STRING}'
    r' selected$'.format(
        POSITION=CAPTURE_POSITION,
        STRING=CAPTURE_STRING,
    ))
@wait_for
def check_selected_option(self, position, label, selected_option):
    """
    Check the selected option is selected in the select box.

    :param position: The index of the desired select box.
        Note: optional, in case there are multiple select boxes with similar
        labels.
    :param label: The label associated with the select box.
    :param selected_option: The string representing the selected option's label.
    :return: None.
    """

    select_element = find_select_element_by_label(label, position)

    selected_options = Select(select_element).all_selected_options

    assert selected_options, 'No options selected'

    # Get the labels for each selected option to compare with the tested option.
    selected_labels = [
        option.get_attribute('label') for option in selected_options
    ]

    assert selected_option in selected_labels, (
        'The option "{expected_option}" was not selected in "{label}"'.format(
            label=label,
            expected_option=selected_option,
        )
    )


@step(
    r'The (?:{POSITION} )?field labelled {STRING} should have a value of'
    r' {STRING}$'.format(
        POSITION=CAPTURE_POSITION,
        STRING=CAPTURE_STRING,
    ))
@wait_for
def check_field_value(self, position, field_label, expected_value):
    """
    Check the field value matches the value provided.

    :param self: Object reference to aloe. [Not used].
    :param position: 1-based index of the desired field.
        Note: optional, in case there are multiple fields with similar labels.
    :param field_label: The label for the input field. This uses exact
        matching.
    :param expected_value: The value expected for the field.
    :return: None.

    Example:
        Then the field labelled "Width" should have a value of "120"
    """
    field = nth_element(
        find_elements_by_label('text', field_label),
        position,
        "Input with label '{field_label}' not found.".format(
            field_label=field_label,
        )
    )

    actual_value = field.get_attribute('value')

    assert_equal(
        actual_value,
        expected_value,
        'The value ({actual_value}) for field "{field_label}" did not match '
        'what was expected ({expected_value})'.format(
            actual_value=actual_value,
            field_label=field_label,
            expected_value=expected_value,
        )
    )


@step(r'I should see a file input for {STRING}$'.format(
    STRING=CAPTURE_STRING,
))
@wait_for
def file_input_exist(self, label):
    """
    Check that a file input exist for the given label.

    :param self: Object reference to aloe. [Not used].
    :param label: Label text for the file input.
    :return: None.
    """

    file_input = find_field(world.browser, 'file', label)

    if not file_input:
        raise AssertionError(
            "File input not found for label '{}'".format(label))


@step(r'I choose file {STRING} for file input {STRING}$'.format(
    STRING=CAPTURE_STRING,
))
def upload_file(self, filename, field):
    """
    Upload a file using selenium.

    NB: Selenium does not support multiple file uploads (as of 2014-12-02):
    https://code.google.com/p/selenium/issues/detail?id=2239
    """
    file_input = find_field(world.browser, 'file', field)

    base_dir = ''

    try:
        # If Django is available use the Project Directory as base.
        from django.conf import settings

        if settings.configured:
            base_dir = settings.PROJECT_DIR
    except ImportError:
        pass

    file_input.send_keys(os.path.join(base_dir, filename))


@step(r'I should( not)? see a button with value {STRING}$'.format(
    STRING=CAPTURE_STRING,
))
@wait_for
def should_see_button(self, not_in, value):
    """
    Check that a button is being displayed.

    :param self: Object reference to aloe. [Not used].
    :param not_in: When set, it specifies that the button should exists or be
        displayed.
    :param value: Text displayed on the button.
    :return: None.
    """

    expected = True
    if not_in:
        expected = False

    try:
        elems = world.browser.find_elements_by_xpath(
            BUTTON_XPATH.format(value)
        )
    except NoSuchElementException:
        raise AssertionError("Button '{value}' not found.".format(
            value=value,
        ))

    if expected:
        assert any(elem.is_displayed() for elem in elems)
    else:
        assert all(not elem.is_displayed() for elem in elems)


@step(r'I type {STRING} on field {STRING}$'.format(
    STRING=CAPTURE_STRING,
))
def send_key_to_element(self, key, field_name):
    """
    Type text in the specified field without deleting the previous content.

    :param self: Object reference to aloe. [Not used].
    :param key: Key to type into the field. It should be defined in:
        selenium.webdriver.common.keys.Keys
    :param field_name: Label or name of the field to type in.
    :return: None.
    """
    field = find_any_field(
        world.browser,
        TEXT_FIELDS + DATE_FIELDS,
        field_name,
    )
    field.send_keys(getattr(Keys, key, key))
