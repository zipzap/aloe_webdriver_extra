"""Gherkin steps related to Django commands."""
from __future__ import unicode_literals

import json

from deprecated import deprecated

from django.core.management import call_command  # pylint:disable=import-error

from aloe import step


@step(
    r'Django management command "([^"]*)" is run(?: with params "([^"]*)")?$')
def django_call_command(self, command, params):
    """
    Call Django administrative commands.

    Params are specified in JSON format:
        {'param1': 'value'}
    """

    dict_params = {}
    if params:
        json_acceptable_string = params.replace("'", "\"")
        dict_params = json.loads(json_acceptable_string)

    call_command(command, **dict_params)


# pylint:disable=invalid-name
original_step_text = r'Call command "([^"]*)"(?: with params "([^"]*)")?$'
reason = (
    'The `Call command ...` step has been deprecated and will be removed in a'
    'future version.\n'
    'It has been replaced with `Django management command ... is run`'
)
deprecated_step = deprecated(reason=reason)(django_call_command)
step(original_step_text)(deprecated_step)
# pylint:enable=invalid-name
