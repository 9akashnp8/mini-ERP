# Generated by Django 4.0.4 on 2022-07-10 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0036_employee_is_assigned_historicalemployee_is_assigned_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='lk_emp_id',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='historicalemployee',
            name='lk_emp_id',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
