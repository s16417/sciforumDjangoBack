# Generated by Django 3.1 on 2020-10-05 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0026_remove_profile_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]
