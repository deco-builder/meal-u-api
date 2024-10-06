# Generated by Django 5.1 on 2024-10-06 05:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0004_deliverylocation_delivery_fee"),
    ]

    operations = [
        migrations.AddField(
            model_name="deliverylocation",
            name="latitude",
            field=models.DecimalField(decimal_places=4, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name="deliverylocation",
            name="longitude",
            field=models.DecimalField(decimal_places=4, max_digits=8, null=True),
        ),
    ]
