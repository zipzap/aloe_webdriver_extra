"""Gherkin steps related to `Select2` plugin."""
from __future__ import unicode_literals

from time import sleep

from aloe import step, world
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

from aloe_webdriver_extra.util import (
    CAPTURE_OPTIONAL_POSITION,
    CAPTURE_STRING,
    CAPTURE_STRING_INSIDE_SINGLE_QUOTE,
    class_xpath,
    find_option_in_select_element,
    find_select_element_by_label,
    get_select_xpath,
    nth_element,
    StringHelper,
    wait_for,
)


# Time in seconds to wait after an action is performed over a Select2 element
# before trying to interact with it.
WAIT_AFTER_ACTION = 0.3


@wait_for
def select2_enter_text_for_search(label, position, text):
    """
    Enter the given text on a Select2 input box.

    :param label: String. Label associated with the control.
    :param position: Integer. 1-based index of the desired select box. If not
        set, it defaults to 1.
    :param text: String to search for. Select2 filtering is case insensitive.
    :return: A Selenium element for the Select2 container (it doesn't contain
        the original Select element).
    """

    container_xpath = (
        get_select_xpath(label)
        + '/following-sibling::span'
        + class_xpath('select2-container')
    )

    # Get Select2 container.
    container = nth_element(
        world.browser.find_elements_by_xpath(container_xpath),
        position,
        'Select2 element "{selector_id}" not found'.format(selector_id=label),
    )

    # For multi-select elements the search box will be a child of the
    # container.
    # For non-multi-select elements, the search box will be an independent
    # element from the container.
    # For the first case using an XPath is easy as it would be relative to the
    # container which is not true for the second case.
    # To simplify it, clicking on the Select2 container will bring the search
    # box to focus, then it would be just necessary to capture the current
    # active element.
    # Using `ActionChains` is an alternative method to `container.click()`,
    # which for some reason doesn't work on PhantomJS.
    try:
        action = ActionChains(world.browser)
        action.move_to_element(container).click().perform()
    except WebDriverException:
        container.click()
    finally:
        # Wait for the search box to be displayed.
        sleep(WAIT_AFTER_ACTION)

    search_box_xpath = '//span{span_class}//input{input_class}'.format(
        span_class=class_xpath('select2-container--open'),
        input_class=class_xpath('select2-search__field'),
    )

    search_box = world.browser.find_element_by_xpath(search_box_xpath)

    try:
        search_box.clear()
    except WebDriverException:
        pass

    try:
        search_box.send_keys(text)
    except WebDriverException:
        # `send_keys` doesn't work on some versions of Geckodriver and Firefox
        # https://github.com/mozilla/geckodriver/issues/647
        # Use this alternative instead.
        world.browser.execute_script(
            'arguments[0].value = {text};'.format(
                text=StringHelper.javascript_escape_quotes(text),
            ),
            search_box,
        )

    # The 'input' event is necessary to trigger the Select2 search, specially
    # when an element has been already selected.
    script = """
        var event = new Event("input", {
            "bubbles": true,
            "cancelable": true
        });
        arguments[0].dispatchEvent(event);
    """
    world.browser.execute_script(script, search_box)

    return container


@wait_for
def select2_click_option(container, option_text, select_it=True):
    """
    Select/unselect an option from a Select2 component pointed by `container`.

    :param container: A Selenium element containing the Select2 container.
    :param option_text: The text displayed on the option.
    :param select_it: Whether to select or deselect the option.
        For non-multiselect Select elements it won't be possible to unselect an
        option, thus this parameter can be set to None.
    :return: None.

    This step will fail if:
    - The option is not displayed.
    - The option is disabled.
    - The option is already selected (if it needs to be selected).
    - The option is already unselected (if it needs to be unselected).
    """

    # Assume the option is being displayed, then click it.
    option_xpath = (
        '//li{class_selector}[.={value}]'
        '[not(@aria-disabled) or @aria-disabled="false"]'.format(
            class_selector=class_xpath('select2-results__option'),
            value=StringHelper.xpath_escape_quotes(option_text),
        )
    )

    if select_it is not None:
        if select_it:
            option_xpath += '[not(@aria-selected) or @aria-selected="false"]'
        else:
            option_xpath += '[@aria-selected]'

    option_element = container.find_element_by_xpath(option_xpath)
    option_element.click()


@step(r'I select "(.*?)" in dropdown "(.*?)"$')
@wait_for
def select2_dropdown(self, value, label):
    """
    Select a value from a multiselect dropdown rendered using Select2 plugin.

    @param self: Aloe step from decorator.
    @param value: String to select from dropdown.
    @param label: String. Label associated with the control.
    @return: None.
    """

    container = select2_enter_text_for_search(label, 1, value)

    select2_click_option(container, value, select_it=None)


@step(
    r'I (de)?select {STRING} from {POSITION}multiselect "(.*?)"$'.format(
        POSITION=CAPTURE_OPTIONAL_POSITION,
        STRING=CAPTURE_STRING,
    ))
@step(
    r"I (de)?select {STRING} from {POSITION}multiselect '(.*?)'$".format(
        POSITION=CAPTURE_OPTIONAL_POSITION,
        STRING=CAPTURE_STRING_INSIDE_SINGLE_QUOTE,
    ))
@wait_for
def select2_numbered_multiselect(self, deselect, value, position, label):
    """
    Select a value from a multiselect dropdown rendered using Select2 plugin.

    :param self: Aloe step from decorator.
    :param deselect: Whether to select or deselect the option.
    :param value: String to select from multiselect. If not an exact match is
        given the first value listed will be selected. Also, Select2 filtering
        is case insensitive.
    :param position: Integer. 1-based index of the desired select box. If not
        set, it defaults to 1.
    :param label: String. Label associated with the control.
    :return: None.
    """

    select_option = bool(deselect is None)

    container = select2_enter_text_for_search(label, position, value)

    select2_click_option(container, value, select_it=select_option)


@step(
    r'option {STRING} should be (disabled|enabled) in {POSITION}selector '
    r'{STRING}$'.format(
        POSITION=CAPTURE_OPTIONAL_POSITION,
        STRING=CAPTURE_STRING,
    ))
@wait_for
def select2_check_option_status(self, option, status, position, label):
    """
    Check the status of an option in a dropdown rendered using Select2 plugin.

    :param self: Aloe step from decorator.
    :param option: String. Label for the option being tested.
    :param status: String. Whether the option is disabled or enabled, choices
        can only be 'disabled' or 'enabled'.
    :param position: Integer. 1-based index of the desired select box. If not
        set, it defaults to 1 when selecting the nth selector.
    :param label: String. Label associated with the control.
    :return: None.
    """

    selector = find_select_element_by_label(label, position, is_select2=True)

    desired_option = find_option_in_select_element(
        select_element=selector,
        label=option,
    )

    actual_status = desired_option.is_enabled()

    status_mapping = {
        'disabled': False,
        'enabled': True,
    }

    assert actual_status == status_mapping[status], (
        'Option "{option}" was not {status} in "{label}"'.format(
            option=option,
            status=status,
            label=label,
        ))
