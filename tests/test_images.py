"""Test Webdriver Extra steps related with images."""
from __future__ import unicode_literals

from aloe.testing import FeatureTest

from aloe_webdriver_extra.tests.base import feature


class TestImageSteps(FeatureTest):
    """Test steps related with images."""

    @feature()
    def test_image_is_present(self):
        """
        When I visit test page "images"
        Then I should see images with file path "images/play.png"
        And I should see images with file path "play.png"
        And I should see images with filename "images/play.png"
        And I should see images with filename "play.png"
        """

    @feature()
    def test_image_is_not_present(self):
        """
        When I visit test page "images"
        Then I should not see an image with filename "images/roundedL.png"
        And I should not see an image with filename "images/roundedH.png"
        """

    @feature(fails=True)
    def test_fail_image_is_not_present(self):
        """
        When I visit test page "images"
        And I should not see an image with file path "play.png"
        """

    @feature()
    def test_number_of_images(self):
        """
        When I visit test page "images"
        And I should see an image with file path "play.png"
        And I should see 3 images with filename "testing_in_progress.gif"
        """

    @feature(fails=True)
    def test_more_than_one_image(self):
        """
        When I visit test page "images"
        Then I should see an image with filename "testing_in_progress.gif"
        """

    @feature(fails=True)
    def test_incorrect_number_of_images(self):
        """
        When I visit test page "images"
        Then I should see 2 images with filename "testing_in_progress.gif"
        """

    @feature()
    def test_clicking_an_image(self):
        """
        When I visit test page "images"
        And I click image with file path "images/play.png"
        Then I should see "Image clicked"

        When I press "Clear"
        And I click image with file path "play.png"
        Then I should see "Image clicked"

        When I press "Clear"
        And I click image with filename "images/play.png"
        Then I should see "Image clicked"

        When I press "Clear"
        And I click image with filename "play.png"
        Then I should see "Image clicked"

        When I press "Clear"
        And I click the 1st image with filename "testing_in_progress.gif"
        Then I should see "First image clicked"

        When I press "Clear"
        And I click the 3rd image with filename "testing_in_progress.gif"
        Then I should see "Third image clicked"
        """

    @feature(fails=True)
    def test_multiple_images_require_position(self):
        """
        When I visit test page "images"
        And I click image with filename "testing_in_progress.gif
        """
