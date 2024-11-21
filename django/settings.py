"""Gherkin steps to modify Django settings."""
from __future__ import unicode_literals

# pylint:disable=import-error
from django.conf import settings, UserSettingsHolder
from django.utils import timezone
# pylint:enable=import-error

from aloe import after, before, step, world


def clear_caches():
    """
    Clear the cache of Django modules initialised with setting values.

    It is possible that overriding the settings doesn't have any effect on
    certain modules or that after the first override a second one doesn't
    change the behavior/status of given modules.

    In that case it is possible that those modules are caching the values from
    settings in which case it would be required to clear the cache every time
    settings are overridden.
    """

    # Clear Timezone cache.
    timezone.get_default_timezone.cache_clear()


def reset_env(scenario, *args):
    """
    Prepare the environment before each scenario.
    """

    world.original_settings = settings._wrapped  # pylint:disable=protected-access
    world.monkeypatched_settings = UserSettingsHolder(world.original_settings)


before.each_example(function=reset_env, name='reset_env')


def reset_django_settings(*args):
    """
    Reset the Django settings to the original values.

    Original values are stored in the world.settings_monkeypatches dictionary.
    """

    if hasattr(world, 'original_settings'):
        setattr(settings, '_wrapped', world.original_settings)
        world.monkeypatched_settings = None

        clear_caches()


after.each_example(function=reset_django_settings, name='reset_django_settings')


def django_setting(name, value, require_existing=True):
    """Set a Django setting."""

    # Raise an exception if the setting is not defined but it's required to be.
    if require_existing and not hasattr(settings, name):
        raise AttributeError

    # Set new value.
    setattr(world.monkeypatched_settings, name, value)

    # Refresh settings.
    setattr(settings, '_wrapped', world.monkeypatched_settings)

    clear_caches()


@step(r'The Django setting "([^"]*)" is "([^"]*)"$')
def django_setting_text(self, name, value, exists=True):
    """Set a text Django setting."""

    django_setting(name, value, exists)


@step(r'The Django setting "([^"]*)" is (-?\d+(?:\.\d+)?)$')
def django_setting_numeric(self, name, value, exists=True):
    """Set a numeric Django setting."""

    django_setting(name, float(value), exists)


@step(r'The Django setting "([^"]*)" is (True|true|False|false)$')
def django_setting_boolean(self, name, value, exists=True):
    """Set a boolean Django setting."""

    value = (value.lower() == 'true')

    django_setting(name, value, exists)
