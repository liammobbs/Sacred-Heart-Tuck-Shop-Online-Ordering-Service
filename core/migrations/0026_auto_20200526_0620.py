# Generated by Django 2.2.10 on 2020-05-26 06:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20200526_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pickup_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Pickup Date'),
        ),
    ]
