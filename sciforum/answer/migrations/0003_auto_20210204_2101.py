# Generated by Django 3.0.5 on 2021-02-04 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('answer', '0002_answer_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='label',
            field=models.CharField(choices=[('CS', 'Cs'), ('STAT', 'Stat'), ('MATHEMATICS', 'Mathematics'), ('PHYSICS', 'Physics'), ('CHEMISTRY', 'Chemistry'), ('ZOOLOGY', 'Zoology'), ('BOTANY', 'Botany'), ('ES', 'Es'), ('OTHER', 'Other')], default='OTHER', max_length=20),
        ),
    ]
