"""Gherkin steps related with PDF files."""
from __future__ import unicode_literals

import platform
import subprocess
import tempfile

from aloe import step, world

from .util import wait_for_file, which


@step(r'downloaded PDF file "(.*?)" should contain:$')
def check_pdf_file(self, filename):
    """
    Assert the given PDF file contains all the strings in the given list.

    :param self: Object reference to aloe.
    :param filename: PDF filename.
    :return: None.

    How it works:
    Convert PDF file to html and loads it in the browser. This allows to use
    the 'I should see' step and to take a screenshot if it fails.
    At the end the browser is send back to the previous page.
    """

    pdftohtml = 'pdftohtml'

    assert self.table is not None, "PDF content not specified."
    assert which(pdftohtml), (
        "Can't find {program}, it is required for inspecting PDF"
        " files.".format(
            program=pdftohtml,
        )
    )

    with tempfile.NamedTemporaryFile(suffix='.html') as output_file:
        subprocess.check_call([
            pdftohtml,
            '-c',
            '-i',
            '-noframes',
            wait_for_file(filename),
            output_file.name,
        ])

        if platform.system() != 'Darwin':
            # Some versions of pdftohtml output spaces in PDF as non-breakable
            # spaces; convert them back. Not required on Mac.
            subprocess.check_call([
                'sed',
                '-i',
                's/&#160;/ /g',
                output_file.name,
            ])

        # Open html file in browser.
        world.browser.get(output_file.name)

        for (text,) in self.table:
            self.behave_as('And I should see "{0}"'.format(text))

        # Go back to the previous window.
        world.browser.back()
