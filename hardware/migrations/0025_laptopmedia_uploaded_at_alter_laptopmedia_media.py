# Generated by Django 4.0.1 on 2022-03-08 10:39

from django.db import migrations, models
import django.utils.timezone
import hardware.models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0024_remove_historicallaptop_media_remove_laptop_media_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='laptopmedia',
            name='uploaded_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='laptopmedia',
            name='media',
            field=models.ImageField(upload_to=hardware.models.path_and_rename),
        ),
    ]
