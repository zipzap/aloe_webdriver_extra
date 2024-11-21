"""Test Webdriver Extra utilities."""
from __future__ import unicode_literals

from aloe.testing import FeatureTest

from aloe_webdriver_extra.tests.base import feature


class TestUtils(FeatureTest):
    """Test utilities."""

    @feature()
    def test_waitfor(self):
        """
        When I visit test page "util"
        Then I should see table containing rows:
            | Header 3 |
            | Value 3  |
        """
