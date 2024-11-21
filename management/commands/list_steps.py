"""Management command to list all available Gherkin steps."""

from django.core.management.commands.test import Command as TestCommand

from aloe.fs import FeatureLoader
from aloe_webdriver_extra.__main__ import list_steps_to_console


class Command(TestCommand):
    """Django command: list_steps"""

    help = "List available Gherkin steps."

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-substitutions',
            dest='use_substitutions',
            action='store_const',
            const=False,
            default=True,
            help=(
                'Do not replace common regular expressions with easier to '
                'read text'
            ),
        )

    def handle(self, *test_labels, **options):
        """List available Gherkin steps."""

        feature_dirs = [
            dir_
            for dir_ in FeatureLoader.find_feature_directories('.')
        ]

        for feature_dir in feature_dirs:
            FeatureLoader.find_and_load_step_definitions(feature_dir)

        list_steps_to_console(options['use_substitutions'])
