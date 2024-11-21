"""Test date and time related steps."""
from __future__ import unicode_literals

import datetime

from flask import Flask
from threading import Thread

from aloe.testing import FeatureTest

from aloe_webdriver_extra.tests.base import feature


PORT = 5000
SERVER_ADDRESS = '0.0.0.0'
FLASK_APP = Flask(__name__)


def startup_server():
    """Startup webserver."""

    FLASK_APP.run(host=SERVER_ADDRESS, port=PORT)


@FLASK_APP.route("/")
def print_datetime():
    """Print mocked datetime."""

    now = datetime.datetime.utcnow()

    return """
    <p>Date: {now:%Y-%m-%d}</p>
    <br>
    <p>Time: {now:%H:%M:%S}</p>
    """.format(now=now)


WEBSERVER_THREAD = Thread(target=startup_server, name="Test Server")
WEBSERVER_THREAD.daemon = True
WEBSERVER_THREAD.start()


class TestListSteps(FeatureTest):
    """Test date and time related steps"""

    @feature()
    def test_setting_date(self):
        """
        Given today's date is 2014-12-24
        When I visit "http://SERVER_HOST:5000"
        Then I should see "Date: 2014-12-24"
        """

    @feature()
    def test_setting_datetime(self):
        """
        Given today's date is 2015-11-23 and time is 14:35h
        When I visit "http://SERVER_HOST:5000"
        Then I should see "Time: 14:35"
        """

    @feature()
    def test_setting_datetime_timezone_amsterdam(self):
        """
        Given today's date is 2016-10-22 and time is 17:55h in timezone "Europe/Amsterdam"
        When I visit "http://SERVER_HOST:5000"
        Then I should see "Date: 2016-10-22"
        And I should see "Time: 15:55"
        """

        pass

    @feature()
    def test_setting_datetime_timezone_melbourne(self):
        """
        Given today's date is 2016-10-22 and time is 17:56h in timezone "Australia/Melbourne"
        When I visit "http://SERVER_HOST:5000"
        Then I should see "Date: 2016-10-22"
        And I should see "Time: 06:56"
        """

        pass
