"""Steps related with browser navigation."""
from __future__ import unicode_literals

from aloe import before, world, step


@before.each_feature
def reset_page(feature):
    """Reset the browser before each feature."""
    world.browser.get('about:blank')


@step(r'I visit test page "([^"]+)"$')
def visit_test_page(self, page):
    """Open a test page in the browser."""
    self.when('I visit "http://{address[0]}:{address[1]}/{page}.html"'.format(
        address=world.base_address,
        page=page,
    ))
