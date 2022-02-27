# Generated by Django 4.0.1 on 2022-02-15 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0009_alter_laptop_hardware_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='laptop',
            name='laptop_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hardware.location'),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='hardware_id',
            field=models.CharField(blank=True, default=None, max_length=50, null=True, unique=True),
        ),
    ]