"""Base functions for tests."""
from __future__ import unicode_literals

import os
import threading
from contextlib import contextmanager
from functools import wraps
from http.server import SimpleHTTPRequestHandler

from aloe.testing import in_directory
from aloe_webdriver.tests.base import (
    TestRequestHandler as OriginalTestRequestHandler,
    TestServer,
)


def feature(fails=False):
    """
    Decorate a test method to test the feature contained in its docstring.

    For example:
        @feature(failed=False)
        def test_some_feature(self):
            '''
            When I ...
            Then I ...
            '''

    The method code is ignored.
    """

    def outer(func):
        """
        A decorator to run the function as the feature contained in docstring.
        """

        @wraps(func)
        @in_directory(os.path.dirname(__file__))
        def inner(self):
            """Run the scenario from docstring."""

            scenario = func.__doc__

            # Make it possible to reference SERVER_HOST in URLs inside
            # scenarios
            scenario = scenario.replace(
                'SERVER_HOST',
                os.environ.get('SERVER_HOST', '0.0.0.0')
            )

            feature_string = """
            Feature: {name}
            Scenario: {name}
            {scenario_string}
            """.format(name=func.__name__, scenario_string=scenario)

            result = self.run_feature_string(feature_string)

            if fails:
                self.assertFalse(result.success)
            else:
                self.assertTrue(result.success)

        return inner

    return outer


class TestRequestHandler(OriginalTestRequestHandler):
    """A handler serving the test pages."""

    def translate_path(self, path):
        """Serve the pages directory instead of the current directory."""

        source_dirname = 'html_pages'

        if path.startswith('/static/'):
            source_dirname = 'static_files'

            path = path[7:]

        return SimpleHTTPRequestHandler.translate_path(
            self,
            '/'
            + os.path.relpath(
                os.path.join(os.path.dirname(__file__), source_dirname)
            )
            + path,
        )


@contextmanager
def test_server():
    """A context manager starting a server for the test pages."""

    port = 7755

    server = TestServer(('', port), TestRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    # When running the browser in Docker, pass the host address
    # to allow the container to access the server on the host
    if 'SERVER_HOST' in os.environ:
        address = (os.environ['SERVER_HOST'], port)
    else:
        address = server.server_address

    yield server, address

    server.shutdown()
    server_thread.join()
    server.server_close()
