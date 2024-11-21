"""Test steps for select2 element."""
from __future__ import unicode_literals

from aloe.testing import FeatureTest

from aloe_webdriver_extra.tests.base import feature


class TestSelect2Steps(FeatureTest):
    """Test class for select2 steps"""

    @feature()
    def test_dropdown_select2(self):
        """
        When I visit test page "select2"
        And I select "Cranberry" in dropdown "More Extra Fruits"
        And I click "Submit"
        Then I should see ':::Cranberry'

        When I select "Crab apples" in dropdown "More Extra Fruits"
        And I click "Submit"
        Then I should see ':::Crab apples'
        """

    @feature()
    def test_multioption_select2(self):
        """
        When I visit test page "select2"
        And I select 'Pineapple "2.0"' from the 1st multiselect 'Fruits'
        And I select "Mango" from multiselect "Fruits"
        And I select "Kiwi" from the 2nd multiselect "Fruits"
        And I click "Submit"
        Then I should see 'Pineapple "2.0",Mango:Kiwi::'

        When I deselect 'Pineapple "2.0"' from multiselect 'Fruits'
        And I click "Submit"
        Then I should see "Mango:Kiwi::"

        When I deselect "Mango" from the 1st multiselect "Fruits"
        And I deselect "Kiwi" from multiselect "More Fruits"
        And I click "Submit"
        Then I should see ":::"
        """

    @feature()
    def test_select2_option_status(self):
        """
        When I visit test page "select2"
        Then option "Pomegranate" should be enabled in the 1st selector "Extra Fruits"
        And option "Tomato" should be enabled in the 1st selector "Extra Fruits"
        And option "Durian" should be disabled in the 1st selector "Extra Fruits"

        When I click "Toggle"
        Then option "Pomegranate" should be disabled in the 2nd selector "Extra Fruits"
        And option "Tomato" should be disabled in the 2nd selector "Extra Fruits"
        And option "Durian" should be enabled in the 2nd selector "Extra Fruits"
        """
