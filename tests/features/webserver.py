"""Steps related with the web server."""

from __future__ import unicode_literals

from contextlib import contextmanager

from aloe import around, world

from aloe_webdriver_extra.tests.base import test_server


@around.all
@contextmanager
def with_test_server():
    """Start a server for the test pages."""

    with test_server() as (server, address):
        world.server = server
        world.base_address = address
        yield
