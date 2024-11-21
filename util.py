"""Common utilities."""
from __future__ import division, unicode_literals

import operator

from functools import wraps
from time import time, sleep

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)

from aloe import world


BOOLEAN = r'(?:true|false)'
NULL = r'null'
NUMBER = r'-?\d+(?:\.\d*)?'
STRING = r'|'.join((r'"[^"]*"', r"'[^']*'"))
# Match without capturing either:
# - A quote-delimited string.
# - A number, with or without leading minus sign.
# - `true` or `false`.
# - The text `null`.
TOKEN = r'(?:{STRING}|{NUMBER}|{BOOLEAN}|{NULL})'.format(
    BOOLEAN=BOOLEAN,
    NULL=NULL,
    NUMBER=NUMBER,
    STRING=STRING,
)

CAPTURE_NUMBER = r'({NUMBER})'.format(NUMBER=NUMBER)
CAPTURE_OPTIONAL_POSITION = r'(?:the (?:({NUMBER})(?:st|nd|rd|th)) ?)?'.format(
    NUMBER=NUMBER)
CAPTURE_POSITION = r'({NUMBER})(?:st|nd|rd|th)'.format(NUMBER=NUMBER)
CAPTURE_STRING = r'"([^"]*)"'
CAPTURE_STRING_INSIDE_SINGLE_QUOTE = CAPTURE_STRING.replace('"', "'")

BUTTON_XPATH = r"""
    //input[
        @type[.="submit" or .="button" or .="reset" or .="image"]
        and normalize-space(@value)="{0}"
    ] |
    //button[normalize-space(.)="{0}"]
"""
LABEL_XPATH = r'//label[contains(normalize-space(.), "{label}")]'
LABEL_WITHOUT_FOR_XPATH = (
    r'//label[contains(normalize-space(.), "{label}") and not(@for)]'
)
XPATH_LABELED_ELEMENTS = (
    r'//input[@id=(' + LABEL_XPATH + r'/@for)][{xpath_type}]',
    LABEL_WITHOUT_FOR_XPATH + r'/descendant::input[{xpath_type}]',
    LABEL_WITHOUT_FOR_XPATH + r'/following-sibling::input[{xpath_type}][1]',
)


HTML5_FIELD_TYPES = [
    'color',
    'date',
    'datetime',
    'datetime-local',
    'email',
    'image',
    'month',
    'number',
    'password',
    'range',
    'search',
    'tel',
    'time',
    'url',
    'week',
]

JAVASCRIPT = 'javascript'
XPATH = 'xpath'


class StringHelper(object):
    """
    Container for helper functions on processing string literals.
    """
    @staticmethod
    def normalize_text(text):
        """
        Normalise the given text.

        Normalisation trims (from beginning and end) and removes
        extra ones in between of the text.

        :param text: String to normalise.
        """
        return ' '.join(text.split())

    @staticmethod
    def _escape_quotes(text, _format):
        """
        Escape the quotes in the given text.

        :param text: A text string.
        :param _format: Either JAVASCRIPT or XPATH.
        :return: An expression that represents the given text and that does not
            need to be enclosed in quotes.
        """
        double_quote = '"'
        single_quote = "'"
        quote_types = 0

        if double_quote in text:
            quote_types += 1

        if single_quote in text:
            quote_types += 2

        # Text contains single and double quotes.
        if quote_types == 3:
            output = []
            init_position = 0
            position = text.find(double_quote)

            while position > 0:
                # Add block of text surrounded with double quotes.
                output.append(
                    double_quote + text[init_position:position] + double_quote
                )

                # Add a double quote surrounded with single quotes.
                output.append("'\"'")

                # Find next double quote in text.
                init_position = position + 1
                position = text.find(double_quote, position + 1)

                # If there are no more double quotes, surround the rest of the
                # text with double quotes.
                if position < 0:
                    output.append(
                        double_quote + text[init_position:] + double_quote
                    )

            if _format == JAVASCRIPT:
                expression = ' + '.join(output)
            elif _format == XPATH:
                expression = 'concat(' + ', '.join(output) + ')'
            else:
                raise NotImplementedError(
                    'No quote escaping defined for {format}'.format(
                        format=_format,
                    )
                )
        elif quote_types == 0 or quote_types == 2:
            # Text contains single quotes or no quotes at all.
            expression = double_quote + text + double_quote
        else:
            # Text contains double quotes.
            expression = single_quote + text + single_quote

        return expression

    @staticmethod
    def xpath_escape_quotes(text):
        """
        Make the given text valid to be used in a XPath expression.

        :param text: A text string.
        :return: An expression that can be used in XPath and represents the
            input text.
            The returned expression does not need to be enclosed in quotes.
        """
        return StringHelper._escape_quotes(text, XPATH)

    @staticmethod
    def javascript_escape_quotes(text):
        """
        Make the given text valid to be used in a Javascript expression.

        :param text: A text string.
        :return: An expression that can be used in Javascript and represents
            the input text.
            The returned expression does not need to be enclosed in quotes.
        """
        return StringHelper._escape_quotes(text, JAVASCRIPT)

    @staticmethod
    def contains(target, source):
        """
        Check if target is a substring of source.

        :param target: Target string to be searched.
        :param source: Source string.
        """

        return target in source

    @staticmethod
    def equals(target, expected):
        """
        Check if target is equal to expected.

        :param target: Target string.
        :param expected: Expected string.
        """

        return target == expected


