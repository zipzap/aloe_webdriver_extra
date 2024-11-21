"""Gherkin steps helpful for debugging."""
from __future__ import print_function, unicode_literals

from aloe import step
from builtins import input  # pylint:disable=redefined-builtin


@step(r"pause for a debugging session$")
def pause_debug(self):
    """
    Wait for a key to be pressed for debugging.

    :param self: Object reference to aloe. [Not used].
    :return: None.
    """

    print("Press Enter to continue...")
    input()
