"""Test Webdriver Extra steps."""
from __future__ import unicode_literals

from aloe.testing import FeatureTest

from aloe_webdriver.tests.base import skip_if_browser
from aloe_webdriver_extra.tests.base import feature


class TestSteps(FeatureTest):
    """Test steps."""

    @feature()
    def test_page_title(self):
        """
        When I visit test page "verify_page"
        Then I should see page title "Page Title"
        """

    @skip_if_browser('phantomjs', "PhantomJS doesn't support alerts")
    @feature()
    def test_alert_containig_text(self):
        """
        When I visit test page "alert_page"
        Then I should see an alert containing text "alerting alert"
        """

    @feature()
    def test_text_multiple_times(self):
        """
        When I visit test page "verify_page"
        Then I should see "This text is repeated." 3 times
        """

    @feature()
    def test_page_contains(self):
        """
        When I visit test page "verify_page"
        Then page source should contain "This text is repeated."
        And page source should not contain "Aliens"
        """

    @feature()
    def test_definition_list(self):
        """
        When I visit test page "verify_page"
        Then I should see "Description 1" as the value for "Term 1"
        And I should see "Description 2" as the value for "Term 2"
        """
