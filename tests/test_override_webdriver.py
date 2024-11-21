# -*- coding: utf-8 -*-
"""Test steps that override those in `aloe_webdriver`."""
from __future__ import unicode_literals

from aloe.testing import FeatureTest

from aloe_webdriver_extra.tests.base import feature


class TestSteps(FeatureTest):
    """Test steps."""

    @feature()
    def test_click(self):
        """
        When I visit test page "links"
        And I click "Link 1"
        Then I should see "link1"
        """

    @feature()
    def test_click2(self):
        """
        When I visit test page "links"
        And I click the 1st "Link 2"
        Then I should see "link2_1"
        """

    @feature()
    def test_click3(self):
        """
        When I visit test page "links"
        And I click the 2nd "Link 2"
        Then I should see "link2_2"
        """

    @feature()
    def test_click4(self):
        """
        When I visit test page "links"
        And I click the 3rd "Link 2"
        Then I should see "link2_3"
        """

    @feature()
    def test_click_font_icon(self):
        """
        When I visit test page "links"
        And I click "menu"
        Then I should see "Menu clicked"
        """

    @feature()
    def test_click_unicode(self):
        """
        When I visit test page "links"
        And I click "持続する »"
        Then I should see "Unicode link clicked"
        """

    @feature()
    def test_click_button1(self):
        """
        When I visit test page "links"
        And I click "Edit"
        Then I should see "Edit link clicked"
        """

    @feature()
    def test_seeing_link(self):
        """
        When I visit test page "links"
        Then I should see a link to "Link to anchor" with the url "#anchor"
        And I should see a link to "Link 1" with the url "javascript:result('link1')"
        And I should see a link to "Doodles" with the url "/doodles?q=interactive"
        And I should see a link to "Link to anchor"
        And I should see a link to "Link 1"
        And I should see a link to "Doodles"
        """

    @feature()
    def test_not_seeing_link(self):
        """
        When I visit test page "links"
        Then I should see a link to "Link to anchor" with the url "#anchor"
        And I should not see a link to "This is not a link"
        """

    @feature()
    def test_nbsp(self):
        """
        When I visit test page "links"
        And I click "Link 3"
        Then I should see "link_3"
        """

    @feature()
    def test_link_with_exact_text(self):
        """
        When I visit test page "links"
        And I click link with exact text "Link 3"
        Then I should see "link_3"
        """

    @feature()
    def test_link_with_optional_matching_text(self):
        """
        When I visit test page "links"
        And I click link with text "3"
        Then I should see "link_3"
        """

    @feature()
    def test_link_with_matching_text(self):
        """
        When I visit test page "links"
        And I click link with matching text "3"
        Then I should see "link_3"
        """

    @feature()
    def test_link_with_spaces_between(self):
        """
        When I visit test page "links"
        And I click "Spaces between me"
        Then I should see "space_between_me"
        """

    @feature()
    def test_delayed_link(self):
        """
        When I visit test page "links"
        And I click "Delayed Link"
        Then I should see "delayed_link"
        """

    @feature()
    def test_link_as(self):
        """
        When I visit test page "links"
        And I click button with matching text "Edit"
        Then I should see "Edit link clicked"

        When I click button with matching text "Spaces between"
        Then I should see "space_between_me"

        When I click element "Edit"
        Then I should see "Edit link clicked"

        When I click button "Link 3"
        Then I should see "link_3"

        When I click collapsible "menu"
        Then I should see "Menu clicked"
        """


class TestRadioButtonSteps(FeatureTest):
    """Test radio button steps."""

    @feature()
    def test_radio_input(self):
        """
        When I visit test page "radio"

        And I choose "Second radio button"
        Then I should see "radio_2"

        When I choose the 1st "radio button"
        Then I should see "radio_1"

        When I choose "radio_3"
        Then I should see "radio_3"
        """

    @feature(fails=True)
    def test_radiobutton_step_match(self):
        """
        When I visit test page "radio"
        And I choose "Second radio button" with some extra text
        """
        # It fails because a matching step can't be found.


class TestCheckboxSteps(FeatureTest):
    """Test checkbox steps."""

    @feature(fails=True)
    def test_checkbox_no_position(self):
        """
        When I visit test page "checkbox"
        And I check "Car"
        """
        # It fails because multiple checkboxes are found and no position was
        # given.

    @feature(fails=True)
    def test_checkbox_step_match(self):
        """
        When I visit test page "checkbox"
        And I check "House" with some extra text
        """
        # It fails because a matching step can't be found.

    @feature()
    def test_checkbox_position(self):
        """
        When I visit test page "checkbox"
        And I check the 2nd "Car"
        And I press the 1st "Submit"
        Then I should see "Selected [Car, Caravan]"

        When I uncheck "Caravan"
        And I uncheck the 1st "Car"
        And I check "Bike"
        And I press the 1st "Submit"
        Then I should see "Selected [Bike]"
        """

    @feature()
    def test_checkbox_by_id(self):
        """
        When I visit test page "checkbox"
        And I uncheck the 1st "vehicle_2"
        And I check "vehicle_1"
        And I press the 1st "Submit"
        Then I should see "Selected [Bike]"
        """

    @feature()
    def test_checkbox_by_name(self):
        """
        When I visit test page "checkbox"
        And I check "agree"
        And I press the 3rd "Submit"
        Then I should see "Selected [Yes]"
        """

    @feature(fails=True)
    def test_checkbox_check_already_checked(self):
        """
        When I visit test page "checkbox"
        And I check "House"
        """
        # It fails as it is trying to check an already checked checkbox.

    @feature(fails=True)
    def test_checkbox_uncheck_already_unchecked(self):
        """
        When I visit test page "checkbox"
        And I uncheck "Yes"
        """
        # It fails as it is trying to uncheck an already unchecked checkbox.

    @feature()
    def test_checkbox_is_checked(self):
        """
        When I visit test page "checkbox"
        Then the 1st "Car" checkbox should be checked
        """

    @feature()
    def test_checkbox_is_unchecked(self):
        """
        When I visit test page "checkbox"
        Then the 2nd "Car" checkbox should not be checked
        """

    @feature(fails=True)
    def test_checkbox_is_checked_fails(self):
        """
        When I visit test page "checkbox"
        Then the 1st "Car" checkbox should not be checked
        """
        # It fails as the 1st Car checkbox is checked.
