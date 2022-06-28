# Generated by Django 4.0.4 on 2022-06-27 10:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0030_alter_employee_emp_date_joined_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='profilePic',
        ),
        migrations.RemoveField(
            model_name='historicalemployee',
            name='profilePic',
        ),
        migrations.AlterField(
            model_name='employee',
            name='emp_date_joined',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='emp_email',
            field=models.CharField(default='NA', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='emp_name',
            field=models.CharField(default='NA', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='emp_status',
            field=models.CharField(choices=[('Active', 'Active'), ('InActive', 'Inactive')], default='Active', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historicalemployee',
            name='emp_date_joined',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historicalemployee',
            name='emp_email',
            field=models.CharField(default='NA', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historicalemployee',
            name='emp_name',
            field=models.CharField(default='NA', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historicalemployee',
            name='emp_status',
            field=models.CharField(choices=[('Active', 'Active'), ('InActive', 'Inactive')], default='Active', max_length=10),
            preserve_default=False,
        ),
    ]