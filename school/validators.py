from django.core.exceptions import ValidationError


def validate_school_year_at_admin_site(value):
    if len(str(value)) != 4:
        raise ValidationError('Year must be four digits.')
