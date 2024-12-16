from django import forms
from django.contrib.auth.forms import  UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from test_app.users.models import Profile
from test_app.users.validators import clean_password_confirm


class EditProfileForm(UserChangeForm):
    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'current_user'})
    )
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'current_first_name'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'current_last_name'})
    )
    profile_pic = forms.ImageField(
        required=False
    )
    is_superuser = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput()
    )
    is_staff = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput()
    )
    is_active = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the current user
        super(EditProfileForm, self).__init__(*args, **kwargs)

        # Remove the password field if it exists
        self.fields.pop('password', None)

        # Hide or disable status fields for non-admin users
        if not user.is_superuser:
            self.fields['is_superuser'].required = False
            self.fields['is_staff'].required = False
            self.fields['is_active'].required = False
            self.fields['is_superuser'].widget = forms.HiddenInput()
            self.fields['is_staff'].widget = forms.HiddenInput()
            self.fields['is_active'].widget = forms.HiddenInput()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['first_name', 'last_name', 'profile_pic', 'bio', 'facebook_url', 'instagram_url']
#         widgets = {
#             'bio': forms.Textarea(attrs={'rows': 3, 'cols': 30}),
#         }
#
#     def clean(self):
#         cleaned_data = super().clean()
#         # Add additional validation if needed
#         return cleaned_data
# class RegistrationForm(forms.ModelForm):
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
#         label="Password",
#         required=True,
#     )
#     password_confirm = forms.CharField(
#         widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
#         label="Confirm Password",
#         required=True,
#     )
#     profile_pic = forms.URLField(
#         required=False,
#         widget=forms.URLInput(attrs={'placeholder': 'Profile picture URL'}),
#         label="Profile Picture",
#     )
#     bio = forms.CharField(
#         widget=forms.Textarea(attrs={'placeholder': 'Write something about yourself'}),
#         label="Bio",
#         required=False,
#     )
#     facebook_url = forms.CharField(
#         max_length=100,
#         required=False,
#         widget=forms.TextInput(attrs={'placeholder': 'Facebook URL'}),
#         label="Facebook URL",
#     )
#     instagram_url = forms.CharField(
#         max_length=100,
#         required=False,
#         widget=forms.TextInput(attrs={'placeholder': 'Instagram URL'}),
#         label="Instagram URL",
#     )
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name', 'password')
#
#
#
#         def clean(self):
#             cleaned_data = super().clean()
#             password = cleaned_data.get('password')
#             password_confirm = cleaned_data.get('password_confirm')
#             clean_password_confirm(password, password_confirm)
#
#             return cleaned_data
#
#         def clean_username(self):
#             username = self.cleaned_data.get('username')
#             if User.objects.filter(username=username).exists():
#                 raise ValidationError("Username is already taken. Please choose a different one.")
#             return username
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','type': 'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','type': 'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')