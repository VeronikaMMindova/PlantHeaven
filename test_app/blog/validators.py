import re

from django.core.exceptions import ValidationError


def plant_habitat_validate_only_letters(value):
    if not re.fullmatch(r'[A-Za-z\s]+', value):
        raise ValidationError("Habitat must contain only letters.")

def title_validate_only_letters(value):
    if not re.fullmatch(r'[A-Za-z\s]+', value):
        raise ValidationError("Title must contain only letters.")