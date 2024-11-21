"""Gherkin steps to work with downloaded CSV files."""
from __future__ import absolute_import, print_function, unicode_literals

import csv
from codecs import open  # pylint:disable=redefined-builtin

from aloe import step
from aloe.tools import guess_types
from nose.tools import (
    assert_equal,
    assert_true,
)

from aloe_webdriver.util import wait_for
from aloe_webdriver_extra.util import (
    CAPTURE_STRING,
    NUMBER,
    get_lookup_function,
)
from .util import wait_for_file


# Do not limit output from diff in assert_equal.
assert_equal.__self__.maxDiff = None  # pylint:disable=no-member


def downloaded_csv_file(filename, dicts=True):
    """
    Return the content of a downloaded CSV file as a list of dicts or lists.

    :param filename: CSV filename.
    :param dicts: whether to convert CSV rows to dicts; if False, the first
        row in the result is the header row.
    :return: List of dicts or lists with the content of the given file.
    """

    with open(wait_for_file(filename), 'r') as csv_file:
        if dicts:
            return [row for row in guess_types(csv.DictReader(csv_file))]

        return guess_types(csv.reader(csv_file))


def rows_match(csv_row, given_row):
    """
    Compare a CSV row and a row given in a feature test.

    :param csv_row: A dictionary mapping column names to values.
    :param given_row: A dictionary mapping column names (with optional string
        compare functions affixed with '__') to values.
    :return: True if every key in the given row is found in the CSV row, and
        the values for each key compare equally for the given key function.
    """

    print('Compare\n{}\n{}\n'.format(csv_row, given_row))

    for column_name in given_row:

        given_value = given_row[column_name]

        lookup_function, column_name = get_lookup_function(column_name)

        if column_name not in csv_row:
            print('{} not in {}\n'.format(column_name, csv_row))
            return False

        csv_value = csv_row[column_name]

        if not lookup_function(given_value, csv_value):
            print('{} returns {} for {}, {}'.format(
                lookup_function,
                lookup_function(given_value, csv_value),
                csv_value,
                given_value,
            ))
            return False

    return True


def find_row(csv_rows, given_row):
    """
    Find a row given in a feature test in a list of CSV rows.

    :param csv_rows: A list of dictionaries mapping column names to values.
    :param given_row: A dictionary mapping column names (with optional string
        compare functions affixed with '__') to values.
    :return: The index of the matching row, or None if it isn't found.
    """

    for index, csv_row in enumerate(csv_rows):
        if rows_match(csv_row, given_row):
            return index

    return None


def check_for_rows_in_csv(csv_filename, given_rows):
    """
    Check that the CSV contains the expected rows.

    :param csv_filename: CSV filename to check.
    :param given_rows: A list of dictionaries containing the
        rows expected in the csv.
    :return: A list with the position of each row in the file.
    """

    csv_rows = downloaded_csv_file(csv_filename)

    row_indices = []

    for given_row in given_rows:

        found_index = find_row(csv_rows, given_row)

        assert_true(
            found_index is not None,
            'CSV row not found in {}: {}'.format(
                csv_filename,
                given_row,
            )
        )

        row_indices.append(found_index)

    return row_indices


@step(r'Downloaded CSV file {STRING} should contain:$'.format(
    STRING=CAPTURE_STRING,
))
@wait_for
def check_csv_file(self, filename):
    """
    Check that the given data exists on the CSV file.

    :param self: Object reference to aloe.
    :param filename: Filename of the CSV file to verify.
    :return: None.
    """
    assert self.table is not None, 'CSV content not specified'

    check_for_rows_in_csv(filename, guess_types(self.hashes))


@step(r'Downloaded CSV file {STRING} should contain rows in order:$'.format(
    STRING=CAPTURE_STRING,
))
@wait_for
def check_csv_file_in_order(self, filename):
    """
    Check that the given data exists on the CSV file in the required order.

    :param self: Object reference to aloe.
    :param filename: Filename of the CSV file to verify.
    :return: None.
    """
    assert self.table is not None, 'CSV content not specified'

    row_indices = check_for_rows_in_csv(filename, guess_types(self.hashes))

    # Check that the rows are in the expected order
    assert_equal(
        row_indices,
        sorted(row_indices),
        "Rows found in CSV but not in the order specified."
    )


@step(r'Downloaded CSV file {STRING} should have ({NUMBER}) rows$'.format(
    NUMBER=NUMBER,
    STRING=CAPTURE_STRING,
))
@wait_for
def check_csv_length(self, filename, length):
    """
    Check that the given CSV have the exact number of columns.

    :param self: Object reference to aloe. [Not used]
    :param filename: Filename of the CSV file to verify.
    :param length: Number of rows to be expected in the file. The header is not
        counted.
    """

    csv_array = downloaded_csv_file(filename)
    len_csv = len(csv_array)

    assert len_csv == int(length), (
        "CSV has {found} rows, expected {expected}.".format(
            found=len_csv,
            expected=length,
        )
    )


@step(r'downloaded CSV file {STRING} should have headers:$'.format(
    STRING=CAPTURE_STRING,
))
@wait_for
def check_csv_headers(self, filename):
    """
    Check that the CSV file has the specified headers.

    :param self: Object reference to aloe.
    :param filename: Filename of the file to verify.
    :return: None
    """

    assert self.table is not None, 'CSV content not specified'

    expected = [header for (header,) in self.table]

    actual = downloaded_csv_file(filename, dicts=False)

    assert actual, "Downloaded CSV file has no data."

    assert_equal(expected, actual[0])
