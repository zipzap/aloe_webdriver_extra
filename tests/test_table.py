"""Test `table steps` command."""
from __future__ import unicode_literals

from aloe.testing import FeatureTest
from aloe_webdriver_extra.tests.base import feature


class TestTableSteps(FeatureTest):
    """Test table step commands"""

    @feature()
    def test_content_in_table_rows(self):
        """
        When I visit test page "table"
        Then I should see table containing rows:
            | Name__contains | Age__equals | Address             |
            | Markel         | 50          | CBD, Sydney         |
            | Jill           | 55          | Melbourne, Victoria |

        And I should see table containing rows in order:
            | Name__contains | Age__equals | Address             |
            | Jill           | 55          | Melbourne, Victoria |
            | Markel         | 50          | CBD, Sydney         |
        """
