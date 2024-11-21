"""Test Form steps."""
from __future__ import unicode_literals

from aloe.testing import FeatureTest

from aloe_webdriver.tests.base import skip_if_browser
from aloe_webdriver_extra.tests.base import feature


class TestSteps(FeatureTest):
    """Test steps."""

    @feature()
    def test_options_are_present_or_absent(self):
        """
        When I visit test page "form"
        Then option "Option 1" should be present in selector "Select Example 1"
        And option "option2" should be absent in selector "Select Example 1"
        And option "Option 3" should be absent in selector "Select Example 1"

        And option "Option 1" should be present in selector "select1"
        And option "option2" should be absent in selector "select1"
        And option "Option 3" should be absent in selector "select1"

        And option "Option2 1" should be present in the 2nd selector "Select Example 2"
        And option "Option2 2" should be present in the 2nd selector "Select Example 2"
        And option "Option2 3" should be absent in the 2nd selector "Select Example 2"
        """

    @feature()
    def test_check_selected_option(self):
        """
        When I visit test page "form"
        And I select "Option2 1" from the 1st "Select Example 2"
        Then the 1st select box labelled "Select Example 2" should have "Option2 1" selected

        When I select "Option2 2" from "Select Example 2"
        Then the select box labelled "Select Example 2" should have "Option2 2" selected
        """

    @feature()
    def test_input_values(self):
        """
        When I visit test page "form"
        Then the field labelled "Color Input" should have a value of "#aabbcc"
        And the field labelled "Date Input" should have a value of "1979-12-31"
        And the field labelled "Datetime Input" should have a value of "2017-03-18T04:45"
        And the field labelled "Datetime-local Input" should have a value of "2017-03-18T23:21"
        And the field labelled "Email Input" should have a value of "example@email.com"
        And the field labelled "Image Input" should have a value of "C:\\fakepath\\image.png"
        And the field labelled "Month Input" should have a value of "2015-01"
        And the field labelled "Number Input" should have a value of "12345"
        And the field labelled "Password Input" should have a value of "password"
        And the field labelled "Range Input" should have a value of "18"
        And the field labelled "Search Input" should have a value of "searching"
        And the field labelled "Tel Input" should have a value of "987654321"
        And the 1st field labelled "Text Input" should have a value of "string"
        And the 2nd field labelled "Text Input" should have a value of "string2"
        And the field labelled "Time Input" should have a value of "05:07"
        And the field labelled "URL Input" should have a value of "http://aloe.com/"
        And the field labelled "Week Input" should have a value of "2017-W10"
        """

    @feature()
    def test_file_input_is_present(self):
        """
        When I visit test page "form"
        Then I should see a file input for "File Input"
        """

    @skip_if_browser('phantomjs', "PhantomJS doesn't support file uploading")
    @feature()
    def test_choose_file(self):
        """
        When I visit test page "form"
        Then I choose file "demo_files/dummy.pdf" for file input "File Input"
        """

    @feature()
    def test_button(self):
        """
        When I visit test page "form"
        Then I should see a button with value "Normal button"
        And I should see a button with value "HTML5 button"
        And I should not see a button with value "Exit"
        """

    @feature()
    def test_typing_in_field(self):
        """
        When I visit test page "form"
        And I type "DELETE" on field "Date Input"
        And I type "ENTER" on field "Test textarea"
        """
