# Generated by Django 4.0.4 on 2023-02-14 15:28

from django.db import migrations, models
import finance.models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='invoice_doc',
            field=models.FileField(blank=True, null=True, upload_to=finance.models.dynamic_invoice_storage_path),
        ),
    ]
