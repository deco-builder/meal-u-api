# Generated by Django 5.1 on 2024-09-11 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0003_remove_ingredient_measurement_size_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='category_id',
        ),
    ]
