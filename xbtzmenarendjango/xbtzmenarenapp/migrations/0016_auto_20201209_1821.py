# Generated by Django 3.0.8 on 2020-12-09 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xbtzmenarenapp', '0015_auto_20201207_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='doge',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
