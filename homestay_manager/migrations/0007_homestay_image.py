# Generated by Django 5.1 on 2024-11-13 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homestay_manager', '0006_remove_room_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='homestay',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='homestay_images/'),
        ),
    ]
