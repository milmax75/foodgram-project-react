from django.core.exceptions import ValidationError
import re


def validate_username(value):
    if not re.compile(r'[\w.@+-]+').match(value):
        raise ValidationError(
            'Enter a valid username',
            params={'value': value},
        )
