"""Gherkin steps to create Django Users."""
from __future__ import unicode_literals

import hashlib

from django.contrib.auth.models import User  # pylint:disable=import-error

from aloe.tools import guess_types
# pylint:disable=import-error
from aloe_django.steps.models import (
    writes_models,
    write_models,
    reset_sequence,
)
# pylint:enable=import-error

EMAIL_DOMAIN = 'aloe.webdriver.extra.com'
SUPERUSER_EMAIL = 'superuser@{domain}'.format(domain=EMAIL_DOMAIN)
DEFAULT_PASSWORD = 'abc123'


@writes_models(User)
def create_user(data, field=None):
    """
    Allow creating/updating users using Gherkin steps.

    :param data: A list of hashes to build models from.
    :param field: A field name to match models on, or None.
        `field` is the field that is used to get the existing models out of the
        database to update them; otherwise, if ``field=None``, new models are
        created.
    :return: None.

    This can then be accessed via the steps:

    .. code-block:: gherkin

        And I have a user in the database:
            | username | first_name |
            | Baz      | Quux       |

        And I update existing users by pk in the database:
            | pk | username |
            | 1  | Bar      |
    """

    if field:
        return write_models(User, data, field=field)

    user = None
    data = guess_types(data)
    for hash_ in data:
        is_superuser = hash_.pop('is_superuser', False)
        is_staff = None

        if is_superuser:
            if 'email' not in hash_:
                hash_['email'] = SUPERUSER_EMAIL
            if 'password' not in hash_:
                hash_['password'] = DEFAULT_PASSWORD
            if 'is_staff' in hash_:
                del hash_['is_staff']

            user = User.objects.create_superuser(**hash_)
        else:
            is_staff = hash_.pop('is_staff', None)

            if 'username' not in hash_:
                hash_['username'] = (
                    hashlib.md5(hash_['email']).hexdigest()[:30]
                )
            if 'email' not in hash_:
                hash_['email'] = '{username}@{domain}'.format(
                    domain=EMAIL_DOMAIN,
                    username=hash_['username'],
                )
            user = User.objects.create_user(**hash_)

        if is_staff is not None:
            user.is_staff = is_staff
        user.save()

    reset_sequence(User)

    return user
