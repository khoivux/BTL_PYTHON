# Generated by Django 5.1 on 2024-11-05 17:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Homestay',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('name', models.CharField(max_length=255)),
                ('number_of_rooms', models.BigIntegerField()),
                ('price', models.BigIntegerField()),
                ('rating', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HomestayFacilities',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('price', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HomestayFacility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facilities', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homestay_manager.homestayfacilities')),
                ('homestay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homestay_manager.homestay')),
            ],
        ),
        migrations.AddField(
            model_name='homestay',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homestay_manager.province'),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('numbers', models.BigIntegerField()),
                ('type', models.CharField(max_length=255)),
                ('homestay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homestay_manager.homestay')),
            ],
        ),
        migrations.CreateModel(
            name='HomestayService',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('homestay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homestay_manager.homestay')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homestay_manager.service')),
            ],
        ),
    ]
