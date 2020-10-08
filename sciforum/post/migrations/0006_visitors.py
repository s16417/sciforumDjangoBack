# Generated by Django 3.1 on 2020-10-08 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20201006_2148'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitors',
            fields=[
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='post.post')),
                ('visitorIp', models.GenericIPAddressField(blank=True, null=True)),
                ('visitDate', models.DateTimeField(blank=True)),
            ],
        ),
    ]
