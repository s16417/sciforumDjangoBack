# Generated by Django 3.1 on 2020-09-27 03:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0011_remove_profile_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
