"""Entry point definitions."""
from __future__ import absolute_import, print_function, unicode_literals

import argparse
from textwrap import dedent

from aloe.registry import STEP_REGISTRY
from aloe_webdriver_extra.util import (
    BOOLEAN,
    NULL,
    NUMBER,
    STRING,
    TOKEN,
    CAPTURE_NUMBER,
    CAPTURE_OPTIONAL_POSITION,
    CAPTURE_POSITION,
    CAPTURE_STRING,
    CAPTURE_STRING_INSIDE_SINGLE_QUOTE,
)

# pylint:disable=ungrouped-imports,unused-import
import aloe_webdriver.css
import aloe_webdriver_extra
import aloe_webdriver_extra.files
import aloe_webdriver_extra.select2

try:
    from django.conf import settings

    DJANGO_IS_INSTALLED = True

    # If Django has been configured then load the Django steps.
    if settings.configured:
        import aloe_webdriver.django
        import aloe_webdriver_extra.django
except ImportError:
    # Django is not installed, ignore Django steps.
    DJANGO_IS_INSTALLED = False
# pylint:enable=ungrouped-imports,unused-import


RESET_COLOR = '\033[0m'
TITLE_COLOR = '\33[34m'  # Blue.
SUBSTITUTION_COLOR = '\033[32m'  # Green.

REGEXES_TO_REPLACE = {
    BOOLEAN: '{BOOLEAN}',
    NULL: '{NULL}',
    NUMBER: '{NUMBER}',
    STRING: '"STRING"' + " or 'STRING'",
    TOKEN: '{TOKEN}',
    CAPTURE_NUMBER: '{NUMBER}',
    CAPTURE_OPTIONAL_POSITION: '{OPTIONAL_POSITION}',
    CAPTURE_POSITION: '{POSITION}',
    CAPTURE_STRING: '"STRING"',
    CAPTURE_STRING_INSIDE_SINGLE_QUOTE: "'STRING'",
}

REGEXES_TO_COLOR = {
    '\033[31m': [  # Red.
        r'(?:st|nd|rd|th)',
    ],
    '\033[91m': [  # Light Red.
        r'\d+',
        r'.*?',
        r'[^"]*',
        r"[^']*",
        r'[^"]+',
        r"[^']+",
        r'-?\d+(?:\.\d*)',
        r'\d{4}-\d{2}-\d{2}',
        r'(\d{,2}):(\d{2})h)?',
    ],
}


def color_regexes(string, use_substitutions=True):
    """Simple function to ANSI color regular expressions in strings."""

    if use_substitutions:
        for pattern in sorted(REGEXES_TO_REPLACE, key=len, reverse=True):
            substitution = REGEXES_TO_REPLACE[pattern]

            string = string.replace(
                pattern, '{COLOR}{SUBSTITUTION}{RESET}'.format(
                    COLOR=SUBSTITUTION_COLOR,
                    RESET=RESET_COLOR,
                    SUBSTITUTION=substitution,
                )
            )

    for color, patterns in REGEXES_TO_COLOR.items():
        for pattern in patterns:
            string = string.replace(
                pattern,
                '{COLOR}{REGEX}{RESET}'.format(
                    COLOR=color,
                    REGEX=pattern,
                    RESET=RESET_COLOR,
                )
            )

    return string


def substitution_info():
    """Print the substitutions made on regular expressions."""

    print('{COLOR}\nConventions:'.format(
        COLOR=TITLE_COLOR,
    ))
    print('{UNDERLINE}{RESET}'.format(
        UNDERLINE=('=' * 12),
        RESET=RESET_COLOR,
    ))

    for pattern in sorted(REGEXES_TO_REPLACE, key=len):
        substitution = REGEXES_TO_REPLACE[pattern]
        print('{COLOR}{SUBSTITUTION}{RESET}  {PATTERN}'.format(
            COLOR=SUBSTITUTION_COLOR,
            SUBSTITUTION=substitution,
            PATTERN=pattern,
            RESET=RESET_COLOR,
        ))


def steps_per_module():
    """Read `aloe` step registry and sort the steps by module."""

    modules = {}

    for regex, func in STEP_REGISTRY.steps.values():
        steps = modules.setdefault(func.__module__, [])
        steps.append(regex.pattern)

    for module_name, steps in modules.items():
        modules[module_name] = sorted(steps)

    return modules


def django_info():
    """Check if Django is installed and provide extra information."""

    display_message = False

    if DJANGO_IS_INSTALLED and not settings.configured:
        display_message = True

    if display_message:
        print('\n\n{COLOR}Steps for Django\n{UNDERLINE}{RESET}'.format(
            COLOR=TITLE_COLOR,
            RESET=RESET_COLOR,
            UNDERLINE=('=' * 16),
        ))
        print(dedent("""\
            Steps related to Django are not listed.

            To display these steps, add ``aloe_webdriver_extra`` to your
            project's ``INSTALLED_APPS`` and instead execute:

            python manage.py list_steps
        """))


def list_steps_to_console(use_substitutions=True):
    """
    Print to console the list of steps currently registered in Aloe.

    :param use_substitutions: Whether to substitute known regular expressions
        with a more user friendly text.
    """

    print('List of steps registered')

    counter = 0
    modules = steps_per_module()

    for module_name in sorted(modules):
        print('\n{COLOR}Module: {MODULE_NAME}'.format(
            COLOR=TITLE_COLOR,
            MODULE_NAME=module_name,
        ))
        print('{UNDERLINE}{RESET}'.format(
            UNDERLINE=('=' * (8 + len(module_name))),
            RESET=RESET_COLOR,
        ))

        steps = [
            color_regexes(pattern, use_substitutions)
            for pattern in modules[module_name]
        ]

        print('\n'.join(steps))
        counter += len(steps)

    if use_substitutions:
        substitution_info()

    django_info()

    print('\n\nTotal steps found: {total}'.format(
        total=counter,
    ))


def list_steps():
    """Read `aloe` step registry and list them."""

    parser = argparse.ArgumentParser(description='List all Gherkin steps.')
    parser.add_argument(
        '--no-substitutions',
        dest='use_substitutions',
        action='store_const',
        const=False,
        default=True,
        help=(
            'Do not replace common regular expressions with easier to read '
            'text'
        ),
    )
    args = parser.parse_args()

    list_steps_to_console(args.use_substitutions)
