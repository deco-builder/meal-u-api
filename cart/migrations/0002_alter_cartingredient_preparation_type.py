# Generated by Django 5.1.1 on 2024-10-12 05:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('groceries', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartingredient',
            name='preparation_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groceries.preparationtype'),
        ),
    ]