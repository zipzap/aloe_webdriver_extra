"""Override steps defined in `aloe_webdriver` with improved modifications."""
from __future__ import unicode_literals

from aloe import step, world
from aloe_webdriver import (
    assert_checked_checkbox,
    assert_not_checked_checkbox,
    check_checkbox,
    choose_radio,
    click,
    fill_in_textfield,
    press_button,
    select_single_item,
    should_see_link_text,
    uncheck_checkbox,
)
from aloe_webdriver.util import ElementSelector, find_field
from nose.tools import assert_false, assert_true
from selenium.common.exceptions import NoSuchElementException

from aloe_webdriver_extra.util import (
    BUTTON_XPATH,
    CAPTURE_OPTIONAL_POSITION,
    CAPTURE_POSITION,
    CAPTURE_STRING,
    click_nth_link,
    ends_with_xpath,
    find_elements_by_label,
    find_visible_elements_by_xpath,
    nth_element,
    StringHelper,
    wait_for,
)


# A lookup for comparator functions based on the wording used in RegEx.
LOOKUP_COMPARATOR = {
    'exact': StringHelper.equals,
    'matching': StringHelper.contains,
}


def unregister(method):
    """
    Unregister an `aloe_webdriver` method.

    :param method: Method reference to be unregister.
    :return: None.
    """

    if hasattr(method, 'unregister'):
        method.unregister()
    else:
        print(
            "Method '{method}' hasn't been registered, make sure you imported"
            " `aloe_webdriver_extra` after `aloe_webdriver`.".format(
                method=method,
            )
        )


# Unregister `I click "STRING"`, it fails if multiple links have the same text.
# e.g. Click here
unregister(click)


@step(
    r'I click ?{POSITION}(?:link|button|element|collapsible)?'
    r'(?: with ?(matching|exact)? text)? {STRING}$'.format(
        POSITION=CAPTURE_OPTIONAL_POSITION,
        STRING=CAPTURE_STRING,
    )
)
@wait_for
def numbered_click(self, position, comparator_name, link_text):
    """
    Click the n-link with the provided link text.

    :param self: Object reference to aloe. [Not used].
    :param position: 1-based position of the element in the list. Optional.
    :param comparator_name: Name of comparing method. 'matching'
        is used by default.
    :param link_text: Text displayed on the link.
    :return: None.

    It also helps to click on links that doesn't have any text e.g. image.

    Regex Test: https://regex101.com/r/jPwJ7s/1/
    Links:
        I click "hello"
        I click with matching text "hello"
        I click with text "hello"
        I click link "hello"
        I click link with exact text "hello"
        I click link with text "hello"
        I click the 1st "hello"
        I click the 1st with exact text "hello"
        I click the 1st with text "hello"
        I click the 1st link "hello"
        I click the 1st link with exact text "hello"
        I click the 1st link with text "hello"
    """

    if comparator_name is None:
        comparator_name = 'matching'

    comparator = LOOKUP_COMPARATOR[comparator_name]

    click_nth_link(link_text, position, comparator)


# Unregister `I press "STRING"`, it fails when two buttons have the same label
# or value.
unregister(press_button)


@step(r'I press {POSITION}{STRING}$'.format(
    POSITION=CAPTURE_OPTIONAL_POSITION,
    STRING=CAPTURE_STRING,
))
@wait_for
def press_button_extra(self, position, value):
    """
    Press a button based on its position.

    :param self: Object reference to aloe. [Not used].
    :param position: 1-based position of the element in the list.
    :param value: Text displayed on the button.
    :return: None.

    If there are multiple buttons with the same text, this step allows to press
    one of them without failing.
    """

    button = nth_element(
        find_visible_elements_by_xpath(BUTTON_XPATH.format(value)),
        position,
        "Button '{value}' not found.".format(
            value=value,
        )
    )

    button.click()


# Unregister `I fill in "STRING" with "STRING"`, it fails when two text inputs
# have the same label.
unregister(fill_in_textfield)


