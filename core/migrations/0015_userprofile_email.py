# Generated by Django 2.2.10 on 2020-05-25 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_remove_userprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.CharField(default='', max_length=100),
        ),
    ]
