# Generated by Django 5.1.3 on 2024-11-18 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homestay_manager', '0011_alter_transaction_amount_alter_transaction_date_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]
