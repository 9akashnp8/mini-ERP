# Generated by Django 4.0.4 on 2022-06-28 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0036_rename_laptop_manufacture_date_historicallaptop_laptop_date_purchased_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LaptopMedia',
        ),
    ]
