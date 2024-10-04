import re
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


def cat_validate_name(value):
    if not re.match(r'^[a-zA-Zа-яА-Я\s]+$', value):
        raise ValidationError(
            'Имя котенка не должно содержать специальных '
            'символов, только буквы и пробелы.'
        )


def cat_validate_birth_date(value):
    max_age_limit_in_years = 25
    today = timezone.now().date()
    max_birth_date = today - timedelta(days=max_age_limit_in_years * 365.25)
    if value < max_birth_date:
        raise ValidationError('Возраст котенка не может быть больше 25 лет.')
