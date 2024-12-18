# Generated by Django 5.1.3 on 2024-11-19 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_likes_post_snippet'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='blog_posts_likes', to='users.profile'),
        ),
    ]
