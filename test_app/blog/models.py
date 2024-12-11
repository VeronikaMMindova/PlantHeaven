from test_app.blog.validators import plant_habitat_validate_only_letters, title_validate_only_letters
from test_app.users.models import Profile
from django.db import models
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('home')


class Post(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        blank=False,
        null=False,
    )
    title = models.CharField(
        max_length=35,
        null=False,
        blank=False,
        validators=[title_validate_only_letters]
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='images/',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    snippet = models.CharField(
        max_length=75,default='Click on details to read more about it',
    )
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='author_posts',
    )
    is_deleted = models.BooleanField(default=False)
    likes = models.ManyToManyField(
        to=Profile,related_name='blog_posts_likes',blank=True,
    )


    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

class Plant(models.Model):
    TYPE_CHOICES = (
        ('Flower', 'Flower'),
        ('Cactus','Cactus'),
        ('Herb', 'Herb'),
        ('Tree', 'Tree'),
        ('Bush', 'Bush'),
    )

    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        default='Plant')
    habitat = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        validators=[plant_habitat_validate_only_letters],
    )
    image = models.ImageField(
        upload_to='images/plants/',
        blank=True,
        null=True,
    )
    wikipedia_url = models.URLField(
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='plants')
    type_of_plant = models.CharField(
        choices=TYPE_CHOICES,
        default='Flower')

    def __str__(self):
        return self.name

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.profile.username} on {self.post.title}"