@step(r'I fill in {POSITION}{STRING} with {STRING}$'.format(
    POSITION=CAPTURE_OPTIONAL_POSITION,
    STRING=CAPTURE_STRING,
))
@wait_for
def fill_in_numbered_textfield(self, position, field_name, value):
    """
    Fill a text box based on its position.

    :param self: Object reference to aloe.
    :param position: 1-based position of the element in the list.
    :param field_name: The label associated with the text box.
    :param value: String to place as the value of the text box, it will replace
        any value currently in there.
    :return: None.


    When multiple text boxes have the same label, this will select the
    right one based on its position.
    """

    elements = find_elements_by_label('text', field_name)

    if elements:
        field = nth_element(elements, position, "Textbox not found.")

        field.clear()
        field.send_keys(value)
    else:
        # No fields were found using the `field_name` as a label, try the
        # old function.
        fill_in_textfield(self, field_name, value)


# Unregister `I select "STRING" from "STRING"`, it performs a partial match
# over the options in the select and it prevents to select an option which full
# text is contained in another option's text.
unregister(select_single_item)


@step(
    r'I select {STRING} from {POSITION}{STRING}'
    r'( using partial match)?$'.format(
        POSITION=CAPTURE_OPTIONAL_POSITION,
        STRING=CAPTURE_STRING,
    )
)
@wait_for
def single_item_multiple_select(
        self, option_name, position, select_name, partial_match):
    """
    Select an option from the select box specified by the position.

    :param self: Object reference to aloe. [Not used].
    :param option_name: String to match the visible part of the option.
    :param position: A 1-based index used when multiples select fields share
        the same name or label.
        If no specified it defaults to 1.
    :param select_name: Label or identifier for the select field.
    :param partial_match: If present, it will force the `option_name` string to
        partially matched the text on the options.
        By default an exact match is performed.
    :return: None.
    """

    partial_match = bool(partial_match is not None)

    select_box = nth_element(
        find_field(world.browser, 'select', select_name),
        position,
        "Select box '{label}' not found.".format(
            label=select_name,
        )
    )

    if partial_match:
        xpath = r'.//option[contains(normalize-space(.), "{name}")]'
    else:
        xpath = r'.//option[normalize-space(text())="{name}"]'

    try:
        option = select_box.find_element_by_xpath(
            xpath.format(name=option_name))
    except NoSuchElementException:
        raise AssertionError(
            "Option '{option}' not found in select '{label}'.".format(
                option=option_name,
                label=select_name,
            ))

    option.click()


# Unregister `I check "STRING"`, `I uncheck "STRING"`,
# `The "STRING" checkbox should be checked` and
# `The "STRING" checkbox should not be checked`. They fail if multiple
# checkboxes have the same text. e.g [ ] Yes.
unregister(check_checkbox)
unregister(uncheck_checkbox)
unregister(assert_checked_checkbox)
unregister(assert_not_checked_checkbox)


def find_numbered_checkbox(position, label):
    """
    Find a checkbox in the page by position and label.

    :param position: 1-based index of the desired checkbox.
    :param label: Label used for the checkbox. If no elements can be found it
        will try to match ID and Name.
    :return: The matched checkbox, if no checkbox is found then an exception is
        raised.
    """

    elements = find_elements_by_label('checkbox', label)

    if not elements:
        elements = find_visible_elements_by_xpath(
            r'//input[@type="checkbox"][@id="{0}" or @name="{0}"]'.format(
                label,
            ))

    if not position and len(elements) > 1:
        raise AssertionError(
            'Multiple elements were found with label: "{label}". Position must '
            'be specified when there are multiple elements.'.format(
                label=label,
            ))

    return nth_element(elements, position, "Checkbox not found.")


@step(r'I (un)?check {POSITION}{STRING}$'.format(
    POSITION=CAPTURE_OPTIONAL_POSITION,
    STRING=CAPTURE_STRING,
))
@wait_for
def check_numbered_checkbox(self, uncheck, position, label):
    """
    Check/Uncheck a checkbox based on its position.

    :param self: Object reference to aloe. [Not used].
    :param uncheck: If set, it indicates that the checkbox has to be unchecked.
    :param position: 1-based index of the desired checkbox.
    :param label: Label used for the checkbox. If no elements can be found it
        will try to match ID and Name.
    :return: None.
    """

    check_box = find_numbered_checkbox(position, label)

    check = not bool(uncheck)
    selected = check_box.is_selected()

    if check != selected:
        # Change the checkbox state iff the new state is different from the
        # current state.
        check_box.click()
    else:
        raise AssertionError(
            'The checkbox with label: "{label}" is already {status} which is '
            'the action you are trying to perform'.format(
                label=label,
                status='checked' if selected else 'unchecked'
            ))


