# Generated by Django 2.2.10 on 2020-03-22 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200322_2107'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='pickup_date',
            new_name='pickup_day',
        ),
    ]
