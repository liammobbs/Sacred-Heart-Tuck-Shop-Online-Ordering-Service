# Generated by Django 2.2.10 on 2020-05-25 22:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_userprofile_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
    ]