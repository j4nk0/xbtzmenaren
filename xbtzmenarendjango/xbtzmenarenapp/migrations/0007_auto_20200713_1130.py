# Generated by Django 3.0.8 on 2020-07-13 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xbtzmenarenapp', '0006_auto_20200710_0720'),
    ]

    operations = [
        migrations.RenameField(
            model_name='withdrawal_btc',
            old_name='datetime',
            new_name='time_created',
        ),
        migrations.RenameField(
            model_name='withdrawal_eur',
            old_name='datetime',
            new_name='time_created',
        ),
        migrations.RenameField(
            model_name='withdrawal_ltc',
            old_name='datetime',
            new_name='time_created',
        ),
        migrations.AddField(
            model_name='withdrawal_btc',
            name='time_processed',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='withdrawal_eur',
            name='time_processed',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='withdrawal_ltc',
            name='time_processed',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='withdrawal_btc',
            name='address',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='withdrawal_eur',
            name='iban',
            field=models.CharField(max_length=42),
        ),
        migrations.AlterField(
            model_name='withdrawal_ltc',
            name='address',
            field=models.CharField(max_length=100),
        ),
    ]
