"""Gherkin steps to interact with HTML tables."""
from __future__ import print_function, unicode_literals

from aloe import step, world
from aloe.tools import guess_types
from nose.tools import assert_equal
from selenium.webdriver.common.by import By

from aloe_webdriver_extra.util import (
    wait_for,
    get_lookup_function,
)


# Do not limit output from diff in assert_equal.
assert_equal.__self__.maxDiff = None  # pylint:disable=no-member


def parse_html_table(html_table):
    """
    Convert an HTML table to Python.

    :param html_table: Selenium element representing an HTML `<table>`.
    :return: A list of dictionaries where each dictionary represent a row and
        the keys represent the table headers.
    """

    # There might be several *rows* of headers. Take the last one as the
    # closest to the data.
    # This works for cases like this:
    #  --------------------------------------------------------
    #  | Header 1 |        Group 1      | Group 2  | Header 5 |
    #  |          |---------------------|----------|          |
    #  |          | Header 2 | Header 3 | Header 4 |          |
    #  --------------------------------------------------------
    header_rows = [
        row
        for row in html_table.find_elements(By.TAG_NAME, 'tr')
        if row.find_elements(By.TAG_NAME, 'th')
    ]

    if not header_rows:
        return []

    header_row = header_rows[-1]

    headers = [
        elem.text
        for elem in header_row.find_elements(By.TAG_NAME, 'th')
        # Skip headers spanning several columns - they most likely refer to
        # column groups and not to individual columns.
        if int(elem.get_attribute('colspan') or 1) == 1
    ]

    return [
        guess_types(dict(zip(
            headers,
            [column.text for column in row.find_elements(By.TAG_NAME, 'td')]
        )))
        for row in html_table.find_elements(By.TAG_NAME, 'tr')
    ]


def get_page_tables():
    """
    A list of all the tables present in the current page.

    :return: A list of lists, each list represent an HTML table in the page.
    """

    return [
        parse_html_table(html_table)
        for html_table in world.browser.find_elements_by_xpath(r'//table')
    ]


def is_row_in_table(table, expected_row):
    """
    Check if the given row is part of the table.

    :param table: A list of dictionaries. Each item represents a row, each key
        in the dictionary represents a column.
    :param expected_row: A dictionary. Each key represents a column.
    :return: An integer representing the index of the row in the table. If the
        row can't be found it return's None.
    """

    row_found = None
    for row_index, table_row in enumerate(table):
        values_found = []

        for key, value in expected_row.items():

            lookup_function, key = get_lookup_function(key)

            values_found.append(
                key in table_row
                and lookup_function(value, table_row[key])
            )

        if all(values_found):
            row_found = row_index
            break

    return row_found


def get_table_containing_rows(expected_table):
    """
    Get the first matching table in the page that contains the given rows.

    :param expected_table: A list of dictionaries. Each item represents a row,
        each key in the dictionary represents a column.
    :return: Two values:
      - A table.
      - A list of indexes where the expected rows where found in the table.

    Raise an assertion error if it can't find a table containing all the rows.
    """

    tables = list(enumerate(get_page_tables()))

    # Missing rows, keyed by table index, to dump in case of failure.
    missing_rows = {}

    for table_index, table in tables:
        all_found = True

        # Each element represents the index on the page's table where the
        # expected row was found.
        rows_index = []

        for expected_row in expected_table:
            # Each row searched for should be found in at least one row of the
            # actual table.
            row_index = is_row_in_table(table, expected_row)

            if row_index is not None:
                rows_index.append(row_index)
            else:
                all_found = False
                missing_rows.setdefault(table_index, []).append(expected_row)

        if all_found:
            # This table matches.
            return table, rows_index

    # None of the tables matched, print a nice error message.
    print("Found tables:")
    for table_index, table in tables:
        print(table)
        print("Missing rows:")
        for row in missing_rows[table_index]:
            print(row)
        print('--------')

    raise AssertionError("No table on the page matches the expected rows.")


@step(r'I should see table containing rows?(?: in any order)?:$')
@wait_for
def check_table(self):
    """
    Check that there is a table on the page containing the given rows.

    :param self: Object reference to aloe.
        The expected rows are specified as a Gherkin step table.
    :return: None.

    Notes:
        - It checks all the tables in the page.
        - All the rows must be in the same table.
        - Order of columns and rows is not checked.
        - Columns support lookups. Check `LOOKUP_MAP` for available lookups.
    Example:
        And I should see table containing rows in any order:
            | Header 1       | Header 5       | Header6__contains            |
            | Row 7 Column 1 | Row 7 Column 5 | Row 7 Column 6 partial match |
            | Row 1 Column 1 | Row 1 Column 5 | Row 7 Column 6 partial match |

    A table will be found even if it contains some extra columns or rows not
    specified in the step.
    """

    get_table_containing_rows(guess_types(self.hashes))


@step(r'I should see table containing rows in order:$')
@wait_for
def check_table_columns(self):
    """
    Assert expected rows are displayed in the same order and same HTML table.

    :param self: Object reference to aloe.
        The expected rows are specified as a Gherkin step table.
    :return: None.

    Notes:
        - It checks all the tables in the page.
        - All the rows must be in the same table.
        - Rows don't need to be consecutive.
        - Rows can be a subset of the table.
        - Columns can be a subset of the row.
        - Columns support lookups. Check `LOOKUP_MAP` for available lookups.
    Example:
        And I should see table containing rows in order:
            | Header 1       | Header 5       | Header6__contains            |
            | Row 3 Column 1 | Row 3 Column 5 | Row 3 Column 6 partial match |
            | Row 6 Column 1 | Row 6 Column 5 | Row 6 Column 6 partial match |
    """

    __, rows_index = get_table_containing_rows(guess_types(self.hashes))

    # Check that the rows are in the expected order.
    assert_equal(
        rows_index,
        sorted(rows_index),
        "Rows found in table but not in the order specified.",
    )
