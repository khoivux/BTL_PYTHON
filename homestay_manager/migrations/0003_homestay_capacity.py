# Generated by Django 5.1 on 2024-11-06 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homestay_manager', '0002_homestay_facilities_delete_homestayfacility'),
    ]

    operations = [
        migrations.AddField(
            model_name='homestay',
            name='capacity',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
