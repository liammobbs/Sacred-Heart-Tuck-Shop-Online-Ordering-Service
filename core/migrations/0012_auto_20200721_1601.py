# Generated by Django 2.2.10 on 2020-07-21 04:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20200721_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='netitem',
            name='item',
        ),
        migrations.RemoveField(
            model_name='netitem',
            name='item_variations',
        ),
        migrations.RemoveField(
            model_name='netorders',
            name='net_item',
        ),
        migrations.AddField(
            model_name='netitem',
            name='date',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='core.NetOrders'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='netorders',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
