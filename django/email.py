"""Steps for handling emails"""

from __future__ import absolute_import, unicode_literals

import re

from django.core import mail  # pylint:disable=import-error

from aloe import step

from aloe_webdriver_extra.util import CAPTURE_POSITION, CAPTURE_NUMBER


LINK_RE = re.compile(r'https?://[^/]+(/[^\s]*)')


@step(r'I open the {POSITION} link from the(?: last)? email$'.format(
    POSITION=CAPTURE_POSITION,
))
def click_link_in_email(self, position):
    """
    Click the link from the last email.

    :param self: Object reference to aloe.
    :param position: 1-based position of the link in the email.
    :return: None.
    """

    last_email = mail.outbox[-1]  # pylint:disable=no-member

    link = LINK_RE.findall(last_email.body)[int(position) - 1]

    self.given('I visit site page "{link}"'.format(link=link))


@step(
    r'last email should have {NUMBER} recipients? in the (to|cc|bcc)$'.format(
        NUMBER=CAPTURE_NUMBER,
    ))
def number_of_recipients(self, expected, section):
    """
    Check that an email has been sent to a certain number of recipients.

    :param self: Object reference to aloe. [Not used].
    :param expected: Number of expected recipients.
    :param section: Section of the email header to check for recipients.
    :return: None.
    """

    last_email = mail.outbox[-1]  # pylint:disable=no-member

    recipients = getattr(last_email, section)
    total_recipients = len(recipients)

    assert int(expected) == total_recipients, (
        "Expected {expected} addresses on the {section}, got {found}:\n"
        "{recipients}".format(
            expected=expected,
            section=section,
            found=total_recipients,
            recipients=recipients,
        ))
