# Generated by Django 2.2.10 on 2020-06-09 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_userprofile_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default='static_in_env/img/no-image-available-icon-template-260nw-1036735678.jpg.png', upload_to='media/images/'),
        ),
    ]