# Generated by Django 5.1.3 on 2024-11-15 18:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homestay_manager', '0008_homestayroom_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.BigIntegerField()),
                ('date', models.DateField()),
                ('homestay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homestay_manager.homestay')),
            ],
        ),
    ]
