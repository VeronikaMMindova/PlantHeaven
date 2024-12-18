import re

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.validators import URLValidator


def validate_wikipedia_url(value):
    url_validator = URLValidator(schemes=['http', 'https'])
    try:
        url_validator(value)
    except ValidationError:
        raise ValidationError(f'{value} is not a valid URL. Please enter a valid Wikipedia URL.')
def validate_image_file(value):
    try:
        image = get_image_dimensions(value)
    except (IOError, ValueError):
        raise ValidationError(f'{value.name} is not a valid image file. Only JPEG, PNG, and GIF images are allowed.')

    if not value.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        raise ValidationError(f'{value.name} is not a valid image file. Only JPEG, PNG, and GIF images are allowed.')
def plant_habitat_validate_only_letters(value):
    if not re.fullmatch(r'[A-Za-z\s]+', value):
        raise ValidationError("Habitat must contain only letters.")

def title_validate_only_letters(value):
    if not re.fullmatch(r'[A-Za-z\s]+', value):
        raise ValidationError("Title must contain only letters.")