# Generated by Django 5.1.3 on 2024-11-18 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(default='plant', max_length=35),
        ),
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
