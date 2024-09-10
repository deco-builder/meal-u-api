# Generated by Django 5.1 on 2024-09-10 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groceries', '0002_remove_category_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='price_per_unit',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='unit_size',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
