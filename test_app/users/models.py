from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.db import models

from test_app.blog.validators import validate_image_file
from test_app.users.validators import last_name_validate_only_letters, \
    first_name_validate_only_letters, validate_socials_url


class Profile(models.Model):
    INSTAGRAM_URL_LENTGH = 100
    FACEBOOK_URL_LENTGH = 100
    LAST_NAME_LENTGH = 80
    FIRST_NAME_LENTGH = 80
    BIO_MAX_LENTGH = 150


    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(
        max_length=FIRST_NAME_LENTGH,
        validators=[
            MaxLengthValidator(FIRST_NAME_LENTGH),
            first_name_validate_only_letters,
        ],
        null=True,
        blank=True)
    last_name = models.CharField(
        max_length=LAST_NAME_LENTGH,
        validators=[
            MaxLengthValidator(LAST_NAME_LENTGH),
            last_name_validate_only_letters,
        ],
        null=True,
        blank=True,
    )
    profile_pic = models.ImageField(
        upload_to='images/profile/',
        null=True,
        blank=True,
        validators=[validate_image_file],
    )
    bio = models.TextField(
        max_length=BIO_MAX_LENTGH,
        blank=True,
        null=True,
    )
    facebook_url = models.URLField(
        max_length=FACEBOOK_URL_LENTGH,
        null=True,
        blank=True,
        validators=[validate_socials_url],
    )
    instagram_url = models.URLField(
        max_length=INSTAGRAM_URL_LENTGH,
        null=True,
        blank=True,
        validators=[validate_socials_url],
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)



    def __str__(self):
        return str(self.user)

