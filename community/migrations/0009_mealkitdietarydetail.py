# Generated by Django 5.1 on 2024-09-14 02:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0008_alter_mealkit_photo'),
        ('groceries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MealkitDietaryDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dietary_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groceries.dietarydetail')),
                ('mealkit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.mealkit')),
            ],
            options={
                'unique_together': {('mealkit', 'dietary_details')},
            },
        ),
    ]