# Generated by Django 2.2.10 on 2020-06-09 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200609_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default='media/images/no-image-available-icon-template-260nw-1036735678.jpg_xctPfVt.png', upload_to='media/images/'),
        ),
    ]
