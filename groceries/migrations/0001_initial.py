# Generated by Django 5.1 on 2024-09-10 05:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DietaryDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('unit_size', models.DecimalField(decimal_places=2, max_digits=3)),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=3)),
                ('description', models.TextField()),
                ('stock', models.PositiveIntegerField(default=0)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='groceries.categories')),
            ],
        ),
        migrations.CreateModel(
            name='Units',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Nutrition',
            fields=[
                ('ingredient_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='groceries.ingredients')),
                ('carb', models.DecimalField(decimal_places=2, max_digits=3)),
                ('protein', models.DecimalField(decimal_places=2, max_digits=3)),
                ('fat', models.DecimalField(decimal_places=2, max_digits=3)),
                ('calories', models.DecimalField(decimal_places=2, max_digits=3)),
            ],
        ),
        migrations.AddField(
            model_name='ingredients',
            name='unit_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='groceries.units'),
        ),
        migrations.CreateModel(
            name='IngredientDietaryDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dietary_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groceries.dietarydetails')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groceries.ingredients')),
            ],
            options={
                'unique_together': {('ingredient', 'dietary_details')},
            },
        ),
    ]
