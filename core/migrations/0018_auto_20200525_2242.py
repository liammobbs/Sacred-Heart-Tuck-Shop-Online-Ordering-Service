# Generated by Django 2.2.10 on 2020-05-25 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_userprofile_user_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='user_email',
            new_name='userprofile_email',
        ),
    ]