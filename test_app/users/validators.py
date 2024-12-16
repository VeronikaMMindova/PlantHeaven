import re
from django.core.exceptions import ValidationError

def staff_check(user):
    return user.is_staff

def admin_check(user):
    return user.is_superuser

def clean_password_confirm(password, password_confirm):
    if password != password_confirm:
        raise ValidationError("Passwords do not match.")
    return password_confirm

def first_name_validate_only_letters(value):
    if not re.fullmatch(r'[A-Za-z\s]+', value):
        raise ValidationError("First name must contain only letters.")

def last_name_validate_only_letters(value):
    if not re.fullmatch(r'[A-Za-z\s]+', value):
        raise ValidationError("Last name must contain only letters.")