def class_xpath(class_name):
    """
    XPath expression to match against a specific class name.

    :param class_name: CSS class name to match.
    :return: An XPath expression that can be used to filter elements using
        their CSS classes.

    Extra spaces prevent partial matches.
    Based in http://stackoverflow.com/a/1604480
    """

    return (
        r"[contains("
        r"concat(' ', normalize-space(@class), ' '),"
        r" ' {CLASS_NAME} ')]".format(
            CLASS_NAME=class_name
        )
    )


def ends_with_xpath(attribute, text):
    """
    Implement XPath function `ends-with` which is not available in version 1.0.

    :param attribute: Element's attribute to check.
    :param text: Text to compare against.
    :return: A string with the XPath expression to perform a `ends-with`
        operation.

    http://stackoverflow.com/a/22437888
    """

    xpath = (
        r'substring({attribute},'
        r' string-length({attribute}) - string-length("{text}") +1)'
        r' = "{text}"'
    ).format(
        attribute=attribute,
        text=text,
    )

    return xpath


def xpath_for_labeled_elements(field_type, label):
    """
    Return an XPath expression to match input elements.

    :param field_type: HTML type of the required elements.
    :param label: Label used for the elements.
    :return: A list of Selenium objects.

    It will match elements of the given type under the given label.
    """

    if field_type == 'text':
        # Include other HTML5 types as well.
        field_types = HTML5_FIELD_TYPES
    else:
        field_types = [field_type]

    input_type_xpath = ' or '.join([
        r'@type="{}"'.format(input_type)
        for input_type in field_types
    ])

    # Allow selecting text inputs even when the attribute `type` is not set.
    if 'text' in field_type:
        input_type_xpath = r'{xpath} or (@type="text" or not(@type))'.format(
            xpath=input_type_xpath,
        )

    for xpath in XPATH_LABELED_ELEMENTS:
        yield xpath.format(
            label=label,
            xpath_type=input_type_xpath,
        )


def find_normalized_elements(xpath, text, comparator):
    """
    Find normalized elements by XPath and comparator test using the text.

    :param xpath: XPath string used for finding the text.
    :param text: String to match.
    :param comparator: A comparator lambda function for String.
    :return: A list of Selenium WebElement.
    """

    filtered_elements = find_visible_elements_by_xpath(xpath)
    elements = [elem
                for elem in filtered_elements
                if comparator(text, StringHelper.normalize_text(elem.text))]

    return elements


def find_visible_elements_by_xpath(xpath):
    """
    Return a list of visible elements that match the given XPath.

    :param xpath: String representing the XPath to retrieve the elements.
    :return: A list of Selenium objects.
    """

    return [
        elem
        for elem in world.browser.find_elements_by_xpath(xpath)
        if elem.is_displayed()
    ]


def find_elements_by_label(field_type, label):
    """
    List of visible elements of the same kind with the same label.

    :param field_type: HTML type of the elements to retrieve.
    :param label: Label used for the elements.
    :return: A list of Selenium objects.
    """

    # Try looking for elements using different XPaths
    for xpath in xpath_for_labeled_elements(field_type, label):
        elements = find_visible_elements_by_xpath(xpath)

        if elements:
            return elements

    return []


def nth_element(elements, position, message):
    """
    Get the element indexed by position (1-based), asserting it exists.

    :param elements: List of Selenium objects.
    :param position: 1-based position of the element in the list. If `None` is
        set (for cases where the position is optionally captured in the step)
        it will default to 1.
    :param message: Message to display if the element can't be found (position
        number is greater than size of list).
    :return: A Selenium object.
    """
    if position is None:
        position = 1

    try:
        return elements[int(position) - 1]
    except (IndexError, TypeError):
        raise AssertionError(message)


