# Generated by Django 5.2.4 on 2025-07-08 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_cart_car_alter_cart_travel_package'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='customer',
            new_name='user',
        ),
    ]
