# Generated by Django 4.0.4 on 2022-11-27 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.category')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_id', models.CharField(blank=True, max_length=100)),
                ('payment_interval', models.CharField(choices=[('OT', 'One Time'), ('M', 'Monthly'), ('Q', 'Quaterly'), ('H', 'Half-Yearly'), ('Y', 'Yearly')], max_length=20)),
                ('current_cost', models.CharField(max_length=50)),
                ('estimated_due_date', models.DateField()),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=10)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finance.category')),
                ('end_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.department')),
                ('platform', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finance.platform')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(blank=True, max_length=100)),
                ('payment_for_month', models.DateField()),
                ('payment_status', models.CharField(choices=[('Paid', 'Paid'), ('Pending', 'Pending')], default='Pending', max_length=10)),
                ('amount', models.CharField(blank=True, max_length=50, null=True)),
                ('invoice_no', models.CharField(blank=True, max_length=150, null=True)),
                ('invoice_doc', models.FileField(blank=True, null=True, upload_to='')),
                ('invoice_date', models.DateField(blank=True, null=True)),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('payment_mode', models.CharField(blank=True, choices=[('Card', 'Card'), ('Paypal', 'Paypal')], max_length=20, null=True)),
                ('card_no', models.CharField(blank=True, max_length=20, null=True)),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finance.service')),
            ],
        ),
    ]
