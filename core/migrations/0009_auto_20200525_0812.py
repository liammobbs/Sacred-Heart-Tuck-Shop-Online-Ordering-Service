# Generated by Django 2.2.10 on 2020-05-25 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200521_0149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='one_click_purchasing',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='stripe_customer_id',
        ),
    ]
