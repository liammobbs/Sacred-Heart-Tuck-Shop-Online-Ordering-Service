# Generated by Django 2.2.10 on 2020-05-20 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200519_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default='static/img/no-image-available-icon-template-260nw-1036735678.jpg.png', upload_to=''),
        ),
    ]
