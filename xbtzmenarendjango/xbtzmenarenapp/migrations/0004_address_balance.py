# Generated by Django 3.0.7 on 2020-07-08 11:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xbtzmenarenapp', '0003_auto_20200706_2125'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('vs', models.CharField(max_length=10, unique=True)),
                ('btc', models.CharField(max_length=100, unique=True)),
                ('ltc', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('eur', models.DecimalField(decimal_places=2, max_digits=9)),
                ('btc', models.DecimalField(decimal_places=8, max_digits=11)),
                ('ltc', models.DecimalField(decimal_places=8, max_digits=14)),
            ],
        ),
    ]
