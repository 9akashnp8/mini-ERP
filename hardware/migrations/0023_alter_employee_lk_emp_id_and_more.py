# Generated by Django 4.0.1 on 2022-03-04 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0022_remove_employee_laptop_assiged_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='lk_emp_id',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='historicalemployee',
            name='lk_emp_id',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='historicallaptop',
            name='hardware_id',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='emp_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hardware.employee'),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='hardware_id',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='media',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hardware.laptopmedia'),
        ),
    ]
