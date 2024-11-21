"""Helper steps that smooth the operation of Django when running Aloe."""

from time import sleep

# pylint:disable=import-error
from django.db.utils import DatabaseError
from django.core.management import call_command
from django.core.management.base import CommandError
# pylint:enable=import-error

from aloe import after


def flush_db(self, scenario, outline):
    """Flush the database after each example."""

    # The browser might still keep some connections alive, try a few times
    max_attempts = 10
    for attempt in range(max_attempts + 1):
        try:
            call_command('flush', interactive=False, verbosity=0)
            break
        except (DatabaseError, CommandError):
            if attempt == max_attempts:
                raise
            sleep(1)


after.each_example(function=flush_db, name='flush_db')
