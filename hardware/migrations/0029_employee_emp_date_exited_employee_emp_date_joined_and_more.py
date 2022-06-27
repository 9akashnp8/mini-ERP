# Generated by Django 4.0.4 on 2022-06-27 10:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0028_alter_historicallaptop_laptop_sr_no_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='emp_date_exited',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='emp_date_joined',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalemployee',
            name='emp_date_exited',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalemployee',
            name='emp_date_joined',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='emp_phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='historicalemployee',
            name='emp_phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
