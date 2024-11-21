"""Test the lookup functions for CSV tables work."""
from __future__ import unicode_literals

from aloe.testing import FeatureTest

from aloe_webdriver.tests.base import skip_if_browser
from aloe_webdriver_extra.tests.base import feature


@skip_if_browser('phantomjs', "PhantomJS doesn't support downloading files.")
class TestCSVLookup(FeatureTest):
    """Test the lookup functions for CSV tables work."""

    @feature()
    def test_row_contains(self):
        """
        When I visit test page "csv_test"
        And I click "Download"
        Then downloaded csv file "csv_test.csv" should contain:
            | person | age | favourite food__contains |
            | bob    | 50  | rice                     |
            | lisa   | 25  | rice                     |
        """

    @feature(fails=True)
    def test_contains_should_fail(self):
        """
        When I visit test page "csv_test"
        And I click "Download"
        Then downloaded csv file "csv_test.csv" should contain:
            | person | favourite food__contains |
            | bob    | eggs                     |
        """

    @feature()
    def test_row_exact(self):
        """
        When I visit test page "csv_test"
        And I click "Download"
        Then downloaded csv file "csv_test.csv" should contain:
            | person | age | favourite food | is_ok |
            | bob    | 50  | fried rice     | true  |
        """

    @feature(fails=True)
    def test_exact_should_fail(self):
        """
        When I visit test page "csv_test"
        And I click "Download"
        Then downloaded csv file "csv_test.csv" should contain:
            | person | favourite food |
            | bob    | eggs           |
        """

    @feature()
    def test_empty_value(self):
        """
        When I visit test page "csv_test"
        And I click "Download"
        Then downloaded csv file "csv_test.csv" should contain:
            | person | age | favourite food |
            | dan    | 33  |                |
        And downloaded csv file "csv_test.csv" should contain:
            | person | age | favourite food__contains |
            | dan    | 33  |                          |
            | lisa   | 25  |                          |
        """

    @feature()
    def test_in_order_passes(self):
        """
        When I visit test page "csv_test"
        And I click "Download"
        Then downloaded csv file "csv_test.csv" should contain rows in order:
            | person | age | favourite food |
            | bob    | 50  | fried rice     |
            | lisa   | 25  | steamed rice   |
            | dan    | 33  |                |
        """

    @feature(fails=True)
    def test_out_of_order_fails(self):
        """
         When I visit test page "csv_test"
        And I click "Download"
        Then downloaded csv file "csv_test.csv" should contain rows in order:
            | person | age | favourite food |
            | lisa   | 25  | steamed rice   |
            | bob    | 50  | fried rice     |
            | dan    | 33  |                |
        """

    @feature()
    def test_boolean_pass(self):
        """
        When I visit test page "csv_test"
        And I click "Download"
        Then downloaded csv file "csv_test.csv" should contain:
            | person | is_ok |
            | bob    | true  |
            | lisa   | true  |
            | dan    | false |
        """

    @feature(fails=True)
    def test_boolean_fail(self):
        """
        When I visit test page "csv_test"
        And I click "Download"
        Then downloaded csv file "csv_test.csv" should contain:
            | person | is_ok |
            | bob    | false |
            | lisa   | true  |
            | dan    | false |
        """

    @feature()
    def test_null(self):
        """
        When I visit test page "csv_test"
        And I click "Download"
        Then downloaded csv file "csv_test.csv" should contain:
            | person | age   | favourite food | is_ok |
            | null   | null  | null           | null  |
        """

    @feature()
    def test_delayed_download_passes(self):
        """
        When I visit test page "csv_test"
        And I click "Download with 6 second delay"
        Then downloaded csv file "csv_test.csv" should contain:
            | person | age | favourite food | is_ok |
            | bob    | 50  | fried rice     | true  |
        """

    @feature()
    def test_longer_delayed_download_passes(self):
        """
        When I visit test page "csv_test"
        And I click "Download with 11 second delay"
        Then downloaded csv file "csv_test.csv" should contain:
            | person | age | favourite food | is_ok |
            | bob    | 50  | fried rice     | true  |
        """

    @feature(fails=True)
    def test_delayed_download_fails(self):
        """
        When I visit test page "csv_test"
        And I click "Download with 25 second delay"
        Then downloaded csv file "csv_test.csv" should contain:
            | person | age | favourite food | is_ok |
            | bob    | 50  | fried rice     | true  |
        """
