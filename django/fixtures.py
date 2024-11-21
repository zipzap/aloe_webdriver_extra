"""Gherkin steps related to Django fixtures."""
from __future__ import unicode_literals

from aloe import step
from django.core.management import call_command  # pylint:disable=import-error


@step(r'fixtures from "([^"]+)" are loaded$')
def fixtures_loaded(self, fixtures):
    """
    Load some fixtures from a directory or file.

    :param self: Object reference to aloe. [Not used].
    :param fixtures: Path to a directory or a single file.
    :return: None.
    """

    call_command('loaddata', fixtures, interactive=False, verbosity=0)


@step(r"^fixtures are loaded:$")
def multiple_fixtures_loaded(self):
    """
    Load several fixtures at once.

    :param self: Object reference to aloe.
    :return: None.

    Fixture directories or files path are specified in a table. e.g:

        Given fixtures are loaded:
            | path/to/directory/ |
            | path/to/file.json  |
    """

    for (fixtures,) in self.table:
        fixtures_loaded(self, fixtures)
