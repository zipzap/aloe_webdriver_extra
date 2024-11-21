"""Steps for testing."""

import os

try:
    reload
except NameError:
    # pylint:disable=no-name-in-module,redefined-builtin
    from importlib import reload
    # pylint:enable=no-name-in-module,redefined-builtin

# Register steps.
import aloe_webdriver
import aloe_webdriver_extra.files.csv
import aloe_webdriver_extra.date_and_time
import aloe_webdriver_extra.debug
import aloe_webdriver_extra.files  # pylint:disable=redefined-builtin
import aloe_webdriver_extra.form
import aloe_webdriver_extra.iframe
import aloe_webdriver_extra.image
import aloe_webdriver_extra.misc
import aloe_webdriver_extra.override_webdriver
import aloe_webdriver_extra.table
import aloe_webdriver_extra.verify
import aloe_webdriver_extra.wcag
import aloe_webdriver_extra.select2
import aloe_webdriver_extra.window


# This module is reloaded during testing in order to re-register the steps and
# callbacks. This makes sure the modules where the steps are defined are, too.
reload(aloe_webdriver)
reload(aloe_webdriver_extra.files.csv)
reload(aloe_webdriver_extra.date_and_time)
reload(aloe_webdriver_extra.debug)
reload(aloe_webdriver_extra.files.csv)
reload(aloe_webdriver_extra.files.download)
reload(aloe_webdriver_extra.files.pdf)
reload(aloe_webdriver_extra.files.xlsx)
reload(aloe_webdriver_extra.form)
reload(aloe_webdriver_extra.iframe)
reload(aloe_webdriver_extra.image)
reload(aloe_webdriver_extra.misc)
reload(aloe_webdriver_extra.override_webdriver)
reload(aloe_webdriver_extra.table)
reload(aloe_webdriver_extra.verify)
reload(aloe_webdriver_extra.wcag)
reload(aloe_webdriver_extra.select2)
reload(aloe_webdriver_extra.window)

if os.environ.get('TAKE_SCREENSHOTS'):
    # Only register the screenshot steps if asked to.
    import aloe_webdriver.screenshot_failed  # pylint:disable=ungrouped-imports
    reload(aloe_webdriver.screenshot_failed)

    SCREENSHOTS_DIR = os.environ.get('SCREENSHOTS_DIR')
    if SCREENSHOTS_DIR:
        aloe_webdriver.screenshot_failed.DIRECTORY = SCREENSHOTS_DIR
