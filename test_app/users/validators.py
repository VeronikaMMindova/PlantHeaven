import re
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def validate_socials_url(value):
    url_validator = URLValidator(schemes=['http', 'https'])
    try:
        url_validator(value)
    except ValidationError:
        raise ValidationError(f'{value} is not a valid URL. Please enter a valid Facebook/Instagram URL.')
def staff_check(user):
    return user.is_staff

def admin_check(user):
    return user.is_superuser

def clean_password_confirm(password, password_confirm):
    if password != password_confirm:
        raise ValidationError("Passwords do not match.")
    return password_confirm
def custom_password_validator(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password must contain at least one digit.")
    if not any(char.isupper() for char in password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not any(char.islower() for char in password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>).")
def first_name_validate_only_letters(value):
    if not re.fullmatch(r'[A-Za-z\s]+', value):
        raise ValidationError("First name must contain only letters.")

def last_name_validate_only_letters(value):
    if not re.fullmatch(r'[A-Za-z\s]+', value):
        raise ValidationError("Last name must contain only letters.")