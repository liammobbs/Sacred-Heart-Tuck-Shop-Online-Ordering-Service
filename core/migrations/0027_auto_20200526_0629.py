# Generated by Django 2.2.10 on 2020-05-26 06:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20200526_0620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pickup_date',
            field=models.DateField(default=datetime.date(2020, 5, 27), verbose_name='Pickup Date'),
        ),
    ]
