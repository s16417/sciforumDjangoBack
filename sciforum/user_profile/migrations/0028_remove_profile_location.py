# Generated by Django 3.1 on 2020-10-05 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0027_profile_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
    ]
