# Generated by Django 4.0.4 on 2022-09-26 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicallaptop',
            name='laptop_owner_type',
            field=models.CharField(choices=[('CO', 'Company Owned'), ('Rental', 'Rental')], default='Rental', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='historicallaptop',
            name='laptop_rental_vendor',
            field=models.CharField(choices=[('NG', 'NextGen'), ('NC', 'NetCom')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='laptop',
            name='laptop_owner_type',
            field=models.CharField(choices=[('CO', 'Company Owned'), ('Rental', 'Rental')], default='Rental', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='laptop',
            name='laptop_rental_vendor',
            field=models.CharField(choices=[('NG', 'NextGen'), ('NC', 'NetCom')], max_length=50, null=True),
        ),
    ]