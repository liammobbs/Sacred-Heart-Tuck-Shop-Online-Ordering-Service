# Generated by Django 2.2.10 on 2020-06-08 08:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='ordered_date',
            new_name='order_date',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='one_click_purchasing',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='stripe_customer_id',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='firstname',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lastname',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_email',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default='static/img/no-image-available-icon-template-260nw-1036735678.jpg.png', upload_to='media/images/'),
        ),
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='', editable=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='orderitem', to='core.OrderItem'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='order',
            name='pickup_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Pickup Date'),
        ),
        migrations.CreateModel(
            name='NetOrders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('net_item', models.ManyToManyField(related_name='netitems', to='core.OrderItem')),
            ],
        ),
    ]