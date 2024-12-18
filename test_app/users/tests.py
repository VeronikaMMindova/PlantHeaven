from django.contrib.auth.models import User
from django.test import TestCase

from test_app.users.models import Profile


class TestUsers(TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.profile = None
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password')
        self.profile = Profile(user=self.user)
        self.profile.save()

    def test_profile_creation(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user.username, 'test')

    def test_profile_user_type(self):
        profile = Profile.objects.get(user=self.user)
        self.assertIsInstance(profile.user, User)