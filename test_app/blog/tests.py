from multiprocessing.connection import Client

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from test_app.blog.models import Post, Category
from test_app.users.models import Profile


class BlogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password')
        self.profile = Profile.objects.create(user=self.user)
        self.category = Category.objects.create(name="Test Category")
        self.post = Post.objects.create(
            title="Test Post",
            category=self.category,
            author=self.profile,
            created_at=timezone.now()
        )

    def test_like_post(self):
        self.client.login(username='test', password='password')
        self.assertEqual(self.post.likes.count(), 0)

        response = self.client.post(reverse('like_post', kwargs={'post_id': self.post.pk}))
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertIn(self.profile, self.post.likes.all())

        response = self.client.post(reverse('like_post', kwargs={'post_id': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.profile, self.post.likes.all())