def click_nth_link(link_text, position, comparator):
    """
    Click link with given text, position and matching comparator.

    :param link_text: Text in the target link.
    :param position: 1-based position of the target link.
    :param comparator: A lambda function that performs string comparison.
        Example:
            Equality -> lambda(x, y): x == y
            Contains -> lambda(x, y): x in y
    """

    nth_element(
        find_normalized_elements(r'//a', link_text, comparator),
        position,
        "Link ({text}) not found.".format(text=link_text)
    ).click()


def get_select_xpath(label):
    """Build an XPath to get select elements by label."""

    return (
        '//select[@id=(//label[contains(normalize-space(.), '
        '{label})]/@for)]'.format(label=StringHelper.xpath_escape_quotes(label))
    )


def find_select_element_by_label(label, position, is_select2=False):
    """
    Find and return the select element at position n matching the given label.

    :param label: String representing the label for the select element.
    :param position: 1-based index of the desired select box. If not set, it
        defaults to 1 within 'nth_element'.
    :param is_select2: Whether the select is being rendered using Select2
        plugin, in that case the original select can't or won't be visible.
    :return: A selenium object for the matching Select element.
    """

    select_xpath = get_select_xpath(label)

    if is_select2:
        elements = world.browser.find_elements_by_xpath(select_xpath)
    else:
        elements = find_visible_elements_by_xpath(select_xpath)

    return nth_element(
        elements,
        position,
        'Select element "{selector_id}" not found'.format(selector_id=label))


def find_option_in_select_element(select_element, label, raise_error=True):
    """
    Find an option within a select element by label.

    :param select_element: A selenium object representing the Select element to
        search in.
    :param label: String representing the option's label.
    :param raise_error: Boolean, whether to raise an AssertionError or not.
    :return: A selenium object for the matching Option in the Select element, if
        raise_error=False then return None.
    """

    try:
        return select_element.find_element_by_xpath(
            './/option[normalize-space(text())="{label}"]'.format(
                label=label))
    except NoSuchElementException:
        if raise_error:
            raise AssertionError('Option "{label}" was not found.'.format(
                label=label))

    return None


def wait_for(func):
    """
    A decorator that retry the function when certain exceptions are detected.

    The function is invoked every `check_every` amount of seconds (default 0.2)
    for a duration of `timeout` seconds (default 15).

    To override the defaults, add `timeout` and/or `check_every` as kwargs to
    `func`.

    The exceptions that are tracked are:
        - AssertionError: Usually assertions are made against elements in the
            browser, if the refresh on the browser is slow this decorator
            allows to retry some more times.
        - StaleElementReferenceException: Modern JS libraries like AngularJS,
            ReactJS and Vue.js usually delete an element and replace it with
            with the same ID or attributes.
            This decorator allows to retry again in order to grab the new
            element.
    """

    default_timeout = 15
    default_check_every = 0.2

    @wraps(func)
    def wrapped(*args, **kwargs):
        """Wrapper for decorator."""
        timeout = kwargs.pop('timeout', default_timeout)
        check_every = kwargs.pop('check_every', default_check_every)

        start = None

        while True:
            try:
                return func(*args, **kwargs)
            except (AssertionError, StaleElementReferenceException):
                # The function took some time to test the assertion, however,
                # the result might correspond to the state of the world at any
                # point in time, perhaps earlier than the timeout. Therefore,
                # start counting time from the first assertion fail, not from
                # before the function was called.
                if not start:
                    start = time()
                if time() - start < timeout:
                    sleep(check_every)
                    continue
                else:
                    raise

    return wrapped


def get_lookup_function(table_header):
    """
    Allow a lookup function for comparison in a table column.

    :param table_header: The column name we're processing.
    :return: A function which will compare given data with data in the column
        at a specific row, and return true if the given data should be accepted
        as a match.
    """

    # Allow equality for any data type by default.
    # When a table supplied in a Gherkin test step is parsed,
    # the values are set to different data types (Integer, String, etc) if
    # the value matches certain criteria.
    # See Aloe's guess_types function for how this works.
    # This means the `default` lookup must be able to handle all data types.
    # Current lookups `equals` and `contains` can only handle strings.
    # For inspiration for more lookups visit:
    # https://docs.djangoproject.com/en/1.10/ref/models/querysets/#field-lookups
    lookup_function_map = {
        'equals': StringHelper.equals,
        # Allow equality for any data type by default.
        'default': operator.__eq__,
        'contains': StringHelper.contains,
    }

    function_name = 'default'

    if '__' in table_header:
        table_header, function_name = table_header.split('__')

    function = lookup_function_map[function_name]

    return function, table_header
