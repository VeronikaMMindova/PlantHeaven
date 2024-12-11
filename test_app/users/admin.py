from django.contrib import admin

from test_app.users.models import Profile


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
    # list_display = ('user', 'first_name', 'last_name', 'is_staff', 'is_superuser')