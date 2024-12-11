# Generated by Django 5.1.3 on 2024-11-22 10:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_plant_type_of_plant'),
        ('users', '0003_profile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='auhtor_posts', to='users.profile'),
        ),
    ]
