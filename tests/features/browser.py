"""Steps related to browsers."""
from __future__ import unicode_literals

import os
import shutil
import tempfile
from contextlib import contextmanager

from aloe import world, around
from aloe_webdriver.tests.base import browser_type
from selenium import webdriver


def remove_dir_contents(path):
    """Remove contents in given directory."""

    if not path.startswith('/tmp/'):
        raise RuntimeError('Directory must be located on /tmp/')

    for root, dirs, files in os.walk(path):
        for file_ in files:
            os.unlink(os.path.join(root, file_))
        for directory in dirs:
            shutil.rmtree(os.path.join(root, directory))


@contextmanager
def temporary_directory():
    """
    A context manager to create a temporary directory and remove it on exit.
    """

    if 'SELENIUM_DOWNLOAD_DIR' in os.environ:
        tempdir = os.environ['SELENIUM_DOWNLOAD_DIR']
    else:
        tempdir = tempfile.mkdtemp()

    try:
        yield tempdir
    finally:
        if 'SELENIUM_DOWNLOAD_DIR' in os.environ:
            # Remove directory contents but not the directory itself.
            remove_dir_contents(tempdir)
        else:
            # Remove the directory and all its contents.
            shutil.rmtree(tempdir)


def firefox_profile(is_remote=False):
    """
    Build a Firefox profile.

    This profile enforces saving downloaded files instead of asking and
    also store them in the directory defined by `world.DOWNLOAD_DIR`.
    """
    profile = webdriver.FirefoxProfile()
    download_dir = world.DOWNLOAD_DIR

    if is_remote:
        download_dir = '/home/seluser/Downloads'

    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', download_dir)
    profile.set_preference(
        'browser.helperApps.neverAsk.saveToDisk', 'text/csv')

    return profile


def capabilities_for(browser):
    """Build capabilities for given browser."""

    capabilities = getattr(webdriver.DesiredCapabilities, browser.upper())

    return capabilities


def create_browser():
    """Create a Selenium browser for tests."""

    browser = browser_type()

    if 'SELENIUM_ADDRESS' in os.environ:
        address = 'http://{}/wd/hub'.format(os.environ['SELENIUM_ADDRESS'])

        extra_args = {}

        if browser == 'firefox':
            extra_args['browser_profile'] = firefox_profile(is_remote=True)

        return webdriver.Remote(
            address,
            desired_capabilities=capabilities_for(browser),
            **extra_args)

    if browser == 'chrome':
        capabilities = webdriver.DesiredCapabilities.CHROME
        capabilities.update({
            'goog:chromeOptions': {
                'prefs': {
                    'download.default_directory': world.DOWNLOAD_DIR,
                    'download.prompt_for_download': False,
                },
            },
        })
        browser_driver = webdriver.Chrome(desired_capabilities=capabilities)
    elif browser == 'firefox':
        # Firefox >= 53
        browser_driver = webdriver.Firefox(firefox_profile=firefox_profile())
    else:
        browser_driver = webdriver.PhantomJS()

    # Explicitly specify the browser locale for the date input tests to work
    # regardless of the user's settings.
    old_lc_all = os.environ.get('LC_ALL', '')
    try:
        os.environ['LC_ALL'] = 'en_US'
        return browser_driver
    finally:
        os.environ['LC_ALL'] = old_lc_all


@around.all
@contextmanager
def with_browser():
    """Start a browser for the tests."""

    with temporary_directory() as temp_dir:
        world.DOWNLOAD_DIR = temp_dir

        world.browser = create_browser()

        yield

        world.browser.quit()
        delattr(world, 'browser')
