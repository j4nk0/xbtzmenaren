# Generated by Django 3.0.8 on 2020-07-06 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xbtzmenarenapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
