from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def valid_user_type(value):
    if value != "student" and value != "professor":
        raise ValidationError(
            _('An invalid user type was entered.')
        )

def valid_post_type(value):
    if value != 'academic' and value != 'office':
        raise ValidationError(
            _('An invalid post type was entered.')
        )