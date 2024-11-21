"""Gherkin steps related with browser's window."""
from __future__ import unicode_literals

from aloe import step, world

from aloe_webdriver_extra.util import wait_for


@step(r'I switch to browser window with name "(.*?)"$')
@wait_for
def switch_to_window(self, window_id):
    """
    Switch to another browser window. Useful for lookup popups.

    :param self: Object reference to aloe. [Not used].
    :param window_id: ID that identify the window.
    :return: None.
    """
    world.browser.switch_to.window(window_id)


@step(r"I switch to the newly opened window$")
@wait_for
def switch_to_new_window(self):
    """
    Check that a new window was opened and switch to it.

    :param self: Object reference to aloe. [Not used].
    :return: None.
    """

    current_window = world.browser.current_window_handle
    new_window = world.browser.window_handles[-1]

    assert current_window != new_window, "Couldn't find newly opened window"

    world.browser.switch_to_window(new_window)


@step(r"I close the current window$")
@wait_for
def close_current_window(self):
    """
    Close current window, unless is the main window.

    :param self: Object reference to aloe. [Not used].
    :return: None.
    """

    current_window = world.browser.current_window_handle
    main_window = world.browser.window_handles[0]

    assert current_window != main_window, "Can't close the main window"

    world.browser.close()
    world.browser.switch_to_window(main_window)
