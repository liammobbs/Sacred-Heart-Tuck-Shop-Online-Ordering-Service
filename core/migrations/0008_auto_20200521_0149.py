# Generated by Django 2.2.10 on 2020-05-21 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200521_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='', editable=False),
        ),
    ]
