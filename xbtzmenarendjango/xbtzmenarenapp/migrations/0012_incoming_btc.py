# Generated by Django 3.0.8 on 2020-11-29 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xbtzmenarenapp', '0011_order_buy_btc_order_buy_ltc_order_sell_btc_order_sell_ltc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Incoming_btc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('btc', models.DecimalField(decimal_places=8, max_digits=11)),
                ('confirmations', models.IntegerField()),
                ('txid', models.CharField(max_length=64)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
