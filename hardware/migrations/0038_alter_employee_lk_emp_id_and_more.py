# Generated by Django 4.0.4 on 2022-07-11 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0037_alter_employee_lk_emp_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='lk_emp_id',
            field=models.CharField(max_length=15, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='historicalemployee',
            name='lk_emp_id',
            field=models.CharField(db_index=True, max_length=15, null=True),
        ),
    ]