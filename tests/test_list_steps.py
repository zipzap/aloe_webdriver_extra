"""Test `list_steps` command."""
from __future__ import unicode_literals

from unittest import TestCase

from aloe_webdriver_extra.__main__ import steps_per_module


class TestListSteps(TestCase):
    """Test `list_steps` command."""

    def test_steps_per_module(self):
        """Execute the command and check that a dictionary is returned."""

        modules = steps_per_module()

        assert isinstance(modules, dict), (
            "Expected dictionary with module names"
        )
        assert modules, "No modules defined."

        for module_name, steps in modules.items():
            assert steps, "Module {module} doesn't have steps defined".format(
                module=module_name,
            )


class TestStepsRegex(TestCase):
    """Test steps' regex ends with an end-of-line character `$`."""
    ignore_modules = [
        'aloe_webdriver',
        'aloe_webdriver.css',
    ]

    def test_line_ending(self):
        """Check there is an end-of-line character in the step regex."""

        steps = []

        for module, module_steps in steps_per_module().items():
            if module not in self.ignore_modules:
                for step in module_steps:
                    if not step.endswith('$'):
                        steps.append('{module}: {step}'.format(
                            module=module,
                            step=step,
                        ))

        assert not steps, (
            "The following steps don't have an end-of-line character `$`:\n"
            "{steps}".format(
                steps='\n'.join(steps),
            )
        )
