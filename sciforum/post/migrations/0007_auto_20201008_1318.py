# Generated by Django 3.1 on 2020-10-08 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_visitors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitors',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='post.post', unique=True),
        ),
    ]
