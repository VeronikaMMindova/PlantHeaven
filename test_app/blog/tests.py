from multiprocessing.connection import Client

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from test_app.blog.models import Post, Category, Plant
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



    def test_add_comment_unauthenticated(self):
        response = self.client.post(reverse('add_comment', kwargs={'post_id': self.post.pk}), {
            'comment_text': 'This should not be saved.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post.comments.count(), 0)

class PlantModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_plant_creation(self):
        # Creating a Plant instance
        plant = Plant.objects.create(
            name='Rose',
            habitat='Garden',
            image='images/plants/rose.jpg',
            wikipedia_url='https://en.wikipedia.org/wiki/Rose',
            category=self.category,
            type_of_plant='Flower'
        )

        self.assertEqual(plant.name, 'Rose')
        self.assertEqual(plant.habitat, 'Garden')
        self.assertEqual(plant.image, 'images/plants/rose.jpg')
        self.assertEqual(plant.wikipedia_url, 'https://en.wikipedia.org/wiki/Rose')
        self.assertEqual(plant.category, self.category)
        self.assertEqual(plant.type_of_plant, 'Flower')

    def test_plant_str_method(self):
        # Creating a Plant instance
        plant = Plant.objects.create(
            name='Sunflower',
            habitat='Field',
            category=self.category,
            type_of_plant='Herb'
        )

        self.assertEqual(str(plant), 'Sunflower')

    def test_plant_type_choices(self):
        # Create a Plant with different types
        flower_plant = Plant.objects.create(
            name='Tulip',
            habitat='Garden',
            category=self.category,
            type_of_plant='Flower'
        )
        cactus_plant = Plant.objects.create(
            name='Cactus',
            habitat='Desert',
            category=self.category,
            type_of_plant='Cactus'
        )

        self.assertEqual(flower_plant.type_of_plant, 'Flower')
        self.assertEqual(cactus_plant.type_of_plant, 'Cactus')

    def test_plant_validation(self):
        invalid_plant = Plant(name='Invalid Plant', habitat='12345')
        with self.assertRaises(ValidationError):
            invalid_plant.full_clean()

        invalid_name_plant = Plant(name='1234', habitat='Field')
        with self.assertRaises(ValidationError):
            invalid_name_plant.full_clean()
