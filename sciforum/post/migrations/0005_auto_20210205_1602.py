# Generated by Django 3.0.5 on 2021-02-05 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20210205_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='label',
            field=models.TextField(choices=[('CS', 'Cs'), ('STAT', 'Stat'), ('MATHEMATICS', 'Mathematics'), ('PHYSICS', 'Physics'), ('CHEMISTRY', 'Chemistry'), ('ZOOLOGY', 'Zoology'), ('BOTANY', 'Botany'), ('ES', 'Es'), ('OTHER', 'Other')], default='OTHER'),
        ),
    ]
