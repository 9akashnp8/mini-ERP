# Generated by Django 4.0.1 on 2022-02-23 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hardware', '0016_laptop_emp_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalLaptop',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True, editable=False)),
                ('hardware_id', models.CharField(blank=True, db_index=True, default=None, max_length=50, null=True)),
                ('laptop_sr_no', models.CharField(db_index=True, max_length=100)),
                ('laptop_status', models.CharField(choices=[('Working', 'Working'), ('Repair', 'Repair'), ('Replace', 'Replace')], max_length=20, null=True)),
                ('laptop_date_purchased', models.DateField(null=True)),
                ('laptop_date_sold', models.DateField(blank=True, null=True)),
                ('laptop_date_created', models.DateField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('brand', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='hardware.laptopbrand')),
                ('emp_id', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='hardware.employee')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('laptop_location', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='hardware.location')),
                ('media', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='hardware.laptopmedia')),
                ('model', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='hardware.laptopmodel')),
            ],
            options={
                'verbose_name': 'historical laptop',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.DeleteModel(
            name='HistoricalHardware',
        ),
    ]
