# Generated by Django 3.0.8 on 2020-07-06 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xbtzmenarenapp', '0002_customuser_is_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
