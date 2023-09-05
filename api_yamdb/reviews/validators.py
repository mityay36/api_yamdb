import datetime
from django.core.exceptions import ValidationError


def validate_title_year(value):
    year = datetime.date.today().year
    if not (value <= year):
        raise ValidationError('Некоректный год.')
    return value