@step(r'the (?:{POSITION} )?{STRING} checkbox should( not)? be checked$'.format(
    POSITION=CAPTURE_POSITION,
    STRING=CAPTURE_STRING,
))
@wait_for
def check_state_of_numbered_checkbox(self, position, label, unchecked):
    """
    Check the state of a checkbox based on its position.

    :param self: Object reference to aloe. [Not used].
    :param position: 1-based index of the desired checkbox.
    :param label: Label used for the checkbox. If no elements can be found it
        will try to match ID and Name.
    :param unchecked: If set, it indicates that the checkbox should be
        unchecked.
    :return: None.
    """

    check_box = find_numbered_checkbox(position, label)

    checked = not bool(unchecked)

    assert_true(
        checked == check_box.is_selected(),
        'The checkbox with label: "{label}" is {status} when it should be '
        '{alt_status}.'.format(
            label=label,
            status='checked' if checked else 'unchecked',
            alt_status='unchecked' if checked else 'checked',
        ))


# Unregister `I choose "STRING"`, it fails if multiple radio buttons have the
# same text.
unregister(choose_radio)


@step(r'I choose {POSITION}{STRING}$'.format(
    POSITION=CAPTURE_OPTIONAL_POSITION,
    STRING=CAPTURE_STRING,
))
@wait_for
def check_numbered_radiobutton(self, position, value):
    """
    Checks a radio button.

    :param self: Object reference to aloe. [Not used].
    :param position: 1-based index of the desired checkbox. Optional.
    :param value: String. The identifier for the radio button. When a position
        is provided this must be the label, otherwise it can be the id, name or
        label.
    :return: None.

    If position is not given then it finds the radio element by id, name
    or label.

    When multiple radio buttons have the same label, this will select the right
    one based on its position. However, if no position is given for this
    scenario then it'll throw exception.
    """

    if not position:
        element = find_field(world.browser, 'radio', value)
    else:
        element = nth_element(
            find_elements_by_label('radio', value),
            position,
            "Radio button not found."
        )

    element.click()


# Unregister `I should see a link to "STRING" with the url "STRING"`
unregister(should_see_link_text)


@step(
    r'I should( not)? see a link'
    r' to {STRING}(?: with the url {STRING})?$'.format(
        STRING=CAPTURE_STRING,
    )
)
@wait_for
def should_see_link_text_extra(self, not_in, link_text, link_url):
    """
    Assert a link with the provided text points to the provided URL.

    :param self: Object reference to aloe. [Not used].
    :param link_text: Text displayed in the link.
    :param link_url: URL where the link points to. [Optional]
    :return: None.

    This overrides the same step defined in `aloe_webriver`.
    The difference with the original step is that this one allows to specify
    relative URLs and also it trims spaces from the text attribute.

    An extra difference is that it allows to check for the presence of links
    without checking for their urls. In order to check if the link works it's
    recommended to click on it.
    """

    url_xpath = ''

    if link_url is not None:
        xpath = r'@href="{url}"'

        # If link starts with '/' then assume it is a relative path.
        if link_url.startswith('/'):
            xpath = ends_with_xpath('@href', '{url}')

        url_xpath = '[{xpath}]'.format(xpath=xpath.format(url=link_url))

    xpath = r'''
        //a{URL_XPATH}[normalize-space(text())="{TEXT}"]
        | //text()[contains(., "{TEXT}")]/ancestor::*[self::a{URL_XPATH}]
    '''.format(
        URL_XPATH=url_xpath,
        TEXT=link_text,
    )

    expected = True

    if not_in:
        expected = False

    element = ElementSelector(world.browser, xpath, filter_displayed=True)

    if expected:
        assert_true(element)
    else:
        assert_false(element)
