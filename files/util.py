"""Utilities for working with downloaded files."""
from __future__ import unicode_literals

import os

from aloe import world
from nose.tools import assert_true

from aloe_webdriver_extra.util import wait_for


def which(program):
    """
    Check if the given program is available in current $PATH.

    :param program: Program name.
    :return: The same program name if it could be found in $PATH and also is
        executable.
        None otherwise.

    Based on http://stackoverflow.com/a/377028
    """

    def is_exe(filepath):
        """
        Check if the file is executable.

        :param filepath: Path to the file to check.
        :return: Boolean. True if the file can be executed.
        """
        return os.path.isfile(filepath) and os.access(filepath, os.X_OK)

    filepath, __ = os.path.split(program)
    if filepath:
        if is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)

            if is_exe(exe_file):
                return exe_file

    return None


def wait_for_file(filename, timeout=None):
    """
    Asserts the file exists otherwise waits for it to be downloaded.

    :param filename: Filename of the expected file without any path
    :param timeout: Time in seconds to wait for the download. Default 5 seconds
    :returns Full path of the downloaded file.

    It is expected that `DOWNLOAD_DIR` is defined in `aloe.world`.
    """

    if timeout is None:
        timeout = 5

    assert hasattr(world, 'DOWNLOAD_DIR'), (
        "`DOWNLOAD_DIR` must be defined in `aloe.world` in order to use any"
        " step related to files downloaded with the browser."
    )

    filename = os.path.join(world.DOWNLOAD_DIR, filename)
    wait_for(
        lambda: assert_true(os.path.isfile(filename))
    )(timeout=int(timeout))

    return filename
