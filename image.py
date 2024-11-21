"""Gherkin steps related with images."""
from __future__ import unicode_literals

from aloe import step

from aloe_webdriver_extra.util import (
    CAPTURE_NUMBER,
    CAPTURE_OPTIONAL_POSITION,
    CAPTURE_STRING,
    find_visible_elements_by_xpath,
    nth_element,
)


def get_image_elements(
        path, allow_multiple_images=True, assert_images_exist=True):
    """
    Extract an image elements matching the given path.

    :param path: String to match against `src` as in `<img src="path">`.
        The path is not matched in full, but is should match the last part, it
        allows to specify the filename if needed. e.g.
            image.src = '/static/img/image.jpg'

            matching_paths = [
                'image.jpg',
                'img/image.jpg',
                '/static/img/image.jpg',
            ]
    :param allow_multiple_images: Whether to check if there is one or multiple
        images matching the given `path`.
    :param assert_images_exist: Whether to assert if images were found.
    :return: A list of images.
    """

    xpath = '//img[contains(@src, "{}")]'.format(path)
    images = find_visible_elements_by_xpath(xpath)

    if images:
        images = [
            image
            for image in images
            if image.get_attribute('src').endswith(path)
        ]

    if assert_images_exist:
        assert images, (
            "Image with file path '{}' was not present.".format(path)
        )

    if not allow_multiple_images:
        assert len(images) == 1, "Multiple images were found."

    return images


@step(r"I should see images with (?:file path|filename) {STRING}$".format(
    STRING=CAPTURE_STRING,
))
def should_see_images(self, path):
    """
    Assert that an image with given path|filename is present.

    This step passes regardless of the number of images present.
    """

    get_image_elements(path, allow_multiple_images=True)


@step(
    r"I should not see an image with (?:file path|filename) {STRING}$".format(
        STRING=CAPTURE_STRING,
    )
)
def should_not_see_images(self, path):
    """Assert that an image with given path|filename is not present."""

    images = get_image_elements(
        path,
        allow_multiple_images=True,
        assert_images_exist=False,
    )

    found = len(images)

    assert found == 0, (
        "Images with file path '{path}' are present. Found {found}.".format(
            path=path,
            found=found,
        )
    )


@step(
    r"I should see (?:an image|{NUMBER} images?) with (?:file path|filename)"
    r" {STRING}$".format(
        NUMBER=CAPTURE_NUMBER,
        STRING=CAPTURE_STRING,
    )
)
def should_see_a_number_of_images(self, number, path):
    """
    Assert that an image is present in certain quantity.

    :param number: A numeric value indicating the number of images expected.
    :param path: The expected image path or part of it.
    """

    if number is None:
        number = 1

    images = get_image_elements(path, allow_multiple_images=True)

    found = len(images)
    assert found == int(number), (
        "Found {found} images with path [{path}], expected"
        " {expected}".format(
            expected=number,
            found=found,
            path=path,
        )
    )


@step(r"I click {POSITION}image with (?:file path|filename) {STRING}$".format(
    POSITION=CAPTURE_OPTIONAL_POSITION,
    STRING=CAPTURE_STRING,
))
def click_image(self, position, path):
    """Click an image containing the given path|filename."""

    multiple_images = False

    if position is not None:
        multiple_images = True

    image = nth_element(
        get_image_elements(path, allow_multiple_images=multiple_images),
        position,
        "Couldn't find the {position} image with file path or filename"
        " {path}".format(
            position=position,
            path=path,
        )
    )
    image.click()
